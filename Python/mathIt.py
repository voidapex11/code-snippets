import argparse
import math

parser = argparse.ArgumentParser(
    prog="CalcIt",
    description="A quick and easy calculator",
    epilog="Thanks for using %(prog)s! :)",
)

parser.add_argument(
  "equation",
  type=str,
  help="The equation to be solved",
)

args = parser.parse_args()

def calcIt(data:str):
  try:
    data=eval(data,{"math": math}, {})
    return data
  except Exception as e:
    return "ERROR:",e

ans=calcIt(args.equation)
match isinstance(ans,tuple):
  case True:
    print(ans[0],ans[1])
    break
  case False:
    print(ans)
    break
  case _:
    print("wtf (error)") # ;)
