
#functions
ls()
objects()
rm(list=ls())

#vectors and matrices
x1<-c(1,2,3,4)
x2<-c(1,0,1,0)
y=x1+x2
length(y)

?matrix
x=matrix(c(1,2,3,4),2,2)
sqrt(x)

#random variables
rm(list=ls())
set.seed(123)
z1=rnorm(10)
mu=mean(z1)
s2=var(z1)

#graphics
rm(list=ls())
x1=rnorm(100)
x2=rnorm(100)
pdf("lab1_plot.pdf") #save the plot
plot(x1,x2, xlab='x-axis',ylab='y-axis',main='y vs. x')
dev.off() #end of save

rm(list=ls())
x=seq(1,10)
x=seq(-pi,pi,length=50)
y=x
f=outer(x,y,function(x,y) cos(y)/(1+x^2))
contour(x,y,f)
contour(x,y,f,nlevels=45,add=T)
fa=(f-t(f))/2
contour(x,y,fa,nlevels=15)
image(x,y,fa)
persp(x,y,fa)
persp(x,y,fa,theta=30)
persp(x,y,fa,theta=30,phi=20)

#indexing data
rm(list=ls())
A=matrix(1:16,4,4)
A[1,2]
A[c(1,3),c(2,4)]
A[1:3,2:4]
A[,2:4]
A[1,]
A[-c(1,3),] #all rows except c(1,3)
dim(A)

#loading data
#read.table()
#write.table()

#http://www-bcf.usc.edu/~gareth/ISL/data.html
Auto=read.table("Auto.data")
fix(Auto)
rm(Auto)

Auto=read.csv("Auto.csv", header=T, na.strings="?")
#only 5 rows contain missing data: omit those rows
Auto=na.omit(Auto)
names(Auto)

#indicate that cylinders and mpg belong to Auto data-frame
plot(Auto$cylinders, Auto$mpg)
attach(Auto) #tells R to make variables in data frame Auto available by name
plot(cylinders,mpg)

#convert cylinders to a qualitative (categorical) variable
cylinders=as.factor(cylinders)

#box plot automatically produced for categorical variable
plot(cylinders,mpg)
plot(cylinders,mpg, col="red")
plot(cylinders,mpg, col="red",varwidth=T)
plot(cylinders,mpg, col="red",varwidth=T,horizontal=T)
plot(cylinders,mpg, col="red",varwidth=T,horizontal=T,xlab="cylinders",ylab="MPG")

#plot a histogram
hist(mpg)
hist(mpg,col=2)
hist(mpg,col=2,breaks=15)

#plot a scatterplot matrix (scatterplot for every pair of elements)
pairs(Auto)
#scatter plot for a subset of variables in Auto data-set
pairs(~mpg+displacement+horsepower+weight+acceleration,Auto)

#identify (prints out information about points on the plot)
plot(horsepower,mpg)
identify(horsepower,mpg,name)

#statistical summary of each variable in the data set
summary(Auto)

#statistical summary for a single variable
summary(mpg)

#savehistory()
#loadhistory()








