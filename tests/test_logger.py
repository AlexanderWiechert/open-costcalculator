from core import logger


def test_logger_methods(capsys):
    logger.info("Test")
    logger.warn("Warnung")
    logger.error("Fehler")
    logger.success("Erfolg")
    captured = capsys.readouterr()
    assert "Test" in captured.out
    assert "Warnung" in captured.out
    assert "Fehler" in captured.out
    assert "Erfolg" in captured.out
