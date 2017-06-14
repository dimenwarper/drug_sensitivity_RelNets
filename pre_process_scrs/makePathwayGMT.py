#!/usr/bin/env python2.7
"""
makes a single .gmt file out of the pathway.tsv descriptions from pharmGKB
"""

import pandas as pd
import sys
import os 

# Need to gather pathway files
pathway_dir = "../raw_data/pharmGKB_pathways/"

# Output file name
gmt_path = "../data/pharmGKB_pathways.gmt"

def isTsv(filename):
    return filename[-4:] == ".tsv"

def getPathwayFiles():
    """return  *.tsv files in the """
    listOfFiles = os.listdir(pathway_dir)
    return [filename for filename in listOfFiles if isTsv(filename)]

def getPathwayName(filename):
    """parses the pathway name from the filename"""
    pathway_name = filename.split("-")[1]

    try:
        pathway_name = pathway_name[:pathway_name.index("_Pharma")]
    except ValueError:
        pathway_name = pathway_name[:-4]
        pass

    return pathway_name

def gmtToFile(pathway_dict):

    fout = open(gmt_path,'w')

    for pathway_ in pathway_dict.keys():
        fout.write(pathway_ + "\t" + "\t")
        fout.write("\t".join(pathway_dict[pathway_]) +"\n")

    fout.close()

    return None

def main():
    pathway_files = getPathwayFiles()
    pathways = {}

    for filename in pathway_files:
        pathway_name = getPathwayName(filename)
        pharmGKB_pathway_df = pd.read_table(pathway_dir + filename)
        raw_genes = pharmGKB_pathway_df.Genes.dropna()
        geneset = set()

        for genes in raw_genes:
            # Need to get rid of extra string quotes
            cleaned = genes.replace('"',"")

            cleaned = cleaned.split(",")

            geneset |= set(cleaned)

        pathways[pathway_name] = list(geneset)

    gmtToFile(pathways)

if __name__ == "__main__":
    sys.exit(main())