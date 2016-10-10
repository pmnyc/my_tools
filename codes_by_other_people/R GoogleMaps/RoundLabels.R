RoundLabels <- function(treeobj, digits=3){
  cutleft <- sub("<NA","", paste("<", round(as.numeric(sub("^<", "", treeobj$frame$splits[,"cutleft"])), digits),sep=""))
  cutright <- sub(">NA","", paste(">", round(as.numeric(sub("^>", "", treeobj$frame$splits[,"cutright"])), digits),sep=""))
  treeobj$frame$splits <- cbind(cutleft=cutleft, cutright= cutright);
  try(treeobj$frame[,"yval"] <- round(treeobj$frame[,"yval"], digits));
  return(treeobj)
}