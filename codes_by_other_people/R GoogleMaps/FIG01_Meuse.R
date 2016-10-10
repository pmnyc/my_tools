
########################################
#code for development of two versions of meuse figure
########################################

#######
#left graph
#######
require(sp)

data("meuse", package = "sp", envir = environment())
data(lat.lon.meuse, package="loa")
#map <- GetMap.bbox(bb$lonR, bb$latR, destfile = filename, maptype="mobile", SCALE = 2);
map <- GetMap(center=c(lat=50.97494,lon=5.743606), zoom=13,size=c(480,480),destfile = paste0(tempdir(),"\\meuse.png"), maptype="mobile", SCALE = 1);

png("Figures/meuseBubble2.png", width=480, height=480)
par(cex=1.5)
bubbleMap(lat.lon.meuse, coords = c("longitude","latitude"), map=map,zcol='zinc',
          key.entries = 100+ 100 * 2^(0:4));
#bubbleMap(meuse, map=map,zcol='zinc',key.entries = 100+ 100 * 2^(0:4));
dev.off()

data(meuse)
coordinates(meuse) <- c("x", "y")
png("Figures/meuseBubble1.png", width=480, height=480)
par(cex.main=2,cex.lab=2)
bubble(meuse, "zinc", main = "zinc concentrations (ppm)",#maxsize=5,
       key.entries =  100+ 100 * 2^(0:4),key.space = "inside")
dev.off()
