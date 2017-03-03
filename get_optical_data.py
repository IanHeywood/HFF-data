import urllib2
import os

ffs = ['macs0416','macs0717','macs1149']

bases = (['https://archive.stsci.edu/missions/hlsp/clash/','/catalogs/subaru/'],
	['https://archive.stsci.edu/pub/hlsp/frontier/','/catalogs/ebeling/'],
	['https://archive.stsci.edu/missions/hlsp/clash/','/catalogs/hst/'],
	['https://archive.stsci.edu/pub/hlsp/frontier/','/models/'])

runfile = 'get_all.sh'

def gi(message):
 	print '\033[92m'+message+'\033[0m'

def bi(message):
	print '\033[94m\033[1m'+message+'\033[0m'

def ri(message):
	print '\033[91m'+message+'\033[0m'

f = open(runfile,'w')
for base in bases:
	for ff in ffs:
		cats = []
		fitsfiles = []
		requesturl = base[0]+ff+base[1]
		request = urllib2.Request(requesturl)
		try:
			result = urllib2.urlopen(request)
			pagesrc = result.readlines()
			for item in pagesrc:
				cols = item.split()
				if len(cols) > 4:
					if cols[4] == '<a': 
						cat = cols[5].split('"')[1]
						if cat[0] == 'h':
							cats.append(cat)
			for cat in cats:
				caturl = base[0]+ff+base[1]+cat
				syscall = 'wget '+caturl
				print >>f,syscall

		except:
			ri(requesturl+' failed: probably requested a model that does not exist for '+ff)

f.close()
gi('Done, source '+runfile+' to begin downloads')
