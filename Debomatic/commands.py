# Deb-o-Matic
#
# Copyright (C) 2007-2009 Luca Falavigna
#
# Author: Luca Falavigna <dktrkranz@debian.org>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; version 3 of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA 02110-1301, USA.

import os
from glob import glob
from re import findall, split
from sys import exit
from Debomatic import gpg
from Debomatic import Options

SUPPORTED_COMMANDS = ('rm|rebuild')

def run_command_rm(args):
    for files in args:
        for pattern in split(' ', files):
            for absfile in glob(os.path.join(directory, os.path.basename(pattern))):
                os.remove(absfile)

def run_command_rebuild(args):
    pass

def process_commands():
    directory = Options.get('default', 'packagedir')
    try:
        filelist = os.listdir(directory)
    except:
        print _('Unable to access %s directory') % directory
        exit(-1)
    for filename in filelist:
        cmdfile = os.path.join(directory, filename)
        if os.path.splitext(cmdfile)[1] == '.commands':
            try:
                gpg.check_commands_signature(cmdfile)
            except RuntimeError, error:
                os.remove(cmdfile)
                print error
                continue
            fd = os.open(cmdfile, os.O_RDONLY)
            cmd = os.read(fd, os.fstat(fd).st_size)
            os.close(fd)
            try:
                cmdline = findall('\s?(%s)\s+(.*)' % SUPPORTED_COMMANDS, cmd)[0]
            except IndexError:
                raise Exception(_('Command not supported.'))
            exec "run_command_%s(%s)" % (cmdline[0], cmdline[1])
            # Purge command file
            if os.path.exists(cmdfile):
                os.remove(cmdfile)

