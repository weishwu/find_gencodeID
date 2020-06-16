## What it does
This repo contains scripts and data files that find Gencode gene IDs with given gene names. It relies on 3 resources to find the hits, and the search is attempted in the following priority order:
- Gencode GTF: https://www.gencodegenes.org/human/ (currently using v34)
- NCBI gene records: https://www.ncbi.nlm.nih.gov/gene/?term=homo+sapiens (downloaded in Feb 2020)
- HGNC gene aliases: https://www.genenames.org/download/custom/ (downloaded in June 2020)

**Note: if a gene name is found to be linked with more than one Gencode ID it will be reported as no hit.**

## Load function and data in R
```
library(RCurl)
script=getURL("https://raw.githubusercontent.com/weishwu/find_gencodeID/master/find_gencodeID.r", ssl.verifypeer = FALSE)
load(url("https://raw.githubusercontent.com/weishwu/find_gencodeID/master/queryTabs.RData"))
eval(parse(text = script))
```

## Example run
- Read input from a file name which has to end with ".txt". The file contains gene names in the first column, one name per line.
```
hits=find_gencodeID("ENSG_Missing.txt")
```
- Read input from the variable name of a vector of characters. The first column of the matrix is the gene names, one per row.
```
hits=find_gencodeID(ENSG_Missing)
```

## Read below only if data needs to be re-created
- Merge NCBI and HGNC records with Gencode GTF to find the unique matches (each NCBI/HGNC record can only be linked with one Gencode ID; each gene name can only be linked with on Gencode ID).
- Requried inputs: gencode.v34.annotation.gtf.zip, NCBI_genes.txt.zip, HGNC_gene_aliases.txt.zip (downloaded from the links listed above)
```
python gencodeID_queryTables.py gencode.v34.annotation.gtf.zip
```
- Combine the gene name and ID tables created above into an R object
```
Rscript gencodeID_queryTables.r
```



