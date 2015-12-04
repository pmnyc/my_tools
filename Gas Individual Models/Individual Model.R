library(RODBC)
library(forecast)
library(glmnet)
library(quantmod)
library(stringr)
library(parallel)
library(doSNOW)
library(foreach)
library(MASS)
library(fields)

source("Fun_DataSelection.R",chdir = TRUE);
source("Fun_HDDCDD_Model.R",chdir = TRUE);
source("Fun_BoostHDDCDD_Model.R",chdir = TRUE);
source("Fun_FindBalanceTemp.R",chdir = TRUE);
source("Fun_LinearModel.R",chdir = TRUE);
source("Fun_CalError.R",chdir = TRUE);
source("Fun_StepAIC.R",chdir = TRUE);
source("Fun_ElasticNet_Model.R",chdir = TRUE)

TempHDDSearchRange <- seq(50,76,by=0.1); ##This is to define the range of cutoff 
                                      ##temperature to derive each ModelID's HDD

TempCDDSearchRange <- seq(60,86,by=0.1); ##This is to define the range of cutoff 
                                      ##temperature to derive each ModelID's DDD
if (!exists("UseCDD_Ind")) {UseCDD_Ind = "N"}; ##This is to default no Gas for Cooling
											  ##if this indicator was not specified
if (UseCDD_Ind != "Y") {TempCDDSearchRange <- max(TempCDDSearchRange)};

TempSearchTable <- merge(as.data.frame(TempHDDSearchRange),as.data.frame(TempCDDSearchRange));
TempSearchTable$TempHDDSearchRange <- as.numeric(TempSearchTable$TempHDDSearchRange);
TempSearchTable$TempCDDSearchRange <- as.numeric(TempSearchTable$TempCDDSearchRange);
TempSearchTable <- TempSearchTable[TempSearchTable$TempHDDSearchRange <= TempSearchTable$TempCDDSearchRange,];

WgtIncrease_byMonth <- 1.01;
TimeSeries_Window <- 10; ##This is to specify the number of years of data used
                        ##for each individual model
Error_Cal_Window <- 3; ##This is to specify the number of years used for calculating error %
MinDataCount <- 10 ; ##This is to set the minimum number of data records for running any model
ErrorChangeThrhld = 0.1; ##This is to set the error change threshold for finding data that do not
                         ##fall out of pattern

ModelID_Seq <- unique(Data_Raw$Model_ID);

####################### Codes Above are for Specifying Model Features, Below are
####################### more generic codes for realizing the individual models
### This is part of Fun_IndividualModel for searching best Balance Temperature point

Fun_IndiVModel <- function(id) {  
  #### Below is generic code for extracting the balance temperature point and their corresponding coefficients ####
        data_2 <- Data_Raw[Data_Raw$Model_ID == id,];
        LinearSearch_Table <- data.frame();
		Model_Coef_Table <- data.frame();
		fileConn2 <- file(paste(log_dir,"/Current_Model_log.txt",sep=""));
        writeLines(paste("Running Model ID ",id," ...",sep=""), fileConn2,sep="\n");
        close(fileConn2);
		
		data_2$YearMonth <- round(as.numeric(data_2$Year)+(as.numeric(data_2$Month)-1)/12,3);
		One_Year_Data <- data_2[data_2$YearMonth > max(data_2$YearMonth)-1,];
		
        if (nrow(One_Year_Data) >= MinDataCount) {
          data_2$YearMonth <- round(as.numeric(data_2$Year)+(as.numeric(data_2$Month)-1)/12,3);
          data_2 <- data_2[data_2$YearMonth > max(data_2$YearMonth) - TimeSeries_Window -0.05,]  
          YearMonth_Wgt <- data.frame(matrix(data=NA,nrow=length(unique(data_2$YearMonth)),ncol=0));
          YearMonth_Wgt$YearMonth <- unique(data_2$YearMonth);
          YearMonth_Wgt$Wgt <- WgtIncrease_byMonth ^ (12* (unique(YearMonth_Wgt$YearMonth) - min(unique(YearMonth_Wgt$YearMonth))));
          data_2 <- merge(data_2,YearMonth_Wgt,by="YearMonth");
          data_2$Wgt <- data_2$Wgt * data_2$Days;
		 
			data_2$YearMonth <- as.numeric(data_2$YearMonth) ;
			data_2$Model_ID <- as.numeric(data_2$Model_ID) ;
			data_2$Year <- as.numeric(data_2$Year) ;
			data_2$Month <- as.numeric(data_2$Month) ;
			data_2$Days <- as.numeric(data_2$Days) ;
			data_2$Temp_perday <- as.numeric(data_2$Temp_perday) ;
			data_2$Vol_perday <- as.numeric(data_2$Vol_perday) + 1e-7 ; ##This is to prevent having all 0 volumes
																##in modeling and 0 denominator in calculations
			data_2$Wgt <- as.numeric(data_2$Wgt) ;
		 
		 ## ErrorChangeThrhld = 0.3 means if error percentage is over 30% of error percentage by recent
		 ## year's model, then we drop the part of data. This is to ensure only selecting data
		 ## where the pattern is similar to most recent year's
		 MinYearMonth <- Fun_DataSelect(data=data_2,YearRange=1,ErrorChangeThrhld=ErrorChangeThrhld,TempSearchTable=TempSearchTable);
		 data_2 <- data_2[data_2$YearMonth >= MinYearMonth,];
		 LinearSearch_Table <- Fun_BoostHDDCDD_Model(data=data_2,YearRange=TimeSeries_Window,TempSearchTable=TempSearchTable);
		 
		 data_2$HDD <- LinearSearch_Table$BalanceHDDTemp - as.numeric(data_2$Temp_perday);
          data_2$HDD <- round(data_2$HDD,8) * (data_2$HDD > 0);
          data_2$CDD <- as.numeric(data_2$Temp_perday) - LinearSearch_Table$BalanceCDDTemp;
          data_2$CDD <- round(data_2$CDD,8) * (data_2$CDD > 0);
          data_2$HDD_2 <- data_2$HDD ^ 2;
          data_2$CDD_2 <- data_2$CDD ^ 2;
		 data_2$One <- 1;
		 Coef <- LinearSearch_Table[,c("Intercept_Coef", "HDD_Coef", "HDD2_Coef", "CDD_Coef", "CDD2_Coef")];
		 data_2$Pred_Linear <- as.matrix(data_2[,c("One","HDD","HDD_2","CDD","CDD_2")]) %*% t(Coef);
		 
          data_2$Error_Linear <- data_2$Vol_perday - data_2$Pred_Linear + rnorm(nrow(data_2))*(1e-7);
									##This is to prevent a so-called perfect data causing glmnet to crash;
                  ##We use actual - pred so that final prediction is sum of predictions
                  ##in those two stages
          data_2_window <- data_2[max(1,nrow(data_2)-12*Error_Cal_Window+1):nrow(data_2),];
          #Boxtest <- Box.test(data_2$Error_Linear[max(1,nrow(data_2)-48):nrow(data_2)],type = c("Box-Pierce", "Ljung-Box"),lag=log(nrow(data_2[max(1,nrow(data_2)-48):nrow(data_2),])), fitdf=0);
          #if (is.na(Boxtest$p.value)) {BoxLjungTest.pvalue <- 1} else {BoxLjungTest.pvalue <- Boxtest$p.value};
          #LinearSearch_Table$BoxLjungTest.pvalue <- round(BoxLjungTest.pvalue,2);
          
          ########## The following is to account for time trend ###########
         
		## Create extra variables for 2nd stage of elastic net model
		data_2$T = (data_2$Month - rep(1,nrow(data_2)))/12;
		data_2$T_2 <- data_2$T ^2;
		data_2$T_3 <- data_2$T ^3;
		data_2$Sin_2piT <- sin(2*pi*data_2$T);
		data_2$Cos_2piT <- cos(2*pi*data_2$T);
		data_2$CurrMonth_TempPred <- data_2$Pred_Linear;
		data_2$LastMonth_TempPred <- Lag(data_2$Pred_Linear,1);
			data_2$LastMonth_TempPred[1] <- data_2$CurrMonth_TempPred[1];
			data_2 <- data_2[-1,];
		data_2$Cur_TempPred_X_Sin_2piT <- data_2$CurrMonth_TempPred * data_2$Sin_2piT;
		data_2$Cur_TempPred_X_Cos_2piT <- data_2$CurrMonth_TempPred * data_2$Cos_2piT;
		data_2$Last_TempPred_X_Sin_2piT <- data_2$LastMonth_TempPred * data_2$Sin_2piT;
		data_2$Last_TempPred_X_Cos_2piT <- data_2$LastMonth_TempPred * data_2$Cos_2piT;
		data_2$CurrMonth_TempPred_X_T <- data_2$CurrMonth_TempPred * data_2$T ; 
		data_2$CurrMonth_TempPred_X_T_2 <- data_2$CurrMonth_TempPred * data_2$T_2 ; 
		data_2$CurrMonth_TempPred_X_T_3 <- data_2$CurrMonth_TempPred * data_2$T_3 ; 
		data_2$LastMonth_TempPred_X_T <- data_2$LastMonth_TempPred * data_2$T ; 
		data_2$LastMonth_TempPred_X_T_2 <- data_2$LastMonth_TempPred * data_2$T_2 ; 
		data_2$LastMonth_TempPred_X_T_3 <- data_2$LastMonth_TempPred * data_2$T_3 ; 
		
		Var_Include_2ndModel <- c("T","T_2","T_3","Sin_2piT","Cos_2piT","CurrMonth_TempPred","LastMonth_TempPred",
									"Cur_TempPred_X_Sin_2piT","Cur_TempPred_X_Cos_2piT",
									"Last_TempPred_X_Sin_2piT","Last_TempPred_X_Cos_2piT",
									"CurrMonth_TempPred_X_T", "CurrMonth_TempPred_X_T_2", "CurrMonth_TempPred_X_T_3",
									"LastMonth_TempPred_X_T", "LastMonth_TempPred_X_T_2", "LastMonth_TempPred_X_T_3");
						## Use Elastic Net for regularization
		ElasNet.Coef <- Fun_ElasticNet_Model(data=data_2,x=Var_Include_2ndModel,y="Error_Linear",wgt="Wgt",alpha=0.05,family="gaussian");
		ElasNet.Coef <- as.data.frame(as.matrix(t(ElasNet.Coef)));
		names(ElasNet.Coef) <- paste("Coef_",names(ElasNet.Coef),sep="");
		names(ElasNet.Coef)[1] <- "Coef_Intercept_ElasNet";
		
		## Calculate Error for combing two stages of models
		data_2_window <- data_2[data_2$YearMonth >= min(data_2_window$YearMonth),];
		
		Error_Perct_1 <- paste0(round(100 * sum(abs(data_2_window$Error_Linear)*data_2_window$Days)/sum(as.numeric(data_2_window$Vol_perday)*data_2_window$Days),1),"%");
        LinearSearch_Table$Error_Perct_1 <- Error_Perct_1;
		
		data_2_window$ONE <- 1;
		
		matrix_2_window <- as.matrix(data_2_window[,c("ONE",Var_Include_2ndModel)]);
		
		data_2_window$Pred_2 <- matrix_2_window %*% t(as.matrix(ElasNet.Coef));
		
		data_2_window$Final_Pred <- data_2_window$Pred_Linear + data_2_window$Pred_2;
		data_2_window$Final_Error <- data_2_window$Vol_perday - data_2_window$Final_Pred;
		
		## If the second stage of modeling provides worse error rate, then do not use 
				## the results from this stage
		Err1 <- data_2_window$Error_Linear;
				Err2 <- data_2_window$Final_Error;
				Myvol <- data_2_window$Vol_perday;
				Mywgt <- data_2_window$Days;
		if (sum(abs(Err1) * Mywgt)/sum(Mywgt) < sum(abs(Err2) * Mywgt)/sum(Mywgt)) {ElasNet.Coef[,] <- 0};
		
		Model_Coef_Table <- cbind(LinearSearch_Table,data.frame(T_Def = "(BilLStartMonth - 1)/12"),ElasNet.Coef);
		Final_Error_Perct <- paste0(round(100 * sum(abs(data_2_window$Final_Error) * data_2_window$Days)/sum(data_2_window$Vol_perday * data_2_window$Days),1),"%");
		Model_Coef_Table$Final_Error_Perct <- Final_Error_Perct;
		
		######################## Rename fields in the final table ################
		
		Model_Coef_Table <- Model_Coef_Table[,c("Model_ID", "UseHDD_Ind", "UseCDD_Ind", "T_Def", "BalanceHDDTemp", 
							"BalanceCDDTemp", "Intercept_Coef", "HDD_Coef", "HDD2_Coef", "CDD_Coef", "CDD2_Coef", 
							"Coef_Intercept_ElasNet", "Coef_T", "Coef_T_2", "Coef_T_3", "Coef_Sin_2piT", 
							"Coef_Cos_2piT", "Coef_CurrMonth_TempPred", "Coef_LastMonth_TempPred", 
							"Coef_Cur_TempPred_X_Sin_2piT", "Coef_Cur_TempPred_X_Cos_2piT", 
							"Coef_Last_TempPred_X_Sin_2piT", "Coef_Last_TempPred_X_Cos_2piT", 
							"Coef_CurrMonth_TempPred_X_T", "Coef_CurrMonth_TempPred_X_T_2", 
							"Coef_CurrMonth_TempPred_X_T_3", "Coef_LastMonth_TempPred_X_T", 
							"Coef_LastMonth_TempPred_X_T_2", "Coef_LastMonth_TempPred_X_T_3", "R_Sqr", 
							"Error_Perct_1", "Final_Error_Perct")];

		FUN_SwapWords <- function(char,x){
				##This function is to swap characters for manipulating the variable names
				## for example, change HDD_Coef to Coef_HDD, where x="_Coef", char="HDD_Coef"
				## This function uses library stringr
				loc <- unlist(str_locate_all(pattern =x,char))[1];
				if (is.na(loc)) {return(char)} else {
					secondpart <- substring(char,1,loc-1);
					firstpart <- gsub("_","",x);
					return(paste(firstpart,"_",secondpart,sep=""))}
		}
		
		names <- names(Model_Coef_Table);
		newnames <- unlist(sapply(names,FUN_SwapWords,x="_Coef"));
		names(newnames) <- NULL;
		names(Model_Coef_Table) <- newnames;
	}
  return(Model_Coef_Table);
}

##cl <- makeForkCluster(n.cores);
cl<-makeCluster(n.cores)
registerDoSNOW(cl)

start <- Sys.time();

Model_Table <- foreach (i=1:length(ModelID_Seq), .combine=rbind) %dopar%
{          library(forecast)
           library(glmnet)
           library(quantmod)
           library(stringr)
           library(MASS)
           id <- ModelID_Seq[i];
           LinearSearch_Test <- try(Fun_IndiVModel(id));
		  if (class(LinearSearch_Test) == "try-error") {
				stop(paste("Model ID",id,"goes wrong...",sep=" "))} ;
		  LinearSearch_Table <- LinearSearch_Test;
		  };

timeeplase <- Sys.time() - start;
stopCluster(cl)

timelogline <- paste("It took ",round(timeeplase,3)," ",attributes(timeeplase)["units"]," run this partition;\n",sep="");

setwd(output_dir);
save(Model_Table,file=paste0("Model_OutputTable_",ii,".RData"));
setwd(Main_Directory);
rm(Data_Raw);
##rm(TempSearchTable);