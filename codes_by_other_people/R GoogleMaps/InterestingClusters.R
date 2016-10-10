if (0) {
  drugPhrases=c("opium","methadone","marijuana","hallucinogenic","heroin",
                "opiates","cocaine","amphetamine","drugs", "narcotics","controlled substance")
  robbery = c("robbery")
  burglary = c("burglary")
  bicycles="bicycles"
  PeopleMissing = c("missing")
  drugCrimes = FilterCrimes(2007:2013, KeyWords=drugPhrases, file = "data/drugCrimes.rda")
  robberyCrimes = FilterCrimes(2007:2013, KeyWords=robbery, file = "data/robberyCrimes.rda")
  burglaryCrimes = FilterCrimes(2007:2013, KeyWords=burglary, file = "data/burglaryCrimes.rda")
  missingCrimes = FilterCrimes(2007:2013, KeyWords=PeopleMissing, file = "data/missingCrimes.rda")
  
  drugPolys = PlotCrimeClusters("data/drugCrimes.rda", TRUE)
  #PlotCrimeClusters("data/drugCrimes.rda", TRUE, polys = drugPolys)
  drugPolysRel = PlotCrimeClusters("data/drugCrimes.rda", FALSE)
  #PlotCrimeClusters("data/drugCrimes.rda", TRUE, polys = drugPolysRel)
  robberyPolys = PlotCrimeClusters("data/robberyCrimes.rda", TRUE)
  #PlotCrimeClusters("data/robberyCrimes.rda", TRUE, polys = robberyPolys)
  burglaryPolys = PlotCrimeClusters("data/burglaryCrimes.rda", TRUE)
  burglaryPolysRel = PlotCrimeClusters("data/burglaryCrimes.rda", FALSE)
  
  
    TimeOfWeekModelGAM = bam(violent ~ s(HourOfWeek, k=60,  bs = "cc") , data=crimes, family=binomial(link="logit"))
    Figure.RateHrOfWeek(main="burglaries")
     
  load("data/drugCrimes.rda")
  PlotCrimes(SFzoom12, incidents=crimes, polys=NULL, cex = 0.45, alpha = 0.4)
  PlotCrimes(SFMap, incidents = subset(crimes, violent == TRUE), polys = NULL, cex = 0.45, alpha =0.4)
  
             
  polys = FindClusters(crimes,DENS=FALSE, OR2=0,OR1=1.2,minArea=10,maxArea=1000)
  polys = FindClusters(subset(crimes, violent == TRUE),DENS=TRUE, OR2=0,OR1=1.2,minArea=10,maxArea=1000)
  
  polys2 = polys[1:50,];#top ten clusters #subset(polys, yval>5)
  yval=round(polys2[polys2[,"POS"]==1,"yval"],1)
  ColorMap(yval, SFzoom13, polys2, add = FALSE, alpha = 0.35, log = FALSE,
           include.legend = list(FALSE), textInPolys=yval)
}
    
PlotCrimeClusters = function(crimeFile="data/drugCrimes.rda",DENS=FALSE, polys, 
                             map = SFzoom13, topClus=10){
  
  #PlotCrimes(SFzoom12, incidents=crimes, polys=NULL, cex = 0.45, alpha = 0.4)
  #PlotCrimes(SFMap, incidents = subset(crimes, violent == TRUE), polys = NULL, cex = 0.45, alpha =0.4)
  
  if (missing(polys)) {
    load(crimeFile)
    crimes$violent = as.logical(crimes$violent)
    if (DENS) crimes = subset(crimes, violent == TRUE)
    polys = FindClusters(crimes,DENS=DENS, OR2=0,OR1=1.2,minArea=10,maxArea=1000)
  }
  #polys = FindClusters(subset(crimes, violent == TRUE),DENS=TRUE, OR2=0,OR1=1.2,minArea=10,maxArea=1000)
  
  topClus = min(c(topClus, nrow(polys)/5))
  polys2 = polys[1:(5*topClus),];#top ten clusters #subset(polys, yval>5)
  yval=round(polys2[polys2[,"POS"]==1,"yval"],1)
  #browser()
  ColorMap(yval, map, polys2, add = FALSE, alpha = 0.35, log = FALSE,
           include.legend = list(FALSE), textInPolys=yval)
  
  invisible(polys)
}
FilterCrimes = function(
  YEARS = 2003:2013,##<< which years to load
  KeyWords = c("opium"),##<< which phrases to grep for in the Descript column
  Nran = 5000, ##<< how many random "background" cases to extract
  file = "data/drugCrimes.rda" ##<< file to save results to
){
  i = 1;crimes=list()
  for (year in YEARS) {
    incidents = AugmentIncidents(file=paste0("d:/Data/SFcrimeData/sfpd_incident_all_csv/sfpd_incident_",year,".csv"))
    N=nrow(incidents)
    #browser()
    incidents[,"MATCH"]=0
    if (length(KeyWords)>1) KeyWords=paste(KeyWords, collapse = "|")
    matchedRows=grep(KeyWords, incidents$Descript, ignore.case=TRUE)
    incidents[matchedRows,"MATCH"]=1
    ranRows = sample((1:N)[-matchedRows], Nran)
    crimes[[i]] = incidents[c(matchedRows,ranRows),]
    cat("done with ", year, "\n")
    i = i +1
  }
  crimes = do.call("rbind", crimes)
  crimes[,"violent"] = crimes[,"MATCH"]
  if (!is.null(file)) save(crimes, file = file)
  return(crimes)
}

