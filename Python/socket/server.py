#!/usr/bin/env python3

import selectors
import socket
import sys
import traceback

import libserver

import logging

from datetime import datetime

from pathlib import Path
# make the logs file if it doesn't exist
Path("logs").mkdir(parents=True, exist_ok=True)

logging.basicConfig(
  level=logging.DEBUG,
  handlers=[
      logging.FileHandler("logs/"+datetime.now().strftime("%Y-%m-%d") + ".log",),  # writes to file and console
      logging.StreamHandler()
  ],
  format="[%(asctime)s] %(name)s-%(levelname)s: [%(filename)s:%(lineno)s - %(funcName)s()]:\n\t%(message)s\n",
  datefmt="%Y-%m-%d %H:%M:%S",
)

logger = logging.getLogger("client")

sel = selectors.DefaultSelector()


def accept_wrapper(sock):
    conn, addr = sock.accept()  # Should be ready to read
    logger.info(f"Accepted connection from {addr}")
    conn.setblocking(False)
    message = libserver.Message(sel, conn, addr)
    sel.register(conn, selectors.EVENT_READ, data=message)


if len(sys.argv) != 3:
    print(f"Usage: {sys.argv[0]} <host> <port>")
    sys.exit(1)

host, port = sys.argv[1], int(sys.argv[2])
lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Avoid bind() exception: OSError: [Errno 48] Address already in use
lsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
lsock.bind((host, port))
lsock.listen()
logger.info(f"Listening on {(host, port)}")
lsock.setblocking(False)
sel.register(lsock, selectors.EVENT_READ, data=None)

try:
    while True:
        events = sel.select(timeout=None)
        for key, mask in events:
            if key.data is None:
                accept_wrapper(key.fileobj)
            else:
                message = key.data
                try:
                    message.process_events(mask)
                except Exception:
                    logger.error(
                        f"Main: Error: Exception for {message.addr}:\n"
                        f"{traceback.format_exc()}"
                    )
                    message.close()
except KeyboardInterrupt:
    logger.error("Caught keyboard interrupt, exiting")
finally:
    sel.close()
