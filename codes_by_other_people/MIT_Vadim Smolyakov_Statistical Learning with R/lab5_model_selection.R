
library(ISLR)
fix(Hitters)
names(Hitters)
dim(Hitters)

#is.na(): identifies missing (NA) data; returns: TRUE for missing data, FALSE otherwise
sum(is.na(Hitters$Salary))

#na.omit(): removes all rows with missing dat
Hitters=na.omit(Hitters)
dim(Hitters)
sum(is.na(Hitters))

library(leaps) #search for best sub-sets (AIC,BIC,CIC,DIC) using branch-and-bound algorithm
#regsubsets(): identifies the best model that contains a given number of predictors
regfit.full=regsubsets(Salary~.,Hitters)
summary(regfit.full)

regfit.full=regsubsets(Salary~.,data=Hitters,nvmax=19)
reg.summary=summary(regfit.full)
names(reg.summary)
reg.summary$rsq

#plotting RSS, adjusted R^2, Cp, and BIC
par(mfrow=c(2,2))
plot(reg.summary$rss,xlab='Number of Variables',ylab='RSS',type='l')
plot(reg.summary$adjr2,xlab='Number of Variables',ylab='Adjusted RSq',type='l')

which.max(reg.summary$adjr2)
#points() add points to the graph already created (as opposed to creating a new one)
points(11,reg.summary$adjr2[11],col='red',cex=2,pch=20)

plot(reg.summary$cp,xlab='Number of variables',ylab='Cp',type='l')
which.min(reg.summary$cp)
points(10,reg.summary$cp[10],col='red',cex=2,pch=20)

plot(reg.summary$bic,xlab='Number of variables',ylab='BIC',type='l')
which.min(reg.summary$bic)
points(6,reg.summary$bic[6],col='red',cex=2,pch=20)

#plot.regsubsets
plot(regfit.full,scale='r2')
plot(regfit.full,scale='adjr2')
plot(regfit.full,scale='Cp')
plot(regfit.full,scale='bic')
coef(regfit.full,6) #coef for 6-variable model

#forward and backward multivariable fit selection
regfit.fwd=regsubsets(Salary~.,data=Hitters,nvmax=19,method='forward')
summary(regfit.fwd)
regfit.bwd=regsubsets(Salary~.,data=Hitters,nvmax=19,method='backward')
summary(regfit.bwd)

#comparison of 7 variable models
coef(regfit.full,7)
coef(regfit.fwd,7)
coef(regfit.bwd,7)

#choosing among models using the validation set approach and cross-validation
set.seed(1)
train=sample(c(TRUE,FALSE),nrow(Hitters),rep=TRUE)
test=(!train)

regfit.best=regsubsets(Salary~.,data=Hitters[train,],nvmax=19)

#build a model matrix X
test.mat=model.matrix(Salary~.,data=Hitters[test,])

#for each size i, extract the coeffs from regfit.best for the best model of that size
#form predictions y = X beta + eps and compute the test MSE
val.errors=rep(NA,19)
for (i in 1:19){
  coefi=coef(regfit.best,id=i)
  pred=test.mat[,names(coefi)]%*%coefi
  val.errors[i]=mean((Hitters$Salary[test]-pred)^2)
}

plot(val.errors)
which.min(val.errors) #best model contains 10 variables
coef(regfit.best,10)

#capture steps above into a function
predict.regsubsets=function(object,newdata,id,...){
  form=as.formula(object$call[[2]])
  mat=model.matrix(form,newdata)
  coefi=coef(object,id=i)
  xvars=names(coefi)
  mat[,xvars]%*%coefi
}

#regress on the full dataset
regfit.best=regsubsets(Salary~.,data=Hitters,nvmax=19)
coef(regfit.best,10)

#k-fold cross validation
k=10
set.seed(1)
folds=sample(1:k,nrow(Hitters),replace=TRUE)

#cv.errors: 10x19 (k x nvars) matrix where (i,j)-th element
#test MSE for ith cross-validation for the best jth variable
cv.errors=matrix(NA,k,19,dimnames=list(NULL,paste(1:19)))
for (j in 1:k){
  best.fit=regsubsets(Salary~.,data=Hitters[folds!=j,],nvmax=19)
  for(i in 1:19){
    pred=predict(best.fit,Hitters[folds==j,],id=i)
    cv.errors[j,i]=mean((Hitters$Salary[folds==j]-pred)^2)
  }
}

mean.cv.errors=apply(cv.errors,2,mean)
par(mfrow=c(1,1))
plot(mean.cv.errors,type='b')

#cross-validation selects an 11-variable model
#perform best subset selection on the full data set for 11 variables
reg.best=regsubsets(Salary~.,data=Hitters,nvmax=19)
coef(reg.best,11)








