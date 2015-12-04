Fun_BoostHDDCDD_Model <- function(data=list(),YearRange=NULL, TempSearchTable) {
		if (is.null(YearRange)) {YearRange = 10};
		steps = 1;
		##Boost speed for finding optimal HDD cutoff point
		max_cdd_temp <- max(TempSearchTable$TempCDDSearchRange);
		sequence_hdd_1 <- seq(min(TempSearchTable$TempHDDSearchRange),max(TempSearchTable$TempHDDSearchRange),by=steps);
		Temp_Table_1 <- TempSearchTable[TempSearchTable$TempCDDSearchRange == max_cdd_temp,];
		temptble <- Temp_Table_1;
		Temp_Table_1 <- Temp_Table_1[1:length(sequence_hdd_1),];
		Temp_Table_1$TempHDDSearchRange <- sequence_hdd_1;
		Temp_Table_1 <- as.list(as.data.frame(t(Temp_Table_1)));
		
		data <- data[data$YearMonth > max(data$YearMonth) - YearRange,];
		ModelTable_1 <- lapply(Temp_Table_1,FUN=Fun_LinearModel,data=data);
    
    	Varname <- names(ModelTable_1[[1]]);
		ModelTable_1 <- matrix(unlist(ModelTable_1), ncol = length(names(ModelTable_1[[1]])), byrow = TRUE);
		ModelTable_1 <- as.data.frame(ModelTable_1);
		names(ModelTable_1) <- Varname;
	
		SearchGrid <- unique(TempSearchTable$TempHDDSearchRange);
		SearchGrid  <- sort(SearchGrid );
		PolyInter <- fields::splint(ModelTable_1$BalanceHDDTemp,ModelTable_1$R_Sqr,xgrid=SearchGrid);
		idx <- which(PolyInter == max(PolyInter))[1];
		balanceHDD_cutoff <- SearchGrid[idx];
    
		##Boost speed for finding optimal CDD cutoff point
		Temp_Table_1 <- TempSearchTable[TempSearchTable$TempHDDSearchRange == balanceHDD_cutoff,];
		
		sequence_cdd_1 <- seq(min(Temp_Table_1$TempCDDSearchRange),max(Temp_Table_1$TempCDDSearchRange),by=steps);
		temptble <- Temp_Table_1;
		Temp_Table_1 <- Temp_Table_1[1:length(sequence_cdd_1),];
		Temp_Table_1$TempCDDSearchRange <- sequence_cdd_1;
		Temp_Table_1 <- as.list(as.data.frame(t(Temp_Table_1)));
		ModelTable_1 <- lapply(Temp_Table_1,FUN=Fun_LinearModel,data=data);
		Varname <- names(ModelTable_1[[1]]);
		ModelTable_1 <- matrix(unlist(ModelTable_1), ncol = length(names(ModelTable_1[[1]])), byrow = TRUE);
		ModelTable_1 <- as.data.frame(ModelTable_1);
		names(ModelTable_1) <- Varname;
		SearchGrid <- unique(TempSearchTable$TempCDDSearchRange);
		SearchGrid  <- sort(SearchGrid[SearchGrid >= balanceHDD_cutoff]);
		PolyInter <- fields::splint(ModelTable_1$BalanceCDDTemp,ModelTable_1$R_Sqr,xgrid=SearchGrid);
		idx <- which(PolyInter == max(PolyInter))[1];
		balanceCDD_cutoff <- SearchGrid[idx];
    
    TempSearch = TempSearchTable[TempSearchTable$TempHDDSearchRange == balanceHDD_cutoff,];
		TempSearch = TempSearch[TempSearch$TempCDDSearchRange == balanceCDD_cutoff,];
		ModelTable_2 <- Fun_HDDCDD_Model(data=data,YearRange=YearRange,TempSearchTable=TempSearch);
		
		return(ModelTable_2)
}