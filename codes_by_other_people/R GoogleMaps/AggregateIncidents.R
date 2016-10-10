table2vec = function(x){
  y = table(x)
  yy=as.vector(y)
  names(yy)=names(y)
  return(yy)
}

CrimesByDay = function(incidents){

  incByDay=by(incidents$violent, list(incidents$Date), FUN = table )  
  incByDay = as.data.frame(do.call("rbind",incByDay))
  colnames(incByDay)[1:2] = c( "violent.FALSE", "violent.TRUE")
  incByDay[,"Date"] = as.Date(rownames(incByDay), format="%Y-%m-%d")
  
  return(incByDay)
}
CrimesByHour = function(incidents){
  
  incByHour=by(incidents$violent, list(incidents$HrOfDay), FUN = table )  
  incByHour = as.data.frame(do.call("rbind",incByHour))
  colnames(incByHour)[1:2] = c( "violent.FALSE", "violent.TRUE")
  incByHour[,"Hour"] = as.numeric(rownames(incByHour))
  
  return(incByHour)
}
CrimesByDayOfWeek = function(
  incidents,
  DoW=c("Friday","Saturday","Sunday","Monday","Tuesday","Wednesday","Thursday"),
  verbose=0
){
  
  incByDayOfWeek=by(incidents$violent, list(incidents$DayOfWeek), FUN = table )  
  incByDayOfWeek = as.data.frame(do.call("rbind",incByDayOfWeek))
  colnames(incByDayOfWeek)[1:2] = c( "violent.FALSE", "violent.TRUE")
  incByDayOfWeek = incByDayOfWeek[DoW,]
  incByDayOfWeek[,"DoW"] = DoW
  
  incByDayOfWeek[,"violentRate"] = 100*incByDayOfWeek[,"violent.TRUE"]/rowSums(incByDayOfWeek[,c("violent.TRUE","violent.FALSE")])
  incByDayOfWeek[,"dayofWeek"] = factor(incByDayOfWeek$DoW, levels = DoW) 
  
  return(incByDayOfWeek)
}
CrimesByDistrict = function(
  incidents,
  verbose=0
){
  
  incByDistrict=by(incidents$violent, list(incidents$PdDistrict), FUN = table )  
  incByDistrict = as.data.frame(do.call("rbind",incByDistrict))
  colnames(incByDistrict)[1:2] = c( "violent.FALSE", "violent.TRUE")
  incByDistrict[,"PdDistrict"] = rownames(incByDistrict)
  
  return(incByDistrict)
}
################The above was simple tabulation. From here one we use kd trees to aggregate in space:

CrimesByCensusBlock = function(
  incidents,
  SFpolys,
  colName="CensusBlock",
  smoothRate = list("epiR",10,"naive")[[1]],
  verbose=0
){
  
  incByCensusBlock=by(incidents$violent, list(incidents[,colName]), FUN = table )  
  incByCensusBlock = as.data.frame(do.call("rbind",incByCensusBlock))
  colnames(incByCensusBlock)[1:2] = c( "violent.FALSE", "violent.TRUE")
  incByCensusBlock[,"CensusBlock"] = rownames(incByCensusBlock)
  
  
  PIDS2keep=which(SFpolys$data[,"fips"] %in% rownames(incByCensusBlock));#1:nrow(SFpolys$data)
  #take PID=197 out as it seem like the top right polygon:
  PIDS2keep = PIDS2keep[-which(PIDS2keep==197)]
  polys2keep = which(SFpolys$polys[,"PID"] %in% PIDS2keep)
  polys = SFpolys$polys[polys2keep,]
  polyCenters= SFpolys$polyCenters[polys2keep,c("X","Y")]
  
  incByCensusBlock=incByCensusBlock[SFpolys$data[PIDS2keep,"fips"],]
  #incByCensusBlock[,"blockArea"] = NA
  #for (i in 1:nrow(incByCensusBlock)) incByCensusBlock[,"blockArea"] = 
  #  incByCensusBlock[,"blockPop"] = NA
  
  incByCensusBlock[,"totCrimes"] = rowSums(incByCensusBlock[,1:2])
  
  obs =incByCensusBlock[,"violent.TRUE"]
  pop = incByCensusBlock[,"totCrimes"]
  OverallRate = sum(obs)/sum(pop) 
  if (smoothRate == "naive"){
    incByCensusBlock[,"violentRate"] = 100*obs/pop
  } else if (smoothRate == "epiR") {
    #some empirical Bayes type smoothing:
    require(epiR)
    est <- epi.empbayes(obs, pop)
    incByCensusBlock[,"violentRate"] = 100*(obs + est[4]) / (pop + est[3])
  } else if (is.numeric(smoothRate)) {
    incByCensusBlock[,"violentRate"] = 100*(obs+smoothRate*OverallRate)/(pop+smoothRate)
  }
  return(list(incByCensusBlock=incByCensusBlock, polys=polys))
}

FetchManyYears = function(
  YEARS = 2003:2013,##<< which years to load
  file = "data/incByDay.rda" ##<< file to save results to
){
  i = 1;incByDay=list()
  for (year in YEARS) {
    crimes = AugmentIncidents(file=paste0("d:/Data/SFcrimeData/sfpd_incident_all_csv/sfpd_incident_",year,".csv"))
    incByDay[[i]] = CrimesByDay(crimes)
    cat("done with ", year, "\n")
    i = i +1
  }
  incByDay = do.call("rbind", incByDay)
  incByDay[,"AllCrimes"] = rowSums(incByDay[,1:2])
  rmRows = which(incByDay[,"AllCrimes"]<100)
  incByDay = incByDay[-rmRows,]
  incByDay[,"violentRate"] = 100*incByDay[,"violent.TRUE"]/incByDay[,"AllCrimes"]
  if (!is.null(file)) save(incByDay, file = file)
  return(incByDay)
}

FetchInterval = function(
  from = as.Date("2005-12-18"),##<< from which date
  to = as.Date("2006-01-03"),##<< from which date
  file = NULL ##<< file to save results to
){
  i = 1;crimes=list()
  YEARS = (as.numeric(format(from, "%Y"))):(as.numeric(format(to, "%Y")))
  for (year in YEARS) {
    crimes[[i]] = AugmentIncidents(file=paste0("d:/Data/SFcrimeData/sfpd_incident_all_csv/sfpd_incident_",year,".csv"))
    keepRows = crimes[[i]]$Date >= from & crimes[[i]]$Date <= to;
    crimes[[i]] =  crimes[[i]][keepRows,]
    cat("done with ", year, "\n")
    i = i +1
  }
  crimes = do.call("rbind", crimes)
  return(crimes)
}