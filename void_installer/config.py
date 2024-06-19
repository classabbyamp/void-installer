from datetime import datetime
from pathlib import Path
from typing import Any

import yaml
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

from pydantic import BaseModel, computed_field, Field

from . import __version__


CONFIG_VERSION = 1


class GeneratedInfo(BaseModel):
    @computed_field
    def version(self) -> str:
        return __version__

    @computed_field
    def at(self) -> datetime:
        return datetime.utcnow()


class Config(BaseModel):
    version: int = CONFIG_VERSION
    generated: GeneratedInfo | None = None
    settings: dict[str, Any] = Field(default_factory=dict)

    @classmethod
    def load_yaml(cls, path: Path):
        with path.open() as f:
            cfg = yaml.load(f, Loader=Loader)
            return cls(**cfg)

    def dump_yaml(self, path: Path):
        with path.open("w") as f:
            self.generated = GeneratedInfo()
            yaml.dump(self.model_dump(), f, Dumper=Dumper)
