import os
import logging

def setup_logging():
    log_dir = r"C:\Users\ncbof\hypoxia\waveroseproj\logs"
    os.makedirs(log_dir, exist_ok=True)
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        handlers=[
            logging.FileHandler(
                r"C:\Users\ncbof\hypoxia\waveroseproj\logs\waverose.log"
            ),
            logging.StreamHandler()
        ]
    )