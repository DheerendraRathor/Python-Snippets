import os
import argparse
import tempfile

file_present = False

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


parser = argparse.ArgumentParser(description='This will generate list of all elements inside a directory',
	epilog='And this is how you this rolls')

parser.add_argument('-d', '--dir', 
	dest='directory',
	default='./',
	help='Enter the directory name you want to list the content for',
	type=directory
	)

parser.add_argument('-o', '--out',
	help='output file where you want to save listing',
	type=file_check
	)

group = parser.add_mutually_exclusive_group()

group.add_argument('-D', '--directory-only',
	action='store_true',
	help='Add this argument if you want files only',
	default=False
	)

group.add_argument('-F', '--files-only',
	action='store_true',
	help='Add this argument if you want files only',
	default=False
	)

parser.add_argument('--no-hidden',
	action='store_true',
	help='Don\'t show hidden files/directories',
	default=False
	)

parser.add_argument('-r', '--regex',
	dest='pattern',
	help='Show only pattern matched files/directories'
	)

args = parser.parse_args()

if args.out is None:
	temp = tempfile.NamedTemporaryFile()
	args.out = temp.name

f = open(args.out, 'w+')
base_url = ""
for root, dirs, files in os.walk(args.directory):
	if args.directory_only:
		for name in dirs:
			name_i = os.path.join(root, name)
			f.write(base_url+name_i+"\n")
	elif args.files_only:
		for name in files:
			name_i = os.path.join(root, name)
			f.write(base_url+name_i+"\n")
	else:
		for name in dirs:
			name_i = os.path.join(root, name)
			f.write(base_url+name_i+"\n")
		for name in files:
			name_i = os.path.join(root, name)
			f.write(base_url+name_i+"\n")
if not file_present:
	f.seek(0)
	data = f.read()
	print data
