import asyncio
import logging
import shlex
import subprocess as sp
from asyncio import subprocess as asp

from .. import TARGET_DIR

__all__ = [
    "run",
    "target_run",
]

logger = logging.getLogger(__name__)


async def __log_stream(stream: asyncio.StreamReader | None,
                       text: bool, capture: bool, log: int, chan: str) -> str | bytes | None:
    """Log the output streams of a command"""
    if stream is None:
        return None

    io = []
    while not stream.at_eof():
        line: bytes = await stream.readline()
        if text:
            line = line.decode()  # type: ignore (spooky reassignment)
        if capture:
            io += [line]
        if log > logging.NOTSET and line.strip():
            if text:
                logger.log(log, f"[{chan}] {line.removesuffix("\n")}",  # type: ignore (line is str here)
                           extra={"stream": chan})
            else:
                logger.log(log, f"[{chan}] {line.decode().removesuffix("\n")}", extra={"stream": chan})
    if capture:
        if text:
            return "".join(io)
        return b"".join(io)
    return None


def __set_stdio(stdio: int | None, capture: bool) -> int | None:
    if capture:
        if stdio is None:
            return sp.PIPE
        return stdio
    return None


async def __run(
    args: str | list[str],
    log: int = logging.INFO,
    shell: bool = False,
    text: bool = True,
    capture_output: bool = True,
    check: bool = True,
    **kwargs
) -> sp.CompletedProcess[str | bytes]:
    """Run a command in a subprocess using the asyncio API. This is necessary to
    prevent hanging either the interpreter or the subprocess when logging it."""
    env = kwargs.get("env", dict())
    env |= {
        "SHELL": "/bin/sh",
        "USER": "root",
        "HOME": "/tmp",
        "LC_ALL": "C.UTF-8",
        "LANG": "C.UTF-8",
    }
    kwargs |= {
        "stdout": __set_stdio(kwargs.get("stdout", None), capture_output),
        "stderr": __set_stdio(kwargs.get("stderr", None), capture_output),
        "env": env,
    }
    logger.log(log, f"Running command '{args}'")
    if shell:
        if isinstance(args, list):
            cmdstr = shlex.join(args)
        else:
            cmdstr = args
        proc = await asp.create_subprocess_shell(cmdstr, **kwargs)
    else:
        if isinstance(args, str):
            cmd = tuple(shlex.split(args))
        else:
            cmd = tuple(args)
        proc = await asp.create_subprocess_exec(cmd[0], *cmd[1:], **kwargs)

    outstream, errstream = await asyncio.gather(
        *(
            __log_stream(proc.stdout, text, capture_output, log, "stdout"),
            __log_stream(proc.stderr, text, capture_output, log, "stderr"),
        )
    )
    await proc.communicate()
    ret: int = proc.returncode  # type: ignore (process is terminated when communicate() returns)

    if check and ret != 0:
        logger.error(f"Command '{args}' returned non-zero exit status {ret}")
        raise sp.CalledProcessError(cmd=args, returncode=ret, output=outstream, stderr=errstream)

    logger.log(log, f"Command '{args}' returned exit status {ret}")
    return sp.CompletedProcess(args=args, returncode=ret, stdout=outstream, stderr=errstream)


def run(args: str | list[str], target: bool = False, **kwargs) -> sp.CompletedProcess[str | bytes]:
    """Run a command in a subprocess, like `subprocess.run`. Takes the same arguments,
    but additionally `log`, which says what level to log the output as (defaults to `logging.INFO`).
    Defaults to `text=True, capture_output=True, check=True, stdout=PIPE, stderr=PIPE`."""
    if target:
        if isinstance(args, str):
            args = f"chroot {TARGET_DIR} " + args
        elif isinstance(args, list):
            args = ["chroot", str(TARGET_DIR), *args]
    return asyncio.run(__run(args, **kwargs))
