#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2006-2024 wolfSSL Inc.
#
# This file is part of wolfSSL. (formerly known as CyaSSL)
#
# wolfSSL is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# wolfSSL is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA

import subprocess
import argparse
import sys
import os

WOLFSSLPATH = None
TMP_DIR = "./tmp"
CONFOPTEXT = os.path.join(os.path.dirname(__file__), "configureOptionsExtractor.py")
HEADCOMP = os.path.join(os.path.dirname(__file__),"headerComparator.py")
OPTIONSFILE = "options.txt"
DEFAULTHEADER = "default.h"
TMP_INCREMENT = "increment.txt"
FAILED_OPTIONS_FILE = "failed_options.txt"

def configureOptionsExtractor() -> list[str]:
    """
    Extract all configure options from wolfssl/configure.
    """
    global WOLFSSLPATH, OPTIONSFILE
    program_command = ['sh', '-c', f'python3 {CONFOPTEXT} --wolfssl-path {WOLFSSLPATH} --output {TMP_DIR}/{OPTIONSFILE}']
    result = subprocess.run(program_command, capture_output=True, text=True)
    if result.returncode != 0:
        print('Error has occurred while running configure options extractor', file=sys.stderr)
        print(f'\tScript: {" ".join(program_command)}', file=sys.stderr)
        print('\t' + result.stderr, file=sys.stderr)
        raise Exception("Error while running configure options extractor")

def configureExecute(option: str):
    """
    Execute the configure command with the given option and return the result.
    """
    configure_command = ['sh', '-c', f'cd {WOLFSSLPATH} && ./configure {option}']
    print(f'Running configure command: {" ".join(configure_command)}')
    result = subprocess.run(configure_command, capture_output=True, text=True)
    if result.returncode != 0:
        print('Error has occurred while running configure command', file=sys.stderr)
        print(f'\tScript: {" ".join(configure_command)}', file=sys.stderr)
        print('\t' + result.stderr, file=sys.stderr)
        with open(f"{FAILED_OPTIONS_FILE}", 'a') as f:
            f.write(option + '\n')
    return

def storeSourceHeaderFile():
    """
    Store the default header file from wolfssl/options.h.
    """
    configureExecute("")
    copy_command = ['sh', '-c', f'cp {WOLFSSLPATH}/wolfssl/options.h {TMP_DIR}/{DEFAULTHEADER}']
    result = subprocess.run(copy_command, capture_output=True, text=True)
    if result.returncode != 0:
        print('Error has occurred while copying header file', file=sys.stderr)
        print(f'\tScript: {" ".join(copy_command)}', file=sys.stderr)
        print('\t' + result.stderr, file=sys.stderr)
        raise Exception("Error while copying header file")
    return

def recordDiff(option: str, ignore_macros: set[str]) -> list[str]:
    """
    Record the diff between the generated header by given option and the default header.
    """
    configureExecute(option)
    diff_command = ['sh', '-c', f'python3 {HEADCOMP} --source \
        {TMP_DIR}/{DEFAULTHEADER} --target {WOLFSSLPATH}/wolfssl/options.h\
        --increment {TMP_DIR}/{TMP_INCREMENT}']
    print(f'Running header comparator program...')
    result = subprocess.run(diff_command, capture_output=True, text=True)
    if result.returncode != 0:
        print('Error has occurred while running header comparator program', file=sys.stderr)
        print(f'\tScript: {" ".join(diff_command)}', file=sys.stderr)
        print('\t' + result.stderr, file=sys.stderr)
        raise Exception("Error while running header comparator")

    with open(f"{TMP_DIR}/{TMP_INCREMENT}", 'r') as f:
        return [macro for macro in f.read().splitlines() if macro not in ignore_macros]

def cleanup():
    """
    Remove temporary files and directories.
    """
    print("Cleaning up temporary files...")
    if os.path.exists(f"{TMP_DIR}/{OPTIONSFILE}"):
        os.remove(f"{TMP_DIR}/{OPTIONSFILE}")
    if os.path.exists(f"{TMP_DIR}/{DEFAULTHEADER}"):
        os.remove(f"{TMP_DIR}/{DEFAULTHEADER}")
    if os.path.exists(f"{TMP_DIR}/{TMP_INCREMENT}"):
        os.remove(f"{TMP_DIR}/{TMP_INCREMENT}")
    if os.listdir(TMP_DIR) == []:
        os.rmdir(TMP_DIR)
    return 0

def main():
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('--wolfssl-path', type=str, required=True, help='wolfSSL home dir path.')
    parser.add_argument('--options-file', type=str, help='Text file with options to be executed. If not provided, all options will be executed')
    parser.add_argument('--format', type=str, default='mdtable', help="Output format. mdtable : Markdown table, txt : Plain text")
    parser.add_argument('--output', type=str, default=None, help="Output file to save the results. Default: stdout")
    parser.add_argument('--ignore-macros', type=str, default=None, help="Text file with macros to be ignored.")

    args = parser.parse_args()

    global WOLFSSLPATH, OPTIONSFILE
    os.makedirs(TMP_DIR, exist_ok=True)
    WOLFSSLPATH = args.wolfssl_path
    if os.path.exists(WOLFSSLPATH) == False:
        print(f"Invalid wolfSSL home directory: {WOLFSSLPATH}", file=sys.stderr)
        sys.exit(1)
    if args.format not in ['mdtable', 'txt']:
        print(f"Invalid format: {args.format}", file=sys.stderr)
        sys.exit(1)
    ignore_macros = set()
    if args.ignore_macros:
        if os.path.isfile(args.ignore_macros) == False:
            print(f"Invalid ignore macros file: {args.ignore_macros}", file=sys.stderr)
            sys.exit(1)
        with open(args.ignore_macros, 'r') as f:
            ignore_macros = set(f.read().splitlines())

    options = []
    if args.options_file: 
        if os.path.isfile(args.options_file) == False:
            print(f"Invalid options file: {args.options_file}", file=sys.stderr)
            sys.exit(1)
        with open(args.options_file, 'r') as f:
            options = f.read().splitlines()
    else:
        configureOptionsExtractor()
        with open(f"{TMP_DIR}/{OPTIONSFILE}", 'r') as f:
            options = f.read().splitlines()

    if os.path.exists(f"{FAILED_OPTIONS_FILE}"):
        os.remove(f"{FAILED_OPTIONS_FILE}")

    storeSourceHeaderFile()

    options_len = len(options)
    outputbuf = []
    for idx, option in enumerate(options):
        print(f"Processing {idx+1}/{options_len} : {option}")
        diff = recordDiff(option, ignore_macros)
        if diff == []:
            continue
        outputstr = ""
        if args.format == 'mdtable':
            outputstr += f"# {option}\n"
            for macro in diff:
                outputstr += f"- {macro}\n"
            outputstr += "\n"
        else: # txt format
            outputstr += f"{option}:\n"
            for macro in diff:
                outputstr += f"\t{macro}\n"
            outputstr += "\n"
        if args.output:
            with open(args.output, 'a') as f:
                f.write(outputstr)
        else: # stdout
            outputbuf.append(outputstr)
    
    if args.output == "txt":
        print("### Show Results ###")
        for output in outputbuf:
            print(output, end="")
        print("####################")

    if os.path.exists(f"{FAILED_OPTIONS_FILE}"):
        print("Some options are failed to execute configure command.")
        print(f"Please check {FAILED_OPTIONS_FILE} for the failed options.")
    cleanup()

if __name__ == '__main__':
    main()
