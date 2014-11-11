import os
import tempfile
import re

def search(directory="./", out=None, directory_only=False, files_only=False, no_hidden=False, hidden_only=False, regex=None):
	filename = out
	if out is None:
		filename = tempfile.NamedTemporaryFile().name

	if regex is not None:
		'''
		This is for stopping "Nothing to repeat error"
		'''
		if regex[0] == '*':
			regex = '.' + regex
		regexp = re.compile(regex)

	f = open(filename, 'w+')

	display_all = not directory_only and not files_only
	display_hidden = not hidden_only and not no_hidden

	for root, dirs, files in os.walk(directory):
		if directory_only or display_all:
			for name in dirs:
				if regex is not None:
					match = regexp.match(name)
					if not match:
						continue

				name_i = os.path.join(root, name)
				if no_hidden or display_hidden:
					if not name.startswith('.'):
						f.write("%s\n" % name_i)

				if hidden_only or display_hidden:
					if name.startswith('.'):
						f.write("%s\n" % name_i)


		if files_only or display_all:
			for name in files:
				if regex is not None:
					match = regexp.match(name)
					if not match:
						continue

				name_i = os.path.join(root, name)
				if no_hidden or display_hidden:
					if not name.startswith('.'):
						f.write("%s\n" % name_i)

				if hidden_only or display_hidden:
					if name.startswith('.'):
						f.write("%s\n" % name_i)


	if out is None:
		f.seek(0)
		result = f.read()
		print result

	f.close()


