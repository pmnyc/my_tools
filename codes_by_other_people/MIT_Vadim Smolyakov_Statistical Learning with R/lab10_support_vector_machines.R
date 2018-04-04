
library(e1071)

#generate observations
set.seed(1)
x=matrix(rnorm(20*2),ncol=2) #data (not linearly separable)
y=c(rep(-1,10),rep(1,10)) #labels
x[y==1,]=x[y==1,]+1
plot(x,col=(3-y))

#encode response as a factor variable to perform SVM classification (as opposed to regression)
dat=data.frame(x=x,y=as.factor(y)) #code response as a factor
svmfit=svm(y~.,data=dat,kernel="linear",cost=10,scale=FALSE) #linear kernel, cost=C
plot(svmfit,dat)
summary(svmfit)

#support vectors
svmfit$index

#decrease cost of violating the boundary
svmfit=svm(y~.,data=dat,kernel="linear",cost=0.1,scale=FALSE) #linear kernel, cost=C
plot(svmfit,dat)
svmfit$index  #number of support vectors increases

#tune() in e1071 performs 10-fold cv
set.seed(1)
tune.out=tune(svm,y~.,data=dat,kernel="linear",ranges=list(cost=c(0.001,0.01,0.1,1,5,10,100)))
summary(tune.out) #C=0.1 gives lowest error

#tune() also stores the best model
bestmod=tune.out$best.model
summary(bestmod)

xtest=matrix(rnorm(20*2),ncol=2)
ytest=sample(c(-1,1),20,rep=TRUE)
xtest[ytest==1,]=xtest[ytest==1,]+1
testdat=data.frame(x=xtest,y=as.factor(ytest))

ypred=predict(bestmod,testdat)
table(predict=ypred,truth=testdat$y)

#SVM
set.seed(1)
x=matrix(rnorm(200*2),ncol=2)
x[1:100,]=x[1:100,]+2
x[101:150,]=x[101:150,]-2
y=c(rep(1,150),rep(2,50))
dat=data.frame(x=x,y=as.factor(y))
plot(x,col=y) #not linearly separable

train=sample(200,100)
svmfit=svm(y~.,data=dat[train,],kernel="radial",gamma=1, cost=1) #RBF kernel
plot(svmfit,dat[train,])
summary(svmfit)

#increasing C leads to non-linear decision boundary
svmfit=svm(y~.,data=dat[train,],kernel="radial",gamma=1, cost=1000) #RBF kernel
plot(svmfit,dat[train,])
summary(svmfit)

#perform cv to choose the best gamma
set.seed(1)
tune.out=tune(svm,y~.,data=dat[train,],kernel='radial',ranges=list(cost=c(0.1,1,10,100,1000)), gamma=c(0.5,1,2,3,4))
summary(tune.out) #cost=1, gamma=0.5 is lowest error

table(true=dat[-train,'y'],pred=predict(tune.out$best.model,newx=dat[-train,]))

#ROC curves
library(ROCR)
rocplot=function(pred,truth,...){
  predob=prediction(pred,truth)
  perf=performance(predob,'tpr','fpr')
  plot(perf,...)
}

svmfit.opt=svm(y~.,data=dat[train,],kernel='radial',gamma=2,cost=1,decision.values=T)
fitted=attributes(predict(svmfit.opt,dat[train,],decision.values=TRUE))$decision.values

par(mfrow=c(1,2))
rocplot(fitted,dat[train,'y'],main='Training Data')

svmfit.flex=svm(y~.,data=dat[train,],kernel="radial",gamma=50,cost=1,decision.values=T)
fitted=attributes(predict(svmfit.flex,dat[train,],decision.values=T))$decision.values
rocplot(fitted,dat[train,"y"],add=T,col='red')

#gamma=2 provides most accurate results for test data
fitted=attributes(predict(svmfit.opt,dat[-train,],decision.values=T))$decision.values
rocplot(fitted,dat[-train,'y'],main='Test Data')
fitted=attributes(predict(svmfit.flex,dat[-train,],decision.values=T))$decision.values
rocplot(fitted,dat[-train,'y'],add='T',col='red')

#SVM with multiple classes
set.seed(1)
x=rbind(x,matrix(rnorm(50*2),ncol=2))
y=c(y,rep(0,50))
x[y==0,2]=x[y==0,2]+2
dat=data.frame(x=x,y=as.factor(y))
par(mfrow=c(1,1))
plot(x,col=(y+1))

svmfit=svm(y~.,data=dat,kernel='radial',cost=10,gamma=1)
plot(svmfit,dat)

#application to gene expression
library(ISLR)
names(Khan)
dim(Khan$xtrain)
dim(Khan$xtest)
length(Khan$ytrain)
length(Khan$ytest)

table(Khan$ytrain)
table(Khan$ytest)

dat=data.frame(x=Khan$xtrain,y=as.factor(Khan$ytrain))
out=svm(y~.,data=dat,kernel='linear',cost=10)
summary(out)
table(out$fitted,dat$y) #no training errors

dat.te=data.frame(x=Khan$xtest,y=as.factor(Khan$ytest))
pred.te=predict(out,newdata=dat.te)
table(pred.te,dat.te$y)









