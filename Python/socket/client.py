#!/usr/bin/env python3

import selectors
import socket
import sys
import traceback

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

import libclient

sel = selectors.DefaultSelector()


def create_request(action, value):
  if action == "search":
    return dict(
        type="text/json",
        encoding="utf-8",
        content=dict(action=action, value=value),
    )
  else:
    return dict(
        type="binary/custom-client-binary-type",
        encoding="binary",
        content=bytes(action + value, encoding="utf-8"),
    )


def start_connection(host, port, request):
  addr = (host, port)
  logger.info(f"Starting connection to {addr}")
  sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  sock.setblocking(False)
  sock.connect_ex(addr)
  events = selectors.EVENT_READ | selectors.EVENT_WRITE
  message = libclient.Message(sel, sock, addr, request)
  sel.register(sock, events, data=message)


if len(sys.argv) != 5:
  print(f"Usage: {sys.argv[0]} <host> <port> <action> <value>")
  sys.exit(1)

host, port = sys.argv[1], int(sys.argv[2])
action, value = sys.argv[3], sys.argv[4]
request = create_request(action, value)
start_connection(host, port, request)

try:
  while True:
    events = sel.select(timeout=1)
    for key, mask in events:
      message = key.data
      try:
        message.process_events(mask)
      except Exception:
        logger.error(f"Main: Error: Exception for {message.addr}:\n"
              f"{traceback.format_exc()}")
        message.close()
    # Check for a socket being monitored to continue.
    if not sel.get_map():
      break
except KeyboardInterrupt:
  logger.error("Caught keyboard interrupt, exiting")
finally:
  sel.close()
