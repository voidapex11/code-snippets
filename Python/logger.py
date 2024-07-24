import logging
from datetime import datetime

from pathlib import Path
# make the logs file if it doesn't exist
Path("logs").mkdir(parents=True, exist_ok=True)

logging.basicConfig(
  level=logging.DEBUG,
  handlers=[
      logging.FileHandler("logs/"+datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ".log",),  # writes to file and console
      logging.StreamHandler()
  ],
  format="[%(asctime)s] %(name)s-%(levelname)s: [%(filename)s:%(lineno)s - %(funcName)s()]:\n\t%(message)s\n",
  datefmt="%Y-%m-%d %H:%M:%S",
)


# example context:
#logger = logging.getLogger('example')
#logger.info("Hello world!")
