# This is to perform a step AIC model process given linear model and data (frame)
# @author: pengma

# For example,
#   model <- lm(y=x1+x2, weights=rep(1,length(y)));

stepAIC_Fun <- function(model,data=list()) {

	Fun_ParseDataCol <- function(x){
		text1 <- paste(x," = data$",x,sep="");
		return(text1);
		};
	cmd <- sapply(names(data),FUN=Fun_ParseDataCol);
	names(cmd) <- NULL;
	eval(parse(text=paste(cmd,sep=" ")));
	
    ##This is to perform the stepwise regression for linear regression
    VarList <- names(model$model)[-1];
	if (any(VarList == "(weights)")) {VarList <- VarList[-which(VarList == "(weights)")]};
	##if (!exists("VarList")) {VarList <- c("HDD","HDD_2","CDD","CDD_2")};

	Fun_MatrixToArray <- function(x) {return(tapply(x,rep(1:nrow(x),each=ncol(x)),function(i) i))};
  
	Fun_CreateCombMatrix <- function(x) {apply(combn(VarList,m=x),1,function(i) i)};
  
	Fun_CreateCombArray <- function(x) {t <- Fun_MatrixToArray( as.matrix(Fun_CreateCombMatrix(x)) );
                                      return(t)};
  

	y <- lapply(seq(length(VarList)-1),FUN=Fun_CreateCombArray);
	y2 <- unique(do.call(c,y));
	VarList_CombArray <- y2;
	VarList_CombArray[length(y2)+1] <- list(VarList);
  
    ##Create a test data for this function
	##HDD <- seq(10);
	##HDD_2 <- HDD^2;
	##Vol <- 2+1.5*HDD+0.05*rnorm(10);
	##
	##Test Data is Generated and discarded
	
	formula <- model$call
	class(formula) = "character";
	##sample formula will look like
		## "lm" "Vol ~ HDD + HDD_2" "rep(1, length(Vol))"
	Formula_Split_Loc <- gregexpr(pattern ='~',formula[2])[[1]][1];
	
	Fun_RunModelByFormula <- function(x) {
			t1 <- paste(substring(formula[2],1,Formula_Split_Loc-1),"~ ",paste(x,sep="",collapse=" + "),sep="");
			if (length(formula) == 2) {
					t2 <- paste(formula[1],"(",t1,")",sep="")} else {
					t2 <- paste(formula[1],"(",t1,", ","weights=",formula[3],")",sep="")}
			aic <- AIC(eval(parse(text=t2)));
			return(list(Var=paste(x,sep="",collapse=" + "),AIC=aic))};
	
	StepModel_Array <- lapply(VarList_CombArray,FUN=Fun_RunModelByFormula);
	
	Varname <- names(StepModel_Array[[1]]);
	Out_Table <- matrix(unlist(StepModel_Array), ncol = length(names(StepModel_Array[[1]])), byrow = TRUE);
	Out_Table <- as.data.frame(Out_Table);
	names(Out_Table) <- Varname;
	Out_Table$AIC <- as.numeric(as.character(Out_Table$AIC));
	Out_Table$Var <- as.character(Out_Table$Var);
	Final_Model_Var <- Out_Table[Out_Table$AIC == min(Out_Table$AIC),"Var"];
	Final_Model_Var <- Final_Model_Var[1];

	Fun_RunModel <- function(x) {
			t1 <- paste(substring(formula[2],1,Formula_Split_Loc-1),"~ ",x,sep="");
			if (length(formula) == 2) {
					t2 <- paste(formula[1],"(",t1,")",sep="")} else {
					t2 <- paste(formula[1],"(",t1,", ","weights=",formula[3],")",sep="")}
			lmd <- eval(parse(text=t2));
			return(lmd)};	
			
    return(Fun_RunModel(Final_Model_Var))
}