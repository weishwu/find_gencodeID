## Load function and data in R
```
library(RCurl)
script=getURL("https://raw.githubusercontent.com/weishwu/find_gencodeID/master/find_gencodeID.r", ssl.verifypeer = FALSE)
load(url("https://raw.githubusercontent.com/weishwu/find_gencodeID/master/queryTabs.RData"))
eval(parse(text = script))
```

## Example run
- "ENSG_Missing.txt" is a file that contains gene names in the first column, one name per line.
```
hits=find_gencodeID("ENSG_Missing.txt")
```

## Read below only if data needs to be re-created
- Merge NCBI and HGNC records with Gencode GTF to find the unique matches (each NCBI/HGNC record can only be linked with one gencode ID; each gene name can only be linked with on Gencode ID).
- Requried inputs: gencode.v34.annotation.gtf.zip, NCBI_genes.txt.zip, HGNC_gene_aliases.txt.zip
```
python gencodeID_queryTables.py gencode.v34.annotation.gtf.zip
```
Combine the gene name and ID tables created above into an R object
```
Rscript gencodeID_queryTables.r
```



