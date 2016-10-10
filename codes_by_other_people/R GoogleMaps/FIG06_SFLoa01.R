
##################################################
#code for development of Figure 6: SFloa figure 01
##################################################

#######
#set up
#######
require(loa)
require(latticeExtra)
load("data/incidents2012.rda")
load("data/loaMap.rda")


###################################
#loa map
###################################
#supplied in supporting information

#note
#the map layer using in loaPlots is supplied
#so examples below work offline

#the map was made as follows

GoogleMap(~Y*X, data=incidents,          # the basic plot                  see note 1 
          maptype="roadmap",             # maptype fetched by RgoogleMap   see note 2
          type="n",                      # don't plot points               see note 3
          size=c(470,470))               # reduce the panel size           see note 4
loaMap <- getMapArg()                    # recover map from plot           see note 5

#note 1 
#GoogleMap is basically a wrapper for RgoogleMaps function GetMap and 
#loa function loaPlot.  

#note 2
#maptype sets the type of map requested from the Google Maps API
#see RgoogleMaps ?GetMap for options/details 
#and loa ?makeMapArg for modifications for use with lattice
 
#note 3
#type="n" plots a graph without the data points
#works same way as in plot, xyplot, etc 
#used here to avoid plotting all points while sizing map layer

#note 3
#the Google API returns a limited range of map sizes 
#RgoogleMaps GetMap argument size can be used to fine-tune this
#see RgoogleMaps ?GetMap for details

#note 4
#getMapArg extracts the map from a previous plot
#if this map is then supplied (as the map argument) in subsequent GoogleMap calls
#it will be used rather than recovering a new map from the Google API
#(saves a lot of time if you are drawing multiple plots on the same map!)
#makeMapArg fetches Google Map and modifies it for use with loa panel functions
#see loa ?getMapArg or ?makeMapArg for further details



############################
#basic loa plot 
#(make like fig 4)
############################ 
#NOT shown in paper

cols <- c("cyan", "darkred")
GoogleMap(~Y*X, data=incidents, map=loaMap,             #plot structure and map    see note 1,2
          groups=incidents$violent,                     #                          see note 1
          col=cols, cex=0.1, alpha=0.3,                 #point setting
          panel=panel.loaPlot2,                         #special panel             see note 3
          key.groups=list(main="Violent", 
                          cex=1, col=cols))             #key settings              see note 4

#note 1
#plot is in form z ~ lat * lon
#leaving z blank would by default generate a same size, same color point at each location 
#but data is grouped by violent TRUE/FALSE element of incidents
#by default groups are linked to col and zcases to cex 
#so point are colored by violent TRUE/FALSE 

#note 2
#see above for source of map argument loaMap

#note 3
#we use a special panel panel.loaPlot2 here
#the default loaPlot panel plots plots in their order with the supplied dataset
#violent crime can therefore get hidden under the much larger number of non-violent crimes
#this panel plots all in one group, then all in other group
#so it produces an image with a biased towards violent crime.

#note 4
#we modify the default color key that was designed for use with a bubble plot
#so point size and transparency in key is not linked to point/transparency in plot. 


############################
#basic trellis conditioning 
############################ 
#not shown in paper

cols <- c("yellow", "darkred")
GoogleMap(~Y*X|DayOfWeek,                               #plot conditioned               see note 1
          data=incidents, map=loaMap,
          groups=incidents$violent,                                               
          col=cols, cex=0.1, alpha=0.3,                 
          panel=panel.loaPlot2,                         
          key.groups=list(main="Violent", 
                          cex=1, col=cols))             

#note 1
#the previous plot formula is extend with | DayOfWeek
#generating one panel for each case in the incidents element DayOfWeek
#by default this is not sensibly ordered
#(default is factor handling, i.e. alphabetically)

#force factor
dow <- factor(incidents$DayOfWeek,
              levels=c("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"),
              ordered=T)

cols <- c("yellow", "darkred")
GoogleMap(~Y*X|dow, layout=c(5,2),
          data=incidents, map=loaMap,                            
          groups=incidents$violent,                                               
          col=cols, cex=0.1, alpha=0.3,                 
          panel=panel.loaPlot2,                         
          key.groups=list(main="Violent", 
                          cex=1, col=cols))    

#this might seem a little crude compared to plots that do it all for you
#but with this you can e.g. group MON-FRI as one row and SAT-SUN as another
#or order days exactly as you want them, etc 
#(not just how the package developer wanted them)

#e.g.
wd <- ifelse(incidents$DayOfWeek=="Saturday"|incidents$DayOfWeek=="Sunday", 
             "Weekend", "Weekday")

cols <- c("yellow", "darkred")
GoogleMap(~Y*X|wd, layout=c(5,2),
          data=incidents, map=loaMap,                               
          groups=incidents$violent,                                               
          col=cols, cex=0.1, alpha=0.3,                 
          panel=panel.loaPlot2,                         
          key.groups=list(main="Violent", 
                          cex=1, col=cols)) 


############################
#more complex trellis conditioning 
############################ 
#shown in paper as fig 6 top


temp <- incidents$TimeOfDay
tod <- rep("About Midnight", length(temp))
tod <- ifelse(as.numeric(temp)>2 & as.numeric(temp)<9, "About Dawn", tod)
tod <- ifelse(as.numeric(temp)>8 & as.numeric(temp)<14, "About Midday", tod)
tod <- ifelse(as.numeric(temp)>13 & as.numeric(temp)<20, "About Dusk", tod)
tod <- factor(tod, levels=c("About Dawn", "About Midday", "About Dusk", "About Midnight"))

v <- ifelse(incidents$violent==TRUE, "Violent", "Non-violent")

GoogleMap(~Y*X|tod+v,                                           #re conditioning    see note 1
          data=incidents, map=loaMap,                                                                              
          col="darkred", cex=0.1, alpha=0.1,
          scales=list(draw=FALSE), xlab="", ylab="")            #to hide axes

png("SFLoa01.png", 1690, 717, bg="transparent", res=118, type="cairo-png")
useOuterStrips(trellis.last.object())
dev.off()

#note 1
#Conditioning terms do not need to be factors. lattice simply handles all unique element in 
#a conditioning term data series as a unique panel id. So, character, numeric classes, etc can 
#all be used. However, as lattice does this by forcing all non-factor conditoning terms to factors 
#and then, by default, orders and labels panels using factor information, pre-assigning 
#factor settings is often the easiest way of managing plot outputs. 


############################
#replace points with a density surface 
############################ 
#shown in paper as fig 6 bottom

GoogleMap(~Y*X|tod+v,
          data=incidents, map=loaMap,    
          panel=panel.kernelDensity,                          #surface plot control   see note 1                                                                      
          col.regions=c("lightyellow", "darkred"),            #                       see note 1 
          alpha.regions=0.5,                                  #                       see note 1
          col=1,                                              #surface calculation    see note 2
          n=200, at=c(0.5,1,2.5,5,10,25,50), 
          scales=list(draw=FALSE), xlab="", ylab="")  

png("SFLoa01b.png", 1690, 717, bg="transparent", res=118, type="cairo-png")
useOuterStrips(trellis.last.object())
dev.off()

#note 1
#the surface is generated using panel.kernelDensity in loa
#this uses MASS kd2d and lattice panel.contourplot
#the surface col and transparency are controlled by col.regions and alpha.regions
#the col and transparency of the contour lines are controlled by col and alpha

#note 2
#n is the resolution at which the kernel density surface is generated
#the default generates a realatively crude surface, so was increased
#color regions are bands separated by contour lines, set using at
#the default at is pretty(zlims), which was modified to help visualize clusters

  









