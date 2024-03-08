from abc import ABC

from pydantic import BaseModel

from .installer import Installer
from .interface import Element


class ModuleSettings(BaseModel):
    _layout: dict[str, Element] = {}


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

        required_clsvars = ("id", "name", "desc", "order", "layout")
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

    def pre_configure(self, interactive: bool):
        """Do any setup required before showing the menu page, like collecting data for a select input"""
        pass

    def post_configure(self, interactive: bool):
        """After a page is validated and submitted, do something"""
        pass

    def pre_install(self):
        """Do anything before the installation starts"""
        pass

    def post_install(self):
        """Do anything after the installation is completed"""
        pass

    def cleanup(self, error: bool = False):
        """Do any necessary cleanup on success or error"""
        pass
