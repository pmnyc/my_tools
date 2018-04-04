
library(ISLR)
set.seed(1)

#sample(x,size,replace=FALSE) sample size from x with or without replacement
train=sample(392,196)

#use subset in lm to fit only a subset of data
lm.fit=lm(mpg~horsepower,data=Auto,subset=train)

attach(Auto)
mean((mpg-predict(lm.fit, Auto))[-train]^2)

lm.fit2=lm(mpg~poly(horsepower,2),data=Auto,subset=train)
mean((mpg-predict(lm.fit2, Auto))[-train]^2)

lm.fit3=lm(mpg~poly(horsepower,3),data=Auto,subset=train)
mean((mpg-predict(lm.fit3, Auto))[-train]^2)

#choosing a different training set we obtain different errors during validation

#LOOCV (leave one out cross validation)
glm.fit=glm(mpg~horsepower,data=Auto)
coef(glm.fit)

#cv.glm is part of boot library
library(boot)
glm.fit=glm(mpg~horsepower,data=Auto)
cv.err=cv.glm(Auto,glm.fit)
#cross validation results (test error: cv.err$delta) 
#cv.err$delta: 1st # standard K-fold test error estimate, 2nd # bias corrected version
cv.err$delta

#compute cv error for different polynomial fits
cv.error=rep(0,5)
for (i in 1:5){
  glm.fit=glm(mpg~poly(horsepower,i),data=Auto)
  cv.error[i]=cv.glm(Auto,glm.fit)$delta[1]
}

#K-fold cross-validation
set.seed(17)
cv.error.10=rep(0,10)
for (i in 1:10){
  glm.fit=glm(mpg~poly(horsepower,i),data=Auto)
  cv.error.10[i]=cv.glm(Auto,glm.fit,K=10)$delta[1]  
}

#Bootstrap

#input (X,Y) data and index vector indicating
#which observations should be used to estimate alpha

alpha.fn=function(data,index){
  X=data$X[index]
  Y=data$Y[index]
  return ((var(Y)-cov(X,Y))/(var(X)+var(Y)-2*cov(X,Y)))
}

alpha.fn(Portfolio,1:100)

#randomly sample 100 observations with replacement
set.seed(1)
alpha.fn(Portfolio,sample(100,100,replace=T))

#perform alpha.fn many times, compute alphas and resulting deviation of alphas
boot(Portfolio,alpha.fn,R=1000)
#alpha_est=original, SE(alpha) = std. error (accuracy of alpha)

#estimating the accuracy of a linear regression model
#bootstrap can assess the variability of coefficient estimates
boot.fn=function(data,index){
  return (coef(lm(mpg~horsepower,data=data,subset=index)))
}

set.seed(1)
boot.fn(Auto,1:392)
boot.fn(Auto,sample(392,392,replace=T))
boot.fn(Auto,sample(392,392,replace=T))

#compute accuracy of coefficients
boot(Auto,boot.fn,1000)
summary(lm(mpg~horsepower,data=Auto))$coef

#define the bootstrap function for glm
boot.fn=function(data,index){
  return (coef(lm(mpg~horsepower+I(horsepower^2),data=data,subset=index)))
}

set.seed(1)
boot.fn(Auto,1:392)
summary(lm(mpg~horsepower,data=Auto))$coef


