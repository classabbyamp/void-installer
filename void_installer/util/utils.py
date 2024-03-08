import logging
import re
from pathlib import Path

__all__ = [
    "sed",
]

logger = logging.getLogger(__name__)


def detect_efi() -> str | None:
    efidir = Path("/sys/firmware/efi")
    efibits = None
    if (efidir / "systab").exists():
        try:
            with (efidir / "fw_platform_size").open() as f:
                efibits = f.read().strip()
        except OSError:
            ...  # TODO
        return efibits
    return None


def sed(expr: str, repl: str, path: Path, dest: Path | None = None, g: bool = False):
    lines = []
    cnt = 0
    expr_re = re.compile(expr)
    with path.open() as f:
        lines = f.readlines()

    for line in lines:
        line, n = expr_re.subn(repl, line, count=0 if g else 1)
        cnt += n

    if dest is None:
        dest = path

    with dest.open("w") as f:
        f.writelines(lines)

    logger.info(f"sed: replaced {cnt} occurences of '{expr}' with '{repl}' in '{dest}'")
