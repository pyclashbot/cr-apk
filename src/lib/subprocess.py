"""Subprocess module for running commands."""

from __future__ import annotations

import ctypes
import logging
from subprocess import (
    CREATE_NO_WINDOW,
    PIPE,
    REALTIME_PRIORITY_CLASS,
    STARTF_USESHOWWINDOW,
    STARTF_USESTDHANDLES,
    STARTUPINFO,
    SW_HIDE,
    Popen,
    TimeoutExpired,
)

ST_INFO = STARTUPINFO()
ST_INFO.dwFlags |= STARTF_USESHOWWINDOW | STARTF_USESTDHANDLES | REALTIME_PRIORITY_CLASS
ST_INFO.wShowWindow = SW_HIDE
CR_FLAGS = CREATE_NO_WINDOW
subprocess_flags = {
    "startupinfo": ST_INFO,
    "creationflags": CR_FLAGS,
    "start_new_session": True,
}


def _terminate_process(
    process: Popen[str],
) -> None:
    """Terminate a process forcefully."""
    logging.debug("\tTerminating process %s", process.pid)
    handle = ctypes.windll.kernel32.OpenProcess(1, False, process.pid)  # noqa: FBT003
    ctypes.windll.kernel32.TerminateProcess(handle, -1)
    ctypes.windll.kernel32.CloseHandle(handle)
    process.kill()


def run(
    args: list[str],
    timeout: float | None = None,
) -> tuple[int, str, str]:
    """Run a command and return the exit code and output."""
    logging.debug('\tCommand: "%s"', " ".join(args))
    with Popen(  # noqa: S603
        args,
        shell=False,
        bufsize=-1,
        stdout=PIPE,
        stderr=PIPE,
        close_fds=True,
        universal_newlines=True,
        **subprocess_flags,
    ) as process:
        try:
            result = process.communicate(timeout=timeout)
        except TimeoutExpired:
            _terminate_process(process)
            result = process.communicate()
            raise
        if lines := result[0].splitlines():
            logging.debug("\tOutput: %s", lines.pop(0))
            for line in lines:
                logging.debug("\t\t%s", line)
        return (process.returncode, result[0], result[1])
