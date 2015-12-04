rm(list=ls());

library(RODBC, quietly=TRUE)
library(forecast, quietly=TRUE)
library(glmnet, quietly=TRUE)
library(quantmod, quietly=TRUE)
library(stringr, quietly=TRUE)
library(parallel, quietly=TRUE)
library(doSNOW, quietly=TRUE)
library(foreach, quietly=TRUE)
library(MASS, quietly=TRUE)
library(fields, quietly=TRUE)

NumPartions <- 100;  ##This splits all data into certain num of partitions

Main_Directory <- "C:/Documents and Settings/myproject";
setwd(Main_Directory);
TypeofModel <- "UNY_Resi_Heat";
output_folder <- paste("/",TypeofModel,"_Model_Output",sep="");
log_folder <- paste("/",TypeofModel,"_Model_Log",sep="");
dir.create(file.path(Main_Directory,output_folder), showWarnings = TRUE);
dir.create(file.path(Main_Directory,log_folder), showWarnings = TRUE);
output_dir <- paste(Main_Directory,output_folder,sep="");
log_dir <- paste(Main_Directory,log_folder,sep="");

perct_cores_touse <- 1; ##This is specify the % of cores used for parallel
                           ##computation
n.cores = ceiling( perct_cores_touse * as.numeric(detectCores(logical = TRUE)));

myconn <- odbcConnect("GasGrowth", uid="pengma", pwd="");

#UseCDD_Ind <- "Y"; ##This is to specify if we use CDD to model gas usage

#tablename <- "[temp].[kevin_ZZZZZ]";
tablename <- "[temp].[Individual_Model_Data_UNY_HEAT]";
#tablename <- "[temp].[unyheat_ZZZZZ]";

state <- "NY";

#CateGorytoSelect <- "Rate_Category in ('Residential Heating','Commercial Heating')";
CateGorytoSelect <- "RESI_FLAG = 1";

###### The codes above are for tuning parameters ######
SQL_Cmd <- paste0("SELECT [Model_ID] FROM ",tablename,
                  " where State = '",state,"' and ", CateGorytoSelect,"
                   group by [Model_ID]
                   order by [Model_ID]");
Data_Model_ID <- sqlQuery(myconn,SQL_Cmd);
IDList <- unique(sort(as.numeric(Data_Model_ID$Model_ID)));
close(myconn);
rm(myconn,Data_Model_ID);
setwd(log_dir);
save(IDList,file="List Of ModelIDs.RData");
setwd(Main_Directory);

ModelTable_List <- list();
NumRecs <- ceiling(length(IDList) / (NumPartions + 0.00));
NumPartions <- ceiling(length(IDList)/ NumRecs);

for (ii in seq(1,NumPartions,by=1)) {
     myconn <- odbcConnect("GasGrowth", uid="pengma", pwd="");
     ID_Subset <- IDList[min(length(IDList),NumRecs*ii-(NumRecs-1)):min(length(IDList),NumRecs*ii)];
     
     SQL_Command <- paste0("SELECT [Model_ID], year(Bill_Date_from) Year
                      ,month(Bill_Date_from) Month , sum([Days]) Days
                      ,sum([TEMP])/sum(Days+0.0) as Temp_perday , sum(Vol)/sum(Days + 0.0) as Vol_perday
                      FROM ", tablename, " where state= '",state,"' and ",CateGorytoSelect," 
                              and [Model_ID] between ",min(ID_Subset)," and ",max(ID_Subset),"
                      group by [Model_ID], year(Bill_Date_from)
                      ,month(Bill_Date_from)
                      order by [Model_ID], year(Bill_Date_from), month(Bill_Date_from)");
     Data_Raw <- sqlQuery(myconn, SQL_Command, as.is = TRUE);
     close(myconn);
     if (ii == 1) {starttime <- Sys.time()};
     source("Individual Model.R",chdir = TRUE);
     iicharlengthnchar <- nchar(as.character(NumPartions));
     ii_char <- paste(paste(rep(0,iicharlengthnchar-nchar(as.character(ii))),sep="",collapse=""),ii,sep="");
     if (ii == 1){LogLine = ""};
     LogLine_new <- paste("Iteration ",ii_char," for Model_ID between ",min(ID_Subset)," and ",max(ID_Subset)," is done;\n",sep="");
     LogLine <- paste(LogLine,LogLine_new,timelogline,sep="");
     fileConn<-file(paste(log_dir,"/log.txt",sep=""));
     writeLines(LogLine, fileConn,sep="\n");
     close(fileConn);
}

runtime <- Sys.time() - starttime;
timelogline <- paste("It took ",round(runtime,3)," ",attributes(runtime)["units"]," in total to run",sep="");
fileConn<-file(paste(log_dir,"/timelog.txt",sep=""));
writeLines(timelogline, fileConn,sep="\n");
close(fileConn);

#### The following is to load all individual model files into one file

if (exists("Model_Table")){rm(Model_Table)};
if (exists("FinalTable")){rm(FinalTable)};
FinalTable <- data.frame();
setwd(output_dir);

for (i in seq(1,NumPartions,by=1)) {
  load(paste("Model_OutputTable_",i,".RData",sep=""));
  FinalTable <- rbind(FinalTable,Model_Table);
  rm(Model_Table);
}
Model_Table <- FinalTable;
rm(FinalTable);
save(Model_Table,file="Model_OutputTable_Final.RData");
setwd(Main_Directory);
############ The following is Window Script for
############ running R codes by window task scheduler
##Just create a .bat file including the following codes
#@echo off
#"C:\Program Files\R\R-3.0.2\bin\R.exe" CMD BATCH --vanilla --slave "C:\Documents and Settings\pengma\Desktop\Gas Individual Model\Call_IndividualModel_UNY_ResdHeat.R"