"""Entry point installed by the Homebrew formula; not used by macOS bundles."""
from multiprocessing import freeze_support

from folimeld.app import run


if __name__ == "__main__":
    freeze_support()
    raise SystemExit(run(distribution="homebrew"))
