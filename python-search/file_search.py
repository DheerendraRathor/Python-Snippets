import os
import argparse

import search

def directory(path):
	if not os.path.exists(path):
		msg = "%r is not a directory" % path
		raise argparse.ArgumentTypeError(msg)
	return path

def file_check(filename):
	global file_present
	if not os.path.exists(filename):
		open(filename, 'w').close()
	file_present = True
	return filename


parser = argparse.ArgumentParser(
	description='This will generate list of all elements inside a directory',
	epilog='And this is how you it works',
	)

parser.add_argument('-d', '--directory',
	default='./',
	help='Enter the directory name you want to list the content for (Default is current Directory)',
	type=directory
	)

parser.add_argument('-o', '--out',
	help='output file where you want to save listing (output will be displayed on terminal if not supplied file)',
	type=file_check
	)

boolean_group = parser.add_argument_group('optional boolean arguments')

group_fd = boolean_group.add_mutually_exclusive_group()

group_fd.add_argument('-D', '--directory-only',
	action='store_true',
	help='list directories only',
	)

group_fd.add_argument('-F', '--files-only',
	action='store_true',
	help='list files only',
	)

group_hidden = boolean_group.add_mutually_exclusive_group()
group_hidden.add_argument('--no-hidden',
	action='store_true',
	help='Don\'t show hidden files/directories',
	)

group_hidden.add_argument('--hidden-only',
	action='store_true',
	help='Shows only hidden files/Directories',
	)

parser.add_argument('-r', '--regex',
	help='Show only pattern matched files/directories'
	)

kargs = vars(parser.parse_args())

search.search(**kargs)