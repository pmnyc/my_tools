FetchCrimeData =function(incidents, endDate, K=100, file="incidents.rda", verbose=0){
  if(missing(incidents)){
    if (0) {
      incidents = read.table("Sfpd_Incident_Last_Month.csv.gz", header=T, sep=",", 
                             as.is=T)
    } else {
      incidents=read.csv(url("http://data.sfgov.org/resource/tmnf-yvry.csv?$limit=1000&$offset=0"), stringsAs=FALSE)
      if (missing(endDate)){
        for (o in seq(1000,by=1000,length=K)){
          tmp = read.csv(url(paste0("http://data.sfgov.org/resource/tmnf-yvry.csv?$limit=1000&$offset=",o)), stringsAs=FALSE)
          incidents=rbind(incidents,tmp)
        }
      } else {
        incidents$Date = as.Date(as.character(incidents$Date), "%m/%d/%Y")
        o=1000
        while(tail(incidents$Date,1)>endDate){
          tmp = read.csv(url(paste0("http://data.sfgov.org/resource/tmnf-yvry.csv?$limit=1000&$offset=",o)))
          tmp$Date = as.Date(tmp$Date, "%m/%d/%Y")
          incidents=rbind(incidents,tmp)
          o=o+1000
        }
      }
    }
  }
}

AugmentIncidents =function(incidents, 
                           file="d:/Data/sfpd_incident_all_csv/sfpd_incident_2012.csv", 
                           DoW=c("Friday","Saturday","Sunday","Monday","Tuesday","Wednesday","Thursday"),
                           verbose=0
){
  if (missing(incidents)) incidents=read.csv(file, stringsAs=FALSE)
  
  if (class(incidents$Date) !="Date") 
     incidents$Date = as.Date(incidents$Date, "%m/%d/%Y")
  
  # Create violent indicator
  incidents$violent = with(incidents, 
                           Category %in% c("ASSAULT", "ROBBERY", 
                                           "SEX OFFENSES, FORCIBLE", "KIDNAPPING") 
                           | Descript %in% 
                             c("GRAND THEFT PURSESNATCH", 
                               "ATTEMPTED GRAND THEFT PURSESNATCH"))
  incidents$violent=factor(incidents$violent, levels=c(FALSE, TRUE))
  DoWLookup=0:6;names(DoWLookup) = DoW
  incidents$HrOfDay = substr(incidents$Time, 1,2)
  incidents$TimeOfDay = as.numeric(incidents$HrOfDay)+as.numeric(substr(incidents$Time, 4,5))/60
  incidents$HourOfWeek = incidents$TimeOfDay + DoWLookup[incidents$DayOfWeek]*24
  incidents$DayOfWeek = factor(incidents$DayOfWeek, levels = DoW)
  PhaseOfWeek=DoW;names(PhaseOfWeek) = DoW;PhaseOfWeek[4:7] = "Mon-Thu"
  incidents$PhaseOfWeek = factor(PhaseOfWeek[incidents$DayOfWeek], levels = PhaseOfWeek[1:4])
  
  #incidents = AddCensusBlock(incidents)
  
  if(verbose){
    hist(incidents$NumTime)
    barplot(table(incidents$DayOfWeek)[DoW],las=2)  
  }
  
  #if(!is.null(file)) save(incidents, file = file)
  return(incidents)
  
}
#incidents=FetchCrimeData(incidents, file = NULL, verbose=1)

if (0){
 
  incidents=read.csv(url("http://data.sfgov.org/resource/tmnf-yvry.csv?$limit=1000&$offset=0"), stringsAs=FALSE)
  incidents$Date = as.Date(incidents$Date, "%m/%d/%Y")
  
  
    for (o in seq(1000,by=1000,length=K)){
      tmp = read.csv(url(paste0("http://data.sfgov.org/resource/tmnf-yvry.csv?$limit=1000&$offset=",o)), stringsAs=FALSE)
      tmp$Date = as.Date(tmp$Date, "%m/%d/%Y")
      incidents=rbind(incidents,tmp)
      print(min(incidents$Date))
    }
  
}