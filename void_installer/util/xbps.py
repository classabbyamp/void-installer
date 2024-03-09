import logging
from subprocess import CalledProcessError
from typing import Callable

from .cmd import run

__all__ = [
    "Xbps",
]

logger = logging.getLogger(__name__)


def _native_arch() -> Callable[[], str]:
    """Lazily get the native xbps arch"""
    a = None

    def get_arch():
        nonlocal a
        if a is None:
            try:
                a = run("xbps-uhelper arch").stdout.strip()
            except CalledProcessError:
                pass
        return a

    return get_arch  # type: ignore (run defaults to str)


class Xbps:
    env: dict[str, str] = {}

    def __init__(self, arch: str | None = None, target_arch: str | None = None, **kwargs):
        native_arch = _native_arch()
        self.env |= dict(
            XBPS_ARCH=arch if arch else native_arch(),
            XBPS_TARGET_ARCH=target_arch if target_arch else (arch if arch else native_arch()),
            **kwargs,
        )

    def install(
        self,
        *pkgs,
        automatic: bool = False,
        config: str | None = None,
        cachedir: str | None = None,
        debug: bool = False,
        download_only: bool = False,
        force: bool = False,
        ignore_file_conflicts: bool = False,
        ignore_conf_repos: bool = False,
        memory_sync: bool = False,
        dry_run: bool = False,
        repositories: list[str] = [],
        reproducible: bool = False,
        rootdir: str | None = None,
        sync: bool = False,
        unpack_only: bool = False,
        update: bool = False,
        verbose: bool = False,
        noninteractive: bool = True,
        target: bool = False,
    ):
        """Runs xbps-install with the specified arguments.
        If `target` is `True`, the command will be run by chrooting into the target system."""

        args = ["xbps-install"]
        if automatic:
            args += ["-A"]
        if config is not None:
            args += ["-C", config]
        if cachedir is not None:
            args += ["-c", cachedir]
        if debug:
            args += ["-d"]
        if download_only:
            args += ["-D"]
        if force:
            args += ["-f"]
        if ignore_file_conflicts:
            args += ["-I"]
        if ignore_conf_repos:
            args += ["-i"]
        if memory_sync:
            args += ["-M"]
        if dry_run:
            args += ["-n"]
        for repo in repositories:
            args += ["-R", repo]
        if reproducible:
            args += ["--reproducible"]
        if rootdir and not target:
            args += ["-r", rootdir]
        if sync:
            args += ["-S"]
        if unpack_only:
            args += ["-U"]
        if update:
            args += ["-u"]
        if verbose:
            args += ["-v"]
        if noninteractive:
            args += ["-y"]
        args += pkgs

        run(args, env=self.env, target=target)

    def reconfigure(
        self,
        *pkgs,
        all: bool = False,
        config: str | None = None,
        debug: bool = False,
        force: bool = False,
        ignore: list[str] = [],
        rootdir: str | None = None,
        verbose: bool = False,
        target: bool = False,
    ):
        """Runs xbps-reconfigure with the specified arguments.
        If `target` is `True`, the command will be run by chrooting into the target system."""

        args = ["xbps-reconfigure"]
        if config is not None:
            args += ["-C", config]
        if debug:
            args += ["-d"]
        if force:
            args += ["-f"]
        for ipkg in ignore:
            args += ["-i", ipkg]
        if rootdir and not target:
            args += ["-r", rootdir]
        if verbose:
            args += ["-v"]
        if all:
            args += ["-a"]
        else:
            args += pkgs

        run(args, env=self.env, target=target)
