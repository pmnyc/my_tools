Fun_HDDCDD_Model <- function(data=list(),YearRange=NULL, TempSearchTable) {
  ## ErrorChangeThrhld defines the threshold of error change from latest year's prediction
  ##       for making cut of data used in model building
  ## Data Fields are YearMonth, Model_ID, Year, Month, Days, Temp_perday, Vol_perday, Wgt
  ## YearRange defines how far back we look at data for modelling
		##First, make sure all fields in data are numeric
		data$YearMonth <- as.numeric(data$YearMonth) ;
		data$Model_ID <- as.numeric(data$Model_ID) ;
		data$Year <- as.numeric(data$Year) ;
		data$Month <- as.numeric(data$Month) ;
		data$Days <- as.numeric(data$Days) ;
		data$Temp_perday <- as.numeric(data$Temp_perday) ;
		data$Vol_perday <- as.numeric(data$Vol_perday) ;
		data$Wgt <- as.numeric(data$Wgt) ;

        if (is.null(YearRange)) {YearRange = 10};
		data_GoBackYr <- data[data$YearMonth > max(data$YearMonth) - YearRange,];
		TempSearchRange <- TempSearchTable;
        TempSearchRange <- as.list(as.data.frame(t(TempSearchRange)));
        names(TempSearchRange) <- NULL;
		LinearSearch_List <- lapply(TempSearchRange, FUN=Fun_FindBalanceTemp, data=data_GoBackYr);
		LinearSearch_Table <- matrix(unlist(LinearSearch_List), ncol = length(names(LinearSearch_List[[1]])), byrow = TRUE);
		LinearSearch_Table <- as.data.frame(LinearSearch_Table);
		VarList <- names(LinearSearch_List[[1]]);
		names(LinearSearch_Table) <- VarList;
		
		LinearSearch_Table$Model_ID <- data_GoBackYr$Model_ID[1];
		LinearSearch_Table <- LinearSearch_Table[,c("Model_ID",VarList)];
		LinearSearch_Table <- LinearSearch_Table[LinearSearch_Table$R_Sqr == max(LinearSearch_Table$R_Sqr),];
		LinearSearch_Table <- LinearSearch_Table[1,];
		
	   LinearSearch_Table$UseHDD_Ind <- "Y";
		if (abs(LinearSearch_Table$HDD_Coef) + abs(LinearSearch_Table$HDD2_Coef) < 1e-8) {LinearSearch_Table$UseHDD_Ind = "N"};
		LinearSearch_Table$UseCDD_Ind <- UseCDD_Ind;
		if (abs(LinearSearch_Table$CDD_Coef) + abs(LinearSearch_Table$CDD2_Coef) < 1e-8) {LinearSearch_Table$UseCDD_Ind = "N"};
		         
		return(LinearSearch_Table)
}