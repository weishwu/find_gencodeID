queryTabs=as.list(1:3)
queryTabs[[1]]=read.table('gencode_geneID_geneName.txt',header=T,sep='\t',colClasses="character")
queryTabs[[2]]=read.table('ncbi_genes_queryName_geneID.txt',header=T,sep='\t',comment.char="",quote='\"',colClasses="character")
queryTabs[[3]]=read.table('ncbi_genes_queryName_geneID.txt',header=T,sep='\t',comment.char="",quote='\"',colClasses="character")
save(queryTabs,file='queryTabs.RData')


