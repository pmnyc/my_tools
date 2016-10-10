
###########################################
#code for development of Figure 2: meuseloa
###########################################

#######
#set up
#######
require(loa)

#########################
#basic loa (bubble) plot
######################### 
#NOT shown in paper

#default plot
GoogleMap(zinc~latitude*longitude,                              # plot structure (see note 1) 
          data=lat.lon.meuse, map=roadmap.meuse)                # data sources   (see note 2,3)

#recolor,rescale, etc
GoogleMap(zinc~latitude*longitude,                              
          data=lat.lon.meuse, map=roadmap.meuse,                
          col.regions=c("green", "orange", "darkred"),          # color scale like bubbleplot
          alpha=0.75,                                           # transparent data layer
          cex.range =c(0.75, 2),                                # point size scaling like bubbleplot
          key.z.n.ticks=7, key.z.main="Conc \n(ppm)")           # key updates

#note 1
#the basic plot structure is z ~ lat * lon | cond
#so this is equivalent of figure 1 RgoogleMap bubble plot 
#see ?loaPlot for more details

#note 2
#these data sources are contained included in loa 
#and used here so supporting code runs offline
#see ?lat.lon.meuse and ?roadmap.meuse for details

#note 3
#if the map argument is removed from the above call
#the function recovers a map directly from the Google API (if online)
#note a downloaded map will appear slightly different 
#due to default settings 
#see ?roadmap.meuse for details


####################################
#binning data using specialist panel
####################################
#NOT shown in paper

GoogleMap(zinc~latitude*longitude,                               
          panel = panel.binPlot, breaks=10,                   #data binning (see note 1)  
          data=lat.lon.meuse, map=roadmap.meuse,                
          col.regions=c("green", "orange", "darkred"), 
          alpha=0.75)    

#note 1
#the default data panel for GoogleMap is panel.loaPlot
#other panels can be supplied to generate alternative data visualisations
#here panel.binPlot is used bin and average zinc measurements by location
#note breaks sets number of bins to be used
#note default binning is as mean 
#but this can be altered with statistic argument
#see ?panel.binPlot for details


######################################
#extension of plot to multiple species
######################################
#figure 2 top panel

GoogleMap(cadmium*100+copper*15+zinc~latitude*longitude,        # plot structure (see note 1) 
          data=lat.lon.meuse, map=roadmap.meuse,                   
          panel.zcases=TRUE, layout=c(3,1),                     # plot layout    (see note 1)
          col.regions=c("green", "orange", "darkred"), 
          alpha=0.75,   
          cex.range =c(0.5, 1.3), 
          key.z.n.ticks=7, key.z.main="Conc \n(ppm)")           


png("meuseLoaBubble001.png", 1325, 562, bg="transparent", res=100, type="cairo-png")
trellis.last.object()
dev.off()
   

#note 1
#here the basic plot structure (first plot above) is extended 
#by adding other species in form z1 + z2 + ... ~ lat * lon | cond
#note the 'on fly' rescaling, e.g. cadmium*100 
#note also use panel.zcases=TRUE argument which creates a map per 
#zcase (z1, z2, ...) rather than plotting them all in the same panel
#note also automate update of key type linked to panel


############################################
#using a multivariate (zcase) panel
#(to compare multiple dataseries on one map)
############################################
#figure 2 bottom left

 
GoogleMap(cadmium*100+copper*15+zinc~latitude*longitude,                               
          panel = panel.zcasePiePlot,                           #zcase pie plotting (see note 1)  
          data=lat.lon.meuse, map=roadmap.meuse,                
          col.regions=c("green", "orange", "darkred"), 
          alpha=0.75, 
          cex.range=c(0.75,2))    

png("meuseLoaBubble002.png", 892, 892, bg="transparent", res=118, type="cairo-png")
trellis.last.object()
dev.off()

#note 1
#panel.zcasePiePlot generates pie plots of 
#zcase (z1 + z2 + ...) data series at (lat, lon) locations
#pie segment angle (360 * z1/(z1+z2+..), etc)
#pie size proportional to sum (z1+z2+..., etc)


###############################################
#however such plots can easily become cluttered
#specially is large amounts of informat are sent
#(also unstable)
###############################################


#########################################
#one option is to plot subsamples of data
#########################################
#NOT show in paper

temp <- lat.lon.meuse[c(1:30)*5,]
GoogleMap(cadmium*100+copper*15+zinc~latitude*longitude,                               
          panel = panel.zcasePiePlot,                             
          data=temp, map=roadmap.meuse,                
          col.regions=c("green", "orange", "darkred"), 
          alpha=0.75, 
          cex.range=c(0.75,2))    


#############################################
#another is to combine bin and pieplot panels 
#to handle all the data on the fly
#############################################
#figure 2 bottom right

#my new panel                       

panel.temp <- function(..., plot = TRUE, process = TRUE, 
    loa.settings = FALSE){

    if(loa.settings)
        return(listUpdate(loaHandler(panel.binPlot), 
                          loaHandler(panel.zcasePiePlot)))
    
    if(process)
        if(!plot) return(panel.binPlot(..., plot=plot, process=process))

    if(plot)
        panel.zcasePiePlot(..., plot=plot, process=process)
    
}

#note
#this using the processing element of panel.binPlot
#to bin and average data for each zcase
#then the plotting element of panel.zcasePiePlot 
#to plot these 

#in use
GoogleMap(cadmium*100+copper*15+zinc~latitude*longitude,                               
          panel = panel.temp, breaks=10,                              
          data=lat.lon.meuse, map=roadmap.meuse,                
          col.regions=c("green", "orange", "darkred"), 
          alpha=0.75, 
          cex.range=c(0.75,2))    


png("meuseLoaBubble003.png", 892, 892, bg="transparent", res=118, type="cairo-png")
trellis.last.object()
dev.off()










