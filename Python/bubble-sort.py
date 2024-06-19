import random
import argparse
import sys




parser = argparse.ArgumentParser(
    prog="Bubble sort",
    description="Demmo of bubble sort",
    epilog="Thanks for using %(prog)s! :)",
)



parser.add_argument(
  "count", 
  type=int
)

parser.add_argument(
  '-r',
  '--range',
  type=int,
)

args = parser.parse_args()

try:
  max=args.range
except:
  max = 9

data = []
count = args.count
for i in range(count):
  data.append(random.randint(1, 9))

print(data)

for i in range(len(data)):
  for j in range(len(data)):
    if data[i] < data[j]:
      data[i], data[j] = data[j], data[i]

print(data)
