
#set seed to reproduce kmeans output
set.seed(2)

#synthetic data (K=2 clusters)
x=matrix(rnorm(50*2),ncol=2)
x[1:25,1]=x[1:25,1]+3
x[1:25,2]=x[1:25,2]-4

km.out=kmeans(x,2,nstart=20)
names(km.out)

#cluster assignments
km.out$cluster

#for high dimensional data can first perform PCA and plot the first two components
plot(x,col=(km.out$cluster+1),main='K-means Clustering Results with K=2',xlab='',ylab='',pch=20,cex=2)

set.seed(4)
km.out=kmeans(x,3,nstart=20)
km.out

#nstart: number of initializations
#use high nstart to avoid local optimum
set.seed(3)
km.out=kmeans(x,3,nstart=1)
km.out$tot.withinss

km.out=kmeans(x,3,nstart=20)
km.out$tot.withinss

#hierarchical clustering
hc.complete=hclust(dist(x),method='complete') #complete linkage
hc.average=hclust(dist(x),method='average') #average linkage
hc.single=hclust(dist(x),method='single') #single linkage

#plot dendograms
par(mfrow=c(1,3))
plot(hc.complete,main='Complete Linkage',xlab='',sub='',cex=.9)
plot(hc.average,main='Average Linkage',xlab='',sub='',cex=.9)
plot(hc.single,main='Single Linkage',xlab='',sub='',cex=.9)

#cutree: determines the cluster labels for a given cut level
cutree(hc.complete,2)
cutree(hc.average,2)
cutree(hc.single,2)
cutree(hc.single,4)

#use scale() to scale variables before hierarchical clustering
xsc=scale(x)
plot(hclust(dist(xsc),method='complete'),main="Hierarchical Clustering with Scaled Features")

#use as.dist() for correlation based distance
x=matrix(rnorm(30*3),ncol=3)
dd=as.dist(1-cor(t(x)))
plot(hclust(dd,method='complete'),main='Complete Linkage with Correlation-Based Distance',xlab='',sub='')

#NCI60 data example (mirco-array data)
library(ISLR)
nci.labs=NCI60$labs
nci.data=NCI60$data
dim(nci.data)
nci.labs[1:4]
table(nci.labs)

pr.out=prcomp(nci.data,scale=TRUE)
Cols=function(vec){
  cols=rainbow(length(unique(vec)))
  return(cols[as.numeric(as.factor(vec))])
}

#plot principal component scores
par(mfrow=c(1,2))
plot(pr.out$x[,1:2],col=Cols(nci.labs),pch=19,xlab='Z1',ylab='Z2')
plot(pr.out$x[,c(1,3)],col=Cols(nci.labs),pch=19,xlab='Z1',ylab='Z3')

#similar cancer types tend to have similar gene expression levels on the first two principal components
summary(pr.out)
plot(pr.out)

#proportion of variance explained
pr.var=pr.out$sdev^2
pve=100*pr.var/sum(pr.var)

par(mfrow=c(1,2))
plot(pve,type='o',xlab='Principal Component',ylab='PVE',col='blue')
plot(cumsum(pve),type='o',xlab='Principal Component',ylab='Cumulative PVE',col='brown3')

#clustering of observations
sd.data=scale(nci.data)
data.dist=dist(sd.data)

hc.complete=hclust(data.dist,method='complete') #complete linkage
hc.average=hclust(data.dist,method='average') #average linkage
hc.single=hclust(data.dist,method='single') #single linkage

#plot dendograms
par(mfrow=c(1,3))
plot(hc.complete,main='Complete Linkage',xlab='',sub='',cex=.9)
plot(hc.average,main='Average Linkage',xlab='',sub='',cex=.9)
plot(hc.single,main='Single Linkage',xlab='',sub='',cex=.9)

hc.out=hclust(dist(sd.data))
hc.clusters=cutree(hc.out,4)
table(hc.clusters,nci.labs)

par(mfrow=c(1,1))
plot(hc.out,labels=nci.labs)
abline(h=139,col='red')
hc.out

#rather than performing clustering on the entire data
#we can cluster the first few principal components
hc.out=hclust(dist(pr.out$x[,1:5]))
plot(hc.out,labels=nci.labs,main="Hier. Clust. on First Five Score Vectors")
table(cutree(hc.out,4),nci.labs)

















