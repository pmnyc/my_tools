######################################
# Create a random ID Name of length 12
# @author: pm #
######################################


mkRandomString <- function(len=12){
    n = 1;
    randomString <- c(1:n)  # initialize vector
    for (i in 1:n){
        randomString[i] <- paste(sample(c(0:9, letters, LETTERS),
                                        len, replace=TRUE),
                                 collapse="") ;
    }
    return(randomString)
}

print(mkRandomString(12))
