IdentifyPoints = function#identify points by clicking on map
### The user can try to identify lat/lon pairs on the map by clicking on them
( 
  MyMap, ##<< map object
  n=1,##<< the maximum number of points to locate.
  verbose = 0 ##<< level of verbosity
){
  cat("please identify ", n, "point(s) on the map with your mouse:\n")
  ret = locator(n)
  LatLon <- XY2LatLon(MyMap, ret$x,Y=ret$y)
  return(LatLon)
}


IdentifyPolygons = function#identify polygons by clicking on map
### The user can try to identify polygons drawn on the map by clicking inside them
### The function will then call 
(
  n=1,##<< the maximum number of points to locate. 
  SFpolys, ##<< candidate polygons
  MyMap, ##<< map object
  verbose = 0 ##<< level of verbosity
){
  library("RANN")
  library(sp)
  
  LatLon = IdentifyPoints(MyMap,n,verbose)
  if (verbose>1) browser()                       
  nearest =nn2(SFpolys$polyCenters[,c("X","Y")] , query=LatLon[,c("lon", "lat"), drop=F])
  K = ncol(nearest$nn.idx)
  polyList = split(SFpolys$polys[,c( "POS", "X","Y")], SFpolys$polys[,c("PID")])
  pIDlist = vector()
  
  
  for (i in 1:n){
    pt = LatLon[i,c("lon", "lat")]
    for (j in 1:K){
      try({
        pID=nearest$nn.idx[i,j]
        if (point.in.polygon(pt[1], pt[2], polyList[[pID]][,"X"], polyList[[pID]][,"Y"])>0){
          cat("polygon ID=", pID, "\n")
          pIDlist[i] = pID
          break
        }
      })
    }
  }
  IdentifiedPolys =  do.call("rbind", polyList[pIDlist])
  invisible(IdentifiedPolys)
  
}

#TopRightPoly = IdentifyPolygons(1,SFpolys,SFMap.z13)
