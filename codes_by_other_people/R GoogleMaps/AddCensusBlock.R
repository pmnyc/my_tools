#incidents = AddCensusBlock(incidents, SFpolys)
AddCensusBlock = function(
  incidents,
  SFpolys,
  N,
  verbose=0
){
  if (missing(SFpolys)) load("SFpolys2010.rda")
  library("RANN")
  library(sp)
  #head(SFpolys$polyCenters)
  if (missing(N)) N=nrow(incidents)
  if (!("CensusBlock" %in% colnames(incidents))) incidents[,"CensusBlock"] = NA
  nearest =nn2(SFpolys$polyCenters[,c("X","Y")] , query=incidents[1:N,c("X","Y")])
  K = ncol(nearest$nn.idx)
  polys = split(SFpolys$polys[,c( "POS", "X","Y")], SFpolys$polys[,c("PID")])
  for (i in 1:N) {
    pt = incidents[i,c("X", "Y")]
    for (j in 1:K){
      try({  
        pID=nearest$nn.idx[i,j]
        if (point.in.polygon(pt[1], pt[2], polys[[pID]][,"X"], polys[[pID]][,"Y"])>0){
          #brow
          incidents[i,"CensusBlock"] = as.character(SFpolys$data[pID,"fips"])
          break
          #print(pID)
        }
      })
    }
    if ((i %% 5000) ==0) cat(i, " rows processed...\n")
  }
  return(incidents)
}
PrintTime =function(msg="",verbose=1){
  if (is.null(msg)) {
    #if (verbose) print(msg)
    t0 <<- Sys.time()
    invisible()
  } else {
    deltaT = Sys.time() - t0
    if (verbose) cat(msg, t0, "time units \n")
    t0 <<- Sys.time()
  }
  
}