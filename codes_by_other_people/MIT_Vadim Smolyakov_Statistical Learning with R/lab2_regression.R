

library(MASS)
library(ISLR)

fix(Boston)
names(Boston)
attach(Boston)

#linear model (regression)
#lm(y~x,data): y - response, x - predictor, data - training dataset
lm.fit=lm(medv~lstat) #y=theta dot x + theta_0
summary(lm.fit)
names(lm.fit) #see what else is stored in lm.fit that we can access
coef(lm.fit)  #alternative to lm.fit$coefficients

#confidence interval for coeffs
confint(lm.fit)

#predict medv for a new value of lstat using the linear model
predict(lm.fit,data.frame(lstat=(c(5,10,15))), interval="confidence") #95% conf interval on lstat
predict(lm.fit,data.frame(lstat=(c(5,10,15))), interval="prediction") #95% prediction interval on medv

#plot data and linear fit
#lm.fit=lm(medv~rm) #y=theta dot x + theta_0
#plot(rm,medv,pch="+")
#abline(lm.fit,lwd=3,col='red')

plot(lstat,medv)
plot(lstat,medv,pch=20)
plot(lstat,medv,pch="+")
plot(1:25,1:25,pch=1:25) #plot markers
abline(lm.fit)  #abline(a,b): draws a line with intercept a and slope b
abline(lm.fit,lwd=3,col='red')

#multiple figures
#par(mfrow=c(2,2))
par(mfrow=c(1,1))
plot(lstat,medv)
plot(lstat,medv,pch=20)
plot(lstat,medv,pch="+")
plot(1:25,1:25,pch=1:25) #plot markers

plot(predict(lm.fit),residuals(lm.fit))
plot(predict(lm.fit),rstudent(lm.fit))
plot(hatvalues(lm.fit))
which.max(hatvalues(lm.fit)) #return max index (largest leverage statistic)

#multiple linear regression
lm.fit=lm(medv~lstat+age,data=Boston)
summary(lm.fit)

#regress based on all variables
lm.fit=lm(medv~.,data=Boston)
summary(lm.fit)

?summary.lm #to see what's available to access
summary(lm.fit)$r.sq
summary(lm.fit)$sigma

library(car)
vif(lm.fit) #variance inflation factor vif=1/(1-R_i**2)

#regress based on all variables but one
lm.fit=lm(medv~.-age,data=Boston)
summary(lm.fit)

#alternatively the update() function can be used
lm.fit=update(lm.fit,~.-age) #update and re-fit a model call

#interaction terms
#lstat:black - includes interactin terms between lstat and black: lstat x black
#lstat*age   - includes lstat, age, and lstat x age
summary(lm(medv~lstat*age,data=Boston))

#non-linear transformations of the predictors
#use I(X^2) to create a predictor X^2
lm.fit2=lm(medv~lstat+I(lstat^2))

#use anova() to quantify superiority of quadratic fit to linear fit
#anova: statistical test of whether or not the means of several groups are equal
#generalization of t-test
lm.fit=lm(medv~lstat)
anova(lm.fit,lm.fit2)

#polynomial fit (5th order is still significant)
lm.fit5=lm(medv~poly(lstat,5))
summary(lm.fit5)

#polynomial fit (6th order is no longer significant)
lm.fit6=lm(medv~poly(lstat,6))
summary(lm.fit6)

#logarithmic fit
summary(lm(medv~log(rm),data=Boston))

#Qualitative Predictors
fix(Carseats)
names(Carseat)
#creates dummy vars for quantitative variables
lm.fit=lm(Sales~.+Income:Advertising+Price:Age,data=Carseats)
summary(lm.fit)

attach(Carseats)
contrasts(ShelveLoc) #returns coding used for qualitative variable ShelveLoc
#high positive coef for ShelveLocGood indicates higher contribution to Sales
#compared to a smaller positive coef for ShelveLocMedium
coef(lm.fit)

#function to load libraries
LoadLibraries=function(){
library(ISLR)
library(MASS)
print("The libraries have been loaded.")
}





