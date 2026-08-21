import logging

logger = logging.getLogger(__name__)
def setup_logging():
    logging.basicConfig(
        filename="audit.log",
        level=logging.INFO,
        format = "%(asctime)s - %(levelname)s - %(message)s"
    )
