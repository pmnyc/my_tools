PlotCrimes = function(MyMap, 
        incidents=SFcrime, 
        polys=SFpolys, 
        cex = 0.7,
        cols = c(rgb(0,0,220/255,0.4),rgb(220/255,0,0,0.4)),#brewer.pal(9,"Set1")[c(6,1)], ##<< set of 2 cols denoting non-yes violent (2nd color violent == TRUE)
        alpha=0.5,
        ...
){
  if (!("violent" %in% colnames(incidents))) 
    incidents$violent = with(incidents, 
                             Category %in% c("ASSAULT", "ROBBERY", 
                                             "SEX OFFENSES, FORCIBLE", "KIDNAPPING") 
                             | Descript %in% 
                               c("GRAND THEFT PURSESNATCH", 
                                 "ATTEMPTED GRAND THEFT PURSESNATCH"))
  #col2rgb("darkgreen")
  if (is.factor(incidents$violent)) incidents$violent=as.logical(as.character(incidents$violent))
#  tmp <- PlotOnStaticMap(MyMap, lat = incidents$Y[!incidents$violent], lon = incidents$X[!incidents$violent],
#                         cex=cex,pch=20,col=rgb(0,150,0,alpha,max=255), add=FALSE);
  #col2rgb("darkred")
#  tmp <- PlotOnStaticMap(MyMap, lat = incidents$Y[incidents$violent], lon = incidents$X[incidents$violent],
#                         cex=cex,pch=20,col=rgb(200,0,0,alpha,max=255), add=TRUE);
  v = as.numeric(incidents$violent)+1
  cols = adjustcolor(cols,alpha)# add.alpha(cols)
  #browser()
  tmp <- PlotOnStaticMap(MyMap, lat = incidents$Y, lon = incidents$X,
                         cex=cex,pch=20,col=cols[v], ...);
  
  if (!is.null(polys))
    PlotPolysOnStaticMap(MyMap, polys$polys, lwd=.5, col=rgb(0,0,0,0), border = "purple" , add = TRUE);  
}

InvLogit = function(x, SCALE=TRUE) {
  return(exp(x)) #TO BE FIXED
  if (SCALE) x = x -mean(x)
  return(exp(x)/(1+exp(x)))
}

# add.alpha <- function(col, alpha=1){
#   if(missing(col))
#     stop("Please provide a vector of colours.")
#   apply(sapply(col, col2rgb)/255, 2, 
#         function(x) 
#           rgb(x[1], x[2], x[3], alpha=alpha))  
# }

