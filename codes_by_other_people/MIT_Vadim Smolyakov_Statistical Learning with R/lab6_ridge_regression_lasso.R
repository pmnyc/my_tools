
library(ISLR)
fix(Hitters)
names(Hitters)
dim(Hitters)

#check for missing entries
sum(is.na(Hitters$Salary))
Hitters=na.omit(Hitters)
dim(Hitters)
sum(is.na(Hitters))

#construct design matrix X and regression variable y
x=model.matrix(Salary~.,Hitters)[,-1] #observations vs predictors with categorical data converted to quantitative data
y=Hitters$Salary

#glmnet: used to fit regularized regression models: ridge, lasso, etc...
#alpha=0: ridge regression, alpha=1: lasso model
library(glmnet)
grid=10^seq(10,-2,length=100)
ridge.mod=glmnet(x,y,alpha=0,lambda=grid) #ridge

#matrix: 20 rows (1 for each predictor + intercept) x 100 cols (1 for each lambda)
dim(coef(ridge.mod))
ridge.mod$lambda[50] #lambda=11498
coef(ridge.mod)[,50]
sqrt(sum(coef(ridge.mod)[-1,50]^2)) #exclude intercept col1 and compute l-2 norm

ridge.mod$lambda[60] #lambda=705
coef(ridge.mod)[,60]
sqrt(sum(coef(ridge.mod)[-1,60]^2)) #exclude intercept col1 and compute l-2 norm

#can use new lambda in predict()
predict(ridge.mod,s=50,type='coefficients')[1:20,]

#compare ridge with
set.seed(1)
train=sample(1:nrow(x),nrow(x)/2)
test=(-train)
y.test=y[test]

#predict based on test set by using newx=x[test,] instead of type='coefficients'
ridge.mod=glmnet(x[train,],y[train],alpha=0,lambda=grid,thresh=1e-12) #fit training data
ridge.pred=predict(ridge.mod,s=4,newx=x[test,]) #predict test data (s=lamda)
mean((ridge.pred-y.test)^2) #MSE

#compared to an constant function fit (intercept)
#we would predict the mean of the train data
mean((mean(y[train])-y.test)^2) #MSE

#compare against least squares (i.e. lambda=0)
ridge.pred=predict(ridge.mod,s=0,newx=x[test,],exact=T) #predict test data (s=lamda)
mean((ridge.pred-y.test)^2) #MSE

#use lm for un-regularized fits since it provides p-values for coefficients
lm(y~x,subset=train)
predict(ridge.mod,s=0,exact=T,type='coefficients')[1:20,]

#use cv.glmnet() to choose the value for lambda
#by default does k=10 fold cross-validation can be parameterized with folds
set.seed(1)
cv.out=cv.glmnet(x[train,],y[train],alpha=0) #k=10
plot(cv.out)
bestlam=cv.out$lambda.min #minimum MSE lambda

ridge.pred=predict(ridge.mod,s=bestlam,newx=x[test,])
mean((ridge.pred-y.test)^2) #lower MSE using cv.out$lambda.min

#finally, we refit our ridge regression model on the full dataset
#using the value of lambda chosen by cross-validation and examine coef estimates
out=glmnet(x,y,alpha=0)
predict(out,type='coefficients',s=bestlam)[1:20,]
#as expected, none of the coefficients are zero, ridge regression doesn't perform variable selection

#lasso
lasso.mod=glmnet(x[train,],y[train],alpha=1,lambda=grid)
plot(lasso.mod)

#perform cross validation and compute associated test error
set.seed(1)
cv.out=cv.glmnet(x[train,],y[train],alpha=1)
plot(cv.out)
bestlam=cv.out$lambda.min
lasso.pred=predict(lasso.mod,s=bestlam,newx=x[test,])
mean((lasso.pred-y.test)^2) #similar to ridge regression but sparse

#fit to the whole data-set
out=glmnet(x,y,alpha=1,lambda=grid)
lasso.coef=predict(out,type='coefficients',s=bestlam)[1:20,]
lasso.coef
lasso.coef[lasso.coef!=0] #sparse: only 7 coefficients are non-zero

