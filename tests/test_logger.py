from src.logger import get_logger

def test_get_logger(caplog):
    logger = get_logger(__name__)
    logger.info("testing logger")

    assert "testing logger" in caplog.text
