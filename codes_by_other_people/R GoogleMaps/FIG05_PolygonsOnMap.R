########Figure 5##########################
incidents=AddCensusBlock(incidents, SFpolys)
incByCensusBlock=CrimesByCensusBlock(incidents, SFpolys)

Figure.CrimesByCensusBlock = function(){
  ColorMap(incByCensusBlock[[1]][,"violentRate"], map=SFzoom13, polys = incByCensusBlock$polys, alpha = 0.3, 
           add=F, nclr=4, brks = seq(5,25,length=5), round = 2)
}

png("Figures/CrimesByCensusBlock.png", width=640, height=640)
par(cex=1.5)
Figure.CrimesByCensusBlock()
dev.off()
