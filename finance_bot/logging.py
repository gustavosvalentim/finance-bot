import logging
import os


def configure_logger():
    formatter = logging.Formatter('%(name)s - %(levelname)s - %(asctime)s - %(message)s')

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)

    logging.basicConfig(
        level=logging.DEBUG if os.getenv("DEBUG") == "True" else logging.INFO,
        format='%(name)s - %(levelname)s - %(asctime)s - %(message)s',
        handlers=[stream_handler]
    )
