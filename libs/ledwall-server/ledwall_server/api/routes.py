"""REST API routes for LED wall control."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

if TYPE_CHECKING:
    from ledwall_server.scene import SceneManager
    from ledwall_server.sender import FrameSender

router = APIRouter(prefix="/api")

# These get set by main.py at startup
_scene_manager: SceneManager | None = None
_sender: FrameSender | None = None
_plugin_registry: dict[str, type] = {}
_scene_registry: dict[str, list[dict[str, Any]]] = {}


def configure(
    scene_manager: SceneManager,
    sender: FrameSender,
    plugin_registry: dict[str, type],
    scene_registry: dict[str, list[dict[str, Any]]],
) -> None:
    """Inject dependencies into the routes module."""
    global _scene_manager, _sender, _plugin_registry, _scene_registry  # noqa: PLW0603
    _scene_manager = scene_manager
    _sender = sender
    _plugin_registry = plugin_registry
    _scene_registry = scene_registry


class SetSceneRequest(BaseModel):
    scene: str


class PluginConfigRequest(BaseModel):
    config: dict[str, Any]


class SetBrightnessRequest(BaseModel):
    value: int


@router.get("/scenes")
def list_scenes() -> list[str]:
    """List available scene names."""
    return list(_scene_registry.keys())


@router.post("/scenes/active")
def set_active_scene(req: SetSceneRequest) -> dict[str, str]:
    """Set the active scene by name."""
    if req.scene not in _scene_registry:
        raise HTTPException(status_code=404, detail=f"Scene '{req.scene}' not found")
    if _scene_manager is None:
        raise HTTPException(status_code=500, detail="Scene manager not initialized")

    scene_config = _scene_registry[req.scene]
    layers = []
    for layer in scene_config:
        plugin_type = layer["plugin"]
        if plugin_type not in _plugin_registry:
            raise HTTPException(
                status_code=400, detail=f"Unknown plugin type '{plugin_type}'"
            )
        cls = _plugin_registry[plugin_type]
        config = layer.get("config", {})
        x = layer.get("x", 0)
        y = layer.get("y", 0)
        plugin = cls(
            config, _scene_manager.renderer.width, _scene_manager.renderer.height
        )
        layers.append((plugin, x, y))
    _scene_manager.set_scene(layers)
    return {"status": "ok", "scene": req.scene}


@router.get("/plugins")
def list_plugins() -> list[str]:
    """List available plugin types."""
    return list(_plugin_registry.keys())


@router.post("/plugins/{plugin_id}/config")
def configure_plugin(plugin_id: int, req: PluginConfigRequest) -> dict[str, str]:
    """Update configuration of a plugin instance in the active scene.

    Recreates the plugin with merged config to apply changes.
    """
    if _scene_manager is None:
        raise HTTPException(status_code=500, detail="Scene manager not initialized")
    scene = _scene_manager.active_scene
    if plugin_id < 0 or plugin_id >= len(scene):
        raise HTTPException(
            status_code=404,
            detail=f"Plugin index {plugin_id} out of range "
            f"(scene has {len(scene)} layers)",
        )
    old_plugin, x, y = scene[plugin_id]
    merged_config = {**old_plugin.config, **req.config}
    new_plugin = type(old_plugin)(merged_config, old_plugin.width, old_plugin.height)
    scene[plugin_id] = (new_plugin, x, y)
    return {"status": "ok", "plugin_id": plugin_id}


@router.get("/device")
def device_info() -> dict:
    """Get device info via PING/PONG."""
    if _sender is None:
        raise HTTPException(status_code=500, detail="Sender not initialized")
    info = _sender.send_ping()
    if info is None:
        raise HTTPException(status_code=504, detail="Device not responding")
    return info


@router.post("/device/brightness")
def set_brightness(req: SetBrightnessRequest) -> dict[str, str]:
    """Set display brightness."""
    if _sender is None:
        raise HTTPException(status_code=500, detail="Sender not initialized")
    _sender.send_brightness(req.value)
    return {"status": "ok"}


@router.post("/device/clear")
def clear_display() -> dict[str, str]:
    """Clear the display."""
    if _sender is None:
        raise HTTPException(status_code=500, detail="Sender not initialized")
    _sender.send_clear()
    return {"status": "ok"}
