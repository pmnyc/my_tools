Fun_CalError <- function(data=list(),j,YearRange){
		data_temp <- data[1:j,];
		data_temp <- data_temp[data_temp$YearMonth < min(data_temp$YearMonth) + YearRange,];
		Error_Perc <- sum(abs(data_temp$Error) * data_temp$Days) / sum((abs(data_temp$Vol_perday) + 1e-8) * data_temp$Days);
		List <- data.frame(LastYearMonth=min(data_temp$YearMonth),Error_Perc=Error_Perc);
		return(List)
		}