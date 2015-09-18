#!/usr/bin/env python

import os
import begin
import subprocess


@begin.start
def run (code_dir='.', style='{based_on_style: chromium}', ignore_dirs='migrations,narf'):
  for root, dirs, files in os.walk(code_dir):
    for file in files:
      go = True

      if file.endswith('.py'):
        for ignore in ignore_dirs.split(','):
          if root.endswith(ignore):
            go = False
            break

      else:
        go = False

      if go:
        path = os.path.join(root, file)
        print(path)
        subprocess.call("yapf -i --style='{}' {}".format(style, path),
                        shell=True)
