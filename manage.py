#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
  base_dir = os.path.dirname(__file__)
  ts = os.path.join(base_dir, 'TwoSpaces')
  sys.path.append(ts)
  
  os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pytx.settings")

  from django.core.management import execute_from_command_line

  execute_from_command_line(sys.argv)
  