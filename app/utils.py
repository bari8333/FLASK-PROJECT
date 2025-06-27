import logging
from logging.handlers import RotatingFileHandler
import os
import sys

def setup_logging(app):
    """
    Set up application logging to write INFO-level and higher logs to logs/app.log,
    with rotation (1MB per file, max 3 files), and also show logs in terminal.
    Safe for multiple calls.
    """
    if hasattr(app, '_logging_configured'):
        return

    try:
        # Ensure logs directory exists
        log_dir = os.path.join(os.getcwd(), 'logs')
        os.makedirs(log_dir, exist_ok=True)

        # Log file path
        log_file = os.path.join(log_dir, 'app.log')

        # Rotating file handler (writes to file)
        file_handler = RotatingFileHandler(
            log_file, maxBytes=1 * 1024 * 1024, backupCount=3
        )
        file_handler.setLevel(logging.INFO)
        formatter = logging.Formatter(
            '[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
        )
        file_handler.setFormatter(formatter)

        # Stream handler (writes to terminal)
        stream_handler = logging.StreamHandler(sys.stdout)
        stream_handler.setLevel(logging.INFO)
        stream_handler.setFormatter(formatter)

        # Clear existing handlers
        app.logger.handlers = []

        # Add handlers
        app.logger.addHandler(file_handler)
        app.logger.addHandler(stream_handler)

        # Set logger level for app
        app.logger.setLevel(logging.INFO)
        app.logger.propagate = False
        app._logging_configured = True

        # Log that the logger was set up
        app.logger.info("Logger initialized. Logs will be written to: %s", log_file)

    except Exception as e:
        fallback_handler = logging.StreamHandler(sys.stderr)
        fallback_handler.setFormatter(logging.Formatter('%(levelname)s: %(message)s'))
        app.logger.addHandler(fallback_handler)
        app.logger.error("Logging setup failed: %s", str(e))
