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
distinct_data <- function(data, distinct_by_col,
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
        dftype = "dat.table"
    } else if ("data.frame" %in% class(data)) {
        dftype = "data.frame"
    } else {stop("The data must be either data frame or data table!")}

    if (!(unique_by_op %in% c("min", "max"))) stop("unique_by_op must be one of min, max!")

    if (dftype == "data.frame") data <- data.table::data.table(data)

    cmd <- paste("dt1 <- data[ , .SD[which.", unique_by_op,
                 "(", unique_col, ")], by = c('",
                 paste(distinct_by_col, collapse="' , '"),
                 "')]", sep ="")
    eval(parse(text = cmd))

    if (is.na(cols_to_sum)) cols_to_sum <- ""
    if (is.na(cols_to_min)) cols_to_min <- ""
    if (is.na(cols_to_max)) cols_to_max <- ""
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

