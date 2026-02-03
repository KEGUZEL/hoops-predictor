from loguru import logger
import sys


def setup_logging() -> None:
    """
    Configure loguru logging for the application.
    Logs are structured and written to stdout by default.
    """
    logger.remove()
    logger.add(
        sys.stdout,
        format="{time} | {level} | {message}",
        level="INFO",
        enqueue=True,
        backtrace=False,
        diagnose=False,
    )

