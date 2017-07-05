#!/bin/env python
import argparse

def parse_args():
  """
  Parse and return arguments
  """
  parser = argparse.ArgumentParser()
  parser.add_argument("settings", help="settings module")
  args = parser.parse_args()
  return args

if __name__ == "__main__":
  args = parse_ags()
