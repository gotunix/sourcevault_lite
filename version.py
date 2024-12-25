#!/usr/bin/env python3
# ------------------------------------------------------------------- #
#      #####                                                          #
#     #     #  ####  #    # #####   ####  ######                      #
#     #       #    # #    # #    # #    # #                           #
#      #####  #    # #    # #    # #      #####                       #
#           # #    # #    # #####  #      #                           #
#     #     # #    # #    # #   #  #    # #                           #
#      #####   ####   ####  #    #  ####  ######                      #
#                                                                     #
#                              #     #                                #
#                              #     #   ##   #    # #      #####     #
#                              #     #  #  #  #    # #        #       #
#                              #     # #    # #    # #        #       #
#                               #   #  ###### #    # #        #       #
#                                # #   #    # #    # #        #       #
#                                 #    #    #  ####  ######   #       #
# ------------------------------------------------------------------- #
# Copyright (C) 2024 GOTUNIX Networks                                 #
# Copyright (C) 2024 GOTUNIXCODE                                      #
# Copyright (C) 2024 SourceVault                                      #
# Copyright (C) 2024 Justin Ovens                                     #
# ------------------------------------------------------------------- #
# This program is free software: you can redistribute it and/or       #
# modify it under the terms of the GNU General Public License as      #
# published by the Free Software Foundation, either version 3 of the  #
# License, or (at your option) any later version.                     #
#                                                                     #
# This program is distributed in the hope that it will be useful,     #
# but WITHOUT ANY WARRANTY; without even the implied warranty of      #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the       #
# GNU General Public License for more details.                        #
#                                                                     #
# You should have received a copy of the GNU General Public License   #
# along with this program.  If not, see                               #
# <http://www.gnu.org/licenses/>.                                     #
# ------------------------------------------------------------------- #
from __future__ import annotations

try:
    import argparse
    import datetime
    import os
    import pathlib
    import sys
except ImportError as error:
    print(f"Import failure: {error}")
    exit(1)

BASE_DIR = pathlib.Path(__file__).parent
sys.path.append(os.path.join(BASE_DIR, "src"))

try:
    from sourcevault_lite import version
except ImportError as error:
    print(f"Import failure: {error}")
    exit(1)

parser = argparse.ArgumentParser(description="SourceVault Version script")
parser.add_argument(
    "-v", "--version", type=str, action="store", help="Version number"
)
parser.add_argument(
    "-f", "--final", action="store_true", help="Set final build"
)
args = parser.parse_args()
date = datetime.datetime.today().strftime("%Y%m%d")
time = datetime.datetime.today().strftime("%H%M.%S")

version_number = version.__version__
build_number = version.__build__
final_build = version.__final__

if not final_build:
    if args.final:
        final_build = True

if args.version is None:
    if not final_build:
        build_number = build_number + 1
else:
    print(f"Current version : {version_number}")
    print(f"Specified verion: {args.version}")

    if args.version > version_number:
        version_number = args.version
        build_number = 1
        final_build = False
    elif args.version == version_number:
        if not final_build:
            build_number = build_number + 1
    else:
        print("Unable to update version information")
        exit(1)

version_file = os.path.join(BASE_DIR, "src/sourcevault_lite/version.py")
f = open(version_file, "w")
f.write("version: str\n")
f.write("__version__: str\n")
f.write(f'__version__ = version = "{version_number}"\n')
f.write("build: int\n")
f.write("__build__: int\n")
f.write(f"__build__ = build = {build_number}\n")
f.write("final: bool\n")
f.write("__final__: bool\n")
if final_build:
    f.write("__final__ = final = True\n")
else:
    f.write("__final__ = final = False\n")
f.close()

print(
    f"Update {version_file} with version: {version_number}, build: {build_number}"
)
