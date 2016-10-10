
###################################################
#code for development of figure 10: SFloa figure 02
###################################################

#######
#set up
#######
require(loa)
require(mgcv)
load("data/incidents2012.rda")
load("data/loaMap.rda")


######################################
#See FIG06_SFLoa01.R for loaMap source 
######################################


###############################
#basic loa plot with kd surface
############################### 
#Shown in paper as figure 10 left


GoogleMap(~Y*X, data=incidents, map=loaMap,                   #plot structure and sources    
          panel=panel.kernelDensity,                          #surface panel                 see note 1                                                                      
          col.regions=c("lightyellow", "darkred"),            #surface colors                see note 2 
          alpha.regions=0.5, col=1,                           #surface transpancy and 
                                                              #  contour line color          see note 2
          n=200,                                              #surface resolution            see note 1
          at=c(0.5,1,2.5,5,10,25,50,100,150),                 #contour line locations        see note 3
          xlab="", ylab="")

png("SFLoa02.png", 892, 892, bg="transparent", res=118, type="cairo-png")
trellis.last.object()
dev.off()

#note 1
#This plot uses kd2d in MASS to generate a surface. The extra argument n=200 is passed to kd2d, 
#which uses it set the resolution when generating the surface (x,y,z) estimate.

#note 2
#the surface is shown as a contour plot, with regions between contour lines constantly colored. 
#the region color and transparency is controlled by col.region and alpha.region, while the 
#contour colors (and transparency) are controlled by col (and alpha).  

#note 3
#default at range is pretty(zlim), so this was manually reset to aid the visualization of
#clusters. 


###############################
#gam frequency density function
############################### 

gam.freq.density <- function(x=x, y=y, z=z, n=20, ...){

     require(mgcv) 

     ans <- panel.binPlot(x=x, y=y, statistic=length,        
                          breaks=n, plot=FALSE, pad.grid=TRUE, 
                          process=TRUE)                                #note 1

     data <- na.omit(data.frame(x=ans$x, y=ans$y, z=ans$z))
     mod <- gam(z ~ s(x, y), data=data)
     ans$z <- as.vector(predict(mod, newdata=ans))                     #note 2

     ans
}  
 

#note 1
#This function uses the loa binPlot panel to generate counts
#The output ans is a list of x,y bins and associated counts as z

#note 2
#the (x,y) grid and associated counts from panel.binPlot are 
#then fitted using a GAM to make a surface. Any NAs are removed 
#before fitting because GAMs don't like NAs, but the full data 
#range is used to generate the surface.

#reference: gam used here is
#Wood S (2014)
#mgcv: Mixed GAM Computation Vehicle with GCV/AIC/REML smoothness estimation
#R package version 1.8-2 
#http://cran.r-project.org/web/packages/mgcv/


#figure 10 right

GoogleMap(~Y*X, data=incidents, map=loaMap,                     
          panel=panel.kernelDensity,                                                                                                
          col.regions=c("lightyellow", "darkred"),               
          alpha.regions=0.5, col=1,                                                                                          
          n=200, at=c(0.5,1,2.5,5,10,25,50,100,150),
          kernel.fun = gam.freq.density,                              #note 1
          xlab="", ylab="")                   


png("SFLoa02b.png", 892, 892, bg="transparent", res=118, type="cairo-png")
trellis.last.object()
dev.off()

#note 1
#Same plot as last time, but with density surface estimated by binning and GAM 
#modelling (using gam.freq.density) instead of default kernel density estimation.
#Both can be conditioned and z cases calculated in panels will be automatically 
#tracked by all panels and keys. 

#additional
#If panel.kernelDensity had not allow me to pass an alterative surface fitting function, 
#I could have copied it and editted the fitting steps in the code to achieve the same 
#outcome.
#
#   e.g.
#   my.new.panel <- edit(panel.kernelDensity)
#







