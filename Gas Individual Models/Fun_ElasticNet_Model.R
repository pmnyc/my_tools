Fun_ElasticNet_Model <- function(data=list(),x,y,wgt=NULL,alpha=0.05,family="gaussian"){
		library(glmnet, quietly=TRUE)
		## ex, x = c("Month", "Y_lag1"); This lists input 
			## variables used in the model
		## ex, y = "Vol"; This gives the target variable name
		## ex, wgt = "Wgt"; This gives the weight variable name
		## alpha specifies the alpha value for Elastic net model
  
		if (nrow(data) < 9){stop("Num of records < 9, failed to perform Elastic-Net model")};
		if (is.null(wgt)){wgt="ONE__";  data$ONE__=rep(1,nrow(data))};
		x_matrix <- as.matrix(data[,x]);
		y_target <- data[,y];
		set.seed(31415926);
		seeds <- round(runif(10) * 1e7,0);
  
		set.seed(seeds[1]);
		cv.fit <- cv.glmnet(x_matrix,y_target, family=family, weights=data[,wgt], alpha=alpha, nfolds=3);
		lambda1 <- cv.fit$lambda.min;
		rm(cv.fit);
  
		set.seed(seeds[2]);
		cv.fit <- cv.glmnet(x_matrix,y_target, family=family, weights=data[,wgt], alpha=alpha, nfolds=3);
		lambda2 <- cv.fit$lambda.min;
		rm(cv.fit);
  
		set.seed(seeds[3]);
		cv.fit <- cv.glmnet(x_matrix,y_target, family=family, weights=data[,wgt], alpha=alpha, nfolds=3);
		lambda3 <- cv.fit$lambda.min;
		rm(cv.fit);
  
		set.seed(seeds[4]);
		cv.fit <- cv.glmnet(x_matrix,y_target, family=family, weights=data[,wgt], alpha=alpha, nfolds=3);
		lambda4 <- cv.fit$lambda.min;
		rm(cv.fit);
				
		set.seed(seeds[5]);
		cv.fit <- cv.glmnet(x_matrix,y_target, family=family, weights=data[,wgt], alpha=alpha, nfolds=3);
		lambda5 <- cv.fit$lambda.min;
		rm(cv.fit);
  
		set.seed(seeds[6]);
		cv.fit <- cv.glmnet(x_matrix,y_target, family=family, weights=data[,wgt], alpha=alpha, nfolds=3);
		lambda6 <- cv.fit$lambda.min;
		rm(cv.fit);
  
		set.seed(seeds[7]);
		cv.fit <- cv.glmnet(x_matrix,y_target, family=family, weights=data[,wgt], alpha=alpha, nfolds=3);
		lambda7 <- cv.fit$lambda.min;
		rm(cv.fit);
  
		set.seed(seeds[8]);
		cv.fit <- cv.glmnet(x_matrix,y_target, family=family, weights=data[,wgt], alpha=alpha, nfolds=3);
		lambda8 <- cv.fit$lambda.min;
		rm(cv.fit);
		
		set.seed(seeds[9]);
		cv.fit <- cv.glmnet(x_matrix,y_target, family=family, weights=data[,wgt], alpha=alpha, nfolds=3);
		lambda9 <- cv.fit$lambda.min;
		rm(cv.fit);
  
		set.seed(seeds[10]);
		cv.fit <- cv.glmnet(x_matrix,y_target, family=family, weights=data[,wgt], alpha=alpha, nfolds=3);
		lambda10 <- cv.fit$lambda.min;		
		rm(cv.fit);
  
		lambda <- (lambda1 + lambda2 + lambda3 + lambda4 +lambda5 + lambda6 + lambda7 + lambda8 + lambda9 + lambda10)/10.0 ;
		s <- lambda;
  
		elsnetfit <- glmnet(x_matrix,y_target, family=family, weights=data[,wgt], alpha=alpha, lambda=s);
		elsnet.coef <- coef(elsnetfit,s=s);
		elsnetfit.pred <- predict(elsnetfit, x_matrix, s=lambda);
  
		bias <- sum(data[,y] * data[,wgt])/sum(data[,wgt])- sum(elsnetfit.pred * data[,wgt])/sum(data[,wgt]);
		elsnet.coef["(Intercept)",] <- elsnet.coef["(Intercept)",] + bias;
  
  return(elsnet.coef)
}