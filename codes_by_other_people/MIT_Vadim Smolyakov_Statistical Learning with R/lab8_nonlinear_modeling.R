#pg 302(287)

library(ISLR)
attach(Wage)

fit=lm(wage~poly(age,4),data=Wage)
coef(summary(fit))

#create a grid of values at which we want predictions
agelims=range(age)
age.grid=seq(from=agelims[1],to=agelims[2])
preds=predict(fit,newdata=list(age=age.grid),se=TRUE) #se: standard error
se.bands=cbind(preds$fit+2*preds$se.fit, preds$fit-2*preds$se.fit)

#plot
par(mfrow=c(1,2),mar=c(4.5,4.5,1,1),oma=c(0,0,4,0))
plot(age,wage,xlim=agelims,cex=.5,col='darkgrey')
title('Degree-4 Polynomial',outer=T)
lines(age.grid,preds$fit,lwd=2,col='blue') #fit
matlines(age.grid,se.bands,lwd=1,col='blue',lty=3)

#ANOVA (using F-test) to test if null hypothesis M1 explains the data vs.
#M2 (more complex model). In order to use anova() M1 must be nested inside M2
#predictors in M1 is a subset of predictors in M2

#5 hypothesis tests
fit.1=lm(wage~age,data=Wage)
fit.2=lm(wage~poly(age,2),data=Wage)
fit.3=lm(wage~poly(age,3),data=Wage)
fit.4=lm(wage~poly(age,4),data=Wage)
fit.5=lm(wage~poly(age,5),data=Wage)

#ANOVA
#low  p-value for 1->2 (comparing M1 to M2) shows that M1 is not sufficient
#high p-value for M5 suggests that M5 is unnecessary
anova(fit.1,fit.2,fit.3,fit.4,fit.5)

#alternatively we could use poly() since it reports orthogonal polynomials
coef(summary(fit.5))

#predicting probability of individual earning more than $250K (logistic regression)
#I() is used to create a binary response variable on the fly
fit=glm(I(wage>250)~poly(age,4),data=Wage,family=binomial)
preds=predict(fit,newdata=list(age=age.grid),se=T)
pfit=exp(preds$fit)/(1+exp(preds$fit))
se.bands.logit=cbind(preds$fit+2*preds$se.fit, preds$fit-2*preds$se.fit)
se.bands=exp(se.bands.logit)/(1+exp(se.bands.logit))

#we could have directly computed the probabilites by selecting type="response"
preds=predict(fit,newdata=list(age=age.grid),type='response',se=T)

#rug (carpet) plot (right hand plot of figure 7.1)
plot(age,I(wage>250),xlim=agelims,type='n',ylim=c(0,.2))
points(jitter(age),I((wage>250)/5),cex=.5,pch="|",col='darkgrey')
lines(age.grid,pfit,lwd=2,col='blue')
matlines(age.grid,se.bands,lwd=1,col='blue',lty=3)

#use cut() function to fit a step function
table(cut(age,4))
fit=lm(wage~cut(age,4),data=Wage)
coef(summary(fit))

#splines
library(splines)
fit=lm(wage~bs(age,knots=c(25,40,60)),data=Wage)
pred=predict(fit,newdata=list(age=age.grid),se=T)
plot(age,wage,col='gray')
lines(age.grid,pred$fit,lwd=2)
lines(age.grid,pred$fit+2*pred$se,lty='dashed')
lines(age.grid,pred$fit-2*pred$se,lty='dashed')

#can use df option to produce a spline with with knots at uniform quantiles of data
#bs(): B-Spline Basis for Polynomial Splines
dim(bs(age,df=6))
attr(bs(age,df=6),'knots')

#ns(): for natural spline
fit2=lm(wage~ns(age,df=4),data=Wage)
pred2=predict(fit2,newdata=list(age=age.grid),se=T)
lines(age.grid,pred2$fit,col='red',lwd=2)

#smooth.spline()
plot(age,wage,xlim=agelims,cex=.5,col='darkgrey')
title("Smoothing Spline")
fit=smooth.spline(age,wage,df=16)
fit2=smooth.spline(age,wage,cv=TRUE)
fit2$df

lines(fit,col='red',lwd=2)
lines(fit2,col='blue',lwd=2)
legend("topright",legend=c("16 DF", "6.8 DF"),col=c('red','blue'),lty=1,lwd=2,cex=.8)

#local regression: loess()
plot(age,wage,xlim=agelims,cex=.5,col='darkgrey')
title('Local Regression')
fit=loess(wage~age,span=.2,data=Wage)
fit2=loess(wage~age,span=.5,data=Wage)
lines(age.grid,predict(fit,data.frame(age=age.grid)),col='red',lwd=2)
lines(age.grid,predict(fit2,data.frame(age=age.grid)),col='blue',lwd=2)
legend("topright",legend=c("Span=0.2", "Span=0.5"),col=c('red','blue'),lty=1,lwd=2,cex=.8)

#GAM
#predict wage using natural spline functions of year and age
#treating education as a qualitative predictor

gam1=lm(wage~ns(year,4)+ns(age,5)+education,data=Wage)

library(gam)
#gam(): generalized additive models, s() specifies a smoothing spline
gam.m3=gam(wage~s(year,4)+s(age,5)+education,data=Wage)
par(mfrow=c(1,3))
plot(gam.m3,se=TRUE,col='blue')

#can use plot.gam() with non-gam objects
plot.gam(gam1,se=TRUE,col='red')

#use ANOVA tests to determine which model is best:
#M1: GAM that excludes year
#M2: GAM that uses a linear function of year
#M3: GAM that uses a spline function of year

gam.m1=gam(wage~s(age,5)+education,data=Wage)
gam.m2=gam(wage~year+s(age,5)+education,data=Wage)
anova(gam.m1,gam.m2,gam.m3,test="F")

#there's compelling evidence (p=0.00014) that M2 is better than M1
#no evidence (p=0.349) that a non-linear function of year is needed

summary(gam.m3)







