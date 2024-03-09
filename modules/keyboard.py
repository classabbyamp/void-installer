from pathlib import Path

from pydantic import field_validator

from void_installer import util
from void_installer.interface import RadioSelect
from void_installer.module import Module, ModuleSettings
from void_installer import TARGET_DIR


def setup(ctx):
    ctx.add_module(KeyboardModule)


def list_keymaps() -> list[str]:
    return sorted([
        str(k).removesuffix(".map.gz") for k in Path("/usr/share/kbd/keymaps").glob("*.map.gz") if k.is_file()
    ])


class KeyboardModule(Module):
    id = "keyboard"
    name = "Keyboard Settings"
    desc = "sets the console keymap"
    order = 10

    class Settings(ModuleSettings):
        # fields
        keymap: str = "us"

        # internal state
        _keymaps: list[str] = []

        _layout = {
            "keymap": RadioSelect(label="Select a console keymap"),
        }

        # validators
        @field_validator("keymap")
        @classmethod
        def validate_keymap(cls, v: str) -> str:
            if not cls._keymaps:
                cls._keymaps = list_keymaps()
            if v not in cls._keymaps:
                raise ValueError(f"keymap '{v}' not found")
            return v

    def pre_configure(self, interactive: bool):
        self.Settings._keymaps = list_keymaps()
        self.Settings._layout["keymap"].choices = self.Settings._keymaps

    def post_configure(self, interactive: bool):
        if interactive:
            util.run(["loadkeys", self.Settings.keymap])

    def post_install(self):
        util.sed(
            r"#?KEYMAP=.*",
            f"KEYMAP={self.Settings.keymap}",
            TARGET_DIR / "etc/rc.conf"
        )
