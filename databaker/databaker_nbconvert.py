#!/usr/bin/env python
import os
import subprocess
import sys


def main(argv=sys.argv[1:]):
    if argv is None or len(argv) == 0 or len(argv) > 2:
        print("Usage: databaker_process.py <notebook_file> <input_file>")
        print()
        print("<input_file> is optional; it replaces DATABAKER_INPUT_FILE")
        print("in the notebook.")
        print("The input file should also be in the same directory as the")
        print("notebook.")
        sys.exit(1)

    process_env = os.environ.copy()

    if len(argv) == 2:
        process_env['DATABAKER_INPUT_FILE'] = argv[1]

    # TODO get custom templates working; according to this:
    # https://github.com/jupyter/nbconvert/issues/391
    # they should work, but I get TemplateNotFound when using absolute path
    # for template.
    cmd_line = ['jupyter', 'nbconvert', '--to', 'html', '--execute', argv[0]]
    print("Running:", ' '.join(cmd_line))
    subprocess.call(args=cmd_line, env=process_env)


if __name__ == '__main__':
    main()
