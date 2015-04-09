# @author: pm #
 
whichPython2use_Fun = function(
                            cmdpy_alter1 = "python2.7",
                            cmdpy_alter2 = "python2.6",
                            pyCommd = "-V"){
    ## This is to find which python version to run certain packages/codes
        # in the case when some codes are only compatible with certain version
        # of Python version
    # Sample Inputs
    # cmdpy_alter1 = "python2.7";
    # cmdpy_alter2 = "python2.6";
    # pyCommd = ""  #this is to define the command after $ python2.7 or $ python2.6

    cmdpy = cmdpy_alter1;

    msg = tryCatch({system2(command=cmdpy,args = pyCommd)}, warning=function(w){print(w)});
    if (toString(msg) != "0"){
        cmdpy = cmdpy_alter2
    }

    return(cmdpy)

    print(paste(cmdpy,"is the python version to call GDAL"));
    print(paste("The OS system is",.Platform$OS.type));
}
