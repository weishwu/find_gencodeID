import pandas as pd
import re
import os
import sys

gencode_gtf=sys.argv[1]
# load gencode gtf and extract genes
gn=pd.read_csv(gencode_gtf,sep='\t',comment='#',header=None,dtype=str,compression='zip')
gn=gn.loc[gn.iloc[:,2]=='gene']
gn['gene_id']=gn.iloc[:,8].apply(lambda x: [y for y in x.split(';') if y.startswith('gene_id')][0].split()[1].replace('"','').replace(';',''))
gn['gene_name']=gn.iloc[:,8].apply(lambda x: [y for y in x.split(';') if y.startswith(' gene_name')][0].split()[1].replace('"','').replace(';',''))
gn=gn[['gene_id','gene_name']]
gn['source']='GencodeGTF'

# load HGNC aliases and merge with gencode genes
hgnc=pd.read_csv('HGNC_gene_aliases.txt.zip',sep='\t',dtype=str,compression='zip').fillna('.')
hgnc['all_names']=hgnc.apply(lambda x: re.sub(';$','',re.sub('^;','',';'.join([x.strip() for x in list(set((str(x['Approved symbol'])+','+str(x['Previous symbols,'])+','+str(x['Alias symbols,'])).split(',')))]).replace(';;',';'))),axis=1)
hgnc=hgnc.join(hgnc['all_names'].str.split(';',expand=True).stack().reset_index(level=1,drop=True).rename('query_name')).reset_index().merge(gn,left_on='query_name',right_on='gene_name')[['index','all_names','gene_id','gene_name']].drop_duplicates()
hgnc=hgnc.loc[hgnc['index'].duplicated(keep=False)==False]
hgnc=hgnc.join(hgnc['all_names'].str.split(';',expand=True).stack().reset_index(level=1,drop=True).rename('query_name'))[['query_name','gene_id']].drop_duplicates()
hgnc=hgnc.loc[hgnc['query_name'].duplicated(keep=False)==False]
hgnc['query_name']=';'+hgnc['query_name']+';'
hgnc['source']='HGNC'

# load ncbi records
ncbi=pd.read_csv('NCBI_genes.txt.zip',sep='\t',dtype=str,compression='zip').fillna('.')[['GeneID','Symbol','Aliases']]
ncbi['all_names']=ncbi.apply(lambda x: ';'.join([x['Symbol']]+['LOC'+x['GeneID']]+[y.strip() for y in x['Aliases'].split(',') if y!='.']),axis=1)
ncbi=ncbi.join(ncbi['all_names'].str.split(';',expand=True).stack().reset_index(level=1,drop=True).rename('query_name')).reset_index().merge(gn,left_on='query_name',right_on='gene_name')[['index','all_names','gene_id','gene_name']].drop_duplicates()
ncbi=ncbi.loc[ncbi['index'].duplicated(keep=False)==False]
ncbi=ncbi.join(ncbi['all_names'].str.split(';',expand=True).stack().reset_index(level=1,drop=True).rename('query_name'))[['query_name','gene_id']].drop_duplicates()
ncbi=ncbi.loc[ncbi['query_name'].duplicated(keep=False)==False]
ncbi['query_name']=';'+ncbi['query_name']+';'
ncbi['source']='NCBI'

## write out
gn['gene_name']=';'+gn['gene_name']+';'
gn.to_csv('gencode_geneID_geneName.txt',sep='\t',index=False)
hgnc.to_csv('hgnc_aliases_queryName_geneID.txt',sep='\t',index=False)
ncbi.to_csv('ncbi_genes_queryName_geneID.txt',sep='\t',index=False)


