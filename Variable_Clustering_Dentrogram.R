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
dists = dist(abs(cor(na.omit(xmatrix[, -which(variances < 1e-6)]))))
# Different ways of plotting dendrogram
plot(hclust(dists), main="ARA Ireland Variables Cluster Dentrogram", sub="")
dend = as.dendrogram(hclust(dists), method = "complete")
dendextend::circlize_dendrogram(dend)
dend %>% set("labels_col", "blue") %>% plot(main="ARA Ireland Variables Cluster Dentrogram", sub="")
dend %>%
    set("branches_lwd", c(4,1)) %>%
    set("branches_lty", c(1,1,3)) %>%
    set("branches_col", c(1,2,3)) %>%
    plot(main="ARA Ireland Variables Cluster Dentrogram", sub="")
dend %>% set("branches_k_color", k = 3) %>% plot(main="ARA Ireland Variables Cluster Dentrogram", sub="")
dend %>% set("branches_k_color", value = 3:1, k = 3) %>% plot(main="ARA Ireland Variables Cluster Dentrogram", sub="")
dend %>% rect.dendrogram(k=20,horiz = TRUE,border = 8, lty = 5, lwd = 2)

par(mar=par('mar')+c(0,0,0,6))
dend <- dists %>% hclust %>% as.dendrogram(method = "complete") %>%
    set("branches_k_color", k=3) %>%
    set("branches_lwd", c(1.5,1,1.5)) %>%
    set("branches_lty", c(1,1,3,1,1,2)) %>%
    set("labels_colors") %>%
    set("nodes_pch", 19) %>%
    set("nodes_col", c("orange", "black", "plum", NA))
    #%>%  set("labels_cex", c(.9,1.2))
# plot the dend in usual "base" plotting engine:
plot(dend, main="ARA Ireland Variables Cluster Dentrogram", horiz =TRUE,sub="")
abline(v = 0.5, col = 'gray', lty = 1.0)
abline(v = 1.0, col = 'gray', lty = 1.0)
abline(v = 1.5, col = 'gray', lty = 1.0)

library(ggplot2)
ggd1 <- as.ggdend(dend)
# the nodes are not implemented yet.
ggplot(ggd1) # reproducing the above plot in ggplot2 :)
ggplot(ggd1, horiz = TRUE, theme = NULL)
