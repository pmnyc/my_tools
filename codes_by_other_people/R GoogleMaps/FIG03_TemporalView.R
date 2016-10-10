########Figure 3 top##########################
load(file = "data/incByDay.rda")
# d = ggplot(incByDay, aes(x=Date)) + geom_line(aes(y = AllCrimes/10, colour = "AllCrimes/10"))+
#   geom_line(aes(y = violentRate, colour = "violentRate")) #+ scale_y_continuous(trans=log10_trans())
# theme_update(legend.position = c(0.85,0.85), legend.title = element_blank(),axis.title.y=element_blank())
# #print(d)
# pdf("Figures/SeasonalTrend.pdf", width=7, height=4, version = "1.4")
# print(d)
# dev.off()

library(zoo)
incByDayTS = zoo(incByDay[,-which(colnames(incByDay)=="Date")], incByDay$Date)
incByDayTSrm = rollmean(incByDayTS, k= 60)
#plot(incByDayTS[,c("AllCrimes","violentRate")], col = c("darkgreen", "darkred"), xlab = "")

#manual plotting:
Figure.CrimeTrend = function(){
  par(mar=c(3,4,1,5)+.1)
  plot(incByDay$Date, incByDay$AllCrimes, type="l", col = "darkgreen", xlab = "", 
       ylab ="", ylim = c(0,600))
  lines(index(incByDayTSrm), coredata(incByDayTSrm)[,"AllCrimes"],col="black",lwd=1.5)
  mtext("Crimes per day",side=2,line=2, col="darkgreen")
  abline(h=400, col = "lightgray", lty = "dotted")
  #grid(nx=NA,ny=NULL)
  par(new=TRUE)
  plot(incByDay$Date, incByDay$violentRate,type="l",col="darkred",xaxt="n",
       yaxt="n",xlab="",ylab="", ylim = c(5,50))
  lines(index(incByDayTSrm), coredata(incByDayTSrm)[,"violentRate"],col="black",lwd=1.5)
  axis(4, at = c(10,15,20))
  mtext("violent Rate [%]",side=4,line=2, col="darkred")
  for (i in 0:10) abline(v=as.Date("2003-01-01")+365*i,col = "lightgray", lty = "dotted")
  abline(h=10, col = "lightgray", lty = "dotted")
  #legend("topleft",col=c("red","blue"),lty=1,legend=c("y1","y2"))
}
pdf("Figures/SeasonalTrend.pdf", width=9, height=3, version = "1.4")
Figure.CrimeTrend()
dev.off()


########Figure 3 bottom##########################
require(mgcv)
TimeOfWeekModelGAM = bam(violent ~ s(HourOfWeek, k=60,  bs = "cc") , data=incidents, family=binomial(link="logit"))

Figure.RateHrOfWeek = function(main = "violence, hour of week dependency"){
  par(mar=c(3.5,4,4,1.5))
  plot(TimeOfWeekModelGAM, trans=InvLogit, ylab="multiplicative effect", 
       main = main,xaxt="n", lwd = 1.7, col = "darkblue",
       shade = TRUE, shade.col=rgb(0.5,0,0,0.5), xlab = "")
  axis(1,at=seq(12,by=24,length=7))
  abline(v=seq(24,by=24,length=6), col = "green")
  abline(h=1, col = "purple")
  grid()
  
  for (j in 1:7) mtext(substring(DoW, 1,3)[j], side=3, at =seq(12,by=24,length=7)[j], col = "green")
  mtext("hour of week",side =1, line=2)
}
#pdf("Figures/RateHrOfWeek.pdf", width=8, height=3.5, version = "1.4")
Figure.RateHrOfWeek()
#dev.off()
