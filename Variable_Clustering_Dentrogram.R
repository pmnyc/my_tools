library(data.table)
library(psych)

design_matrix_with_all_levels <- function(vars, dt) {
    # This function is for creating the design matrix without skipping the default
    #    base level of each character variable level.
    # vars is the list of variables used for creating the design matrix
    # dt is the data table
    formula_ <- paste0(vars, collapse = " + ")
    contrast_arg <- paste0("list(@)")
    for (v_ in vars) {
        if (dt[, class(get(v_))] %in% c("character", "factor")) {
            cmd <- paste0(v_, " = contrasts(dt$", v_, ", contrasts=F), @")
            contrast_arg <- gsub("@", cmd, contrast_arg)
        } else {
            next
        }
    }
    contrast_arg <- gsub(", @", "", contrast_arg)
    cmd <- paste0("x_ <- model.matrix(~",formula_,", data=dt, ", contrast_arg,")[,-1]")
    eval(parse(text=cmd))
    return(x_)
}

# dt is the data table
#### Manual Change Variable Names ####
name_mapping <- list()
name_mapping$var1 = "var1_newname"
######################################

for (i in 1:length(name_mapping)) {
    setnames(dt,names(name_mapping)[i], name_mapping[[i]])
}

char_vars <- names(dt[, lapply(.SD, class), .SDcols=colnames(dt)])[dt[, lapply(.SD, class),
                                                                      .SDcols=colnames(dt)] %in% c("character","factor")]
num_vars <- setdiff(colnames(dt), char_vars)
print("Numberical Variables are ")
print(paste0("'", paste0(num_vars, collapse="', '"),"'"))
print("Categorical Variables are ")
print(paste0("'", paste0(char_vars, collapse="', '"),"'"))

for (v_ in char_vars) {
    if (dt[, class(get(v_))] == "character") {dt[, paste(v_) := as.factor(get(v_))]}
    setnames(dt, v_, paste0(v_, "__"))
}

xmatrix <- design_matrix_with_all_levels(colnames(dt), dt)

dists = dist(abs(cor(na.omit(xmatrix))))
plot(hclust(dists), main="Variables Cluster Dentrogram", sub="")
