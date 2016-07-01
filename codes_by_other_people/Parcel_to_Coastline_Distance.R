library(rgdal)   # for readOGR(...); loads package sp as well
library(rgeos)   # for gDistance(...)

setwd(" < directory with all your files > ")
# WGS84 long/lat
wgs.84    <- "+proj=longlat +datum=WGS84 +no_defs +ellps=WGS84 +towgs84=0,0,0"
# ESRI:54009 world mollweide projection, units = meters
# see http://www.spatialreference.org/ref/esri/54009/
mollweide <- "+proj=moll +lon_0=0 +x_0=0 +y_0=0 +ellps=WGS84 +datum=WGS84 +units=m +no_defs"
df        <- read.csv("OSD_All.csv")
sp.points <- SpatialPoints(df[df$Depth==0,c("Long","Lat")], proj4string=CRS(wgs.84))

coast  <- readOGR(dsn=".",layer="ne_10m_coastline",p4s=wgs.84)
coast.moll <- spTransform(coast,CRS(mollweide))
point.moll <- spTransform(sp.points,CRS(mollweide))

set.seed(1)   # for reproducible example
test   <- sample(1:length(sp.points),10)  # random sample of ten points
result <- sapply(test,function(i)gDistance(point.moll[i],coast.moll))
result/1000   # distance in km
#  [1]   0.2185196   5.7132447   0.5302977  28.3381043 243.5410571 169.8712255   0.4182755  57.1516195 266.0498881 360.6789699

plot(coast)
points(sp.points[test],pch=20,col="red")

## not run
## estimated run time ~ 7 hours
result <- sapply(1:length(sp.points), function(i)gDistance(sp.points[i],coast))

library(foreach)   # for foreach(...)
library(snow)      # for makeCluster(...)
library(doSNOW)    # for resisterDoSNOW(...)

cl <- makeCluster(4,type="SOCK")  # create a 4-processor cluster
registerDoSNOW(cl)                # register the cluster

get.dist.parallel <- function(n) {
  foreach(i=1:n, .combine=c, .packages="rgeos", .inorder=TRUE, 
          .export=c("point.moll","coast.moll")) %dopar% gDistance(point.moll[i],coast.moll)
}
get.dist.seq <- function(n) sapply(1:n,function(i)gDistance(point.moll[i],coast.moll))

identical(get.dist.seq(10),get.dist.parallel(10))  # same result?
# [1] TRUE
library(microbenchmark)  # run "benchmark"
microbenchmark(get.dist.seq(1000),get.dist.parallel(1000),times=1)
# Unit: seconds
#                     expr       min        lq      mean    median        uq       max neval
#       get.dist.seq(1000) 140.19895 140.19895 140.19895 140.19895 140.19895 140.19895     1
#  get.dist.parallel(1000)  50.71218  50.71218  50.71218  50.71218  50.71218  50.71218     1
