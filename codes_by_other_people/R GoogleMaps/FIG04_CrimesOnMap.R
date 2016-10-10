########Figure 4##########################

Figure.CrimesOnMap = function(crimes=incidents, map =SFMap, N = c(10000,5000),cols, cex = 0.45){
  if (is.null(N) | sum(N) > nrow(crimes)) ranPts = 1:nrow(crimes) 
  else  {
    if (length(N)==1)
      ranPts = sample(nrow(crimes), N)
    else {
      ranPts1 = sample(which(as.numeric(crimes$violent)==1), N[1])
      ranPts2 = sample(which(as.numeric(crimes$violent)==2), N[2])
      ranPts = sample(c(ranPts1,ranPts2))
    }
  }
  PlotCrimes(map, incidents=jitterLatLon(crimes[ranPts,]), polys=NULL, cex = cex, alpha = 0.4,cols=cols)
}

png("Figures/CrimesOnMap.png", width=1280, height=1280)
colViolent=rgb(240/255,0,0,0.4)
colNonViolent=rgb(0,220/255,220/255,0.4)
Figure.CrimesOnMap(map=SFzoom13,cols = c(colNonViolent,colViolent), N = c(30000,15000),cex=1.55)
legend("topright", col = c(colNonViolent,colViolent), pch=20, 
       legend = c("N","Y"), title="violent", cex = 2.5)
dev.off()

# #yellow-red
# Figure.CrimesOnMap(map=SFzoom13,cols = brewer.pal(9,"Set1")[c(6,1)])
# #purple-red
# dev.off()
# Figure.CrimesOnMap(map=SFzoom13,cols = brewer.pal(9,"Set1")[c(4,1)])
# #orange-red
# dev.off()
# Figure.CrimesOnMap(map=SFzoom13,cols = brewer.pal(9,"Set1")[c(5,1)])
# #green-red
# dev.off()
# Figure.CrimesOnMap(map=SFzoom13,cols = brewer.pal(9,"Set1")[c(3,1)])
# #brown-red
# dev.off()
# Figure.CrimesOnMap(map=SFzoom13,cols = brewer.pal(9,"Set1")[c(7,1)])
# 
#dev.off()
