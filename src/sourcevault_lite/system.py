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
    import subprocess
except ImportError as error:
    print(f"Failure to import module(s): {error}")
    exit(1)


class Command:
    def __init__(self, command, **kwargs):
        self.command = command
        self.kwargs = kwargs

    def run(self, input_data=None, timeout=None):
        process = subprocess.Popen(
            self.command,
            stdin=subprocess.PIPE if input_data else None,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            **self.kwargs,
        )

        try:
            stdout, stderr = process.communicate(
                input=input_data, timeout=timeout
            )
        except subprocess.TimeoutExpired:
            process.kill()
            stdout, stderr = process.communicate()
            raise

        return CompletedProcess(process.returncode, stdout, stderr)


class CompletedProcess:
    def __init__(self, returncode, stdout, stderr):
        self.returncode = returncode
        self.stdout = stdout
        self.stderr = stderr

    def check_returncode(self):
        if self.returncode != 0:
            raise subprocess.CalledProcessError(self.returncode, self.command)
