#!/usr/bin/env python
"""
--------------------------------------------------------------------------------
Created: Jackson Lee 6/22/15
This script reads in the older uniprot xml file and converts it to a fasta AA file
   
   Input uniprot xml file format:
<?xml version="1.0" encoding="ISO-8859-1" ?>
<UniRef100 xmlns="http://uniprot.org/uniref" 
xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
xsi:schemaLocation="http://uniprot.org/uniref http://www.uniprot.org/support/docs/uniref.xsd" 
releaseDate="2012-11-28" version="2012_11" >
<entry id="UniRef100_Q6GZX4" updated="2011-07-27">
<name>Cluster: Putative transcription factor 001R</name>
<property type="member count" value="1"/>
<property type="common taxon" value="Frog virus 3 (isolate Goorha)"/>
<property type="common taxon ID" value="654924"/>
<representativeMember>
  <dbReference type="UniProtKB ID" id="001R_FRG3G">
    <property type="UniProtKB accession" value="Q6GZX4"/>
    <property type="UniParc ID" value="UPI00003B0FD4"/>
    <property type="UniRef90 ID" value="UniRef90_Q6GZX4"/>
    <property type="UniRef50 ID" value="UniRef50_Q6GZX4"/>
    <property type="protein name" value="Putative transcription factor 001R"/>
    <property type="NCBI taxonomy" value="654924"/>
    <property type="source organism" value="Frog virus 3 (isolate Goorha) (FV-3)"/>
    <property type="length" value="256"/>
    <property type="isSeed" value="true"/>
  </dbReference>
  <sequence length="256" checksum="B4840739BF7D4121">
MAFSAEDVLKEYDRRRRMEALLLSLYYPNDRKLLDYKEWSPPRVQVECPKAPVEWNNPPS
EKGLIVGHFSGIKYKGEKAQASEVDVNKMCCWVSKFKDAMRRYQGIQTCKIPGKVLSDLD
AKIKAYNLTVEGVEGFVRYSRVTKQHVAAFLKELRHSKQYENVNLIHYILTDKRVDIQHL
EKDLVKDFKALVESAHRMRQGHMINVKYILYQLLKKHGHGPDGPDILTVKTGSKGVLYDD
SFRKIYTDLGWKFTPL
  </sequence>
</representativeMember>
</entry>
   
   Output:
   fasta file
>UniRef100_Q6GZX4 Putative transcription factor 001R n=1 Tax=Frog virus 3 (isolate Goorha) (FV-3) RepID=001R_FRG3G
MAFSAEDVLKEYDRRRRMEALLLSLYYPNDRKLLDYKEWSPPRVQVECPKAPVEWNNPPS
EKGLIVGHFSGIKYKGEKAQASEVDVNKMCCWVSKFKDAMRRYQGIQTCKIPGKVLSDLD
AKIKAYNLTVEGVEGFVRYSRVTKQHVAAFLKELRHSKQYENVNLIHYILTDKRVDIQHL
EKDLVKDFKALVESAHRMRQGHMINVKYILYQLLKKHGHGPDGPDILTVKTGSKGVLYDD
SFRKIYTDLGWKFTPL

--------------------------------------------------------------------------------   
usage:   simple_convert_uniprotxml_fasta.py -i uniprot.xml  -o out.fasta.file
"""

#-------------------------------------------------------------------------------   
#Header - Linkers, Libs, Constants
from string import strip
from argparse import ArgumentParser, RawDescriptionHelpFormatter

#-------------------------------------------------------------------------------
#function declarations

#-------------------------------------------------------------------------------
#Body
print("Running...")

if __name__ == '__main__':
    parser = ArgumentParser(usage = "simple_convert_uniprotxml_fasta.py -i \
uniprot.xml  -o out.fasta.file",
                            description=__doc__, 
                            formatter_class=RawDescriptionHelpFormatter)
    parser.add_argument("-i", "--input_file", action="store", 
                        dest="inputfilename",
                        help="xml input file (See DocString for format)")
    parser.add_argument("-o", "--output_file", action="store", 
                        dest="outputfilename",
                        help="fasta output file")
    options = parser.parse_args()

    mandatories = ["inputfilename", "outputfilename"]
    for m in mandatories:
        if not options.__dict__[m]:
            print("\nError: Missing Arguments\n")
            parser.print_help()
            exit(-1)
            
    inputfilename = options.inputfilename
    outputfilename = options.outputfilename    
   
    with open(inputfilename,'U') as infile, open(outputfilename, 'w') as outfile:
        print("Reading xml and writing fasta...." )
        #skip header (5 lines)
        for _ in xrange(5):
            next(infile)               
        for line in infile:
            query = line.strip()
            if query[0] == "<":
                #if query[1:9] == "entry id":
                if "entry id" in query:
                    entrydict = {"entry id": query.split("\"")[1]}
                #elif query[1:17] == "dbReference type" or query[1:14] == "property type":
                elif "dbReference type" in query:
                    property = query.split("\"")
                    if property[1] in ["UniProtKB ID", "UniParc ID"]:
                        entrydict["UniPn ID"] = property[3]
                elif "property type" in query:
                    property = query.split("\"")
                    if property[1] in ["protein name", "common taxon", "member count"]:
                        entrydict[property[1]] = property[3]

                if "<sequence length=" in query:
                    if "protein name" not in entrydict:
                        entrydict["protein name"] = "no protein name"
                    if len(entrydict) == 5:
                        outfile.write(">%s %s n=%s Tax=%s RepID=%s\n" % (entrydict["entry id"], entrydict["protein name"], entrydict["member count"], entrydict["common taxon"], entrydict["UniPn ID"] ))
                        entrydict = {}
                    else:
                        print("Malformed header! \n" + str(entrydict) + "\n")
            

            else:
                outfile.write(line)
                
    print("Done!")
