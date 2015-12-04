Fun_DataSelect <- function(data=list(),YearRange=NULL, ErrorChangeThrhld=NULL,TempSearchTable) {
  ## ErrorChangeThrhld defines the threshold of error change from latest year's prediction
  ##       for making cut of data used in model building
  ## Data Fields are YearMonth, Model_ID, Year, Month, Days, Temp_perday, Vol_perday, Wgt
  ## YearRange defines how far back we look at data for modeling
		
		LinearSearch_Table <- Fun_BoostHDDCDD_Model(data=data,YearRange=1,TempSearchTable=TempSearchTable);
        
		data$HDD <- LinearSearch_Table$BalanceHDDTemp - data$Temp_perday;
		data$HDD <- round(data$HDD,8);
		data$HDD <- (data$HDD > 0) * data$HDD;
		data$HDD_2 <- data$HDD ^ 2;
		data$CDD <- data$Temp_perday - LinearSearch_Table$BalanceCDDTemp;
		data$CDD <- round(data$CDD,8);
		data$CDD <- (data$CDD > 0) * data$CDD;
		data$CDD_2 <- data$CDD ^2;
		data$One <- 1;
		Coef <- LinearSearch_Table[,c("Intercept_Coef", "HDD_Coef", "HDD2_Coef", "CDD_Coef", "CDD2_Coef")];
		data$Pred_Linear <- as.matrix(data[,c("One","HDD","HDD_2","CDD","CDD_2")]) %*% t(Coef);
		data$Error <- data$Pred_Linear - data$Vol_perday;
		
		if (is.null(YearRange)) {YearRange =1};
		data_1Yr <- data[data$YearMonth > max(data$YearMonth) - YearRange,];
		Error_Perc_1Yr <- sum(abs(data_1Yr$Error) * data_1Yr$Days) / sum(abs(data_1Yr$Vol_perday) * data_1Yr$Days);
		
		data_Reverse <- data[,c("YearMonth","Days","Vol_perday","Error")];
		attach(data_Reverse);
		data_Reverse <- data_Reverse[order(-YearMonth),];
		statpoint <- sum(data_Reverse$YearMonth > max(data_Reverse$YearMonth) -YearRange);
		if (statpoint+1 > nrow(data_Reverse)) {SearchSeq <- c()} else {
				SearchSeq <- seq(statpoint+1,nrow(data_Reverse),by=1)};
		detach(data_Reverse);
		
		MyLastYearMonth <- min(data_1Yr$YearMonth);
		if (!is.null(SearchSeq)) {
			ListOfError <- lapply(SearchSeq,FUN=Fun_CalError,data=data_Reverse,YearRange=YearRange);
			VarList <- names(ListOfError[[1]]);
			ListOfError <- matrix(unlist(ListOfError), ncol = length(names(ListOfError[[1]])), byrow = TRUE);
			ListOfError <- as.data.frame(ListOfError);
			names(ListOfError) <- VarList;
		
			if (is.null(ErrorChangeThrhld)) {ErrorChangeThrhld = 0.2};
			ErrorUpperBound <- (1 + ErrorChangeThrhld) * Error_Perc_1Yr;
			ListOfLastYYMON <- ListOfError[ListOfError$Error_Perc <= ErrorUpperBound,]$LastYearMonth;
			if (length(ListOfLastYYMON) > 0) {MyLastYearMonth <- min(ListOfLastYYMON)};
		}
		
        return(MyLastYearMonth)
}