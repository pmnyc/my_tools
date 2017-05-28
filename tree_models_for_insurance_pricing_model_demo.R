
###############################################################
# Boosting Tree for Regresison Problem
###############################################################
require(xgboost)
require(TDboost)
require(data.table)
require(tweedie)
require(HDtweedie)
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
y_var (str) is the target loss variable name (str), not the pure premium, but
    the pure premium * exposure
exposure_var (str) is the name of exposure varible, i.e., the weight of each record
training_index (vector) is the indices of the data_table for training
oot_index (vector) is the indices of the data_table for out-of-time validation
"

MAX_DEPTH <- 5  # the max interaction depth in trees
TWEEDIE_VAR_POWER <- 1.91  # set it to NULL if one wants to do power search
REMOVE_TREND_VAR_IN_FREQ_PREDICTORS <- FALSE  # remove year (or trend_var) in
        # the frequency model, could make big improvment, needs to run test
        # to verify
DAMPING_FACTOR <- 1.5  # If factor is 0.9, meaning 2 years older records got weight
                    # of 0.9^2 instead of default 1. If factor is 1.5, meaning weight
                    # of records one year older is 1.5 higher than current weight.
                    # For example, if it's 1.5, then from latest year to oldest
                    # years the weight of each record becomes
                    # 1, 1.5^2, 1.5^3, 1.53^4, ...
WEIGHT_ADJUST_FACTOR_RANGE <- c(1.0, 7.0) # the capping for adjust factor based on
                    # damping factor. 5.0 means we should not boost the weight of record
                    # higher than 5.0


#############################################
### Data Preprocessing ###
#############################################

label_encoder_dt <- data.table(variable=c(""), value=c(""), encoded_value=c(0))[0]
for (col in predictors) {
    if (class(data_table[1, get(col)]) %in% c("factor", "character")) {
        if (class(data_table[1, get(col)]) %in% c("character")) {
            data_table[, paste0(col) := as.factor(get(col))]
        }
        # use the ordering of the varaible to order the variables
        levels <- data_table[, unique(get(col))]
        levels <- sort(as.vector(levels))
        data_table[, paste0(col) := factor(get(col), levels = levels)]
        if (length(data_table[, unique(get(col))]) > 1000) {
            # when there are too many levels in the string field, convert them to
            # integers using simple label encoder
            dt_ <- data.table(variable=rep(col, length(levels)),
                                value=levels,
                                encoded_value=seq(1, length(levels)))
            label_encoder_dt <- rbind(label_encoder_dt, dt_);  rm(dt_)
            data_table[, paste0(col) := as.integer(get(col))]
        }
    }
}


#################### Frequency Model ####################
#########################################################
    # another test needed is to remove the year (or trend_var) from predictors
    # and see how it goes, because we need data to extrapolate.
if (REMOVE_TREND_VAR_IN_FREQ_PREDICTORS) {
    predictors_ <- setdiff(predictors, trend_var)
} else {
    predictors_ <- predictors
}
train_mm_freq <- data.matrix(data_table[training_index, predictors_, with = F])
df_ <- copy(data_table)
df_[oot_index, paste0(trend_var) := df_[training_index, max(as.vector(get(trend_var)))]]
oot_mm_freq <- data.matrix(df_[oot_index, predictors_, with = F])  # use latest year as future

# assign damping factor 1.25 for older years
df_[, record_weights := 1]
x_ <- df_[, sort(unique(as.vector(get(trend_var))), decreasing=T)]
weightadj <- DAMPING_FACTOR ** seq(0, length(x_)-1)
for (x2_ in x_) {
    v_ <- weightadj[x_ == x2_]
    v_ <- max(min(WEIGHT_ADJUST_FACTOR_RANGE), v_)
    v_ <- min(max(WEIGHT_ADJUST_FACTOR_RANGE), v_)
    df_[as.character(get(trend_var)) == x2_, record_weights := v_ * record_weights]
}

train_dm_freq <- xgb.DMatrix(
    data = train_mm_freq,
    label = data_table[training_index, sign(get(y_var))],
    missing = NA,
    weight = df_[training_index, record_weights]
)

oot_dm_freq <- xgb.DMatrix(
    data = oot_mm_freq,
    label = data_table[oot_index, sign(get(y_var))],
    missing = NA,
    weight = df_[oot_index, record_weights]
)

rm(df_)

set.seed(10011)
xgb1_freq <- xgb.train(
        data = train_dm_freq,
        base_score = 0.1,  # can be average frequency, but can not be too small, default value is 0.5
        watchlist = list(train = train_dm_freq, valid = oot_dm_freq),
        eval_metric = "auc",
        objective = "binary:logistic",
        print_every_n = 5, early_stopping_rounds=20, subsample=0.5,
        nrounds = 5000, eta = 0.1, max.depth = MAX_DEPTH,
        colsample_bytree = 0.5,
        min_child_weight=1, alpha = 10, lambda = 0,
        callbacks = list(cb.evaluation.log())
    )

xgb2_freq <- xgb.train(
        data = train_dm_freq,
        base_score = 0.1,  # can be average frequency, but can not be too small, default value is 0.5
        watchlist = list(train = train_dm_freq, valid = oot_dm_freq),
        eval_metric = "logloss",
        objective = "binary:logistic",
        print_every_n = 5, early_stopping_rounds=20, subsample=0.5,
        nrounds = 5000, eta = 0.1, max.depth = MAX_DEPTH,
        colsample_bytree = 0.5,
        min_child_weight=1, alpha = 10, lambda = 0,
        callbacks = list(cb.evaluation.log())
    )

xgb3_freq <- xgb.train(
        data = train_dm_freq,
        base_score = 0.1,  # can be average frequency, but can not be too small, default value is 0.5
        watchlist = list(train = train_dm_freq, valid = oot_dm_freq),
        #eval_metric = "",
        objective = "count:poisson",
        print_every_n = 5, early_stopping_rounds=20, subsample=0.5,
        nrounds = 5000, eta = 0.1, max.depth = MAX_DEPTH,
        colsample_bytree = 0.5,
        min_child_weight=1, alpha = 10, lambda = 0,
        callbacks = list(cb.evaluation.log())
    )

xgb4_freq <- xgb.train(
        data = train_dm_freq,
        base_score = 0.1,  # can be average frequency, but can not be too small, default value is 0.5
        watchlist = list(train = train_dm_freq, valid = oot_dm_freq),
        eval_metric = "auc",
        objective = "count:poisson",
        print_every_n = 5, early_stopping_rounds=20, subsample=0.5,
        nrounds = 5000, eta = 0.1, max.depth = MAX_DEPTH,
        colsample_bytree = 0.5,
        min_child_weight=1, alpha = 10, lambda = 0,
        callbacks = list(cb.evaluation.log())
    )

# COMMENT: The follow matrix is also working, but since there is only one column, no need for matrix
#          operation here
# pred_m_train <- matrix(predict(xgb1_freq, train_dm_freq), nrow = nrow(train_dm_freq), byrow = TRUE)[,1]
# pred_m_test <- matrix(predict(xgb1_freq, test_dm_freq), nrow = nrow(test_dm_freq), byrow = TRUE)[,1]

# xgb1: logistic/auc  xgb2: logistic/logloss   xg3: poisson/mle   xg4: poisson/auc
predictions_weighting <- c(1, 2, 1, 1)  # for xgb1, xgb2, xgb3, xgb4

pred_freq_train <- (1.0/sum(predictions_weighting)) * (predict(xgb1_freq, train_dm_freq) * predictions_weighting[1]
                            + predict(xgb2_freq, train_dm_freq) * predictions_weighting[2]
                            + predict(xgb3_freq, train_dm_freq) * predictions_weighting[3]
                            + predict(xgb4_freq, train_dm_freq) * predictions_weighting[4])
pred_freq_oot <- (1.0/sum(predictions_weighting)) * (predict(xgb1_freq, oot_dm_freq) * predictions_weighting[1]
                            + predict(xgb2_freq, oot_dm_freq) * predictions_weighting[2]
                            + predict(xgb3_freq, oot_dm_freq) * predictions_weighting[3]
                            + predict(xgb4_freq, oot_dm_freq) * predictions_weighting[4])

# Get variable importance for frequency model
xgb_imp_freq <- xgb.importance(feature_names = colnames(train_mm_freq), model = xgb1_freq)
xgb.plot.importance(xgb_imp_freq)


################### Severity Model ######################
#########################################################
pos_idx <- which(data_table[, get(y_var)] > 0)
trnidx <- intersect(training_index, pos_idx)
ootidx <- intersect(oot_index, pos_idx)

if (is.null(TWEEDIE_VAR_POWER)) {
    ## Estimate the Tweedie P
    out <- tweedie.profile(formula(paste0(y_var, " ~ ", paste(predictors, collapse = " + "))),
                            data = data_table[trnidx, c(y_var, predictors), with=F],
                            p.vec=seq(1.1, 2, by=0.1))
    tweedie_p <- round(mean(c(out$p.max, mean(out$ci))), 2)
    print(paste0("The chosen tweedie variance power p is ", tweedie_p))
    TWEEDIE_VAR_POWER <- tweedie_p
}

# remove the trend variable in the predictor list so that the trend is taken care of
# through the detrending process, not in the tree models
predictors_raw <- copy(predictors)
predictors <- setdiff(predictors, trend_var)

data_table[, paste0(trend_relativity_var) := 1]

for (i in seq(1, 2)) {
    if (i == 1) {predlist_ <- predictors_raw} else {predlist_ <- predictors}
    predlist_ <- setdiff(predlist_, exposure_var)  # remove exposure variables
    # xgboost doesn't work well on regression with log-link function
    # First remove the trend relativit since the model needs to extrapolate
    data_table[, yvar_detrend := get(y_var) / get(trend_relativity_var)]

    if (i == 1) {NFOLDS <- 4} else {NFOLDS <- 10}
    set.seed(10011)
    tdbost_serv <- TDboost(formula = formula(paste0("yvar_detrend ~ ", paste(predlist_, collapse = " + "))),
                            distribution = list(name="EDM",alpha = TWEEDIE_VAR_POWER),  # gamma distribution
                            data = data_table[trnidx, c("yvar_detrend", predlist_), with = F],
                            var.monotone = NULL,  # control wheter a variable has to go monotonic
                            n.trees = 1000,
                            interaction.depth = MAX_DEPTH,
                            n.minobsinnode = 1,
                            shrinkage = 0.005,
                            bag.fraction = 0.5,
                            train.fraction = 1.0,
                            cv.folds = NFOLDS,
                            keep.data = FALSE,
                            verbose = TRUE)

    # check performance using 5-fold cross-validation
    best.iter <- TDboost.perf(tdbost_serv, method="cv")
    print(paste0("Best TDboost iteration is ", best.iter))
    # plot the performance
    # plot variable influence
    if (i > 1) {summary(tdbost_serv, n.trees=best.iter)} # based on the estimated best number of trees
    if (i == 1) {
        pred_sev <- predict.TDboost(tdbost_serv,
                                data_table[, predlist_, with=F],
                                best.iter)
        df_ <- data_table[, predlist_, with=F]
        df_[, paste0(trend_var) := as.character(df_[, sort(unique(get(trend_var)), decreasing = T)][1])]
        pred_sev2 <- predict.TDboost(tdbost_serv, df_, best.iter);
        for (x_ in as.vector(data_table[trnidx, sort(unique(get(trend_var)), decreasing = T)])) {
            ratio_ <- mean(pred_sev[
                                intersect(c(trnidx), data_table[, which(get(trend_var) == x_)])
                            ]) / mean(
                            pred_sev2[
                                intersect(c(trnidx), data_table[, which(get(trend_var) == x_)])
                            ])
            data_table[get(trend_var) == x_, paste0(trend_relativity_var) := ratio_]
        }
        rm(pred_sev, pred_sev2, df_)
    }
    pred_sev <- predict.TDboost(tdbost_serv,
                                data_table[, predlist_, with=F],
                                best.iter)
}

pred_sev <- pred_sev * data_table[, get(trend_relativity_var)]  # add trend back

# check if phi makes it as close to 1 as possible
print(paste0("The mean ratio of predicted severity vs actual severity is ",
        mean(pred_sev[trnidx])/mean(data_table[trnidx, get(y_var)])))

# create partial dependency plots
# plot top 10 variables after "best" iterations
top10vars_ <- summary(tdbost_serv, n.trees=best.iter)$var
top10vars_ <- top10vars_[1:min(10, length(top10vars_))]
for (i in seq(1, length(top10vars_))) {
    plot.TDboost(tdbost_serv, i, best.iter)
}

gc()

########## Combine Frequency Model and Severity Model ###########
pred_train_ <- (pred_freq_train/data_table[training_index, get(exposure_var)]) * pred_sev[training_index]
pred_oot_ <- (pred_freq_oot/data_table[oot_index, get(exposure_var)]) * pred_sev[oot_index]

data_table[, pred_pp := NA]
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

#Stopping. Best iteration: with interaction
#[78]    train-gamma-deviance:5285.870605    valid-gamma-deviance:415.426636

#Stopping. Best iteration: without interaction
#[78]    train-gamma-deviance:5277.806641    valid-gamma-deviance:415.250031

###############################################
##################### Summary #################
p=1
modeldata_raw <- copy(modeldata)
modeldata <- data_table
# Plot lift charts on all partitions; Record all performance results
source(file.path(dirname(config_file), "s3_model_staging_helper_part02.R"))


# partial dependency plot
require(pdp)
# make partial dependence plot for most important feature
# Try all nine combnations
grid.arrange(
    partial(xgb1_freq, pred.var = "v1", plot = TRUE, train = train_mm_freq),
    partial(xgb1_freq, pred.var = "v2", plot = TRUE, train = train_mm_freq),
    partial(xgb1_freq, pred.var = "v3", plot = TRUE, train = train_mm_freq),
    ncol = 3
)
pd <- partial(xgb1_freq, pred.var = "v1", train = train_mm_freq)
head(pd)
# ggplot2 version
# Lattice version
p1 <- plotPartial(pd, main = "lattice version")
library(ggplot2)
p2 <- ggplot2::autoplot(pd, contour = TRUE, main = "ggplot2 version",
               legend.title = "Partial\ndependence")
# Show both plots in one figure
grid.arrange(p1, p2, ncol = 2)
