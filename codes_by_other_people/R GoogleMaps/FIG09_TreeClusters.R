# 
#   drugPhrases=c("opium","methadone","marijuana","hallucinogenic","heroin",
#               "opiates","cocaine","amphetamine","drugs", "narcotics","controlled substance")
# robbery = c("robbery")
# burglary = c("burglary")
# bicycles="bicycles"
# PeopleMissing = c("missing")
# drugCrimes = FilterCrimes(2007:2013, KeyWords=drugPhrases, file = "data/drugCrimes.rda")
# robberyCrimes = FilterCrimes(2007:2013, KeyWords=robbery, file = "data/robberyCrimes.rda")
# burglaryCrimes = FilterCrimes(2007:2013, KeyWords=burglary, file = "data/burglaryCrimes.rda")
# missingCrimes = FilterCrimes(2007:2013, KeyWords=PeopleMissing, file = "data/missingCrimes.rda")
# 
# drugPolys = PlotCrimeClusters("data/drugCrimes.rda", TRUE)
# #PlotCrimeClusters("data/drugCrimes.rda", TRUE, polys = drugyPolys)
# drugPolysRel = PlotCrimeClusters("data/drugCrimes.rda", FALSE)
# robberyPolys = PlotCrimeClusters("data/robberyCrimes.rda", TRUE)
# #PlotCrimeClusters("data/robberyCrimes.rda", TRUE, polys = robberyPolys,map = SFzoom13)
# robberyPolysRel = PlotCrimeClusters("data/robberyCrimes.rda", FALSE)
# #PlotCrimeClusters("data/robberyCrimes.rda", FALSE, polys = robberyPolysRel,map = SFzoom13)
# 
# burglaryPolys = PlotCrimeClusters("data/burglaryCrimes.rda", TRUE)
# #PlotCrimeClusters("data/robberyCrimes.rda", TRUE, polys = burglaryPolys)
# burglaryPolysRel = PlotCrimeClusters("data/burglaryCrimes.rda", FALSE)
# #PlotCrimeClusters("data/robberyCrimes.rda", FALSE, polys = burglaryPolysRel, map = )

drugPolys = PlotCrimeClusters("data/drugCrimes.rda", TRUE)

png("Figures/DrugCrimes.png", width=640, height=640)
par(cex=1.5)
PlotCrimeClusters("data/drugCrimes.rda", TRUE, polys = drugPolys, map = SFzoom14, topClus=6)
dev.off()

robberyPolys = PlotCrimeClusters("data/robberyCrimes.rda", TRUE)
png("Figures/RobberyCrimes.png", width=640, height=640)
par(cex=1.5)
PlotCrimeClusters("data/robberyCrimes.rda", TRUE, polys = robberyPolys, map = SFzoom14)
dev.off()
