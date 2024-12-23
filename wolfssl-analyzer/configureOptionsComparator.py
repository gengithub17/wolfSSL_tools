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

import json
import subprocess
import argparse
import sys
import os

WOLFSSLPATH = None
TMP_DIR = "./.tmp"
CONFOPTEXT = os.path.join(os.path.dirname(__file__), "configureOptionsExtractor.py")
HEADCOMP = os.path.join(os.path.dirname(__file__),"headerComparator.py")
OPTIONSFILE = ".options.txt"
DESCRIPTIONFILE = ".description.json"
DEFAULTHEADER = ".default.h"
TMP_INCREMENT = ".increment.txt"
TMP_DECREMENT = ".decrement.txt"
FAILED_OPTIONS_FILE = "failed_options.txt"

def configureOptionsExtractor(opposite:bool = False) -> list[str]:
    """
    Extract all configure options from wolfssl/configure.
    """
    global CONFOPTEXT, WOLFSSLPATH, TMP_DIR, OPTIONSFILE, DESCRIPTIONFILE
    opposite_flag = ""
    if opposite:
        opposite_flag = "--both-enable-disable"
    program_command = ['sh', '-c', f'python3 {CONFOPTEXT} --wolfssl-path {WOLFSSLPATH} \
                       --output {TMP_DIR}/{OPTIONSFILE} \
                        --description-output {TMP_DIR}/{DESCRIPTIONFILE}\
                        {opposite_flag}']
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
    global WOLFSSLPATH, FAILED_OPTIONS_FILE
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
    global WOLFSSLPATH, TMP_DIR, DEFAULTHEADER
    configureExecute("")
    copy_command = ['sh', '-c', f'cp {WOLFSSLPATH}/wolfssl/options.h {TMP_DIR}/{DEFAULTHEADER}']
    result = subprocess.run(copy_command, capture_output=True, text=True)
    if result.returncode != 0:
        print('Error has occurred while copying header file', file=sys.stderr)
        print(f'\tScript: {" ".join(copy_command)}', file=sys.stderr)
        print('\t' + result.stderr, file=sys.stderr)
        raise Exception("Error while copying header file")
    return

def recordDiff(option: str) -> dict:
    """
    Record the diff between the generated header by given option and the default header.
    """
    global WOLFSSLPATH, TMP_DIR, HEADCOMP, DEFAULTHEADER, TMP_INCREMENT, TMP_DECREMENT
    configureExecute(option)
    diff_command = ['sh', '-c', f'python3 {HEADCOMP} --source \
        {TMP_DIR}/{DEFAULTHEADER} --target {WOLFSSLPATH}/wolfssl/options.h\
        --incremental-output {TMP_DIR}/{TMP_INCREMENT} \
        --decremental-output {TMP_DIR}/{TMP_DECREMENT}']
    print(f'Running header comparator program...')
    result = subprocess.run(diff_command, capture_output=True, text=True)
    if result.returncode != 0:
        print('Error has occurred while running header comparator program', file=sys.stderr)
        print(f'\tScript: {" ".join(diff_command)}', file=sys.stderr)
        print('\t' + result.stderr, file=sys.stderr)
        raise Exception("Error while running header comparator")

    retdict = dict()
    with open(f"{TMP_DIR}/{TMP_INCREMENT}", 'r') as f:
        retdict["increment"] = f.read().splitlines()
    with open(f"{TMP_DIR}/{TMP_DECREMENT}", 'r') as f:
        retdict["decrement"] = f.read().splitlines()
    return retdict

    
def cleanup():
    """
    Remove temporary files and directories.
    """
    global TMP_DIR, OPTIONSFILE, DESCRIPTIONFILE, DEFAULTHEADER, TMP_INCREMENT, TMP_DECREMENT
    if not os.path.exists(TMP_DIR):
        return 0
    print("Cleaning up temporary files...")
    if os.path.exists(f"{TMP_DIR}/{OPTIONSFILE}"):
        os.remove(f"{TMP_DIR}/{OPTIONSFILE}")
    if os.path.exists(f"{TMP_DIR}/{DESCRIPTIONFILE}"):
        os.remove(f"{TMP_DIR}/{DESCRIPTIONFILE}")
    if os.path.exists(f"{TMP_DIR}/{DEFAULTHEADER}"):
        os.remove(f"{TMP_DIR}/{DEFAULTHEADER}")
    if os.path.exists(f"{TMP_DIR}/{TMP_INCREMENT}"):
        os.remove(f"{TMP_DIR}/{TMP_INCREMENT}")
    if os.path.exists(f"{TMP_DIR}/{TMP_DECREMENT}"):
        os.remove(f"{TMP_DIR}/{TMP_DECREMENT}")
    if os.listdir(TMP_DIR) == []:
        os.rmdir(TMP_DIR)
    return 0

def main():
    try:
        parser = argparse.ArgumentParser(description='')
        parser.add_argument('--wolfssl-path', type=str, required=True, help='wolfSSL home dir path.')
        parser_group = parser.add_mutually_exclusive_group()
        parser_group.add_argument('--options-file', type=str, help='Text file with options to be executed. '
                            'Cannot be used with --single-option or --both-enable-disable. '
                            'If neither --options-file nor --single-option is specified, all options will be executed.')
        parser_group.add_argument('--single-option', type=str, help='Specify a single option to execute. '
                            'Cannot be used with --options-file or --both-enable-disable.')
        parser_group.add_argument('--both-enable-disable', action='store_true', 
                            help='If an option name contains "enable" or "disable," '
                            'opposite option will automatically be executed. '
                            'Cannot be used with --options-file or --single-option.')
        parser.add_argument('--output', type=str, default=None, help="Output file to save the results. Default: stdout")
        parser.add_argument('--diff-only', action='store_true', help='Skips output for options that have no differences.')
        parser.add_argument('--exclude-options', type=str, help='Text file with options to be excluded from execution.'
                            'If you use --both-enable-disable, you should exclude both "enable" and "disable" options.')

        args = parser.parse_args()

        global WOLFSSLPATH, TMP_DIR, OPTIONSFILE, DESCRIPTIONFILE, FAILED_OPTIONS_FILE
        os.makedirs(TMP_DIR, exist_ok=True)
        WOLFSSLPATH = args.wolfssl_path
        if os.path.exists(WOLFSSLPATH) == False:
            print(f"Invalid wolfSSL home directory: {WOLFSSLPATH}", file=sys.stderr)
            sys.exit(1)

        options = []
        configureOptionsExtractor(args.both_enable_disable)
        if args.options_file: 
            if os.path.isfile(args.options_file) == False:
                print(f"Invalid options file: {args.options_file}", file=sys.stderr)
                sys.exit(1)
            with open(args.options_file, 'r') as f:
                options = f.read().splitlines()
        elif args.single_option:
            options = ["--" + args.single_option]
        else:
            with open(f"{TMP_DIR}/{OPTIONSFILE}", 'r') as f:
                options = f.read().splitlines()
        
        if args.exclude_options:
            if os.path.isfile(args.exclude_options) == False:
                print(f"Invalid exclude options file: {args.exclude_options}", file=sys.stderr)
                sys.exit(1)
            with open(args.exclude_options, 'r') as f:
                lines = f.read().splitlines()
            excluded = [opt for opt in options if opt in lines]

        if os.path.exists(f"{FAILED_OPTIONS_FILE}"):
            os.remove(f"{FAILED_OPTIONS_FILE}")

        storeSourceHeaderFile()
        if args.exclude_options:
            for option in excluded:
                if option in options:
                    options.remove(option)

        diffdict = {}
        options_len = len(options)
        output_buf = ""
        if args.output:
            with open(args.output, 'w') as f:
                f.write("")
        with open(f"{TMP_DIR}/{DESCRIPTIONFILE}", 'r') as f:
            descriptions = json.loads(f.read())
            for idx, option in enumerate(options):
                print(f"Processing {idx+1}/{options_len} : {option}")
                diffdict[option] = recordDiff(option)
                if args.diff_only and not diffdict[option]["increment"] and not diffdict[option]["decrement"]:
                    continue
                output_txt = f"### `{option}`\n\n"
                if option in descriptions.keys():
                    output_txt += f"{descriptions[option]['Description']} \n\n"
                if "increment" in diffdict[option] and diffdict[option]["increment"]:
                    output_txt += "#### Enables\n"
                    for line in diffdict[option]["increment"]:
                        output_txt += f"- `{line}`\n"
                    output_txt += "\n"
                if "decrement" in diffdict[option] and diffdict[option]["decrement"]:
                    output_txt += "#### Removes\n"
                    for line in diffdict[option]["decrement"]:
                        output_txt += f"- `{line}`\n"
                    output_txt += "\n"
                if args.output:
                    with open(args.output, 'a') as f:
                        f.write(output_txt)
                else:
                    output_buf += output_txt

        if not args.output:
            print("\nResults:\n")
            print(output_buf)
        
        if os.path.exists(f"{FAILED_OPTIONS_FILE}"):
            print("Some options are failed to execute configure command.")
            print(f"Please check {FAILED_OPTIONS_FILE} for the failed options.")
    except KeyboardInterrupt:
        pass
    finally:
        cleanup()

if __name__ == '__main__':
    main()
