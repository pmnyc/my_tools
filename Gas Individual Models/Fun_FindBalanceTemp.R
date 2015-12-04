Fun_FindBalanceTemp <- function (data=list(),ListOfTemp){  
  balance_HDDtemp = ListOfTemp[1];
  balance_CDDtemp = ListOfTemp[2];
  Wgt <- data$Wgt;
  HDD <- rep(balance_HDDtemp,each=nrow(data)) - as.numeric(data$Temp_perday);
  HDD <- round(HDD,8) * (HDD > 0);
  CDD <- as.numeric(data$Temp_perday) - rep(balance_CDDtemp,each=nrow(data));
  CDD <- round(CDD,8) * (CDD > 0);
  HDD_2 <- HDD ^ 2;  CDD_2 <- CDD ^ 2; 
  Vol <- as.numeric(data$Vol_perday);
  
  mydata <- data.frame(HDD=HDD,HDD_2=HDD_2,CDD=CDD,CDD_2=CDD_2,Vol=Vol,Wgt=Wgt);
  
  if (UseCDD_Ind == "Y") {lmd <- lm(Vol ~ HDD + HDD_2 + CDD+ CDD_2, weights = Wgt)} else {
    lmd <- lm(Vol ~ HDD + HDD_2, weights = Wgt)};
  summary_lmd <- summary(lmd)$coefficients[,1];
  
  step_lmd <- try(MASS::stepAIC(lmd, direction="both", trace=0));
  ##Use my own version of StepAIC to speed up calculation
  ##step_lmd <- try(Fun_StepAIC(model=lmd, data=mydata));
  if (class(step_lmd) == "try-error") {step_lmd <- lmd};
  ##This is to use AIC to eliminate insignificant variable
  summary <- summary(step_lmd)$coefficients[,1];
  
  if (is.null(names(summary)) | is.numeric(as.numeric(summary))) {Intercept_Coef = as.numeric(summary)};
  if (sum(names(summary) == "(Intercept)") == 0) {Intercept_Coef = 0} else {Intercept_Coef = as.numeric(summary["(Intercept)"])};
  if (sum(names(summary) == "HDD") == 0) {HDD_Coef = 0} else {HDD_Coef = as.numeric(summary["HDD"])};
  if (sum(names(summary) == "HDD_2") == 0) {HDD2_Coef = 0} else {HDD2_Coef = as.numeric(summary["HDD_2"])};
  if (sum(names(summary) == "CDD") == 0) {CDD_Coef = 0} else {CDD_Coef = as.numeric(summary["CDD"])};
  if (sum(names(summary) == "CDD_2") == 0) {CDD2_Coef = 0} else {CDD2_Coef = as.numeric(summary["CDD_2"])};
  
  beta.hat <- as.matrix(cbind(Intercept_Coef, HDD_Coef, HDD2_Coef, CDD_Coef, CDD2_Coef));
  R_Sqr <- summary(step_lmd)$r.squared;
  if (is.na(R_Sqr) | is.null(R_Sqr)) {R_Sqr = 0};
  beta.hat <- t(beta.hat);
  #x <- as.matrix(cbind(1, HDD, HDD_2));
  #y <- Vol;
  ##beta.hat <- solve(t(x) %*% x) %*% t(x) %*% y;
  #y.hat <- x %*% t(beta.hat);
  #error <- sqrt(sum((y - y.hat)^2)/(length(y) - ncol(x)+1));
  result <- list(BalanceHDDTemp = balance_HDDtemp, 
                 BalanceCDDTemp = balance_CDDtemp,
                 Intercept_Coef = beta.hat[1], 
                 HDD_Coef = beta.hat[2], HDD2_Coef = beta.hat[3], 
                 CDD_Coef = beta.hat[4], CDD2_Coef = beta.hat[5],
                 R_Sqr = R_Sqr);
				 
  return(result)
}