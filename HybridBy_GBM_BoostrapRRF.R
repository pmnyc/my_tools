Hybrid_Regression_By_Parallel_GBM_RRF_Fun = function(x,y, ntree_rf, ntree_gb,
                                        gbm_dist="laplace", shrinkage=0.1,
                                        maxdepth_gbm = 30, cvfolds_gbm=25, trainperc=0.7,
                                        maxdepth_rf = NULL, useGBM_ind = "Y", useRRF_ind = "Y",
                                        samplesize_rf=NULL, ncore=NULL, replace_rf=FALSE){
    ## This ensembles the Guided Random Forest and Gradient Descent Boosting Methods
    ## It only applies to the regression analysis, the target variable must be non-negative
    ## The string fields must be converted to factors, and no more than 32 levels
    ## ntree_rf is the number of trees trained for random forest
    ## ntree_gb is the number of trees trained for GBM model
    ## parameters after ntree_gb are for GBM model parameters
    ## maxdepth_gbm is the max depth of GBM trees
    ## trainperc is the percentage of the total sample used for training data to get weights
    ## gamma_ is the gamma for guided random forest
    ## useGBM_ind and useRRF_ind are two indicators to indicate whether to use those two models
    
    ## ncore is the number of computer cores. If not specified, it will use all computer cores
    
    ## RRF uses naroughfix to be as na.action
    
    ## maxdepth_rf is the max number of variables to be used for random forest
    ## samplesize_rf defines the sample size used in each round of tree building
    ## replace_rf tells whether the sampling using replace or not
    
    shrinkage_ = shrinkage;
    rm(shrinkage);
    if (is.null(maxdepth_rf)){maxdepth_rf = ceiling(0.4 * ncol(x))}
    ydata = as.data.frame(y); names(ydata) = "y";
    data_ = cbind(ydata,x);
    
    if (is.null(samplesize_rf)){samplesize_rf = 0.632 * nrow(x)}
    
    ## Define a function that removes factors having more than n levels or only one level
    removeFactrOver_n_Fun = function(data, n){
    ## n defines the highest
        listOfVar = c("");
        for (i in seq(ncol(data))){
            rec = data[1,i];
            if (is.factor(rec)){
                fctrelevel = length(levels(rec));
                if (fctrelevel == 1 | fctrelevel > n){
                    listOfVar = c(listOfVar,names(data)[i]);
                }
            }
        }
        listOfVar = setdiff(listOfVar,"");
        if (length(listOfVar) >=1){data[,listOfVar]=data.frame(NULL)};
        return(data)
    };
    
    ncore_=ncore;
    samplesize_rf_=samplesize_rf;
    parallelRandomForest = function(x,y,ntree=500,mtry,nodesize=1,ncore=ncore_,samplesize_rf=samplesize_rf_){
    # x, y are the training input and target matrix
    # ntree is the total # of trees trained
    # ncore is the number of cores of computer
    
    # mtry is the number of variables to be used in split
    
    library(parallel)
    library(randomForest)

    if (is.null(ncore)){ncore = parallel::detectCores()}
   
    ntree = ceiling(ntree/(ncore+0.000));
    
    RF = function(X,x,y,ntree,mtry,nodesize,samplesize_rf){
        xfix = randomForest::na.roughfix(x);
        set.seed(round(runif(1)*1e5,0));
        sampleindex = sample(seq(nrow(xfix)),samplesize_rf,replace=FALSE);
        xfix_sample = xfix[sampleindex,];
        y_sample = y[sampleindex];
        rf_tree = randomForest::randomForest(x=xfix_sample, y=y_sample, ntree=1, mtry=mtry , nodesize=nodesize, replace=replace_rf);
        
        for (i in seq(ntree)){
            set.seed(round(runif(1)*1e5,0));
            sampleindex = sample(seq(nrow(xfix)),samplesize_rf,replace=FALSE);
            xfix_sample = xfix[sampleindex,];
            y_sample = y[sampleindex];
            rf_tree_new = randomForest::randomForest(x=xfix_sample, y=y_sample, ntree=1, mtry=mtry , nodesize=nodesize, replace=replace_rf);
            rf_tree = randomForest::combine(rf_tree,rf_tree_new);
        }
        return(rf_tree)
    }
    
    cl=makeCluster(ncore);
    randForest_inCluster = parallel::parLapply(cl, X=1:ncore, RF,
            x,y,ntree,mtry,nodesize,samplesize_rf);
    randForest = randForest_inCluster[[1]];
    
    if (ncore > 1){
        for (i in c(2:length(randForest_inCluster))){
            randForest = combine(randForest,randForest_inCluster[[i]]);
        }
    }
    
    return(list(randomForest = randForest, randForest_inCluster=randForest_inCluster))
    
    }

    set.seed(round(runif(1) * 1e5,0));
    trainindex = sample(seq(nrow(x)),size=round(trainperc * nrow(x),0),replace = FALSE);
    testindex = setdiff(seq(nrow(x)),trainindex);
    
    x_raw = x;
    
    library(RRF);
    library(gbm);
    
    ### Models for different scenarios
    if (useGBM_ind == "Y" & useRRF_ind == "N"){
    
        x = removeFactrOver_n_Fun(data=x_raw, n=1e7);
        formula_gbm = as.formula(paste("y ~ ",paste(names(x),collapse=" + "),sep=""));
        if (ncol(x) <= 10){treedepth_gb = min(maxdepth_gbm,10)} else{treedepth_gb = min(maxdepth_gbm, round(0.98*ncol(x),0))};
        # create gbm model
        gb <- gbm(formula=formula_gbm, distribution = gbm_dist, data=data_[trainindex,],
                        n.trees = ntree_gb, interaction.depth = treedepth_gb,
                        shrinkage = shrinkage_, n.minobsinnode =1, keep.data=FALSE, cv.folds=cvfolds_gbm);
        bestiter <- gbm.perf(gb, method="cv");
        var_sumry = summary(gb,n.trees=bestiter);
        
        data_$Pred_gb = predict(gb,data_,bestiter);
        wmape_gb = sum(abs(data_[testindex,"Pred_gb"] - data_[testindex,"y"]))/sum(data_[testindex,"y"]);
        
        gb <- gbm(formula=formula_gbm, distribution = gbm_dist, data=data_,
                        n.trees = ntree_gb, interaction.depth = treedepth_gb,
                        shrinkage = shrinkage_, n.minobsinnode =1, keep.data=FALSE, cv.folds=cvfolds_gbm);
        bestiter <- gbm.perf(gb, method="cv");
        
        return(list(ModelType="GBM", model_GBM=gb, GBM_bestiter = bestiter, wMAPE=wmape_gb));
    
        } else if (useGBM_ind == "N" & useRRF_ind == "Y") {
        
        x = removeFactrOver_n_Fun(data=x_raw, n=31);
        treedepth_rf = round(0.98*ncol(x),0); ##this is used for both RRF and GBM
        treedepth_rf = min(maxdepth_rf,treedepth_rf);
                
        prf = parallelRandomForest(x=x[trainindex,],y=y[trainindex],ntree=ntree_rf,mtry=treedepth_rf);
        prf = prf$randomForest;
        
        data_$Pred_rf = predict(prf,na.roughfix(data_));
        wmape_rf = sum(abs(data_[testindex,"Pred_rf"] - data_[testindex,"y"]))/sum(data_[testindex,"y"]);
        
        prf = parallelRandomForest(x=x,y=y,ntree=ntree_rf,mtry=treedepth_rf);
        prf = prf$randomForest;
        
        return(list(ModelType="RF", model_RF=prf, wMAPE=wmape_rf));
        
        } else if (useGBM_ind == "Y" & useRRF_ind == "Y") {
        
        #*******  The following is for building guided random forest model model  ********#
        x = removeFactrOver_n_Fun(data=x_raw, n=31);
        treedepth_rf = round(0.98*ncol(x),0); ##this is used for both RRF and GBM
        treedepth_rf = min(maxdepth_rf,treedepth_rf);
                
        prf = parallelRandomForest(x=x[trainindex,],y=y[trainindex],ntree=ntree_rf,mtry=treedepth_rf);
        prf = prf$randomForest;
        
        data_$Pred_rf = predict(prf,na.roughfix(data_));
        wmape_rf = sum(abs(data_[testindex,"Pred_rf"] - data_[testindex,"y"]))/sum(data_[testindex,"y"]);
        
        #*******  The following is for building GBM model  ********#
        x = removeFactrOver_n_Fun(data=x_raw, n=1e7);
        formula_gbm = as.formula(paste("y ~ ",paste(names(x),collapse=" + "),sep=""));
        if (ncol(x) <= 10){treedepth_gb = min(maxdepth_gbm,10)} else{treedepth_gb = min(maxdepth_gbm, treedepth_rf)};
        # create gbm model
        gb <- gbm(formula=formula_gbm, distribution = gbm_dist, data=data_[trainindex,],
                        n.trees = ntree_gb, interaction.depth = treedepth_gb,
                        shrinkage = shrinkage_, n.minobsinnode =1, keep.data=FALSE, cv.folds=cvfolds_gbm);
        bestiter <- gbm.perf(gb, method="cv");
        var_sumry = summary(gb,n.trees=bestiter);
        
        data_$Pred_gb = predict(gb,data_,bestiter);
        wmape_gb = sum(abs(data_[testindex,"Pred_gb"] - data_[testindex,"y"]))/sum(data_[testindex,"y"]);
        
        a = (1-wmape_rf)/wmape_rf;
        b = (1-wmape_gb)/wmape_gb;
        
        wgt_rf = (10 ** (a/b))/((10 ** (a/b)) + (10 ** (b/a)));
        wgt_gb = 1-wgt_rf;
        
        data_$Pred = wgt_gb * data_$Pred_gb + wgt_rf * data_$Pred_rf;
        
        wmape = sum(abs(data_[testindex,"Pred"] - data_[testindex,"y"]))/sum(data_[testindex,"y"]);
        
        ######################################################
        ##########    Retrain with all data   ################
        #*******  The following is for building guided random forest model model  ********#
        x = removeFactrOver_n_Fun(data=x_raw, n=31);
        prf = parallelRandomForest(x=x,y=y,ntree=ntree_rf,mtry=treedepth_rf);
        prf = prf$randomForest;
        #*******  The following is for building GBM model  ********#
        gb <- gbm(formula=formula_gbm, distribution = gbm_dist, data=data_,
                        n.trees = ntree_gb, interaction.depth = treedepth_gb,
                        shrinkage = shrinkage_, n.minobsinnode =1, keep.data=FALSE, cv.folds=cvfolds_gbm);
        bestiter <- gbm.perf(gb, method="cv");
        
        if (wmape <= wmape_rf & wmape <= wmape_gb){
            return(list(ModelType="Hybrid", model_RF=prf, model_GBM=gb, GBM_bestiter = bestiter, 
                        Pred_Wgt_RRF = wgt_rf, Pred_Wgt_GBM = wgt_gb, wMAPE=wmape, wMAPE_RF = wmape_rf, wMAPE_GBM =wmape_gb))
            } else if (wmape_rf <= wmape & wmape_rf <= wmape_gb){
            return(list(ModelType="RF", model_RF=prf, wMAPE=wmape_rf))
            } else {return(list(ModelType="GBM", model_GBM=gb, GBM_bestiter = bestiter, wMAPE=wmape_gb))
        };
        } else { return(NULL)
    }
}
