"""PyInstaller Desktop entry point; separate from Store and source/uv launches."""
from multiprocessing import freeze_support
import sys


def main() -> int:
    try:
        from folimeld.desktop_profile import validate_desktop_environment
        validate_desktop_environment()
        import ctypes
        from ctypes import wintypes
        kernel = ctypes.WinDLL("kernel32", use_last_error=True)
        kernel.CreateMutexW.argtypes = [ctypes.c_void_p, wintypes.BOOL, wintypes.LPCWSTR]
        kernel.CreateMutexW.restype = wintypes.HANDLE
        kernel.CloseHandle.argtypes = [wintypes.HANDLE]
        kernel.CloseHandle.restype = wintypes.BOOL
        mutex = kernel.CreateMutexW(None, False, "Local\\Folimeld-Desktop")
        if not mutex:
            raise ctypes.WinError(ctypes.get_last_error())
        already_running = ctypes.get_last_error() == 183
        try:
            if already_running:
                raise RuntimeError("Folimeld Desktop is already running. Close it before starting another instance.")
            from folimeld.app import run
            return run(distribution="desktop")
        finally:
            kernel.CloseHandle(mutex)
    except Exception as error:
        message = f"Folimeld Desktop could not start.\n{error}"
        if sys.stderr is not None:
            print(message, file=sys.stderr)
        if sys.platform == "win32":
            import ctypes
            ctypes.windll.user32.MessageBoxW(None, message, "Folimeld Desktop", 0x10)
        return 1


if __name__ == "__main__":
    freeze_support()
    raise SystemExit(main())
