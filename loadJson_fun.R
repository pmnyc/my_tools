# Load JSON file in R
# @author: pm
#sample usage:
#   loadJson_fun("config.json")

loadJson_fun = function(jsonfilename){
    parseJasonList_Fun <- function(list,listname){
        ## list is the list stream from reading jason file
        ## listname is the name of this list in the workspace
        cmd = "";
        for (i in seq(length(list))){
            cmd <-  paste(cmd," ",names(list)[i]," = ",listname,"$",names(list)[i]," ;",sep="");
        }
        cmd <- substring(cmd,1,nchar(cmd)-1);
        return(cmd);
    }

    #library(RJSONIO)
    require(RJSONIO)
    myconfig271828 <- as.list(RJSONIO::fromJSON(jsonfilename));

    assign("myconfig271828", myconfig271828, envir = .GlobalEnv); #this is to export local values in the function to global environment
    assign("parseJasonList_Fun", parseJasonList_Fun, envir = .GlobalEnv);
    eval(parse(text=parseJasonList_Fun(list=myconfig271828,listname="myconfig271828")), envir=.GlobalEnv);
    rm(parseJasonList_Fun,envir=.GlobalEnv);
    rm(myconfig271828,envir=.GlobalEnv);
}