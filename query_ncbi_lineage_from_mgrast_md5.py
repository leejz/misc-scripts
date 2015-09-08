#!/usr/bin/env python
"""---------------------------------------------------------------------------------------
Jackson Lee 11/4/14
This script reads in a tab delimited file of annotations and queries asynchronously the MGRAST REST API
to parse back the original ncbi tax_id entry.  This script then uses the ncbi tax_id to query the
taxonomic lineage.

Input file format:
query sequence id	hit m5nr id (md5sum)	percentage identity	alignment length,	number of mismatches	number of gap openings	query start	query end	hit start	hit end	e-value	bit score	semicolon separated list of annotations
mgm4581121.3|contig-1350000035_45_1_2592_+	0000679ceb3fc9c950779468e06329a7	61.03	136	53		654	789	366	501	6.80E-44	175	hyalin repeat protein
mgm4581121.3|contig-18000183_1_1_2226_+	0000679ceb3fc9c950779468e06329a7	64.44	45	16		525	569	457	501	1.70E-08	57	hyalin repeat protein
['Download complete. 78538 rows retrieved']

MGRAST REST API:
http://api.metagenomics.anl.gov/m5nr/md5/<M5nr MD5 hash>?source=GenBank
e.g. http://api.metagenomics.anl.gov/m5nr/md5/000821a2e2f63df1a3873e4b280002a8?source=GenBank

resources:
http://api.metagenomics.anl.gov/api.html#m5nr
http://angus.readthedocs.org/en/2014/howe-mgrast.html

Returns:
{"next":null,"prev":null,"version":"10","url":"http://api.metagenomics.anl.gov//m5nr/md5/000821a2e2f63df1a3873e4b280002a8?source=GenBank&offset=0","data":[{"source":"GenBank","function":"sulfatase","ncbi_tax_id":399741,"accession":"ABV39241.1","type":"protein","organism":"Serratia proteamaculans 568","md5":"000821a2e2f63df1a3873e4b280002a8","alias":["GI:157320144"]}],"limit":10,"total_count":1,"offset":0}

This output will then be stored in a buffer and queried for the exact id and grab the xml based lineage 
http://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=taxonomy&id=399741

<TaxaSet><Taxon><TaxId>399741</TaxId><ScientificName>Serratia proteamaculans 568</ScientificName><OtherNames><EquivalentName>Serratia proteamaculans str. 568</EquivalentName><EquivalentName>Serratia proteamaculans strain 568</EquivalentName></OtherNames><ParentTaxId>28151</ParentTaxId><Rank>no rank</Rank><Division>Bacteria</Division><GeneticCode><GCId>11</GCId><GCName>Bacterial, Archaeal and Plant Plastid</GCName></GeneticCode><MitoGeneticCode><MGCId>0</MGCId><MGCName>Unspecified</MGCName></MitoGeneticCode><Lineage>cellular organisms; Bacteria; Proteobacteria; Gammaproteobacteria; Enterobacteriales; Enterobacteriaceae; Serratia; Serratia proteamaculans</Lineage>


Output file format:
A tab delimited file of 
contig-faa-name\tlineage

an error.log of mismatches from both MGRAST and NCBI is also generated  
     
   usage:
   query_ncbi_lineage_from_mgrast_md5.py -i mgrast_organism.txt -o output.file
"""
#---------------------------------------------------------------------------------------

""" #this code taken from: http://stackoverflow.com/questions/2632520/what-is-the-fastest-way-to-send-100-000-http-requests-in-python 
from urlparse import urlparse
from threading import Thread
import httplib, sys
from Queue import Queue

concurrent = 200

def doWork():
    while True:
        url = q.get()
        status, url = getStatus(url)
        doSomethingWithResult(status, url)
        q.task_done()

def getStatus(ourl):
    try:
        url = urlparse(ourl)
        conn = httplib.HTTPConnection(url.netloc)   
        conn.request("HEAD", url.path)
        res = conn.getresponse()
        return res.status, ourl
    except:
        return "error", ourl

def doSomethingWithResult(status, url):
    print status, url

q = Queue(concurrent * 2)
for i in range(concurrent):
    t = Thread(target=doWork)
    t.daemon = True
    t.start()
try:
    for url in open('urllist.txt'):
        q.put(url.strip())
    q.join()
except KeyboardInterrupt:
    sys.exit(1)
"""           


#---------------------------------------------------------------------------------------
#Header - Linkers, Libs, Constants
from string import strip
from optparse import OptionParser
from threading import Thread
import sys
import time
import requests
import json
from Queue import Queue

#---------------------------------------------------------------------------------------

#function declarations

def doWork():
    while not exitapp:
        id, name, mgrast_urlstring = q.get()
        if id % 100 == 0:
            print 'Query: HTTP Thread: ' + str(id) + ' started.'
        try:
            mgrast_response = requests.get(url=mgrast_urlstring, timeout=10)

            if mgrast_response.status_code == 200:
                json_data = json.loads(mgrast_response.text)
                if json_data['data']!= []:
                    if 'ncbi_tax_id' in json_data['data'][0]:
                        eutils_urlstring = 'http://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=taxonomy&id=' + str(json_data['data'][0]['ncbi_tax_id'])
                
                        eutils_response = requests.get(url=eutils_urlstring, timeout=10)
                
                        if eutils_response.status_code == 200:
                            if '<Lineage>' in eutils_response.text:
                                output_dict[name] = eutils_response.text.split('Lineage>')[1][0:-2]
                            else:
                                output_dict[name] = 'No NCBI'                                               
                        else:
                            print 'HTTP error, Thread: ' + str(id) + ' in eutils worker with error: ' + eutils_response.reason
                            logfile.write(str(id) + '\t' + urlstring + '\t' + eutils_response.reason + '\n')
                            raise                    
                    else:
                        output_dict[name] = 'No MGRAST tax ID'
                else:
                    output_dict[name] = 'No MGRAST source data'
            else:
                print 'HTTP error, Thread: ' + str(id) + ' in MG-RAST worker with error: ' + mgrast_response.reason
                logfile.write(str(id) + '\t' + urlstring + '\t' + mgrast_response.reason + '\n')
                raise
        except:
            print 'Thread: ' + str(id) + '. Error. ' 
            print sys.exc_info()[0]
            
        q.task_done()

#---------------------------------------------------------------------------------------
#Body
print "Running..."

if __name__ == '__main__':
    parser = OptionParser(usage = "usage:    query_ncbi_lineage_from_mgrast_md5.py -i mgrast_organism.txt -o output.file",                  
    description='Jackson Lee 11/4/14.  This script reads in a tab delimited file of annotations and queries asynchronously \
    the MGRAST REST API to parse back the original ncbi tax_id entry.  This script then uses the ncbi tax_id to query the \
    taxonomic lineage using the eutils web interface. (See DocString)')    
    parser.add_option("-i", "--input_file", action="store", type="string", dest="inputfilename",
                  help="tab-delimited MGRAST organism file")
    parser.add_option("-o", "--output_filename", action="store", type="string", dest="outputfilename",
                  help="tab-delimited output file")
    (options, args) = parser.parse_args()

    mandatories = ["outputfilename","inputfilename"]
    for m in mandatories:
        if not options.__dict__[m]:
            print "\nError: Missing Arguments\n"
            parser.print_help()
            exit(-1)
    
   
    inputfilename = options.inputfilename    
    outputfilename = options.outputfilename  
        
    infile_list = []
    with open(inputfilename,'U') as infile:
        infile_list = [line.strip().split('\t') for line in infile]
    infile.close()

    urlpool = []
    name_list = []    
    for entry in infile_list[1:-1]:
        contig_name = entry[0]
        md5_hash = entry[1]
        urlpool.append([contig_name, 'http://api.metagenomics.anl.gov/m5nr/md5/' + md5_hash + '?source=RefSeq'])
        name_list.append(contig_name)
            
    concurrent = 10
    exitapp = False
    output_dict = {}
    
    print "Querying MGRAST REST API Service..."          
    with  open('./' + outputfilename + '.errorlog.txt','w') as logfile:           
        q = Queue(concurrent * 2)
        for i in range(concurrent):

            t = Thread(target=doWork)
            t.daemon = True            
            time.sleep(1)            
            t.start()
        try:
            for id, url_load in enumerate(urlpool):
                q.put([id] + url_load)
            q.join()
        except KeyboardInterrupt:
            exitapp = True
            sys.exit(1)                            
            logfile.close()
    logfile.close()
        
    
    print "Matching taxonomies and writing..."            
    with open(outputfilename, 'w') as outfile:
        for name in name_list:
            if name in output_dict:
                outfile.write(name + '\t' + output_dict[name] + '\n')
            else:
                outfile.write(name + '\t' + 'None\n')

    outfile.close()

    print "Done!"
