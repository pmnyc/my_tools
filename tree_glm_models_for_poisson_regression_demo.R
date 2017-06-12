
###############################################################
# Boosting Tree for Poisson Regresison Problem
###############################################################
require(xgboost)
require(TDboost)
require(data.table)
require(Matrix)
require(tweedie)
require(sqldf)
require(glmnet)
require(HDtweedie)
require(foreach)
require(doParallel)
require(statmod) # Needed to use tweedie.profile
# partial dependency plot
require(pdp)

"
data_table  is the model data.table
predictors (vector) is the list of X variales in model
trend_var (str) is the name of variable that is used for calculating the trend
    for example, it can be accident_year in data.
trend_relativity_var (str) is the name of variable that provides trend/relativity, such as
    the relativity by accident year. This is usually derived
    from a preliminary glmnet model in a more traditional glm approach
special_predictors_to_keep (vector) is the list of predictors to keep in whatever
    type model data transformation
y_var (str) is the target loss variable name (str), not the pure premium, but
    the pure premium * exposure
exposure_var (str) is the name of exposure varible, i.e., the weight of each record
training_index (vector) is the indices of the data_table for training
oot_index (vector) is the indices of the data_table for out-of-time validation
"

MAX_DEPTH <- 5  # the max interaction depth in trees
TWEEDIE_VAR_POWER <- 1.91  # set it to NULL if one wants to do power search
DAMPING_FACTOR <- 1.5  # If factor is 0.9, meaning 2 years older records got weight
                    # of 0.9^2 instead of default 1. If factor is 1.5, meaning weight
                    # of records one year older is 1.5 higher than current weight.
                    # For example, if it's 1.5, then from latest year to oldest
                    # years the weight of each record becomes
                    # 1, 1.5^2, 1.5^3, 1.53^4, ...
WEIGHT_ADJUST_FACTOR_RANGE <- c(1.0, 5.0) # the capping for adjust factor based on
                    # damping factor. 5.0 means we should not boost the weight of record
                    # higher than 5.0

create_bins <- function(x, n_bins=31) {
    # x is the vector to be binned
    # n_bins is max number of bins to create
    require(stringr)
    quantiles_ <- quantile(x, sort(unique(c(0, 1, seq(0, 1, by=1/n_bins)))))
    quantiles_ <- c(-Inf, sort(unique(quantiles_)), Inf)
    newlabels <- paste0(str_pad(seq(1,length(quantiles_)-1),
                                               nchar(as.character(length(quantiles_)-1)),
                                               pad = "0"))
    x_ <- cut(x=x, breaks = quantiles_, labels = newlabels)
    return(x_)
}


#############################################
### Data Preprocessing ###
#############################################

levels_ <- c(data_table[training_index, max(as.vector(get(trend_var)))],
                setdiff(data_table[, sort(unique(as.vector(get(trend_var))))],
                        data_table[training_index, max(as.vector(get(trend_var)))]))
data_table[, paste0(trend_var) := factor(get(trend_var), levels=as.character(levels_))]

## Convert the character or factor into sparse matrix
c_ <- copy(sapply(data_table, class))
names_ <- names(c_)
types_ <- as.vector(c_)
char_predictors <- intersect(copy(predictors), names_[which(types_ %in% c("factor", "character"))])

# Convert to factors for character fields
for (col in setdiff(char_predictors, trend_var)) {
    if (class(data_table[1, get(col)]) %in% c("character")) {
        data_table[, paste0(col) := as.factor(get(col))]
    }
    # use the ordering of the varaible to order the variables
    levels <- data_table[, unique(get(col))]
    levels <- sort(as.vector(levels))
    data_table[, paste0(col) := factor(get(col), levels = levels)]
}

# Convert to bins and factors for numerical fields
nvars_ <- length(setdiff(predictors, char_predictors))
counter <- 1
predictorscopy <- copy(predictors)
print("predictorscopy is the original list of predictors before any changes")
for (col in setdiff(predictorscopy, char_predictors)) {
    x_ <- create_bins(data_table[, get(col)], n_bins=31)
    data_table[, paste0(col, "_bins") := as.factor(x_)]
    predictors <- unique(c(predictors, paste0(col, "_bins")))
    if (counter %% as.integer(nvars_ / 10) == 0) {
        print(paste0(counter, " out of ", nvars_, " numerical variables are processed..."))
    }
    counter <- counter + 1
}

c_ <- copy(sapply(data_table, class))
names_ <- names(c_)
types_ <- as.vector(c_)
char_predictors <- intersect(copy(predictors), names_[which(types_ %in% c("factor"))])
# char_predictors is the list of factor variables

#################### Frequency Model ####################
#########################################################

set.seed(10011)
data_table[, random_norm := rnorm(nrow(data_table))]
data_table[, random_pois := rpois(nrow(data_table), 100)]

train_mm_freq <- data.matrix(data_table[training_index, c(predictorscopy,"random_pois","random_norm"), with = F])
test_mm_freq <- data.matrix(data_table[testing_index, c(predictorscopy,"random_pois","random_norm"), with = F])
df_ <- copy(data_table)
df_[oot_index, paste0(trend_var) := df_[training_index, max(as.vector(get(trend_var)))]]
oot_mm_freq <- data.matrix(df_[oot_index, c(predictorscopy,"random_pois","random_norm"), with = F])  # use latest year as future

# assign damping factor 1.25 for older years
df_[, record_weights := 1]
x_ <- df_[c(training_index, oot_index), sort(unique(as.vector(get(trend_var))), decreasing=T)]
weightadj <- DAMPING_FACTOR ** seq(0, length(x_)-1)
for (x2_ in x_) {
    v_ <- weightadj[x_ == x2_]
    v_ <- max(min(WEIGHT_ADJUST_FACTOR_RANGE), v_)
    v_ <- min(max(WEIGHT_ADJUST_FACTOR_RANGE), v_)
    df_[as.character(get(trend_var)) == x2_, record_weights := v_ * record_weights]
}

weights <- df_[, record_weights]
rm(df_); gc();

train_dm_freq <- xgb.DMatrix(
    data = train_mm_freq,
    label = data_table[training_index, sign(get(y_var))],
    missing = NA,
    weight = weights[training_index]
)

test_dm_freq <- xgb.DMatrix(
    data = test_mm_freq,
    label = data_table[testing_index, sign(get(y_var))],
    missing = NA,
    weight = weights[testing_index]
)

oot_dm_freq <- xgb.DMatrix(
    data = oot_mm_freq,
    label = data_table[oot_index, sign(get(y_var))],
    missing = NA,
    weight = weights[oot_index]
)

gc()

set.seed(10011)
xgb1_freq <- xgb.train(
        data = train_dm_freq,
        base_score = mean(getinfo(train_dm_freq, "label")) * 10,  # can be average frequency, but can not be too small, default value is 0.5
        watchlist = list(train = train_dm_freq, test=test_dm_freq, valid = oot_dm_freq),
        eval_metric = "auc",
        objective = "binary:logistic",
        scale_pos_weight = 50,
        print_every_n = 5, early_stopping_rounds=20, subsample=0.5,
        nrounds = 5000, eta = 0.1, max.depth = 1,
        colsample_bytree = 0.5,
        min_child_weight=1, alpha = 10, lambda = 1,
        callbacks = list(cb.evaluation.log())
    )

# use xgg.cv to tune paremeters get sense of the level it can achieve.

# write.table(paste0("current alpha is ",alpha_), "zzz.txt", sep="\t", append = TRUE)
# write.table(xgb1_freq$evaluation_log[xgb1_freq$best_iteration], "zzz.txt", sep="\t", append = TRUE)
# write.table("---------------------------------", "zzz.txt", sep="\t", append = TRUE)
gc()

Features_Selected <- c('exp_log', 'var1', 'var2')
gc()


#### Round 2
char_predictors_ <- NULL
for (p_ in setdiff(Features_Selected, setdiff(special_predictors_to_keep, trend_var))) {
    char_predictors_ <- c(char_predictors_, char_predictors[grepl(pattern=paste0(p_, "*"), x=char_predictors)])
    char_predictors_ <- unique(char_predictors_)
}
char_predictors <- char_predictors_

train_mm_freq <- data.matrix(data_table[training_index, Features_Selected, with = F])
test_mm_freq <- data.matrix(data_table[testing_index, Features_Selected, with = F])
df_ <- copy(data_table)
df_[oot_index, paste0(trend_var) := df_[training_index, max(as.vector(get(trend_var)))]]
oot_mm_freq <- data.matrix(df_[oot_index, Features_Selected, with = F])  # use latest year as future

train_dm_freq <- xgb.DMatrix(
    data = train_mm_freq,
    label = data_table[training_index, sign(get(y_var))],
    missing = NA,
    weight = weights[training_index]
)

test_dm_freq <- xgb.DMatrix(
    data = test_mm_freq,
    label = data_table[testing_index, sign(get(y_var))],
    missing = NA,
    weight = weights[testing_index]
)

oot_dm_freq <- xgb.DMatrix(
    data = oot_mm_freq,
    label = data_table[oot_index, sign(get(y_var))],
    missing = NA,
    weight = weights[oot_index]
)

gc()
set.seed(10011)
xgb1_freq <- xgb.train(
        data = train_dm_freq,
        base_score = mean(getinfo(train_dm_freq, "label")) * 10,  # can be average frequency, but can not be too small, default value is 0.5
        watchlist = list(train = train_dm_freq, test=test_dm_freq, valid = oot_dm_freq),
        eval_metric = "auc",
        objective = "binary:logistic",
        scale_pos_weight = 50,
        print_every_n = 5, early_stopping_rounds=20, subsample=0.8,
        nrounds = 5000, eta = 0.1, max.depth = 6,
        colsample_bytree = 0.5,
        min_child_weight=1, alpha = 100, lambda = 0,
        callbacks = list(cb.evaluation.log())
    )

pred_freq_train <- predict(xgb1_freq, train_dm_freq)
pred_freq_oot <- predict(xgb1_freq, oot_dm_freq)

pred_freq_train <- pred_freq_train / data_table[training_index, get(exposure_var)]
pred_freq_oot <- pred_freq_oot / data_table[oot_index, get(exposure_var)]

# Get variable importance for frequency model
xgb_imp_freq <- xgb.importance(feature_names = colnames(train_mm_freq), model = xgb1_freq)
xgb.plot.importance(xgb_imp_freq)
gc()

# Get GINI on the frequency model
mylift(pred_freq_oot, pred_freq_oot,
        data_table[oot_index, sign(get(y_var))]/data_table[oot_index, get(exposure_var)],
        data_table[oot_index, get(exposure_var)],
        n=10)

################### Pure Premium Model ######################
#########################################################

# prediction of the frequency as offset
data_table[, foldid := 0]
data_table[, random := runif(nrow(data_table))]
data_table[sort(unique(c(training_index, testing_index))), foldid := 1]
data_table[foldid == 1, foldid := (random<=0.5)*2 + (random>0.5)*1]
data_table[, random := NULL]

train_mm_freq <- data.matrix(data_table[foldid==1, Features_Selected, with = F])
test_mm_freq <- data.matrix(data_table[foldid==2, Features_Selected, with = F])
df_ <- copy(data_table)
df_[oot_index, paste0(trend_var) := df_[training_index, max(as.vector(get(trend_var)))]]
oot_mm_freq <- data.matrix(df_[oot_index, Features_Selected, with = F])  # use latest year as future

train_dm_freq <- xgb.DMatrix(
    data = train_mm_freq,
    label = data_table[foldid==1, sign(get(y_var))],
    missing = NA,
    weight = weights[data_table[, which(foldid == 1)]]
)

test_dm_freq <- xgb.DMatrix(
    data = test_mm_freq,
    label = data_table[foldid==2, sign(get(y_var))],
    missing = NA,
    weight = weights[data_table[, which(foldid == 2)]]
)

oot_dm_freq <- xgb.DMatrix(
    data = oot_mm_freq,
    label = data_table[oot_index, sign(get(y_var))],
    missing = NA,
    weight = weights[oot_index]
)

gc()
set.seed(10011)
xgb1_freq <- xgb.train(
        data = train_dm_freq,
        base_score = mean(getinfo(train_dm_freq, "label")) * 10,  # can be average frequency, but can not be too small, default value is 0.5
        watchlist = list(train = train_dm_freq, test=test_dm_freq, valid = oot_dm_freq),
        eval_metric = "auc",
        objective = "binary:logistic",
        scale_pos_weight = 100,
        print_every_n = 5, early_stopping_rounds=20, subsample=0.8,
        nrounds = 5000, eta = 0.01, max.depth = 5,
        colsample_bytree = 0.5,
        min_child_weight=1, alpha = 50, lambda = 0,
        callbacks = list(cb.evaluation.log())
    )

pred_freq_test_ <- predict(xgb1_freq, test_dm_freq) / data_table[foldid==2, get(exposure_var)]
pred_freq_oot_v1_ <- predict(xgb1_freq, oot_dm_freq) / data_table[oot_index, get(exposure_var)]
data_table[, pred_freq := 0]
data_table[foldid==2, pred_freq := pred_freq_test_]
data_table[oot_index, pred_freq := pred_freq_oot_v1_]

## fill in the second part of the partition
train_mm_freq <- data.matrix(data_table[foldid==2, Features_Selected, with = F])
test_mm_freq <- data.matrix(data_table[foldid==1, Features_Selected, with = F])
df_ <- copy(data_table)
df_[oot_index, paste0(trend_var) := df_[training_index, max(as.vector(get(trend_var)))]]
oot_mm_freq <- data.matrix(df_[oot_index, Features_Selected, with = F])  # use latest year as future

train_dm_freq <- xgb.DMatrix(
    data = train_mm_freq,
    label = data_table[foldid==2, sign(get(y_var))],
    missing = NA,
    weight = weights[data_table[, which(foldid == 2)]]
)

test_dm_freq <- xgb.DMatrix(
    data = test_mm_freq,
    label = data_table[foldid==1, sign(get(y_var))],
    missing = NA,
    weight = weights[data_table[, which(foldid == 1)]]
)

oot_dm_freq <- xgb.DMatrix(
    data = oot_mm_freq,
    label = data_table[oot_index, sign(get(y_var))],
    missing = NA,
    weight = weights[oot_index]
)

gc()
set.seed(10011)
xgb1_freq <- xgb.train(
        data = train_dm_freq,
        base_score = mean(getinfo(train_dm_freq, "label")) * 10,  # can be average frequency, but can not be too small, default value is 0.5
        watchlist = list(train = train_dm_freq, test=test_dm_freq, valid = oot_dm_freq),
        eval_metric = "auc",
        objective = "binary:logistic",
        scale_pos_weight = 100,
        print_every_n = 5, early_stopping_rounds=20, subsample=0.8,
        nrounds = 5000, eta = 0.01, max.depth = 5,
        colsample_bytree = 0.5,
        min_child_weight=1, alpha = 50, lambda = 0,
        callbacks = list(cb.evaluation.log())
    )

pred_freq_test_ <- predict(xgb1_freq, test_dm_freq) / data_table[foldid==1, get(exposure_var)]
pred_freq_oot_v2_ <- predict(xgb1_freq, oot_dm_freq) / data_table[oot_index, get(exposure_var)]
data_table[foldid==1, pred_freq := pred_freq_test_]
data_table[oot_index, pred_freq := 0.5*(pred_freq + pred_freq_oot_v2_)]

# Get the variale for severity model
char_predictors_ <- NULL
for (p in setdiff(predictorscopy, setdiff(special_predictors_to_keep, trend_var))) {
    char_predictors_ <- unique(c(char_predictors_,
                        colnames(data_table)[grepl(pattern=paste0(p,"*"), x=colnames(data_table))]))
}
char_predictors_ <- intersect(char_predictors_, colnames(data_table)[sapply(data_table, class) == "factor"])

#m_serv <- sparse.model.matrix(~.-1, data_table[, char_predictors_, with = F])

trnidx <- intersect(training_index, data_table[, which(get(y_var)>0)])
tstidx <- intersect(testing_index, data_table[, which(get(y_var)>0)])
ootidx <- intersect(oot_index, data_table[, which(get(y_var)>0)])

train_dm_sevr <- xgb.DMatrix(
    data = sparse.model.matrix(~.-1, data_table[trnidx, c(char_predictors_, "random_norm", "random_pois"), with = F]),
    label = data_table[trnidx, log(get(y_var)+1)],
    missing = NA
)

test_dm_sevr <- xgb.DMatrix(
    data = sparse.model.matrix(~.-1, data_table[tstidx, c(char_predictors_, "random_norm", "random_pois"), with = F]),
    label = data_table[tstidx, log(get(y_var)+1)],
    missing = NA
)

oot_dm_sevr <- xgb.DMatrix(
    data = sparse.model.matrix(~.-1, data_table[ootidx, c(char_predictors_, "random_norm", "random_pois"), with = F]),
    label = data_table[ootidx, log(get(y_var)+1)],
    missing = NA
)

gc()
set.seed(10011)
xgb1_serv <- xgb.train(
        data = train_dm_sevr,
        watchlist = list(train = train_dm_sevr, test=test_dm_sevr, valid = oot_dm_sevr),
        eval_metric = "rmse",
        objective = "reg:linear",
        print_every_n = 5, early_stopping_rounds=20, subsample=0.8,
        nrounds = 5000, eta = 0.01, max.depth = 1,
        colsample_bytree = 0.5,
        min_child_weight=1, alpha = 0.003, lambda = 0,
        callbacks = list(cb.evaluation.log())
    )
# Get variable importance for severity model
xgb_imp_serv <- xgb.importance(feature_names = attributes(train_dm_sevr)$.Dimnames[[2]], model = xgb1_serv)
xgb.plot.importance(xgb_imp_serv)
gc()

#### Create OffSet for GLM
data_table[, offset := pred_freq_firstround * pred_sevr_firstround]
predictors_pp <- setdiff(xgb_imp_serv$Feature,
                        c("pred_freq_firstround", "pred_sevr_firstround"))
char_predictors_ <- c()
for (p in colnames(data_table)) {
    if (sum(grepl(pattern=paste0(p,"*"), x=predictors_pp)) > 0) {
        char_predictors_ <- unique(c(char_predictors_, p))
    }
}
char_predictors_ <- intersect(char_predictors_, colnames(data_table)[sapply(data_table, class) == "factor"])

mm_pp <- sparse.model.matrix(~.-1, data=data_table[, char_predictors_, with=F])[, xgb_imp_serv$Feature]
gc()
trainidx <- sort(unique(c(training_index, testing_index)))
glm_pp <- cv.glmnet(x = mm_pp[trainidx, ],
                    y = data_table[trainidx, (get(y_var)+0.01)/get(exposure_var)],
                    standardize = TRUE,
                    offset = data_table[trainidx, log(offset)],
                    weights = data_table[trainidx,get(exposure_var)],
                    alpha = 1,
                    type.measure = "mse",
                    family = "poisson",
                    nfolds = 10)

# Another round of variable selection
vars <- as.matrix(coef(glm_pp,s=(glm_pp$lambda.1se * glm_pp$lambda.min)**0.5))
vars <- data.table(names = names(vars[, 1]), values=vars[,1])

mm_pp_backup01 <- mm_pp
mm_pp <- mm_pp[, setdiff(vars$names[vars$values !=0], "(Intercept)")]
gc()
trainidx <- sort(unique(c(training_index, testing_index)))
glm_pp <- cv.glmnet(x = mm_pp[trainidx, ],
                    y = data_table[trainidx, (get(y_var)+0.01)/get(exposure_var)],
                    standardize = TRUE,
                    offset = data_table[trainidx, log(offset)],
                    weights = data_table[trainidx,get(exposure_var)],
                    alpha = 1,
                    type.measure = "mse",
                    family = "poisson",
                    nfolds = 10)

pred_pp_train <- predict(glm_pp, newx = mm_pp[training_index, ],
                    type = 'response', s = glm_pp$lambda.1se,
                    offset = data_table[training_index, log(offset)])
pred_pp_test <- predict(glm_pp, newx = mm_pp[testing_index, ],
                    type = 'response', s = glm_pp$lambda.1se,
                    offset = data_table[testing_index, log(offset)])
pred_pp_oot <- predict(glm_pp, newx = mm_pp[oot_index, ],
                    type = 'response', s = glm_pp$lambda.1se,
                    offset = data_table[oot_index, log(offset)])

gc();

########## Combine Frequency Model and Severity Model ###########

pred_train_ <- pred_pp_train
pred_oot_ <- pred_pp_oot

data_table[, pred_pp := 0]
data_table[training_index, pred_pp := pred_train_]
data_table[oot_index, pred_pp := pred_oot_]

# Rebalance pred_pp by each year or whatever trend variable
indices <- c("training_index", "oot_index")
print(paste0("The mean ratio of acutal loss vs prediction is ",
        data_table[training_index, sum(get(y_var))/sum(pred_pp * get(exposure_var))])
        )
for (trend_ in data_table[, unique(get(trend_var))]) {
    for (index_type in indices) {
        eval(parse(text=paste0("idx_ <- ", index_type)))
        idx_ <- sort(intersect(idx_, which(data_table[, as.character(get(trend_var))]==trend_)))
        adj_factor <- data_table[idx_, sum(get(y_var)) / sum(pred_pp * get(exposure_var))]
        data_table[idx_, pred_pp := pred_pp * adj_factor]
    }
}

gini_train <- NormalizedWeightedGini(data_table[training_index, get(y_var)]/data_table[training_index, get(exposure_var)],
                                    data_table[training_index, get(exposure_var)],
                                    data_table[training_index, pred_pp])
gini_oot <- NormalizedWeightedGini(data_table[oot_index, get(y_var)]/data_table[oot_index, get(exposure_var)],
                                    data_table[oot_index, get(exposure_var)],
                                    data_table[oot_index, pred_pp])
print("The GINIs on train and oot are ")
print(c(gini_train, gini_oot))

# Get GINI on the PP model
mylift(data_table[oot_index, pred_pp], data_table[oot_index, pred_pp],
        data_table[oot_index, get(y_var) / get(exposure_var)],
        data_table[oot_index, get(exposure_var)],
        n=10)
