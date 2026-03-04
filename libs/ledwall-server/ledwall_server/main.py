"""LED wall server entry point — FastAPI + scene render loop."""

import asyncio
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from ledwall_server.api.routes import configure, router
from ledwall_server.config import settings
from ledwall_server.plugins.clock import Clock
from ledwall_server.plugins.effect import ColorCycle, Rainbow, SolidColor
from ledwall_server.plugins.image import AnimatedGif, StaticImage
from ledwall_server.plugins.text import ScrollingText, StaticText
from ledwall_server.plugins.weather import Weather
from ledwall_server.renderer import Renderer
from ledwall_server.scene import SceneManager
from ledwall_server.sender import FrameSender

# Plugin registry
PLUGIN_REGISTRY: dict[str, type] = {
    "solid_color": SolidColor,
    "color_cycle": ColorCycle,
    "rainbow": Rainbow,
    "clock": Clock,
    "static_text": StaticText,
    "scrolling_text": ScrollingText,
    "weather": Weather,
    "static_image": StaticImage,
    "animated_gif": AnimatedGif,
}

# Scene registry — predefined scene configurations
SCENE_REGISTRY: dict[str, list[dict]] = {
    "color_cycle": [
        {"plugin": "color_cycle", "config": {"speed": 5}, "x": 0, "y": 0},
    ],
    "rainbow": [
        {"plugin": "rainbow", "config": {"speed": 3}, "x": 0, "y": 0},
    ],
    "clock": [
        {"plugin": "clock", "config": {"color": [0, 255, 0]}, "x": 0, "y": 0},
    ],
    "hello": [
        {
            "plugin": "static_text",
            "config": {"text": "HELLO", "color": [255, 255, 0]},
            "x": 0,
            "y": 0,
        },
    ],
    "red": [
        {"plugin": "solid_color", "config": {"color": [255, 0, 0]}, "x": 0, "y": 0},
    ],
    "weather": [
        {
            "plugin": "weather",
            "config": {"lat": 45.46, "lon": 9.19},
            "x": 0,
            "y": 0,
        },
    ],
    "dashboard": [
        {
            "plugin": "weather",
            "config": {"lat": 45.46, "lon": 9.19},
            "x": 0,
            "y": 0,
            "w": 16,
            "h": 16,
        },
        {
            "plugin": "clock",
            "config": {"color": [0, 255, 0]},
            "x": 16,
            "y": 0,
            "w": 16,
            "h": 16,
        },
        {
            "plugin": "scrolling_text",
            "config": {"text": "LED WALL DASHBOARD", "color": [255, 200, 0]},
            "x": 0,
            "y": 16,
            "w": 32,
            "h": 8,
        },
    ],
}


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Start the scene render loop on startup, stop on shutdown."""
    renderer = Renderer(settings.display_width, settings.display_height)
    sender = FrameSender(settings.target_ip, settings.target_port)
    scene_manager = SceneManager(renderer, sender, fps=settings.fps)

    configure(scene_manager, sender, PLUGIN_REGISTRY, SCENE_REGISTRY)

    # Start with color_cycle as default scene
    from ledwall_server.api.routes import SetSceneRequest, set_active_scene

    set_active_scene(SetSceneRequest(scene="color_cycle"))

    task = asyncio.create_task(scene_manager.run())
    yield
    scene_manager.stop()
    task.cancel()
    sender.close()


app = FastAPI(title="LED Wall Server", lifespan=lifespan)
app.include_router(router)


def main():
    """Run the server."""
    uvicorn.run(
        "ledwall_server.main:app",
        host=settings.host,
        port=settings.port,
        reload=False,
    )


if __name__ == "__main__":
    main()
