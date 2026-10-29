import logging
from unittest.mock import patch

from folimeld.diagnostics import configure_logging


def test_diagnostics_records_traceback_without_duplicate_handlers(tmp_path):
    logger = logging.getLogger('folimeld')
    original = logger.handlers[:]
    level = logger.level
    logger.handlers = []
    try:
        configure_logging(tmp_path)
        configure_logging(tmp_path)
        assert len(logger.handlers) == 1
        try:
            raise OSError('simulated failure')
        except OSError:
            logging.getLogger('folimeld.model').exception('PDF operation failed')
        contents = (tmp_path / 'folimeld.log').read_text(encoding='utf-8')
        assert 'Traceback' in contents and 'simulated failure' in contents
    finally:
        for handler in logger.handlers:
            handler.close()
        logger.handlers = original
        logger.setLevel(level)


def test_readonly_log_directory_does_not_prevent_startup(tmp_path):
    logger = logging.getLogger('folimeld')
    original = logger.handlers[:]
    logger.handlers = []
    try:
        with patch('folimeld.diagnostics.Path.mkdir', side_effect=PermissionError('read only')):
            configure_logging(tmp_path)
        assert isinstance(logger.handlers[0], logging.NullHandler)
    finally:
        logger.handlers = original
