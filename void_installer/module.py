from abc import ABC

from pydantic import BaseModel

from .installer import Installer


class ModuleSettings(BaseModel):
    pass


class Module(ABC):
    """
    A module of the installer.

    ```
    class MyModule(Module):
        id = "mymodule"
        name = "My Module"
        desc = "does stuff"

        class Settings(ModuleSettings):
            ...

        ...
    ```
    """

    @classmethod
    def __init_subclass__(cls, /, **kwargs):
        super().__init_subclass__(**kwargs)

        required_clsvars = ("id", "name", "desc")
        for var in required_clsvars:
            if not hasattr(cls, var):
                raise NotImplementedError(f"Module '{cls}' lacks required attribute '{var}'")

    def __init__(self, ctx: Installer):
        if hasattr(self, "Settings"):
            if self.id in ctx.config.modules.keys():  # type: ignore (checked for existence in __init_subclass__)
                # checked for existence in __init_subclass__
                ctx.config.modules[self.id] = self.Settings(**ctx.config.modules[self.id])  # type: ignore
            else:
                # checked for existence in __init_subclass__
                ctx.config.modules[self.id] = self.Settings()  # type: ignore

        self.config = ctx.config

    def setup(self):
        pass

    def configure(self):
        pass

    def validate(self):
        pass

    def pre_install(self):
        pass

    def install(self):
        pass

    def post_install(self):
        pass

    def cleanup(self, error: bool = False):
        pass

    def import_settings(self):
        pass

    def export_settings(self):
        pass
