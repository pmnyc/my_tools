##################################
# The following is for using GBM
# to search for the best interaction
# terms
##################################
 
# gbm_formula is formula, e.g.  y ~ . or y ~ x1+x2
    # it can be a fomula type or just a string like "y~x1+x2"
# df is the model data
# distribution is for target variable, e.g. "poisson" for claim counts
# shrinkage is the shirnk number for GBM. Try 0.05, 0.1
# wgt is the vector for weights
# ntrees specifies # of trees to build
# ncores specifies how many cores to use. Default is to use all cores
# candidate_variables is the list of candidate variables for interaction
 
interactionScoreGBM = function( gbm_formula,
                                df, 
                                distribution, 
                                candidate_variables,
                                shrinkage=0.075,
                                ncores=NA,
                                wgt=rep(1,nrow(df)),
                                ntrees=500){
    require(doParallel)
    require(foreach)
    require(gbm)
 
    if (is.na(ncores)){ncores <- parallel::detectCores()}
    if (typeof(gbm_formula) == "character"){gbm_formula <- formula(gbm_formula)}
    candidate_variables = candidate_variables;
 
    gb = gbm(gbm_formula, data =df, distribution = distribution, weights=wgt,
              n.trees = ntrees, interaction.depth = 8,
              shrinkage = shrinkage, n.minobsinnode =2, keep.data=FALSE, cv.folds=ncores,
              n.cores=ncores);
 
    bestiter = gbm.perf(gb, method="cv");
    var_sumry = summary(gb,n.trees=bestiter);
 
    var_sumry = as.data.frame(var_sumry)
    var_sumry_clean2 = var_sumry[var_sumry$rel.inf > 0,]
 
    ### Find Interactions
    vars_inter_cand2 = as.vector(var_sumry_clean2[var_sumry_clean2$rel.inf > 0,"var"])
    vars_inter_cand3 = intersect(candidate_variables, vars_inter_cand2)
 
    var_combinations = as.data.frame(combn(vars_inter_cand3, 2))
 
    tryCatch(stopCluster(cl), error = function(e) {print("Finished GBM model building...")}); # just a dummy statement
    cl = makeCluster(ncores)
    registerDoParallel(cl)
 
    getInteractionScore = function(gbm_obj, df, var_combinations, i){
        comb = var_combinations[,c(i)]
        vars = as.vector(comb)
        score = interact.gbm(gbm_obj, data=df, i.var=vars, n.trees=gbm.perf(gbm_obj, method="cv"))
        row = as.data.frame(t(as.matrix(c(vars, score))))
        colnames(row) = c("var1","var2","interaction_score")
        return(row)
    }
 
    inter_scores <- foreach(comb=seq(ncol(var_combinations)), .combine=rbind, .multicombine=TRUE,
                   .packages='gbm') %dopar% {
        getInteractionScore(gb, df, var_combinations, comb)
    }
 
    tryCatch(stopCluster(cl), error = function(e) {print("cluster already stopped...")})
 
    inter_scores$interaction_score = as.numeric(as.vector(inter_scores$interaction_score))
    inter_scores = inter_scores[with(inter_scores, order(-interaction_score)), ]
    return(inter_scores)
}
 
 
######### Below is for testing the code ############
iris <- read.csv(url("awb://archive.ics.uci.edu/ml/machine-learning-databases/iris/iris.data"), header = FALSE)
names(iris) <- c("Sepal.Length", "Sepal.Width", "Petal.Length", "Petal.Width", "Species")
iris$Species <- as.vector(iris$Species)
iris <- iris[iris$Species != "Iris-virginica",]
iris$Species[iris$Species == "Iris-setosa"] = "1"
iris$Species[iris$Species == "Iris-versicolor"] = "0"
iris$Species = as.integer(iris$Species)
 
interactions = interactionScoreGBM(gbm_formula = "Species ~ .",
                                df = iris, 
                                distribution = "bernoulli",
                                candidate_variables=c("Sepal.Length", "Sepal.Width", "Petal.Length", "Petal.Width"),
                                shrinkage=0.1)