import urllib2
import os

ffs = ['macs0416','macs0717','macs1149']

models = ['bradac',
	'cats',
	'diego',
	'glafic',
	'merten',
	'sharon',
	'williams',
	'zitrin-ltm']

base = 'https://archive.stsci.edu/pub/hlsp/frontier/'
runfile = 'get_all_models.sh'

def gi(message):
        print '\033[92m'+message+'\033[0m'

def bi(message):
        print '\033[94m\033[1m'+message+'\033[0m'

def ri(message):
        print '\033[91m'+message+'\033[0m'

f = open(runfile,'w')

for ff in ffs:
	for model in models:
		versions = []
		fitsfiles = []
		requesturl = base+ff+'/models/'+model
		request = urllib2.Request(requesturl)
		try:
			result = urllib2.urlopen(request)
			pagesrc = result.readlines()
			for item in pagesrc:
				cols = item.split('"')
				if len(cols) > 4:
					if cols[5][0] == 'v':
						versions.append(cols[5])
			request = urllib2.Request(base+ff+'/models/'+model+'/'+versions[-1])
			result = urllib2.urlopen(request)
			pagesrc = result.readlines()
			for item in pagesrc:
				cols = item.split('"')
				if len(cols) > 5:
					if cols[5][-11:] == 'magnif.fits':
						fitsfiles.append(cols[5])
			for fitsfile in fitsfiles:
				wgeturl = base+ff+'/models/'+model+'/'+versions[-1]+fitsfile
				syscall = 'wget '+wgeturl
				if os.path.isfile(fitsfile):
					bi(fitsfile+' exists locally, skipping download')
				else:
					gi(syscall)
					print >>f,syscall
		except:
			ri(requesturl+' failed: probably requested a model that does not exist for '+ff)

f.close()
print 'Done'
print 'Source '+runfile+' to begin downloads'
