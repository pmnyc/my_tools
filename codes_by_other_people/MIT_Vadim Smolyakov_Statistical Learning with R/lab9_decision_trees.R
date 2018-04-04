
library(tree)
library(ISLR)

attach(Carseats)

#create a new variable High
High=ifelse(Sales<=8,'No','Yes')

#merge High with the rest of the dataset
Carseats=data.frame(Carseats,High)

#tree(): fit a classification tree
#to predict High using all variables but Sales
tree.carseats=tree(High~.-Sales,Carseats)
summary(tree.carseats)

#use plot() to display tree structure
#use text() to display node labels
plot(tree.carseats)
text(tree.carseats,pretty=0)
tree.carseats

#use predict() to compute classification (type="class") test error
set.seed(2)
train=sample(1:nrow(Carseats),200)
Carseats.test=Carseats[-train,]
High.test=High[-train]

tree.carseats=tree(High~.-Sales,Carseats,subset=train)
tree.pred=predict(tree.carseats,Carseats.test,type="class")
table(tree.pred,High.test)
accuracy=(86+57)/200

#consider pruning the tree() and computing the result
#cv.tree(): performs cross-validation in order to determing optimum tree complexity
#use FUN=prune.misclass to guide cv and pruning process rather than default: deviance

set.seed(3)
cv.carseats=cv.tree(tree.carseats,FUN=prune.misclass)
names(cv.carseats)
cv.carseats

#tree with 9 terminal nodes results in lowest cross-validation error rate
par(mfrow=c(1,2))
plot(cv.carseats$size,cv.carseats$dev,type='b')
plot(cv.carseats$k,cv.carseats$dev,type='b')

#apply prune.misclass() in order to prune the tree to obtain the nine-node tree
prune.carseats=prune.misclass(tree.carseats,best=9)
plot(prune.carseats)
text(prune.carseats,pretty=0)

#how well does pruned tree perform on the test data
tree.pred=predict(prune.carseats,Carseats.test,type='class')
table(tree.pred,High.test)
accuracy=(94+60)/200  #77% accurate

#fitting regression trees
library(MASS)
set.seed(1)
train=sample(1:nrow(Boston),nrow(Boston)/2)
tree.boston=tree(medv~.,Boston,subset=train)
summary(tree.boston)

plot(tree.boston)
text(tree.boston,pretty=0)

cv.boston=cv.tree(tree.boston)
plot(cv.boston$size,cv.boston$dev,type='b')

prune.boston=prune.tree(tree.boston,best=5)
plot(prune.boston)
text(prune.boston,pretty=0)

#we use unpruned tree to make predictions on the test set
yhat=predict(tree.boston,newdata=Boston[-train,])
boston.test=Boston[-train,'medv']
plot(yhat,boston.test)
abline(0,1)
mean((yhat-boston.test)^2)

#bagging and random forests
library(randomForest)
set.seed(1)
bag.boston=randomForest(medv~.,data=Boston,subset=train,mtry=13,importance=TRUE)
bag.boston

#mtry=13 forces randomForest to consider all 13 predictors
#how well does this bagged model perform on the test set?
yhat.bag=predict(bag.boston,newdata=Boston[-train,])
plot(yhat.bag, boston.test)
abline(0,1)
mean((yhat.bag-boston.test)^2) #MSE=13.16 approx half of MSE of single pruned tree

#change the number of trees grown using ntree
bag.boston=randomForest(medv~.,data=Boston,subset=train,mtry=13,ntree=25)
yhat.bag=predict(bag.boston,newdata=Boston[-train,])
mean((yhat.bag-boston.test)^2) #very close to MSE with ntrees=500

#use sqrt(p) variables when building a random forest for classification
#mtry=6
rf.boston=randomForest(medv~.,data=Boston,subset=train,mtry=6,importance=TRUE)
yhat.rf=predict(rf.boston,newdata=Boston[-train,])
mean((yhat.rf-boston.test)^2) #very close to MSE with ntrees=500

#use importance() to view importance of each variable
importance(rf.boston)
varImpPlot(rf.boston) #variable importance plot

#Boosting (regression trees)
library(gbm)
set.seed(1)
boost.boston=gbm(medv~.,data=Boston[train,],distribution='gaussian',n.trees=5000,interaction.depth=4)
summary(boost.boston)

par(mfrow=c(1,2))
plot(boost.boston,i='rm')
plot(boost.boston,i='lstat')

yhat.boost=predict(boost.boston,newdata=Boston[-train,],n.trees=5000)
mean((yhat.boost-boston.test)^2) #MSE=11.8 similar to random forests and superior to bagging

#we can use a different shrinkage parameter lambda
boost.boston=gbm(medv~.,data=Boston[train,],distribution='gaussian',n.trees=5000,interaction.depth=4,shrinkage=0.2,verbose=F)
summary(boost.boston)
yhat.boost=predict(boost.boston,newdata=Boston[-train,],n.trees=5000)
mean((yhat.boost-boston.test)^2) #slightly lower MSE for lambda=0.2










