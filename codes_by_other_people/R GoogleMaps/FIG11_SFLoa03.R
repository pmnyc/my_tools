
###################################################
#code for development of Figure 11: SFloa figure 03
###################################################

#######
#set up
#######
require(loa)
require(splancs)
load("data/incidents2012.rda")
load("data/loaMap.rda")

###################################
#see SFLoa01.R for loaMap source
###################################

#############################
#basic loa plot 
#(loa make to look like 
#Figure 4 RgoogleMap output)
#see SFLoa01.R for discussion
############################ 


cols=c("cyan", "darkred")
GoogleMap(~Y*X, data=incidents, map=loaMap,             
          groups=incidents$violent,                     
          col=cols, cex=0.3, alpha=0.3,                 
          panel=panel.loaPlot2,                         
          key.groups=list(main="Violent", 
                          cex=1, col=cols),
          xlab="", ylab="")             


###############################
#isolating ploygons on this map
###############################

#my crude function for working with a plot post print

makePolygonRef <- function(polygon, col=1, ..., 
                           object=trellis.last.object(),
                           show.poly=TRUE){

     #this panel
     this.panel <- object$panel

     #draws polygon as outline in col
     message("select polygon region to reference")
     flush.console()

     #latlon.ref is the (lat,lon) that user sees
     #local.ref is the (x,y) that plot uses
     latlon.ref <- getLatLon(object=object, col=col, type="b", pch=20)
     local.ref <- RgoogleMaps:::LatLon2XY.centered(object$panel.args.common$map, 
                                           lat = latlon.ref$lat, lon=latlon.ref$lon)
          
     #get data from plot
     #note this version example only works with one/first panel
     x <- object$panel.args[[1]]$x
     y <- object$panel.args[[1]]$y 
    
     #make polygon ref
     names(local.ref) <- c("x", "y")
     ref <- inout(list(x=x, y=y), local.ref, TRUE)

     #add information to object
     ##names of polys added
     object$panel.args.common$poly.names <- if(!"poly.names" %in% names(object$panel.args.common))
                                             polygon else c(object$panel.args.common$poly.names, polygon)
     #polygons elements
     temp <- if(!"poly.ref" %in% names(object$panel.args[[1]]))
                 rep(NA, length(x)) else object$panel.args[[1]]$poly.ref
     
     temp <- ifelse(!ref, temp, paste(temp, polygon, sep="&"))
     temp <- gsub("NA&", "", temp)
     object$panel.args[[1]]$poly.ref <- temp
     
     if(show.poly)
         object$panel <- function(...){this.panel(...)
                                       panel.polygon(local.ref$x, local.ref$y, col=col, 
                                                     border=TRUE, alpha=0.5)} 
         
     object

}



##########################################
#Please NOte
##########################################
#subsequent code will not run without this
##########################################

#This was run once for each cluster the user wants to manually draw
#each time assigning a unique name and color
#so e.g. for the the clusters in the figure
#
#    makePolygonRef("A", "red")
#    makePolygonRef("B", "green")
#    makePolygonRef("C", "darkblue")
#    etc

##########################################
#Please NOte
##########################################
#subsequent code will not run without this
##########################################


#then exported like other figures
#
#    png("SFLoa03.png",  892, 892, bg="transparent", res=118, type="cairo-png")
#    trellis.last.object()
#    dev.off()

#The above manual steps generate a plot like fig 11 left

#Users can replicate this process but will obviously get the ranges they select 
#rather than the ones shown in the paper.


#my crude function to show selected points


colByPolygonRef <- function(cols, ..., object=trellis.last.object()){

    #reset plot
    object$panel <- function(...){panel.GoogleMapsRaster(object$panel.args.common$map)
                                  panel.loaPlot2(...)}

    temp <- object$panel.args[[1]]$poly.ref
    temp <- factor(ifelse(is.na(temp), "unselected", temp))
    cols <- c(cols, "grey")

    #update groups
    object$panel.args[[1]]$groups <- temp
    object$panel.args.common$group.ids <- levels(temp)
    object$panel.args.common$col <- cols 

    #update groups in key
    object$legend$right$args$key$groups$main <- "Selected\nClusters"
    object$legend$right$args$key$groups$col <- cols
    object$legend$right$args$key$group.ids <- levels(temp)

    object


} 

colByPolygonRef(c("red", "green", "darkblue"))

png("SFLoa03b.png",  892, 892, bg="transparent", res=118, type="cairo-png")
trellis.last.object()
dev.off()

#Following the generation of a plot like fig 11 left
#the above steps will generate a plot like fig 11 right

#Users can replicate this process but will obviously get the ranges they select 
#rather than the ones shown in the paper.



#my crude function to recover (x, y, poly.ref) data from plot.

getXYPolyRef <- function(..., object=trellis.last.object)
   as.data.frame(listHandler(object()$panel.args[[1]], use=c("x", "y", "poly.ref")))

a <- getXYPolyRef()

head(a)


#note 
#Obviously these examples are relatively crude but they do illustrate 
#how the lattice framework can be used to work with plotted data. 
#Extended versions of these functions are intended for inclusion in
#a future version of loa
 


