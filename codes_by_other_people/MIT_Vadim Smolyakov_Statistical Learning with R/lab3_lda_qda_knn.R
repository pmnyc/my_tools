
library(ISLR)
attach(Smarket)
fix(Smarket)

names(Smarket) #Lag1...Lag5 % return on 5 prev day trading, Today: % return on day in question
dim(Smarket)
summary(Smarket)

cor(Smarket) #error: direction variable is qualitative
cor(Smarket[,-9]) #low correlation between today and lag1-5
plot(Volume) #increase in the number of trades

#logistic regression

#glm(): generalized linear models
#family=binomial tells R to run logistic regression
glm.fit=glm(Direction~Lag1+Lag2+Lag3+Lag4+Lag5+Volume,data=Smarket,family=binomial)
#Lag1 has smallest pvalue for market direction
#neg coeff on Lag1 indicates that market direction will be opposite to previous day's
summary(glm.fit)
coef(glm.fit)
summary(glm.fit)$coef

#type=response tells R to output probabilities of the form P(y=1|x)
glm.probs=predict(glm.fit,type="response")
glm.probs[1:10]
contrasts(Direction) #up:1 down:0 (categorical data)

#map predictions to a qualitative vector
glm.pred=rep("Down",length(glm.probs))
glm.pred[glm.probs>0.5]="Up"

#produce the confusion / contingence matrix
table(glm.pred,Direction) #diagonal: correct predictions
mean(glm.pred==Direction) #compute the fraction of correct predictions (i.e. TP+TN / Ntot)

#cross-validation
#train for years 2001-2004 and test for year >= 2005
train=(Year<2005)
Smarket.2005=Smarket[!train,]
dim(Smarket.2005)
Direction.2005=Direction[!train]

#train glm on a subset of data
glm.fit=glm(Direction~Lag1+Lag2+Lag3+Lag4+Lag5+Volume,data=Smarket,family=binomial,subset=train)
glm.probs=predict(glm.fit,Smarket.2005,type="response")

glm.pred=rep("Down",length(glm.probs))
glm.pred[glm.probs>0.5]="Up"
table(glm.pred,Direction.2005)
mean(glm.pred==Direction.2005) #test accuracy rate
mean(glm.pred!=Direction.2005) #test error rate

#predictors with high p-values can increase variance without corresponding decrease in bias
#choose two lowest p-value predictors
glm.fit=glm(Direction~Lag1+Lag2,data=Smarket,family=binomial,subset=train)
glm.probs=predict(glm.fit,Smarket.2005,type="response")
glm.pred=rep("Down",length(glm.probs))
glm.pred[glm.probs>0.5]="Up"
table(glm.pred,Direction.2005)
mean(glm.pred==Direction.2005) #test accuracy rate

#predicting returns associated with particular values of Lag1 and Lag2
predict(glm.fit,newdata=data.frame(Lag1=c(1.2,1.5),Lag2=c(1.1,-0.8)),type="response")

#Linear Discriminant Analysis (for categorical classification into K>2 classes)
library(MASS)
#lda(): linear discriminant analysis
lda.fit=lda(Direction~Lag1+Lag2,data=Smarket,subset=train)
plot(lda.fit)

lda.pred=predict(lda.fit,Smarket.2005)
names(lda.pred)
lda.class=lda.pred$class
table(lda.class,Direction.2005)
mean(lda.class==Direction.2005)

sum(lda.pred$posterior[,1]>=0.5)
sum(lda.pred$posterior[,1]<0.5)

lda.pred$posterior[1:20,1]
lda.class[1:20]

#Quadratic Discriminant Analysis (QDA)
qda.fit=qda(Direction~Lag1+Lag2,data=Smarket,subset=train)
qda.class=predict(qda.fit,Smarket.2005)$class
table(qda.class,Direction.2005)
mean(qda.class==Direction.2005) #test accuracy rate (higher compared to linear)

#K-Nearest Neighbors
library(class)
#cbind() merges columns
train.X=cbind(Lag1,Lag2)[train,] #training data
test.X=cbind(Lag1,Lag2)[!train,] #test data
train.Direction=Direction[train] #training class labels

#knn breaks ties at random (coin flip) so set seed
set.seed(1)
knn.pred=knn(train.X,test.X,train.Direction,k=1) #K=1 (# of NN)
table(knn.pred,Direction.2005)
mean(knn.pred==Direction.2005)

knn.pred=knn(train.X,test.X,train.Direction,k=3) #K=3 (# of NN)
table(knn.pred,Direction.2005)
mean(knn.pred==Direction.2005)

#Caravan Insurance Data
dim(Caravan)
attach(Caravan)
summary(Purchase)

#scale(): standardize data to normalize for units
#centers the columns, all variables are given a mean of zero and variance of one
standardized.X=scale(Caravan[,-86])
var(Caravan[,1])
var(Caravan[,2])
var(standardized.X[,1])
var(standardized.X[,2])

mean(Caravan[,1])
mean(Caravan[,2])
mean(standardized.X[,1])
mean(standardized.X[,2])

test=1:1000
train.X=standardized.X[-test,]
test.X=standardized.X[test,]
train.Y=Purchase[-test]
test.Y=Purchase[test]

set.seed(1)
knn.pred=knn(train.X,test.X,train.Y,k=1)
mean(test.Y!=knn.pred) #error rate
mean(test.Y!="No")
table(knn.pred,test.Y)

knn.pred=knn(train.X,test.X,train.Y,k=2)
mean(test.Y!=knn.pred) #error rate
mean(test.Y!="No")
table(knn.pred,test.Y) #TPR=10.6 > 6% by guessing 

knn.pred=knn(train.X,test.X,train.Y,k=5)
mean(test.Y!=knn.pred) #error rate
mean(test.Y!="No")
table(knn.pred,test.Y) #TPR=26.7 > 6% by guessing

#compare with logistic regression
#for a cut-off of 0.5, 0 predictions are correct
#for a cut-off of 0.25, 33% of predictions are correct

glm.fit=glm(Purchase~.,data=Caravan,family=binomial,subset=-test)
glm.probs=predict(glm.fit,Caravan[test,],type='response')
glm.pred=rep("No",length(glm.probs))
glm.pred[glm.probs>0.5]="Yes"  #0.5 cutoff
table(glm.pred,test.Y) #TPR=0

glm.pred=rep("No",length(glm.probs))
glm.pred[glm.probs>0.25]="Yes"
table(glm.pred,test.Y) #TPR=33.3%


