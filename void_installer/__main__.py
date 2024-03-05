import logging
import subprocess

from .cmd import run

# TODO: log to file (e.g. `filename="void-installer.log"`), also maybe https://stackoverflow.com/a/56944256
logging.basicConfig(format="[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s", level=logging.INFO)
logger = logging.getLogger("void_installer")


def main():
    logger.info("began run")
    try:
        run("ls /sys/block")
        run("ls /asdfasdfsys/block")
    except subprocess.CalledProcessError:
        ...
    logger.info("ended run")


if __name__ == "__main__":
    main()
