from mechanize import Browser
import getpass
import re
import argparse
import os, errno
from git import *

def require_dir(path):
	try:
		os.makedirs(path)
	except OSError, exc:
		if exc.errno != errno.EEXIST:
			raise

def directory(path):
	if not os.path.exists(path):
		msg = "%r is not a directory. Creating directory" % path
		require_dir(path)
	return path

parser = argparse.ArgumentParser()

parser.add_argument('-d', '--dir',
	default='./',
	help='Enter the directory where you want to save files',
	type=directory)

parser.add_argument('--git',
	action='store_true',
	help='Add and commit downloaded files to git. If directory is not git repo then initialize it as git repo')

parser.add_argument('--overwrite',
	action='store_true',
	help='Overwrite existing files')

options = parser.parse_args()
git = options.git
directory = options.dir
overwrite = options.overwrite

if git:
	try:
		repo = Repo(directory)
	except InvalidGitRepositoryError:
		repo = Repo.init(directory, bare=False)

base_url = "http://www.spoj.com/"
#.*?(\d+).*?(\d{4}-\d{2}-\d{2}\s*?[0-9:]+).*?([A-Z]+).*?([A-Z]{2,3}).*?([0-9.]+).*?(\d+).*?([A-Za-z0-9\+\-]+)
#.*?(\d+).*?(\d{4}-\d{2}-\d{2}\s*?[0-9:]+).*?([A-Z0-9]+).*?([A-Z0-9]+).*?([0-9.]+).*?(\d+).*?([A-Za-z0-9\+\-]+)

regex = re.compile('.*?(\d+).*?(\d{4}-\d{2}-\d{2}\s*?[0-9:]+).*?([A-Z0-9]+).*?([A-Z0-9]+).*?([0-9.]+).*?(\d+).*?([A-Za-z0-9\+\-]+)')

auth = False
while not auth:
	user = raw_input("Username: ")
	password = getpass.getpass()

	br = Browser()
	br.open(base_url)

	br.select_form(name='login')
	br['login_user'] = user
	br['password'] = password
	br.find_control(name="autologin").items[0].selected = True
	br.submit()

	for link in br.links():
		if link.text == 'my account':
			auth = True
			break
	if not auth:
		print "Authentication Failed"

print "Authenticated"

sublist = br.open(base_url+"status/"+user+"/signedlist")
sublist = sublist.read()

allsub = regex.findall(sublist)

total=0

for match in allsub:
	if match[3]=='AC' or match[3].isdigit():
		source = br.open(base_url+'files/src/save/'+match[0])
		headers = dict(source.info())
		fileext = headers['content-disposition'].split('=')[1].split('.')[-1]
		filename = match[2]+'.'+fileext
		path = os.path.join(directory, filename)
		if overwrite or not os.path.isfile(path):
			fp = open(path, "w")
			fp.write (source.read())
			fp.close()
			print "%s downloaded" % filename

			if git:
				try:
					repo.git.rm(path)
				except Exception:
					pass
				repo.git.add(path)
				message = 'adding solution for %s in %s. Time=%s, Memory=%s' % (match[2], match[6], match[4], match[5])
				repo.git.commit(m = message, date=match[1])
				print "Committed with message %s" % message

		else:
			print '%s already present' % filename

		total += 1

print 'Total AC and score files are %d' % total



