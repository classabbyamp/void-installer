import logging
from pathlib import Path
from pprint import pprint

from . import Installer

# TODO: log to file (e.g. `filename="void-installer.log"`), also maybe https://stackoverflow.com/a/56944256
logging.basicConfig(format="[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s", level=logging.INFO)
logger = logging.getLogger("void_installer")


def main():
    logger.info("began run")
    installer = Installer()
    installer.load_modules(Path("modules"))
    pprint(dict(installer.config))
    # installer.run()
    logger.info("ended run")


if __name__ == "__main__":
    main()
