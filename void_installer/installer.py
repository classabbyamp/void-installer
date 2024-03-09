import importlib.util
import logging
import sys
from pathlib import Path

from .config import Config

logger = logging.getLogger(__name__)


class Installer:
    def __init__(self):
        self.modules = {}
        self.config = Config.load_yaml(Path("config.yaml"))

    def load_modules(self, path: Path):
        for f in path.glob("*.py"):
            if f.is_file():
                name = f"{f.parent}.{f.stem}"
                spec = importlib.util.spec_from_file_location(f.stem, f)
                if spec is not None:
                    mod = importlib.util.module_from_spec(spec)
                    if spec.loader is not None:
                        sys.modules[name] = mod
                        try:
                            spec.loader.exec_module(mod)
                        except Exception as e:
                            del sys.modules[name]
                            logger.error(f"unable to load module '{name}': {e}")

                        try:
                            setup = getattr(mod, "setup")
                        except AttributeError:
                            del sys.modules[name]
                            logger.error(f"unable to load module '{name}': module does not contain setup()")

                        try:
                            setup(self)
                        except Exception as e:
                            del sys.modules[name]
                            logger.error(f"unable to load module '{name}': setup failed: {e}")

                        logger.info(f"loaded module '{f.stem}' from '{path}'")

    def add_module(self, mod, **kwargs):
        m = mod(self, **kwargs)
        self.modules[m.id] = m

    def run_phase(self, name: str):
        ...

    def configure(self):
        """show the TUI/GUI/whatever, if desired"""
        ...

    def base_install(self):
        """do the base install (xbps-install base-system etc)"""
        ...

    def run(self):
        self.run_phase("setup")
        self.configure()
        self.run_phase("pre_install")
        self.base_install()
        self.run_phase("post_install")
