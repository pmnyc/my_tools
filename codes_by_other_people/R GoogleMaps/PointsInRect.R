PointsInRect = function#returns only those points that lay within a specified bounding box
( 
  XLIM= c(-122.43,-122.39),##<< lon limits
  YLIM = c(37.75,37.79), ##<< lat limits
  BBOX, ##<< instead of XLIM or YLIM we can pass the bounding box from the map tile !
  x =incidents,##<< the data
  LatLonColNames = c("Y","X"), ##<< colnames representing lat,lon
  ReturnData = TRUE, ##<< return subset of data or rows to keep
  verbose = 0 ##<< level of verbosity
){
  if (!missing(BBOX)){
    XLIM = c(BBOX$ll[1,"lon"], BBOX$ur[1,"lon"])
    YLIM = c(BBOX$ll[1,"lat"], BBOX$ur[1,"lat"])
  }
  
  
  lat = x[,LatLonColNames[1]]
  lon = x[,LatLonColNames[2]]
  keepRows = which(lon >XLIM[1] & lon < XLIM[2] & lat >YLIM[1] & lat <YLIM[2] )
  if (ReturnData)
    return(x[keepRows,])
  else 
    return(keepRows)
}

#keepRows = PointsInRect(XLIM= c(-122.43,-122.39),YLIM = c(37.75,37.79), x=incidents,ReturnData=FALSE)