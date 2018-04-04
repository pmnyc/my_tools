
states=row.names(USArrests)
names(USArrests)
apply(USArrests,2,mean)
apply(USArrests,2,var)

#standardize the data to have 0 mean and std dev of 1
#compute PCA
pr.out=prcomp(USArrests,scale=TRUE)
names(pr.out)
pr.out$center
pr.out$scale
pr.out$rotation

#pr.out$x is the projected (on principal components) data
dim(pr.out$x)
biplot(pr.out,scale=0)

#principal components are unique up to a sign change
pr.out$rotation=-pr.out$rotation #direction doesn't change
pr.out$x=-pr.out$x
biplot(pr.out,scale=0)

#standard deviation for each principal component
pr.out$sdev

#variance explained by each component
pr.var=pr.out$sdev^2

#proportion of variance explained
pve=pr.var/sum(pr.var)

#plot % of var explained
plot(pve,xlab='Principal Component',ylab='Proportion of Variance Explained',ylim=c(0,1),type='b')
plot(cumsum(pve),xlab='Principal Component',ylab='Cumulative Proportion of Variance Explained',ylim=c(0,1),type='b')






