import argparse
import math
import cmath

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


def mathIt(data: str):
  try:
    data = eval(data, {"math": math, "cmath": cmath}, {})
    return data
  except Exception as e:
    return "ERROR:", e


# this is a function so that it is import frendly
def calcIt(equation: str, doPrint=True, doReturn=False):

  risk = [
      "import", "exec", "eval", "os", "sys", "subprocess", "global", "requests"
  ]

  # prevent use of high risk keywords
  for i in risk:
    if i in equation:
      if doPrint:
        print("ERROR: Risk of code execution detected, command canceled")
      if doReturn:
        return "ERROR: Risk of code execution detected, command canceled"
      else:
        return -2

  # prevent use of python keywords to prevent posible threat actor problems
  # lower risk though
  for i in __builtins__.__dict__:
    if i in equation:
      if doPrint:
        print("Python keyword Found, comand canceled")
      if doReturn:
        return "Python keyword Found, comand canceled"
      else:
        return -1

  # prevent gits from using __builtins__ as a bypass
  if "__builtins__" in equation:
    if doPrint:
      print("Python keyword Found, comand canceled")
    if doReturn:
      return "Python keyword Found, comand canceled"
    else:
      return -1

  ans = mathIt(equation)
  match isinstance(ans, tuple):
    case True:
      if doPrint:
        print(ans[0], ans[1])
      if doReturn:
        return (ans[0], ans[1])
    case False:
      if doPrint:
        print(ans)
      if doReturn:
        return ans
    case _:
      pass  #print("wtf (error)")  ;)


calcIt(args.equation)
