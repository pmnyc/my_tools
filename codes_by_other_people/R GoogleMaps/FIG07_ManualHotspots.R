########Figure 7a##########################
HotSpot1 = PointsInRect(BBOX=SFzoom17$BBOX, x=incidents[,ImpCols])
#PlotOnStaticMap(SFzoom17, lat=c(37.77472,37.77568), lon=c(-122.4041,-122.4033), col = "red", pch=20, cex=3, add=TRUE)
HotSpot1small = PointsInRect(XLIM=c(-122.4041,-122.4033), YLIM =c(37.77472,37.77568), x=HotSpot1)
HotspotTimeOfDayModelGAM = gam(violent ~ s(TimeOfDay,bs = "cc"), data=HotSpot1small, family=binomial(link="logit"))

Figure.Hotspot1 = function(CrimeCatsOverlay = FALSE){
  #identify the very compact hotspot right at the bend of highway I-80
  #LatLonPt = IdentifyPoints(SFMap)
  #  lat       lon
  #37.77525 -122.4038
  LatLonPt = c(lat=37.77525, lon=-122.4038)
  PlotCrimes(SFzoom17, incidents=jitterLatLon(HotSpot1, sd=0.0001), polys=NULL, cex = 0.45, alpha = 100)
  #locator(2)
  #par(fig=c(x_left, x_right, y_bottom, y_top), new = T)
  figOld=par("fig")
  par(fig=(320+c(16, 16+150, 35, 35+100))/640, new = T)
  plot(HotspotTimeOfDayModelGAM, trans=InvLogit, ylab="", lwd = 2, col = "blue", shade = TRUE,shade.col= rgb(0.75,0,0,0.3))
  if (CrimeCatsOverlay) {
    CrimeCats = sort(table(HotSpot1small[,"Category"]), decreasing = TRUE)
    par(fig=(320+c(-265, -265+220, -160, -160+170))/640, mar = c(0,7,0,0), new = T)
    barplot(CrimeCats[1:8], horiz=TRUE, las=1,col = "bisque", border = "darkgreen", cex.names = 0.9, col.axis="darkblue")
  }
  par(fig=figOld)
}

########Figure 7b##########################
Hotspot2 = PointsInRect(BBOX=SFzoom16$BBOX, x=incidents[,ImpCols])
#PlotOnStaticMap(SFzoom16, lat=c(37.77472,37.77568), lon=c(-122.4041,-122.4033), col = "red", pch=20, cex=3, add=TRUE)
#Hotspot2small = PointsInRect(XLIM=c(-122.4041,-122.4033), YLIM =c(37.77472,37.77568), x=Hotspot2)
HotspotTimeOfDayModelGAM = gam(violent ~ s(TimeOfDay,bs = "cc"), data=Hotspot2, family=binomial(link="logit"))

Figure.Hotspot2 = function(CrimeCatsOverlay=FALSE, Hotspot){
  #identify the longer hotspot on Mission Street
  #LatLonPt = IdentifyPoints(SFMap)
  #           lat       lon
  # 37.76502 -122.4198
  LatLonPt = c(lat=37.76502, lon=-122.4198)
  #get another map centered around that hotspot with a high zoom level:
  #SFzoom16 <- GetMap(center=LatLonPt, destfile = "mapTiles/SFHotspot2.z16.png", GRAYSCALE=FALSE, zoom = 16, SCALE = 2);
  PlotCrimes(SFzoom16, incidents=jitterLatLon(Hotspot, sd=0.0001), polys=NULL, cex = 0.45, alpha = 100)
  #locator(2)
  #par(fig=c(x_left, x_right, y_bottom, y_top), new = T)
  figOld=par("fig")
  par(fig=(320+c(40, 40+150, 50, 50+100))/640, new = T)
  plot(HotspotTimeOfDayModelGAM, trans=InvLogit, ylab="", lwd = 2, col = "blue", shade = TRUE,shade.col= rgb(0.75,0,0,0.3))
  if (CrimeCatsOverlay) {
    CrimeCats = sort(table(Hotspot[,"Category"]), decreasing = TRUE)
    par(fig=(320+c(-275, -275+180, 160, 160+150))/640, mar = c(0,7,0,0), new = T)
    barplot(CrimeCats[1:8], horiz=TRUE, las=1,col = "bisque", border = "darkgreen", cex.names = 0.9, col.axis="purple")
  }
  par(fig=figOld)
}



png("Figures/Hotspot1.png", width=640, height=640)
Figure.Hotspot1()
dev.off()

png("Figures/Hotspot2.png", width=640, height=640)
Figure.Hotspot2(FALSE, Hotspot2[sample(nrow(Hotspot2), 4000),])
dev.off()
