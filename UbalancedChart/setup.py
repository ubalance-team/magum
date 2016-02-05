import shutil, errno, os, time

def setuppingDir(src,dst):
	try:
	    shutil.copytree(src, dst)
	    print 'Done!'
	except OSError as exc: # python >2.5
	    if exc.errno == errno.ENOTDIR:
	        shutil.copy(src, dst)
	        print 'Done!'
	    else: raise

def setuppingFile(src,dst):
	try:
	    shutil.copyfile(src, dst)
	    print 'Done!'
	except OSError as exc: # python >2.5
	    if exc.errno == errno.ENOTDIR:
	        shutil.copy(src, dst)
	        print 'Done!'
	    else: raise

src = './ubalanced-graphs/'
dst = '/home/udooer/ubalanced-graphs/'

print 'Copying site files...'
setuppingDir(src,dst)

time.sleep(2)

os.system('chmod -R 770 /home/udooer/ubalanced-graphs/')
os.system('chown -R root:root /home/udooer/ubalanced-graphs/')

time.sleep(1)

src = './ubalanced'
dst = '/etc/init.d/ubalanced'

print 'Configuring startup...'
setuppingFile(src,dst)

time.sleep(2)

os.system('chmod 770 /etc/init.d/ubalanced')
os.system('chown root:root /etc/init.d/ubalanced')

time.sleep(1)

print 'Starting web application...'
os.system('python /home/udooer/ubalanced-graphs/ubalanced.py &')
print 'Started at http://localhost:5001'