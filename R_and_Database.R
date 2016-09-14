#  R & PostgreSQL
library(RPostgreSQL);
con <- dbConnect(PostgreSQL(), host="NATABCD054", user= "postgres", password="mypassword", dbname="MyDB");
rs <- dbSendQuery(con, "SELECT * FROM data.mytable");
df <- fetch(rs, n=-1); #n=-1 fetches all rows, n=100 fetches first 100 rows
write.csv(df, file = "df.csv", row.names=FALSE, na="");
dbDisconnect(con);

##############################
#  R & Microsoft SQL Server
library(RODBC);
myconn <- odbcConnect('MyDB', uid='Myuser', pwd=''),
df <- sqlQuery(myconn,"select * from dbo.mytable");

##############################
#  R & Text Files
dir.create(file.path('c:/temp','new_folder'), showWarnings = TRUE); #create folder if it doesn't exist
write('abc',file='c:/temp/new_folder/a.txt',append=TRUE); #create file
myfile <- paste('c:/temp/new_folder/',"a.txt",sep="");
fileConn <- file(myTimelogfile);
writeLines('what is up',fileConn,sep="\n"); #add lines to text file
close(fileConn);

##############################
#  Do R Data Frame Aggregation, Distinct
###################################
# The following are commonly used functions
# and tools for data mainpuation
# and data imputaion
###################################

objectSizeList <- function(...) {
    # return object sizes in the workspace
    # sample usage:
        # objectSizeList()
    objs_ <- ls(envir = globalenv())
    for (obj_ in objs_) {
        sz <- object.size(get(obj_))
        sz2 <- utils:::format.object_size(sz, "auto")
        if (!exists("object_size_chart")) {
            object_size_chart <- data.frame(object=obj_, size=sz2, size_byte=c(as.numeric(sz)))
        } else {
            object_size_chart <- rbind(object_size_chart,
                                       data.frame(object=obj_, size=sz2, size_byte=c(as.numeric(sz))))
        }
    }

    object_size_chart$size_byte <- as.numeric(as.vector(object_size_chart$size_byte))
    object_size_chart2 <- object_size_chart[with(object_size_chart, order(-size_byte)) ,]
    return(object_size_chart2)
}


loadExcel <- function(filename, gc_ind=FALSE){
    options ( java.parameters = "-Xmx60g" )
    require(XLConnect)
    wb <- loadWorkbook(filename, create = TRUE)
    lst = readWorksheet(wb, sheet = getSheets(wb))
    for (n in names(lst)){
        name <- gsub("-",'_',gsub(" ",'_',n))
        eval(parse(text=paste(name," <- lst[[n]]", sep="")))
        eval(parse(text=paste("assign(name,",name,", envir = .GlobalEnv)", sep="")))
    }
    if (gc_ind){
        gc()
    }
}

if (FALSE){
    # test
    # load excel file with multiple sheets into data data frame
    loadExcel("ABI Group 201607.xlsx")
}


loadCSV <- function(csvfile, file_format = "data.frame") {
    # load csv file into data frame or data table
    file_format_list_ = c("data.table", "data.frame")
    if (!(file_format %in% file_format_list_)) {
        stop(paste("The file_format must be one of", paste(file_format_list_, collapse=", ")))
    }

    dt = data.table::fread(csvfile, header=TRUE, na.strings=c('NA', 'N/A', 'NAN', 'Nan'),
                           stringsAsFactors = TRUE)
    if (file_format == "data.frame") {
        print("data format returned is data.frame")
        return(as.data.frame(dt))
    } else {
        print("data format returned is data.table")
        return(dt)
    }
}

if (FALSE) {
    # sample usage
    datatable = loadCSV("mycsvfile.csv", file_format = "data.table")
}


replace_column_values <- function(data,
                                  col,
                                  col_value_replace_from,
                                  col_value_replace_to){
    # sample input
    # data is data frame or data.table
    # col is the column to replace
    # col_value_replace_from is the list of values to be replaced
    # col_value_replace_to is the value to be replaced with
    if (!(col %in% colnames(data))) {
        return(data)
        warning(paste("Variable ", col, " is not in the data frame!", sep=""))
    } else {
        if ("data.table" %in% class(data)) {type <- "data.table"
        } else if ("data.frame" %in% class(data) & length(class(data)) == 1) {
            type <- "data.frame"
        } else {stop("The input data is neither data.frame nor data.table!")}

        if (type == "data.table") data <- as.data.frame(data)

        if (!(paste(col,"_orig", sep="") %in% colnames(data))) {
            # avoid being overide twice
            data[ , paste(col,"_orig", sep="")] <- data[, col]  # backup original column values
            print(paste("Back up column ", col, " using new column ", col, "_orig ...", sep=""))
        }
        data[, col] <- as.character(data[, col])
        data[data[, col] %in% as.character(col_value_replace_from), col] <- as.character(col_value_replace_to)
        if (type == "data.table") {
            return(data.table::data.table(data))
        } else {return(data)}
    }
}


convertCSV2RDS <- function(csvfile,
                           R.table.format = c("data.frame", "data.table"),
                           header=TRUE,
                           na.strings=c('NA', 'N/A', 'NAN', 'Nan'),
                           stringsAsFactors = TRUE,
                           compress = F) {
    # This function converts the CSV file to data.table in RDS format on local drive
    if (!(length(setdiff(R.table.format, c("data.frame", "data.table"))) == 0
        & length(c(R.table.format))==1)) {
        stop("The R.table.format has to be one of data.frame and data.table")
    }
    directory <- dirname(csvfile)
    filename <- basename(csvfile)
    dt = data.table::fread(csvfile,
               header=header,
               na.strings=na.strings,
               stringsAsFactors = stringsAsFactors)
    if (R.table.format == "data.frame") {
        dt <- as.data.frame(dt)
    }
    print(paste("Saving ", filename, " file to ", gsub(".csv",".rds", tolower(filename)), " file...", sep=""))
    saveRDS(dt, file = file.path(directory, gsub(".csv",".rds", tolower(filename))), compress=compress)
    print(paste("Use code of format  dt = readRDS(rdsfile) to load .RDS data into ",R.table.format," ...", sep=""))
}


loadRDSfile <- function(rdsfile, R.table.format = c("data.frame", "data.table")) {
    # This function loads in the .RDS data
    if (!(length(setdiff(R.table.format, c("data.frame", "data.table"))) == 0
          & length(c(R.table.format))==1)) {
        stop("The R.table.format has to be one of data.frame and data.table")
    }
    d <- readRDS(rdsfile)
    if ("data.table" %in% class(d)) {
        dtype <- "data.table"
    } else if (class(d) == "data.frame") {
        dtype <- "data.frame"
    } else {stop("The file loaded in is neither data frame nor data table")}
    if (R.table.format == dtype) {
        return(d)
    } else if (R.table.format == "data.frame") {
        return(as.data.frame(d))
    } else {return(data.table::data.table(d))}
}


sampleData <- function(dataframe, sampling_percentage) {
    sample_idx <- sample(nrow(dataframe), floor(nrow(dataframe) * sampling_percentage))
    return(dataframe[sample_idx, ])
}

if (FALSE) {
    # sample usage
    dataframe_sample <- sampleData(dataframe, 0.05)
}


getRandomSeed = function(...){
    # use sys.time() to generate random seeds
    set.seed(as.integer((as.double(Sys.time())*1000+Sys.getpid()) %% 2^31));
    seed2 = as.integer(runif(1,min=0,max=999999999));
    set.seed(seed2);
    last_seed = as.integer(runif(1, -(2^31 - 1), 2^31));
    return(last_seed)
}

subsample <- function(data, sample_percent){
    # this is for getting the subset of data using random percentage
    seed_ <- getRandomSeed()
    set.seed(seed_)
    sub <- sample(nrow(data), floor(nrow(data) * sample_percent));
    return(data[sub, ])
}

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


findZeroVarianceColumns <- function(data){
    zero_var_columns = c()
    ncols <- ncol(data)
    for (i in seq(1,ncols)){
        if (var(data[,i]) == 0){
            print(paste("Column",i,"has 0 variance"))
            zero_var_columns <- c(zero_var_columns, i)
        }
    }
    return(zero_var_columns)
}


removeSingleValueCol <- function(df){
  cols <- colnames(df);
  for (col in cols){
    x_ = df[, col]
    if (nlevels(factor(x_))==1){
      df[, col] <- NULL
    }
  }
  return(df)
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


distinct_data <- function(data,
                          distinct_by_col,
                          unique_col, unique_by_op,
                          cols_to_sum = NA,
                          cols_to_min = NA,
                          cols_to_max = NA) {
    # This is to select unique record based on unique_col column
    # for example, select the company having min employees within each state, example attached below
    # for the rest of columns, speify cols_to_sum, etc. to sum up rest of columns when take
    # other columns in
    require(data.table)
    if ("data.table" %in% class(data)) {
        dftype = "data.table"
    } else if ("data.frame" %in% class(data)) {
        dftype = "data.frame"
    } else {stop("The data must be either data frame or data table!")}
    
    if (!(unique_by_op %in% c("min", "max"))) stop("unique_by_op must be one of min, max!")
    
    if (dftype == "data.frame") data <- data.table::data.table(data)
    
    data$myrowid_temp <- seq(1, nrow(data))
    cmd <- paste("setkey(data, ",paste(unique(c("myrowid_temp", distinct_by_col)), collapse=", "),")", sep="")
    eval(parse(text = cmd))
    cmd <- paste("data[, zzzzz_1 := ",unique_by_op,"(", unique_col,"), by = distinct_by_col]", sep="")
    eval(parse(text = cmd))
    dt1 <- data
    cmd <- paste("setkey(dt1, ",paste(unique(c("myrowid_temp", distinct_by_col)), collapse=", "),")", sep="")
    eval(parse(text = cmd))
    cmd <- paste("dt1 <- dt1[", unique_col," == zzzzz_1]", sep="")
    eval(parse(text = cmd))
    data[ , zzzzz_1 := NULL]
    data[ , myrowid_temp := NULL]
    dt1[ , zzzzz_1 := NULL]
    cmd <- paste("setkey(dt1, ",paste(unique(c(unique_col, distinct_by_col)), collapse=", "),")", sep="")
    eval(parse(text = cmd))
    cmd <- paste("dt1[, zzzzz_1 := ",unique_by_op,"(myrowid_temp), by = c(distinct_by_col, unique_col)]", sep="")
    eval(parse(text = cmd))
    cmd <- paste("dt1 <- dt1[myrowid_temp == zzzzz_1]", sep="")
    eval(parse(text = cmd))
    dt1[ , zzzzz_1 := NULL]
    dt1[ , myrowid_temp := NULL]
    # cmd <- paste("dt1 <- data[ , .SD[which.", unique_by_op,
    #              "(", unique_col, ")], by = c('",
    #              paste(distinct_by_col, collapse="' , '"),
    #              "')]", sep ="")
    # eval(parse(text = cmd))
    # 
    if (is.na(cols_to_sum[1])) cols_to_sum <- ""
    if (is.na(cols_to_min[1])) cols_to_min <- ""
    if (is.na(cols_to_max[1])) cols_to_max <- ""
    all_other_cols <- c(cols_to_sum, cols_to_min, cols_to_max)
    dt1 <- dt1[ , setdiff(colnames(dt1), c(all_other_cols)),with=FALSE]
    cmd2 <- paste("setkey(dt1, ",paste(distinct_by_col, collapse=","),")", sep="")
    eval(parse(text = cmd2))
    
    if (nchar(paste(cols_to_sum, collapse="")) >= 1) {
        dt_ <- data[, lapply(.SD, sum), by=distinct_by_col, .SDcols=cols_to_sum]
        cmd3 <- paste("setkey(dt_, ",paste(distinct_by_col, collapse=","),")", sep="")
        eval(parse(text = cmd3))
        dt1 <- merge(dt1, dt_, all=FALSE) # inner merge data tables
        rm(cmd3, dt_)
    }
    
    if (nchar(paste(cols_to_min, collapse="")) >= 1) {
        dt_ <- data[, lapply(.SD, min), by=distinct_by_col, .SDcols=cols_to_min]
        cmd3 <- paste("setkey(dt_, ",paste(distinct_by_col, collapse=","),")", sep="")
        eval(parse(text = cmd3))
        dt1 <- merge(dt1, dt_, all=FALSE) # inner merge data tables
        rm(cmd3, dt_)
    }
    
    if (nchar(paste(cols_to_max, collapse="")) >= 1) {
        dt_ <- data[, lapply(.SD, max), by=distinct_by_col, .SDcols=cols_to_max]
        cmd3 <- paste("setkey(dt_, ",paste(distinct_by_col, collapse=","),")", sep="")
        eval(parse(text = cmd3))
        dt1 <- merge(dt1, dt_, all=FALSE) # inner merge data tables
        rm(cmd3, dt_)
    }
    
    rm(data)  # save memory
    
    if (dftype == "data.frame") dt1 <- as.data.frame(dt1)
    return(dt1)
}

if (FALSE){
    data <- structure(list(State = structure(c(1L, 1L, 1L, 1L, 2L, 2L, 2L, 2L),
                                             .Label = c("AK", "RI"), class = "factor"),
                           Company = structure(1:8, .Label = c("A", "B", "C", "D", "E", "F", "G", "H"),
                                               class = "factor"), Employees = c(82L, 104L, 37L, 24L, 19L, 118L, 88L, 42L)), .Names = c("State", "Company", "Employees"),
                      class = "data.frame", row.names = c(NA, -8L))
    data$total_counts <- 1
    
    distinct_by_col = c("State")
    unique_col = "Employees"
    unique_by_op = "min" # or max if you need
    
    cols_to_sum <- "total_counts"
    cols_to_min <- NA
    cols_to_max <- NA
    
    distinct_data(data, distinct_by_col,
                  unique_col, unique_by_op,
                  cols_to_sum)
}


check_columns_are_identifier <- function(data, identifier) {
    # check if the columns identifier are the unique keys for data.table data
    if (!("data.table" %in% class(data))) stop("Convert data into data.table first!")
    data <- data[ , identifier,with=FALSE]
    setkey(data)
    # key(data)
    row_diff <- nrow(data) - nrow(unique(data))
    if (row_diff == 0) {
        print("The columns tested are unique identifier of the data")
        return(TRUE)
    } else {
        print(paste(row_diff, " out of ", nrow(data), " rows are NOT unique by the columns tested!", sep=""))
        return(FALSE)
    }
}


drop_column_datatable <- function(data, column_to_drop) {
    # this is for dropping column in the data.table.
    # use with precaution, this is in-place operation function
    column <- column_to_drop  # legacy code
    if (!("data.table" %in% class(data))) stop("Convert data into data.table first!")
    cmd <- paste("data[ , ", column, " := NULL]", sep="")
    eval(parse(text=cmd))
}


remove_dup_rows_by_columns <- function(data, columns) {
    # this function is to remove the rows with duplicate records in the columns specified
    allcols <- colnames(data)
    if (!("data.table" %in% class(data))) stop("Convert data into data.table first!")
    dt <- data[, columns, with=FALSE]
    gc()
    setkey(dt)
    dt <- unique(dt[duplicated(dt[, with = FALSE])])
    gc()
    dt$zzz_extra <- 1
    eval(parse(text=paste("setkey(data, ", paste(columns, collapse = ", "), ")" , sep="")))
    data <- merge(data, dt, all.x = TRUE)
    gc()
    setkey(data, zzz_extra)
    data <- data[is.na(zzz_extra)]
    gc()
    data[, zzz_extra := NULL]
    return(data[, allcols, with=FALSE])
}

if (FALSE){
    data <- structure(list(State = structure(c(1L, 1L, 1L, 1L, 2L, 2L, 2L, 2L),
                                             .Label = c("AK", "RI"), class = "factor"),
                           Company = structure(1:8, .Label = c("A", "B", "C", "D", "E", "F", "G", "H"),
                                               class = "factor"), Employees = c(82L, 104L, 37L, 24L, 19L, 118L, 88L, 42L)), .Names = c("State", "Company", "Employees"),
                      class = "data.frame", row.names = c(NA, -8L))
    data$total_counts <- c(1,1,2,3,4,5,5,6)
    data = data.table::data.table(data)

    data1 = data
    columns <- c("State", "total_counts")
    data <- remove_dup_rows_by_columns(data, columns)
    data1
    data
}


apply_function_to_column <- function(data, func, column) {
    # This function applies the funciton func to the specified column
    # the replacement is in-place, use with pre-caution.
    cmd <- paste("myrandomvar <- as.vector(as.data.frame(data[, ", column, "])[,1])", sep="")
    eval(parse(text=cmd))
    myrandomvar <- func(myrandomvar)
    cmd <- paste("data[, ",column," := myrandomvar","]", sep="")
    eval(parse(text=cmd))
    return(data)
}

if (FALSE) {
    data <- structure(list(State = structure(c(1L, 1L, 1L, 1L, 2L, 2L, 2L, 2L),
                                             .Label = c("AK", "RI"), class = "factor"),
                           Company = structure(1:8, .Label = c("A", "B", "C", "D", "E", "F", "G", "H"),
                                               class = "factor"), Employees = c(82L, 104L, 37L, 24L, 19L, 118L, 88L, 42L)), .Names = c("State", "Company", "Employees"),
                      class = "data.frame", row.names = c(NA, -8L))
    data$total_counts <- c(1,1,2,3,4,5,5,6)
    data = data.table::data.table(data)
    data
    apply_function_to_column(data, func=function(x) x**2, column="total_counts")
    data
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


checkNumofDistinctValues = function(data){
    # check num of levels for columns of type factor
    columns_types = data.frame(columns = colnames(data),
                               type=as.vector(sapply(data, class))) ;
    char_columns = as.vector(columns_types[columns_types$type == "character", "columns"]) ;
    levelCheck = data.frame(col=NA,numLevels=NA)[0,];
    for (col in char_columns){
        num_of_levels = length(unique(data[,col]));
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


## This is the major function that does missing data imputation
dataImputationByH2o = function( training_data_hex,
                                score_data_hex,
                                predictors,
                                percent_data_in_training=1.0,
                                nfolds = 3,
                                weights_column = NULL,
                                model_storage_folder = NULL,
                                impute_categorical_ind=TRUE,
                                bycolumn=NULL){
    # training_data_hex is as.h2o hex data format of training data
        # training_data_hex is the data for training purpose
        # it contains the missing data values
        # model is built ONLY on training_data_hex
    # score_data_hex is the hex data that will be imputed
    # predictors is the list of input variables that need to be imputed
    # bycolumn defines impute by which column, for example c("pol_risk_state_cd")
    # impute_categorical_ind is boolean for whether to impute the categorical variables
    # weights_column specifies which column is the weight column

    # percent_data_in_training is the % of data used in training, to save time when dealing with huge data

    if (is.null(model_storage_folder)){model_storage_folder = gsub("/","\\\\", getwd())}else{model_storage_folder = gsub("/","\\\\", model_storage_folder)}

    data_hex = training_data_hex;
    dataframe = as.data.frame(data_hex[1:2,]);

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
        print(paste("Column",col,"is having missing values imputed..."));
        if (col %in% char_columns){
            if (impute_categorical_ind){
                  #h2o.impute(data=data_hex, column= which(colnames(data_hex)==col), method="mode", by=bycolumn);
                  #h2o.impute(data=data_hex, column= which(colnames(data_hex)==col), method="mode");
                  predict_idx = is.na(data_hex[,col]) | data_hex[,col]=="";
                  train_idx = !(is.na(data_hex[,col]) | data_hex[,col]=="");

                  train_hex <- data_hex[train_idx,];
                  sub <- sample(nrow(train_hex), floor(nrow(train_hex) * percent_data_in_training));
                  sub <- sort(sub);
                  gbm <- h2o.gbm(y=col, x=setdiff(colnames(data_hex),c(col, weights_column)), training_frame = train_hex[sub,],
                                 sample_rate=0.5, nfolds=nfolds, weights_column=weights_column,
                                 model_id = paste(col,"_gbm_model",sep=""));
                  # score on training hex data
                  pred = h2o.predict(object = gbm, newdata = data_hex[predict_idx,]);
                  nums = as.vector(data_hex[,col]);
                  nums[is.na(nums)] = as.vector(pred[,1])
                  data_hex[,col] = as.h2o(nums);
                  # score on the score hex data
                  predict_score_idx = is.na(score_data_hex[,col]) | score_data_hex[,col]=="";
                  predict_score_idx_dataframe = which(as.vector(predict_score_idx) == 1);
                  pred_score = h2o.predict(object = gbm, newdata = score_data_hex[predict_score_idx,]);
                  nums_score = as.vector(score_data_hex[,col]);
                  nums_score[predict_score_idx_dataframe] = as.vector(pred_score[,1])
                  score_data_hex[,col] = as.h2o(nums_score);
                  # save gbm model into the output folder
                  eval(parse(text=paste(col,"_gbm_model <- gbm",sep="")));
                  cmd = paste("h2o.saveModel(object = ", col,"_gbm_model, path = model_storage_folder, force=TRUE);",sep="");
                  eval(parse(text=cmd));
                } else{
                    vec = as.vector(score_data_hex[,col]);
                    vec[is.na(vec) | gsub("^\\s+|\\s+$", "", vec)==""] = "____NA";
                    score_data_hex[,col] <- as.h2o(vec);
                }
        } else {
                #h2o.impute(data=data_hex, column= which(colnames(data_hex)==col), method="median", combine_method = "interpolate");
                predict_idx = is.na(data_hex[,col])
                train_idx = !is.na(data_hex[,col])

                train_hex <- data_hex[train_idx,];
                sub <- sample(nrow(train_hex), floor(nrow(train_hex) * percent_data_in_training));
                sub <- sort(sub);
                gbm <- h2o.gbm(y=col, x=setdiff(colnames(data_hex),c(col, weights_column)), training_frame = train_hex[sub,],
                                sample_rate=0.5, nfolds=nfolds, weights_column=weights_column,
                                model_id = paste(col,"_gbm_model",sep=""));
                # score on the training hex data
                pred = h2o.predict(object = gbm, newdata = data_hex[predict_idx,]);
                col_idx = which(colnames(data_hex)==col);
                var_type = unlist(h2o.getTypes(data_hex))[col_idx];
                nums = as.vector(data_hex[,col]);
                if (var_type == "int" | var_type == "integer"){
                    nums[is.na(nums)] = as.integer(as.vector(pred));
                } else {nums[is.na(nums)] = as.vector(pred)}

                data_hex[,col] = as.h2o(nums);
                # score on the score hex data
                predict_score_idx = is.na(score_data_hex[,col]);
                predict_score_idx_dataframe = which(as.vector(predict_score_idx) == 1);
                pred_score = h2o.predict(object = gbm, newdata = score_data_hex[predict_score_idx,]);
                col_idx = which(colnames(score_data_hex)==col);
                var_type = unlist(h2o.getTypes(score_data_hex))[col_idx];
                nums_score = as.vector(score_data_hex[,col]);
                if (var_type == "int" | var_type == "integer"){
                    nums_score[predict_score_idx_dataframe] = as.integer(as.vector(pred_score));
                } else {nums_score[predict_score_idx_dataframe] = as.vector(pred_score)}

                score_data_hex[,col] = as.h2o(nums_score);
                # save gbm model into the output folder
                eval(parse(text=paste(col,"_gbm_model <- gbm",sep="")));
                cmd = paste("h2o.saveModel(object = ", col,"_gbm_model, path = model_storage_folder, force=TRUE);",sep="");
                eval(parse(text=cmd));
        }
    }
    return(score_data_hex)
}


reassignColumnType = function(hexdata, matched_hexdata_types){
    ## This function converts the column types in hexdata
    # to the desired one based on the specified
    # matched_hexdata_types

    # for example:
    #  hexdata is the hex data by h2o data frame
    #  matched_hexdata_types is data frame like
    #            column  type
    #            var1    enum   #this is like factor
    #            var2    real
    #            var3    int
    current_hexdata_types <- data.frame(column=colnames(hexdata),
                                        type=unlist(h2o.getTypes(hexdata)));

    for (col in current_hexdata_types$column){
        if (col %in% matched_hexdata_types$column){
            curr_type = current_hexdata_types[current_hexdata_types$column==col,"type"];
            new_type = matched_hexdata_types[matched_hexdata_types$column==col,"type"];
            curr_type = as.character(curr_type);
            new_type = as.character(new_type);
            if (curr_type != new_type){
                if (substr(new_type,1,3) %in% c("enu", "str")){
                    hexdata[,col] = as.factor(hexdata[,col])
                }else{hexdata[,col] = as.numeric(hexdata[,col])}
            }
        }
    }
    return(hexdata)
}


convertInt2Factor = function(data, cols=c()){
    # convert the columns (cols) to factor field
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
    # one time use, not used
    # this function tries to get all values for character variables
    columns_types = data.frame(columns = colnames(df),
                              type=as.vector(sapply(df, typeof)));
    columns_char = columns_types[which(columns_types$type=="character"),"columns"];
    values = c();
    for (c in as.vector(columns_char)){
        values = c(values, unique(df[,c]));
    }
    return(unique(values))
}


getVariableTypes = function(df){
    typ = data.frame(column = colnames(df),
                           class=as.vector(sapply(df, class)),
                           type=as.vector(sapply(df, typeof)))
    return(typ)
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


exportTable = function(table_name, csv_file_name_suffix="__temptable"){
    #print(is.environment(.GlobalEnv))
    # table_name is name of the data frame object in work space

    # for example, if we have  data frame called myDataFrame
    # >>> exportTable("myDataFrame")
    # will export it out to a csv file

    if (is.character(table_name)){
        cmd = paste("write.csv(",table_name,", file='", table_name, csv_file_name_suffix,".csv'",
                ", row.names=FALSE)", sep="");
        eval(parse(text=cmd), envir=.GlobalEnv)  #it means execution is on parent envrionemnt
    } else{
        print("The table name input in the function needs to be a string!")
    }

}


groupDesignMatrixColumnNames <- function(design_matrix_names, variable_pool){
    # design_matrix_names is the column names for design matrix
    # variable_pool is list of all possible original variable names
        # for creating design matrix. It can have more irrelevant variables
    x_matrix_orignalnames <- rep(NA, length(design_matrix_names))
    for (x_ in variable_pool){
        match_ = grepl(glob2rx(paste(x_,"*",sep="")) , design_matrix_names)
        if (sum(match_) >=1 ) {
            x_matrix_orignalnames[match_] = x_
        }
    }

    x_matrix_orignalnames = as.data.frame(x_matrix_orignalnames)
    name_counts <- sqldf::sqldf("select a.x_matrix_orignalnames, b.count
                        from x_matrix_orignalnames as a left join
                            (select x_matrix_orignalnames, count(1) as count
                                from x_matrix_orignalnames
                                group by x_matrix_orignalnames) as b
                        on a.x_matrix_orignalnames = b.x_matrix_orignalnames")
    if (length(name_counts[is.na(name_counts)]) >= 1){
        name_counts$count[is.na(name_counts$count)] <- 1
    }
    return(name_counts)
}


scalePredictionbyActual = function(prediction,
                                   actual,
                                   index,
                                   weight=rep(1,length(prediction))){
    #########
    # This function is to scale the predicted values so that weighted
        # average of prediction is the same as weighted average
        # of actual on the index
    #########
    # prediction is the predicted values
    # actual is the actual target values
    # index is the index of predicted values to be scaled by actual
    # weight is the exposure, default is 1 if none is specified

    # Sample input
    # prediction = c(1,2,3,4,5,6,7,8)
    # actual = c(4,8,12,16,20,24,28,32)
    # weight = c(1,1,2,3,4,2,1,9)
    # index = c(2,4,5);
    p_ = prediction[index]
    a_ = actual[index]
    wgt = weight[index]

    p_ = p_ * sum(a_ * wgt) / sum(p_ * wgt)
    p2 = prediction
    p2[index] = p_
    return(p2)
}

###################################################################
## The following are variable manipulation tools

fillMissingwith0 = function(data, cols, convert_variable_to_string_ind=FALSE){
    # this function fills missing integered valued variables with 0
        # for example, for the missing # of incidents
    # data is the data frame
    # cols is the list of columns to be processed
    # if convert_variable_to_string_ind=TRUE, then we set these integered
        # variables to be characters
    for (col in cols){
        data[is.na(data[,col]),col]=0;
        if (convert_variable_to_string_ind){
            data[,col] = as.character(data[,col])
        }
    }
    return(data)
}


convert2CharacterField = function(data, cols){
    # this function converts the specified columns (cols) to charaters
    for (col in cols){
        data[,col] = as.character(data[,col])
    }
    return(data)
}


convertDataFrameToModelMatrix = function(data, predictors, target){
    ## This function converts the data to x_matrix and y_matrix so that
        ## it can be used directly in elastic net
    x_matrix <- as.data.frame(model.matrix(formula(paste("~ -1 +",paste(predictors,collapse="+"))), data));
    x_matrix <- as.matrix(x_matrix);
    y_matrix <- as.matrix(data[, target])
    res = list()
    res[[1]] = x_matrix;
    res[[2]] = y_matrix;
    return(res)
}


assignMostFreqAsBase = function(data, factor_column){
    # this function converts the factor_column to factor column and assign the
        # the level with most frequency as the base level

    a = which.max(table(data[,factor_column]));
    b = table(data[,factor_column]);
    data[,factor_column] <- factor(data[,factor_column], levels = c(names(a),setdiff(names(b),names(a))));
    return(data)
}


changeFactorBaseLevel = function(data, col, factor_base){
    if (class(data[,col]) != "factor"){data[,col] = as.factor(data[,col])}
    lvls = levels(data[,col])
    if (!(factor_base %in% lvls)){stop(paste("Level", factor_base, "does not exist!"))}else{
        new_levels = c(factor_base, setdiff(lvls, factor_base));
        data[,col] <- factor(data[,col], levels = new_levels);
        return(data)
    }
}


MHmakeRandomString <- function(n=1, lenght=18){
            randomString <- c(1:n) # initialize vector
            for (i in 1:n){randomString[i] <- paste(sample(c(0:9, letters), lenght, replace=TRUE), collapse="")}
            return(randomString)
}


convert_var_to_factor <- function(vars, data){
    # convert the categorical variable values into factors
        # where the most frequent value is used as base
    vars2 <- intersect(vars, colnames(data)) #take variables in the data frame
    for (rv in vars2){
        x <- as.factor(data[, rv])
        x_ <- table(x)
        counts <- as.vector(x_)
        names <- names(x_)
        if (length(names)==1){
            print(paste("Variable ",rv," has ",length(names)," distinct levels.", sep=""))
        }
        base_level <- names[min(which(counts == max(counts)))]
        new_levels <- c(base_level, setdiff(names, base_level))
        data[,rv] <- factor(x, levels = new_levels);
        rm(x_, counts, names, x, base_level, new_levels)
    }
    return(data)
}


createInteraction <- function(data, vars_to_interact){
    # varaibles need to be factors first
    # this function is to create interaction terms of categorical variables for a given data
        # and variables to be interact with
    for (v in vars_to_interact){
        if (class(data[, v]) != "factor"){
            stop(paste("Variable",v,"needs to be a factor variable!"))
        }
    }
    x_ <- data[, vars_to_interact];

    base_levels<-c();
    var_level_list <- list();
    for (c in vars_to_interact){
        base_levels <- c(base_levels, levels(x_[,c])[1])
        var_level_list[[c]] = levels(x_[,c]);
        x_[,c] <- as.vector(x_[,c])
    }


    cmd <- paste("x2_ <- within(x_,  combined <- paste(",
                 paste(vars_to_interact, collapse=", "),
                 ", sep='_x_'))", sep="");
    eval(parse(text=cmd));
    base_level <- paste(base_levels, collapse="_x_")
    x2_[,"combined"] <- factor(x2_[,"combined"], levels=unique(c(base_level, unique(x2_[,"combined"]))));
    x3_ = as.data.frame(model.matrix(~0+., data=data.frame(zzz = x2_[,"combined"])));
    colnames(x3_) <- sapply(tolower(colnames(x3_)), FUN=function(x)paste("interaciton_", gsub("zzz","",x), sep=""));
    return(x3_)
    gc()
}


## test ##
if (FALSE){
    insure = data.frame(exposure=c(500,1200,100,400,500,300),
                        claim_count=c(42,37,1,101,73,14),
                        car_size=c("small","medium","large","small","medium","large"),
                        age=c(1,1,1,2,2,2));

    data=insure
    col = "car_size"
    factor_base = "medium"
    data2 = changeFactorBaseLevel(data, col, factor_base)
}

##### Test ######
if (FALSE){
    data = data.frame(exposure=c(500,1200,100,400,500,300),
                      claim_count=c(42,37,1,101,73,14),
                      car_size=c("small","medium","large","small","medium","large"),
                      age=c(1,1,1,2,2,2));

    predictors <- c("exposure", "car_size", "age");
    target <- "claim_count";
    modelDataMatrix = convertDataFrameToModelMatrix(data, predictors, target);
    x_matrix = modelDataMatrix[[1]];
    y_matrix = modelDataMatrix[[2]];
}

###### Test Generalized Linear Mixed Model ##########
if (FALSE){
    insure = data.frame(exposure=c(500,1200,100,400,500,300),
                  claim_count=c(42,37,1,101,73,14),
                  car_size=c("small","medium","large","small","medium","large"),
                  age=c(1,1,1,2,2,2));

    insure$freq = insure$claim_count / insure$exposure;
    #insure$age = factor(insure$age)
    insure$logexp = log(insure$exposure);

    glm_freq_with_weight <- glm(freq ~ car_size + age, family = poisson(), data=insure, weights=exposure);
    summary(glm_freq_with_weight)

    # Call:
    #     glm(formula = freq ~ car_size + age, family = poisson(), data = insure,
    #         weights = exposure)
    #
    # Deviance Residuals:
    #     1         2         3         4         5         6
    # 1.00847  -0.93383  -0.21139  -0.60484   0.71931   0.06088
    #
    # Coefficients:
    #     Estimate Std. Error z value Pr(>|z|)
    # (Intercept)     -5.7209     0.3669 -15.592  < 2e-16 ***
    #     car_sizemedium   1.0715     0.2784   3.848 0.000119 ***
    #     car_sizesmall    1.7643     0.2724   6.478 9.32e-11 ***
    #     age              1.3199     0.1359   9.713  < 2e-16 ***
    #     ---
    #     Signif. codes:  0 ‘***’ 0.001 ‘**’ 0.01 ‘*’ 0.05 ‘.’ 0.1 ‘ ’ 1
    #
    # (Dispersion parameter for poisson family taken to be 1)
    #
    # Null deviance: 175.1536  on 5  degrees of freedom
    # Residual deviance:   2.8207  on 2  degrees of freedom
    # AIC: Inf
    #
    # Number of Fisher Scoring iterations: 6

    ###########

    library(lme4)

    m1 <- glmer(freq ~ age + (1 | car_size), family = poisson(), data = insure, weights=exposure);
    summary(m1)
    #
    # attr(,"class")
    # [1] "coef.mer"
    # > suppressWarnings(warning("testit"))
    # > summary(m1)
    # Generalized linear mixed model fit by maximum likelihood (Laplace Approximation) ['glmerMod']
    # Family: poisson  ( log )
    # Formula: freq ~ age + (1 | car_size)
    # Data: insure
    # Weights: exposure
    #
    # AIC      BIC   logLik deviance df.resid
    # Inf      Inf     -Inf      Inf        3
    #
    # Scaled residuals:
    #     Min      1Q  Median      3Q     Max
    # -0.9169 -0.4678 -0.2116  0.5221  1.0576
    #
    # Random effects:
    #     Groups   Name        Variance Std.Dev.
    # car_size (Intercept) 1        1
    # Number of obs: 6, groups:  car_size, 3
    #
    # Fixed effects:
    #     Estimate Std. Error z value Pr(>|z|)
    # (Intercept)  -4.7529     0.6315  -7.526 5.23e-14 ***
    #     age           1.3168     0.1359   9.690  < 2e-16 ***
    #     ---
    #     Signif. codes:  0 ‘***’ 0.001 ‘**’ 0.01 ‘*’ 0.05 ‘.’ 0.1 ‘ ’ 1
    #
    # Correlation of Fixed Effects:
    #     (Intr)
    # age -0.378
    # convergence code: 0
    #
    # > coef(m1)
    # $car_size
    # (Intercept)      age
    # large    -5.656472 1.316837
    # medium   -4.645398 1.316837
    # small    -3.956790 1.316837
    #
    # attr(,"class")
    # [1] "coef.mer"

    coef(m1)
}
