find_gencodeID=function(input)
{
d=read.table(input,strip.white=T,blank.lines.skip=T,colClasses="character")[,1,drop=F]
print(paste("Read in gene names: ",nrow(d),sep=""))
g=unique(d)
print(paste("Unique gene names: ",nrow(g),sep=""))
g[,2]=paste(';',as.character(g[,1]),';',sep='')
colnames(g)=c('query_name','query_name0')

#load('queryTabs.RData')
gtf=queryTabs[[1]]
ncbi=queryTabs[[2]]
hgnc=queryTabs[[3]]

g_1=merge(g,gtf,by.x='query_name0',by.y='gene_name',all.x=T)
g_11=g_1[!is.na(g_1[,3]),]
g_10=g_1[is.na(g_1[,3]),]
print(paste("Find gene names within Gencode GTF: ",nrow(g_11),sep=""))

g_2=merge(g_10[,1:2],ncbi,by.x='query_name0',by.y='query_name',all.x=T)
g_21=g_2[!is.na(g_2[,3]),]
g_20=g_2[is.na(g_2[,3]),]
print(paste("Find remaining gene names within NCBI records: ",nrow(g_21),sep=""))

g_3=merge(g_20[,1:2],hgnc,by.x='query_name0',by.y='query_name',all.x=T)
g_31=g_3[!is.na(g_3[,3]),]
g_30=g_3[is.na(g_3[,3]),]
print(paste("Find remaining gene names within HGNC aliases: ",nrow(g_31),sep=""))

all=rbind(g_30,g_11,g_21,g_31)
all[is.na(all)]='.'
print(paste("Remaining gene names without hits: ",nrow(all[all[,3]=='.',]),sep=""))
all[,-1]
}
print("Run it as: hits=find_gencodeID(fn) # fn is the name of the file that contains the gene names in the 1st column")

