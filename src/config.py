"""
Pedantic-settings always tries to determine the values of fields by reading them from environment variables.
By default, the name of the environment variable must match the name of the field.
The default values will still be used if the corresponding environment variable is not set.
Environment variables will always take precedence over the values loaded from the dotenv file.
Documentation: https://docs.pydantic.dev/latest/concepts/pydantic_settings/.
"""

from functools import lru_cache
from pathlib import Path

from pydantic import EmailStr
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).parent.parent


class Config(BaseSettings):
    """Class for main settings."""

    model_config = SettingsConfigDict(env_file=BASE_DIR / ".env", env_file_encoding="utf-8")

    MAIL_SERVER: str = "smtp.gmail.com"
    MAIL_PORT: int = 587
    MAIL_USERNAME: EmailStr | None = None
    MAIL_PASSWORD: str | None = None
    MAIL_USE_TLS: bool = True


@lru_cache(maxsize=1)
def get_cfg() -> Config:
    """Return the settings object."""

    return Config()


if __name__ == "__main__":
    from pprint import pformat

    print(pformat(get_cfg().model_dump(), width=150))  # noqa: T201
