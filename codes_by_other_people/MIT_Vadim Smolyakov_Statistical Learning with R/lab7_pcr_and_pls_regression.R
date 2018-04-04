
library(ISLR)
fix(Hitters)
names(Hitters)
dim(Hitters)

#check for missing entries
sum(is.na(Hitters$Salary))
Hitters=na.omit(Hitters)
dim(Hitters)
sum(is.na(Hitters))

#PCR: Principle Component Regression
library(pls)
set.seed(2)
pcr.fit=pcr(Salary~.,data=Hitters,scale=TRUE,validation='CV')
summary(pcr.fit) #shows % of variance explained vs the number of PCA components M

validationplot(pcr.fit,val.type='MSEP') #MSE plot

#perform PCR on the training data
set.seed(1)
pcr.fit=pcr(Salary~.,data=Hitters,subset=train,scale=TRUE,validation='CV')
validationplot(pcr.fit,val.type="MSEP")

x=model.matrix(Salary~.,Hitters)[,-1]
y=Hitters$Salary

#train=sample(c(TRUE,FALSE),nrow(Hitters),rep=TRUE)
test=(!train)
y.test=y[test]
pcr.pred=predict(pcr.fit,x[test,],ncomp=7)
mean((pcr.pred-y.test)^2)

pcr.fit=pcr(y~x,scale=TRUE,ncomp=7)
summary(pcr.fit)

#partial least squares
set.seed(1)
pls.fit=plsr(Salary~.,data=Hitters,subset=train,scale=TRUE,validation="CV")
summary(pls.fit)

#lowest cv error occurs only when M=2
validationplot(pls.fit,val.type="MSEP")

pls.pred=predict(pls.fit,x[test,],ncomp=2)
mean((pls.pred-y.test)^2)

#perform PLS using the full dataset using M=2,
#the number of components identified by cross-validation
#scale=TRUE normalizes the predictor by its std dev
pls.fit=plsr(Salary~.,data=Hitters,scale=TRUE,ncomp=2)
summary(pls.fit)





