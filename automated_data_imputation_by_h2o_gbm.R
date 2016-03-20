###############################################################
# This program is test code for data imputation using h2o package
###############################################################

################
## Functions ###

varNameCaseIncensitive = function(colnames, variable_candidates){
    ## This function is to correct some of the capital or lower case letters of variable names
    # colnames is the list of variable names from the data
    # variable_candidates is the list of variable candidates to be corrected
    colnames_lower = tolower(colnames);
    variable_candidates_lower = tolower(variable_candidates);
    common_var = intersect(colnames_lower, variable_candidates_lower) ;
    idx = unlist(sapply(colnames_lower, FUN=function(x){x %in% common_var}))
    return(colnames[idx])
}


changeDataFrameChar2Factor = function(data){
    ## This function changes character fields to factors
    columns_types = data.frame(columns = colnames(data),
                               type=as.vector(sapply(data, typeof))) ;
    char_columns = as.vector(columns_types[columns_types$type == "character", "columns"]) ;
    non_char_columns = as.vector(columns_types[columns_types$type != "character", "columns"]) ;
    df2 = cbind(data[,non_char_columns], data.frame(as.matrix(data[,char_columns]), stringsAsFactors=TRUE))
    df2 = df2[, colnames(data)];
    return(df2)
}


deleteVarwithTooManylevels = function(data, num_of_levels_threshold=1000){
    ## This function deletes string field that has too many levels
    columns_types = data.frame(columns = colnames(data),
                               type=as.vector(sapply(data, class))) ;
    char_columns = as.vector(columns_types[columns_types$type == "factor", "columns"]) ;
    for (col in char_columns){
        num_of_levels = length(attributes(data[1:2, col])$levels)
        print(paste("There are ",num_of_levels,"levels in the column",col));
        if (num_of_levels > num_of_levels_threshold){
            data[,col] <- NULL
        }
    }
    return(data)
}


checkNumofLevels = function(data){
    # check num of levels for columns of type factor
    columns_types = data.frame(columns = colnames(data),
                               type=as.vector(sapply(data, class))) ;
    char_columns = as.vector(columns_types[columns_types$type == "factor", "columns"]) ;
    levelCheck = data.frame(col=NA,numLevels=NA)[0,];
    for (col in char_columns){
        num_of_levels = length(attributes(data[1:2, col])$levels)
        print(paste("There are ",num_of_levels,"levels in the column",col));
        temp_table = data.frame(col=col,numLevels=num_of_levels);
        levelCheck <- rbind(levelCheck, temp_table);
    }
    return(levelCheck)
}


checkMissingPerct = function(data){
    # check % missing values in the variable
    missingPerct = data.frame(col=NA,missingPerct=NA)[0,];
    for (col in colnames(data)){
        x0 = data[,col];
        temp_table = data.frame(col=col,missingPerct=sum(is.na(x0))/length(x0));
        missingPerct <- rbind(missingPerct, temp_table);
    }
    return(missingPerct)
}


### The function dataImputation_byH2o  is deprecated
dataImputation_byH2o = function(dataframe, data_hex, predictors){
    # data is the original data frame
    # data_hex is as.h2o hex data format of data
    # predictors is the list of input variables that need to be imputed
    # bycolumn defines impute by which column, for example c("pol_risk_state_cd")
    columns_types = data.frame(columns = colnames(dataframe),
                               type=as.vector(sapply(dataframe, class))) ;
    char_columns = as.vector(columns_types[columns_types$type %in% c("factor","character"), "columns"]) ;
    non_char_columns = as.vector(columns_types[(!(columns_types$type %in% c("factor","character"))),"columns"]) ;

    predictors = intersect(predictors, colnames(dataframe));
    for (i in seq(length(predictors))){
        col = predictors[i];
        if (col %in% char_columns){
            h2o.impute(data=data_hex, column= which(colnames(data_hex)==col), method="mode", combine_method="interpolate");
            }else{
                h2o.impute(data=data_hex, column= which(colnames(data_hex)==col), method="median", combine_method = "interpolate");
            }
    }
    return(data_hex)
}


dataImputationByH2o = function( dataframe, 
                                data_hex, 
                                predictors,
                                percent_data_in_training=1.0,
                                impute_categorical_ind=TRUE,
                                bycolumn=NULL){
    # data is the original data frame
    # data_hex is as.h2o hex data format of data
    # predictors is the list of input variables that need to be imputed
    # bycolumn defines impute by which column, for example c("pol_risk_state_cd")
    # impute_categorical_ind is boolean for whether to impute the categorical variables

    # percent_data_in_training is the % of data used in training, to save time when dealing with huge data
    columns_types = data.frame(columns = colnames(dataframe),
                               type=as.vector(sapply(dataframe, class))) ;
    char_columns = as.vector(columns_types[columns_types$type %in% c("factor","character"), "columns"]) ;
    non_char_columns = as.vector(columns_types[(!(columns_types$type %in% c("factor","character"))),"columns"]) ;
    
    predictors = intersect(predictors, colnames(dataframe));
    for (col in predictors){
        if (sum(is.na(data_hex[,col])) + sum(data_hex[,col]=="") == 0){
            predictors <- setdiff(predictors, col);
            print(paste("Column",col,"does not have missing values..."))
        }
    }

    for (col in intersect(predictors, char_columns)){
            if (h2o.nlevels(data_hex[,col]) > 1000){
                predictors <- setdiff(predictors, col);
                print(paste("Column",col,"has move than 1000 levels..."))
            }
    }

    for (i in seq(length(predictors))){
        col = predictors[i];
        if (col %in% char_columns){
            if (impute_categorical_ind){
                  #h2o.impute(data=data_hex, column= which(colnames(data_hex)==col), method="mode", by=bycolumn);
                  #h2o.impute(data=data_hex, column= which(colnames(data_hex)==col), method="mode");
                  predict_idx = is.na(data_hex[,col]) | data_hex[,col]=="";
                  train_idx = !(is.na(data_hex[,col]) | data_hex[,col]=="");
                  
                  train_hex <- data_hex[train_idx,];
                  sub <- sample(nrow(train_hex), floor(nrow(train_hex) * percent_data_in_training));
                  sub <- sort(sub);
                  gbm <- h2o.gbm(y=col, x=setdiff(colnames(data_hex),col), training_frame = train_hex[sub,],
                                 sample_rate=0.5);
                  pred = h2o.predict(object = gbm, newdata = data_hex[predict_idx,]);
                  nums = as.vector(data_hex[,col]);
                  nums[is.na(nums)] = as.vector(pred[,1])
                  data_hex[,col] = as.h2o(nums);
                } else{
                    vec = as.vector(data_hex[,col]);
                    vec[is.na(vec) | gsub("^\\s+|\\s+$", "", vec)==""] = "____NA";
                    data_hex[,col] <- as.h2o(vec);
                }
        } else {
                #h2o.impute(data=data_hex, column= which(colnames(data_hex)==col), method="median", combine_method = "interpolate");
                predict_idx = is.na(data_hex[,col])
                train_idx = !is.na(data_hex[,col])

                train_hex <- data_hex[train_idx,];
                sub <- sample(nrow(train_hex), floor(nrow(train_hex) * percent_data_in_training));
                sub <- sort(sub);
                gbm <- h2o.gbm(y=col, x=setdiff(colnames(data_hex),col), training_frame = train_hex[sub,],
                    sample_rate=0.5);
                pred = h2o.predict(object = gbm, newdata = data_hex[predict_idx,]);
                col_idx = which(colnames(data_hex)==col);
                var_type = unlist(h2o.getTypes(data_hex))[col_idx];
                nums = as.vector(data_hex[,col]);
                if (var_type == "int" | var_type == "integer"){
                    nums[is.na(nums)] = as.integer(as.vector(pred));
                } else {nums[is.na(nums)] = as.vector(pred)}

                data_hex[,col] = as.h2o(nums);
        }
    }
    return(data_hex)
}


convertInt2Factor = function(data, cols=c()){
    cols = intersect(cols, colnames(data));
    for (col in cols){
        data[ , col] <- as.character(data[ , col])
        data[ , col] <- as.factor(data[ , col])
    }
    return(data)
}


dropColumnWithSingleValue = function(df, col, missing_threshold=0.4){
    ###
    # This function removes the column col of data frame df if
        # there is one value in the column or more than 40% of
        # data are missing in df
    ###
    # df = as.data.frame(data_sample)
    # col = "pol_split_pd_liab_deductible_am"
    # missing_threshold defines the threshold of % of missing to be dropped
    colvec = df[,col];
    unique_values = unique(colvec);
    unique_values2 = unique_values[!is.na(unique_values)]
    if (length(unique_values2) <= 1){
        df[,col] <- NULL ;
        return(df)
    } else if (sum(is.na(colvec))*1.0/length(colvec) >= missing_threshold){
        df[,col] <- NULL ;
        return(df)
    } else {return(df)}
}


replaceWithNA = function(df, col, 
                        missing_values=c("","N/A","UNKNOWN","UNKN","n/a","NA","na","Unknown","unkn")){
    ###
    # This function changes the values of col to NA if some values are
        # specified in the missing_values list
    ###
    # df = as.data.frame(data_sample)
    # col = "pol_tier_tx"
    # missing_values=c("","N/A","UNKNOWN")
    colvec = as.vector(df[,col]);
    if (typeof(colvec) == "character"){
        colvec = trimws(colvec,which="both");
        colvec2=as.vector(sapply(colvec, FUN=function(x){if (x %in% missing_values){return(NA)}else{return(x)}}));
        df[,col] = colvec2 ;
        return(df)
        } else {return(df)}
}


getAllCharacterValuesInDF = function(df){
    columns_types = data.frame(columns = colnames(df),
                              type=as.vector(sapply(df, typeof)));
    columns_char = columns_types[which(columns_types$type=="character"),"columns"];
    values = c();
    for (c in as.vector(columns_char)){
        values = c(values, unique(df[,c]));
    }
    return(unique(values))
}


removeBadColumns = function(df){
    ###
    # This function is to remove the columns with too many missing values 
        # or just a unique value
    ###
    colname = colnames(df)
    counter = 1
    for (col_ in colname){
        df = replaceWithNA(df, col_);
        df = dropColumnWithSingleValue(df, col_)
        print(paste("Finished ",counter,"out of ",length(colname),"columns", sep=" "))
        counter = counter +1
    }
    return(df)
}


findAlphaLambda = function(x){
    # x = "Elastic Net (alpha = 0.5, lambda = 5.387E-4 )"
    pattern = 'alpha'
    loc = gregexpr(pattern =pattern,x)[[1]][1]
    x2 = substr(x, loc, 1000000)
    x3 = gsub(",", "", gsub(")", "", gsub("=", "", x2)))
    x4 = strsplit(x3," ")[[1]]
    x5 = x4[! x4 %in% ""]
    if (length(x5) == 4) {
        alpha = as.numeric(x5[2]) ;
        lambda = as.numeric(x5[4]) ;
    } else {print("No Alpha or Lambda value found")}
    return(c(alpha, lambda))
}


### Test Code ###
library(h2o)

insure = data.frame(exposure=c(500,1200,100,400,500,300),
                    claim_count=c(42,37,1,101,73,14),
                    car_size=c("small","medium","large","small","medium","large"),
                    age=c(1,1,1,2,2,2));

insure$freq = insure$claim_count / insure$exposure;
#insure$age = factor(insure$age)
insure$logexp = log(insure$exposure);

glm_freq_with_weight <- glm(freq ~ car_size + age, family = poisson(), data=insure, weights=exposure);
summary(glm_freq_with_weight)

h2o.init(nthreads=-1)
insure$car_size[c(1,3)] <- NA;
insure$claim_count[c(4)] <- NA;
insure_hex <- as.h2o(insure);
insure_hex = h2o.rbind(insure_hex,insure_hex,insure_hex,insure_hex,insure_hex,insure_hex);

dataImputationByH2o( dataframe = insure, 
                    data_hex = insure_hex, 
                    predictors = colnames(insure),
                    impute_categorical_ind=TRUE,
                    bycolumn=NULL)

