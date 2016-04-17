#code to illustrate natural spline and b-spline

library(splines)

x<-sort(rnorm(500,0,2)) #make sure sort x for spline basis
hist(x,nclass=100)
a<-quantile(x,probs=c(0.00,0.05,0.25,0.50,0.75,0.95,1.00))  #7 knots, including 2 boundary knots


# create b-spline basis
x.bs1<-bs(x, df=8, degree=3, intercept=F)  #automatic placement of knots
x.bs2<-bs(x, knots=a[2:6],degree=3, intercept=F) #specifiy knots using percentiles
cor(x.bs1)
cor(x.bs2)

plot(x,x.bs1[,1],type='l',ylim=c(0,1))
lines(x,x.bs1[,2])
lines(x,x.bs1[,3])
lines(x,x.bs1[,4])
lines(x,x.bs1[,5])
lines(x,x.bs1[,6])
lines(x,x.bs1[,7])
lines(x,x.bs1[,8])

plot(x,x.bs2[,1],type='l',ylim=c(0,1))
lines(x,x.bs2[,2])
lines(x,x.bs2[,3])
lines(x,x.bs2[,4])
lines(x,x.bs2[,5])
lines(x,x.bs2[,6])
lines(x,x.bs2[,7])
lines(x,x.bs2[,8])

# matrix plot
matplot(x, x.bs1, type="l", lwd=2)
matplot(x, x.bs2, type="l", lwd=2)
# matrix plot of orthgonized spline bases
matplot(x, qr.Q(qr(x.bs1)), type="l", lwd=2)
matplot(x, qr.Q(qr(x.bs2)), type="l", lwd=2)


# create natural spline basis 

b1<-(x-a[1])^3*(x>=a[1])
b2<-(x-a[2])^3*(x>=a[2]) 
b3<-(x-a[3])^3*(x>=a[3])
b4<-(x-a[4])^3*(x>=a[4])
b5<-(x-a[5])^3*(x>=a[5])
b6<-(x-a[6])^3*(x>=a[6])
b7<-(x-a[7])^3*(x>=a[7])

d1<-(b1-b7)/(a[7]-a[1]) 
d2<-(b2-b7)/(a[7]-a[2]) 
d3<-(b3-b7)/(a[7]-a[3]) 
d4<-(b4-b7)/(a[7]-a[4])
d5<-(b5-b7)/(a[7]-a[5])
d6<-(b6-b7)/(a[7]-a[6])

N2<-x    #N1, N3, N3, N4, N5, N6, N7 are basis functions, N1 ignored b/c intercept
N3<-d1-d6
N4<-d2-d6
N5<-d3-d6
N6<-d4-d6
N7<-d5-d6


#let's see whether b-splines or natural splines can fit data generated from quadratic polynomial 
y1<-0.5-1.0*x+2.4*x^2-0.5*x^3+0.1*x^4+rnorm(length(x),0,100)
plot(x,y1,cex=.5)
lines(x,0.5-1.0*x+2.4*x^2-0.5*x^3+0.1*x^4,type='l',col=1)


lm1<-lm(y1~x.bs1) #b-spline with automatic knots placement
lines(x,fitted(lm1),type='l',col=2)
summary(lm1)
lm2<-lm(y1~x.bs2) #b-spline with user specified knots placement
lines(x,fitted(lm2),type='l',col=3)
summary(lm2)
lm3<-lm(y1~N2+N3+N4+N5+N6+N7) #natural splines    
lines(x,fitted(lm3),type='l',col=4)
summary(lm3)

## use orthogonal spline basis
lm4<-lm(y1~ qr.Q(qr(x.bs1))) #b-spline with automatic knots placement
lines(x,fitted(lm4),type='l',col=2)
summary(lm4)

