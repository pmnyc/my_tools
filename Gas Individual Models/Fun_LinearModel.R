Fun_LinearModel <- function (data=list(),ListOfTemp){  
  balance_HDDtemp = ListOfTemp[1];
  balance_CDDtemp = ListOfTemp[2];
  Wgt <- data$Wgt;
  HDD <- rep(balance_HDDtemp,each=nrow(data)) - data$Temp_perday;
  HDD <- round(HDD,8) * (HDD > 0);
  CDD <- data$Temp_perday - rep(balance_CDDtemp,each=nrow(data));
  CDD <- round(CDD,8) * (CDD > 0);
  HDD_2 <- HDD ^ 2;  CDD_2 <- CDD ^ 2; 
  Vol <- data$Vol_perday;
  #mydata <- data.frame(Vol, HDD, HDD_2, CDD, CDD_2, Wgt);
  
  if (UseCDD_Ind == "Y") {lmd <- lm(Vol ~ HDD + HDD_2 + CDD+ CDD_2, weights = Wgt)} else {
    lmd <- lm(Vol ~ HDD + HDD_2, weights = Wgt)};
  
  #mydata$pred <- predict(lmd,mydata);
  #R_Sqr = 1- sum(abs(mydata$Vol - mydata$pred) * mydata$Wgt)/sum(mydata$Vol * mydata$Wgt);
  R_Sqr = -1 * AIC(lmd);
         ##This is not R-square. I just use it because this term is used in
         ##other funciton files
  #R_Sqr <- summary(lmd)$r.squared;
  #if (is.na(R_Sqr) | is.null(R_Sqr)) {R_Sqr = 0};
  if (is.na(R_Sqr) | is.null(R_Sqr)) {R_Sqr = 1e7};
  result <- list(BalanceHDDTemp = balance_HDDtemp, 
                 BalanceCDDTemp = balance_CDDtemp,
                 R_Sqr = R_Sqr);
  return(result)
}