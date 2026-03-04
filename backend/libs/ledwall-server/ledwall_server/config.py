"""Server configuration using pydantic-settings."""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """LED wall server settings, loaded from environment variables."""

    # Display dimensions
    display_width: int = 32
    display_height: int = 24

    # Target device
    target_ip: str = "192.168.1.100"
    target_port: int = 21324

    # Rendering
    fps: int = 30

    # Server
    host: str = "0.0.0.0"
    port: int = 8000

    model_config = {"env_prefix": "LEDWALL_"}


settings = Settings()
