"""Bounded local diagnostics; never include PDF contents or passwords."""
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path


def configure_logging(directory: str | Path) -> None:
    logger = logging.getLogger('folimeld')
    if logger.handlers:
        return
    try:
        root = Path(directory)
        root.mkdir(parents=True, exist_ok=True)
        handler = RotatingFileHandler(root / 'folimeld.log', maxBytes=1024 * 1024,
                                      backupCount=2, encoding='utf-8')
    except OSError:
        # Diagnostics must not prevent startup on a read-only profile.
        logger.addHandler(logging.NullHandler())
        return
    handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s %(name)s: %(message)s'))
    logger.addHandler(handler)
    logger.setLevel(logging.WARNING)
