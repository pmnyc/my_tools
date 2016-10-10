TestRotation = function(x, angles = c(0,30,45,60), OVERLAY=FALSE){
#   for (a in angles[-1]) {
#     theta = pi*(a/180)
#     #rotate data:
#     R = rbind(c(cos(theta), -sin(theta)),c(sin(theta), cos(theta)));
#     x=cbind(X=c(1,1),Y=c(0,1))
#     xRot = t(R %*% t(x))
#     cat("angle ", a,"\n"); print(round(xRot,3))
#     xRot = t(t(R) %*% t(xRot))
#     print(round(xRot,3))
#   }
#   return();
  require(tree)
  if (missing(x)){
    N= 250
    x1 = cbind.data.frame(X=runif(N),Y=runif(N), violent = 0)
    x2 = cbind.data.frame(X=runif(N,0.4,0.6),Y=runif(N,0.4,0.6), violent = 1)
    x = rbind.data.frame(x1,x2)
  }
  N = nrow(x)
  #xM = colMeans(x[,c("X","Y")])
  #x[,c("X","Y")] = as.data.frame(sweep(x[,c("X","Y")],2, xM))
  
  for (a in angles) {
    theta = pi*(a/180)
    rotX = x
    #rotate data:
    R = rbind(c(cos(theta), -sin(theta)),c(sin(theta), cos(theta)));
    if (theta!=0) {
      rotX[,c("X","Y")] = as.data.frame(t(R %*% t(as.matrix(x[,c("X","Y")]))))
      colnames(rotX) = colnames(x)
    } 
    rotX <<- rotX
    v = rotX[,"violent"]
    fit =tree(violent ~ X+Y, data = rotX)
    plot(rotX[,c("X","Y")], pch=20, col = rgb(v,0,1-v,0.5), cex = 0.7 ,
         main = paste("angle ", a), ylim=c(-0.8,1.4), xlim=c(-0.8,1.4) )
    #abline(v=0,col="red");abline(h=0,col="red")
    abline(a=0,b=1,col="red")
    
    if (OVERLAY) partition.tree(fit, ordvars=c("X","Y"), add= TRUE)
    #ret=readLines(n=1)
    #rotate them back:
    rotX2 = rotX
    if (theta!=0) rotX2[,c("X","Y")] = t(t(R) %*% t(as.matrix(rotX[,c("X","Y")])))
    #plot(rotX[,c("X","Y")], pch=20, col = rgb(0,0,1,0.5), cex = 0.7,main = paste("angle ", a) )
    #abline(v=0,col="red");abline(h=0,col="red")
    cat("angle ", a, ", mse:", round(mean((rotX2[,c("X","Y")]-x[,c("X","Y")])^2),3),"\n")
    
  }
}

FindClusters = function(x=incidents, 
                        angles = c(0,30,45,60),
                        minsize = 200,
                        minArea=20,
                        maxArea=250,
                        OR1=1.8,
                        OR2=0.1,
                        DENS = FALSE,
                        joinIntersect = TRUE,
                        verbose=0
){
  #x = x[,c("X","Y","violent")];
  #xM = colMeans(x[,c("X","Y")])
  #x[,c("X","Y")] = as.data.frame(sweep(x[,c("X","Y")],2, xM))
  N = nrow(x)
  if (DENS) {#find density clusters!
    rX = range(x$X)
    rY = range(x$Y)
    xBckg = cbind.data.frame(X=runif(3*N, rX[1], rX[2]), Y=runif(3*N, rY[1], rY[2]), violent=FALSE)
    x[,"violent"]=TRUE
    x = rbind(x[,c("X","Y","violent")],xBckg)
    x[,"violent"]= as.logical(x[,"violent"])
  }
  polys = list()
  #if (theta ==0) BoundBox = Rect2PBSpolys(xy[1,,drop=F])
  Xr=range(x[,"X"])
  Yr=range(x[,"Y"])
  yv = mean(x[,"violent"],na.rm=T)
  BoundBox = Rect2PBSpolys(matrix(c(Xr[1],Yr[1], Xr[2],Yr[2], yv),nrow=1, 
                          dimnames=list(NULL,c("xleft","ybottom", "xright","ytop", "yval"))))
  
  #browser()
  for (a in angles) {
    if (verbose) cat("angle: ", a, "\n")
    theta = pi*(a/180)
    rotX = x
    #rotate data:
    R = rbind(c(cos(theta), -sin(theta)),c(sin(theta), cos(theta)));
    if (theta!=0) {
      rotX[,c("X","Y")] = as.data.frame(t(R %*% t(as.matrix(x[,c("X","Y")]))))
      colnames(rotX) = colnames(x)
    } 
    #This is a bug in tree.model.frame which seems to search for the data in the global environment
    rotX <<- rotX
    rotPolys = getHotspots(xy, rotX,minsize, minArea, maxArea,OR1,OR2, verbose)
    #browser()
    #rotate them back:
    if (theta!=0) rotPolys[,c("X","Y")] = t(t(R) %*% t(as.matrix(rotPolys[,c("X","Y")])))
    polys[[as.character(a)]] = rotPolys
  }
  #add the column means back:
  polys = do.call("rbind", polys)
  #polys[,c("X","Y")] = sweep(polys[,c("X","Y")],2, xM, "+")
  #correct the PIDs:
  NumPolys = nrow(polys)/5
  polys[,"PID"] = rep(1:NumPolys, each = 5)
  
  polys=CleanUpPolys(polys, BoundBox);
  
  return(polys)
}

getHotspots =function(xy,
                      rotX,
                      minsize = 200,
                      minArea=20,
                      maxArea=250,
                      OR1=1.8,
                      OR2=0.1,
                      verbose=1
) {
  fit =tree(violent ~ X+Y, data = rotX, mindev=0.000275, minsize = minsize)
  
  xy=TreePartition(fit,ordvars=c("X","Y"))
  if (verbose) cat("overall avg:", xy[1,"yval"], "\n")
  if (verbose>1) {
    browser()
    partition.tree(fit)
    #point to the cluster outside 
    getGeoCode("850 Bryant Street, San Francisco")
    points(-122.4038,37.7753, col = "red", pch=20)
  }
  if (1) {
    #correct the extreme values 0 and 1:
    xy[xy[,"yval"]> 0.999,"yval"] = 0.999
    xy[xy[,"yval"]< 0.01,"yval"] = 0.01
    #change class percentage to OR
    xy[,"yval"]=xy[,"yval"]/(1-xy[,"yval"])
    xy[,"yval"]=xy[,"yval"]/xy[1,"yval"]
  }
  OR = xy[,"yval"]/xy[1,"yval"]
  #browser()
  
  HotSpots = which( (OR>OR1 | OR < OR2) & (xy[,"area"]>minArea & xy[,"area"]<maxArea))
  rotPolys = Rect2PBSpolys(xy[HotSpots,,drop=F])
  return(rotPolys)
}
CleanUpPolys = function(polys, BoundBox, minAutonFrac = 0.9, maxOL=0.15){
NumPolys = nrow(polys)/5
  polys[,"PID"] = rep(1:NumPolys, each = 5)
  
  polyList = split(polys, polys[,"PID"])
  yvals = sapply(polyList, function(x) return(max(x$yval)))
  #sort them by yval:
  ix = order(yvals, decreasing=TRUE)
  polyList = polyList[ix]
  for (i in 1:length(polyList)) polyList[[i]][,"PID"] = i
  activePolys = c(1)
  for (i in 2:length(polyList)) {
    if (PolyOverlap(BoundBox,polyList[[i]])[2] > minAutonFrac){ 
      pF=rep(NA,length(activePolys));k=1
      for (j in activePolys){
        pF[k]=PolyOverlap(polyList[[j]],polyList[[i]])[2]
        k=k+1
      }
      #if less than 15% overlap, count as a polygon on its own
      if (max(pF,na.rm=TRUE)<= maxOL) activePolys = c(activePolys,i)
    }
  }
  polys = do.call("rbind", polyList[activePolys])
  return(polys)
}

PolyOverlap = function(polysA,polysB){
  polysC = try(joinPolys(polysA,polysB,operation="INT"),silent=TRUE)#from PBSmapping
  if (class(polysC)[1] =="try-error" | is.null(polysC) ) return(c(0,0))
  #print(class(polysC))
  #browser()
  areaIntersect = calcArea(polysC)[,"area"]
  OverlappolysA = areaIntersect/calcArea(polysA)[,"area"]
  OverlappolysB = areaIntersect/calcArea(polysB)[,"area"]
  return(c(OverlappolysA,OverlappolysB))
}

TreePartition = function (tree, label = "yval", add = FALSE, ordvars, ndigits=3, verbose=0, ...) 
{
  LeafRectangles <- function(x, v, xrange, xcoord = NULL, ycoord = NULL, 
                             tvar, i = 1L, xrangeAll = NULL, verbose=0) {
    if (verbose>1) browser()
    if (v[i] == "<leaf>") {
      y1 <- (xrange[1L] + xrange[3L])/2
      y2 <- (xrange[2L] + xrange[4L])/2
      if (verbose){
        cat("leaf:", i, xrange, "\n")
        rn=runif(3)
        COL=rgb(rn[1],rn[2],rn[3]);
        rect(xleft=xrange[1L], ybottom=xrange[2L], xright=xrange[3L], ytop=xrange[4L], col = COL)
      }
      xrangeAll = c(xrangeAll,xrange)
      return(list(xcoord = xcoord, ycoord = c(ycoord, y1, y2), i = i,xrangeAll=xrangeAll))
    }
    if (v[i] == tvar[1L]) {
      xcoord <- c(xcoord, x[i], xrange[2L], x[i], xrange[4L])
      xr <- xrange
      xr[3L] <- x[i]
      #xrangeAll = c(xrangeAll,xr)
      ll2 <- Recall(x, v, xr, xcoord, ycoord, tvar, i + 1L, xrangeAll)
      xr <- xrange
      xr[1L] <- x[i]
      #xrangeAll = c(ll2$xrangeAll,xr)
      #cat(v[i], i, xr,  "\n")
      return(Recall(x, v, xr, ll2$xcoord, ll2$ycoord, tvar, 
                    ll2$i + 1L,ll2$xrangeAll))
    }
    else if (v[i] == tvar[2L]) {
      xcoord <- c(xcoord, xrange[1L], x[i], xrange[3L], 
                  x[i])
      xr <- xrange
      xr[4L] <- x[i]
      #xrangeAll = c(xrangeAll,xr)
      ll2 <- Recall(x, v, xr, xcoord, ycoord, tvar, i + 1L,xrangeAll)
      xr <- xrange
      xr[2L] <- x[i]
      #xrangeAll = c(ll2$xrangeAll,xr)
      #cat(v[i], i, xr,  "\n")
      return(Recall(x, v, xr, ll2$xcoord, ll2$ycoord, tvar, 
                    ll2$i + 1L,ll2$xrangeAll))
    }
    else stop("wrong variable numbers in tree.")
  }  ###########end of function########################################################
   
  if (inherits(tree, "singlenode")) 
        stop("cannot plot singlenode tree")
    if (!inherits(tree, "tree")) 
        stop("not legitimate tree")
    frame <- tree$frame
    leaves <- frame$var == "<leaf>"
    var <- unique(as.character(frame$var[!leaves]))
    if (length(var) > 2L || length(var) < 1L) 
        stop("tree can only have one or two predictors")
    nlevels <- sapply(attr(tree, "xlevels"), length)
    if (any(nlevels[var] > 0L)) 
        stop("tree can only have continuous predictors")
    x <- rep(NA, length(leaves))
    x[!leaves] <- as.double(substring(frame$splits[!leaves, "cutleft"], 
        2L, 100L))
    m <- model.frame(tree)

    
    if (length(var) == 1L) {
        x <- sort(c(range(m[[var]]), x[!leaves]))
        if (is.null(attr(tree, "ylevels"))) 
            y <- frame$yval[leaves]
        else y <- frame$yprob[, 1L]
        y <- c(y, y[length(y)])
        if (add) 
            lines(x, y, type = "s", ...)
        else {
            a <- attributes(attr(m, "terms"))
            yvar <- as.character(a$variables[1 + a$response])
            xo <- m[[yvar]]
            if (is.factor(xo)) 
                ylim <- c(0, 1)
            else ylim <- range(xo)
            plot(x, y, ylab = yvar, xlab = var, type = "s", ylim = ylim, 
                xaxs = "i", ...)
        }
        invisible(list(x = x, y = y))
    }
    else {
        if (!missing(ordvars)) {
            ind <- match(var, ordvars)
            if (any(is.na(ind))) 
                stop("unmatched names in vars")
            var <- ordvars[sort(ind)]
        }
        
        rx <- range(m[[var[1L]]])
        rx <- rx + c(-0.025, 0.025) * diff(rx)
        rz <- range(m[[var[2L]]])
        rz <- rz + c(-0.025, 0.025) * diff(rz)
        xrange <- c(rx, rz)[c(1, 3, 2, 4)]
        xcoord <- NULL
        ycoord <- NULL
        if (0) if (!add) 
          plot(rx, rz, xlab = var[1L], ylab = var[2L], type = "n", 
               xaxs = "i", yaxs = "i", ...)
        
        xy <- LeafRectangles(x, frame$var, xrange, xcoord, ycoord, 
            var,verbose=verbose)
        yy <- matrix(xy$ycoord, nrow = 2L)
        
        #
        TreeRects = matrix(xy$xrangeAll, ncol=4, byrow=TRUE)
        colnames(TreeRects) = c("xleft", "ybottom", "xright", "ytop")
        TreeRects = as.data.frame(rbind(c(rx,rz)[c(1,3,2,4)], TreeRects))
        rownames(TreeRects) = paste0("rect" , 1:nrow(TreeRects) - 1)
        
        TreeRects[,c("yy1","yy2")] = rbind(c(NA,NA), t(yy))
        TreeRects[,"area"] = 10^6*(TreeRects[,"xright"]-TreeRects[,"xleft"])*(TreeRects[,"ytop"]-TreeRects[,"ybottom"])
        attr(TreeRects, "vars") = var
        
        lab <- frame$yval[leaves]
        #browser()
        if (is.null(frame$yprob)) {
          lab <- format(signif(lab, 3L))
          TreeRects[,"yval"] = as.numeric(c(signif(frame[1,"yval"], 3L) ,lab))
        } else {#if (match(label, attr(tree, "ylevels"), nomatch = 0L)) { 
          #lab <- format(signif(frame$yprob[leaves, label], ,3L))
          lab <- format(signif(frame$yprob[leaves, "TRUE"], ,3L))
          if (!is.null(ndigits)) lab = as.character( round(as.numeric(lab), ndigits) )
          TreeRects[,"yval"] = as.numeric(c(signif(frame$yprob[1, "TRUE"], 3L) ,lab))
        }
        
        #attr(TreeRects, "yy") = yy
        return(TreeRects)
        
        #xx <- matrix(xy$xcoord, nrow = 4L)
        #
        
        #browser()
        #if (verbose>1) browser()
        
        #if (0) for (i in 1:ncol(xx)){
        #  segments(xx[1L, i], xx[2L, i], xx[3L, i], xx[4L,i ])
        #  readLines(n=1)
        #}
        #segments(xx[1L, ], xx[2L, ], xx[3L, ], xx[4L, ])
        #text(yy[1L, ], yy[2L, ], as.character(lab), ...)
    }
}

PlotPartition = function(xy, add = FALSE, col = NULL, lab = NULL, ...){
  if (!add) {
    rx = as.numeric(xy[1,c("xleft", "xright")])
    ry = as.numeric(xy[1,c("ybottom", "ytop")])
    plot(rx, ry, xlab = attr(xy, "vars")[1L], ylab = attr(xy, "vars")[2L],
     type = "n",  xaxs = "i", yaxs = "i", ...)
  }
  if (is.null(col)) {
    rn=matrix(runif(3*nrow(xy)),ncol=3)
    COL=rgb(rn[,1],rn[,2],rn[,3]);
  } else if (is.character(col)) {
    tmpCol= (xy[,col]+min(xy[,col]))
    tmpCol = tmpCol/max(tmpCol)
    COL = rgb(tmpCol,tmpCol,tmpCol, 0.4)
    #browser()
  }
  
  for (i in 1:nrow(xy)) {  
    rect(xleft=xy[i,"xleft"], ybottom=xy[i,"ybottom"], xright=xy[i,"xright"], 
         ytop=xy[i,"ytop"], col = COL[i])
  }
  if (!is.null(lab)) {
    yy = t( xy[,c("yy1","yy2")])
    lab = as.character(xy[,"yval"])
    text(yy[1L, ], yy[2L, ], lab)
  }
}

Rect2PBSpolys = function(xy){
  N = nrow(xy)
  if (N==0) return(NULL)
  #browser()
  polys = cbind.data.frame(PID = rep(1:N, each=5), SID = rep(1,N*5), POS=rep(1:5, times=N), X= NA, Y=NA, yval=NA)
  for (i in 1:N){
    k = (i-1)*5+1;
    polys[k,"X"]=xy[i,"xleft"];polys[k,"Y"]=xy[i,"ybottom"];
    polys[k+1,"X"]=xy[i,"xright"];polys[k+1,"Y"]=xy[i,"ybottom"];
    polys[k+2,"X"]=xy[i,"xright"];polys[k+2,"Y"]=xy[i,"ytop"];
    polys[k+3,"X"]=xy[i,"xleft"];polys[k+3,"Y"]=xy[i,"ytop"];
    polys[k+4,c("X","Y")]=polys[k,c("X","Y")];
    polys[k:(k+4),"yval"] = xy[i,"yval"]
  }
  return(polys)
}

#Example code:
if (0){
  library(tree)
  data(cpus, package="MASS")
  cpus.ltr <- tree(log10(perf) ~ mmax+cach, cpus)
  summary(lm(log10(perf) ~ 1, data=cpus))
  #cpus.ltr
  #summary(cpus.ltr)
  #plot(cpus.ltr);  text(cpus.ltr)
  
  xy=TreePartition(cpus.ltr,verbose=0)
  PlotPartition(xy)
  PlotPartition(xy,lab=TRUE)
  
  data(NYleukemia)
  population <- NYleukemia$data$population
  cases <- NYleukemia$data$cases
  mapNY <- GetMap(center=c(lat=42.67456,lon=-76.00365), destfile = "NYstate.png", zoom=8)
  mapNY <- ReadMapTile("NYstate.png")
  data = merge(NYleukemia$data,NYleukemia$geo,by="censustract.FIPS")
  polys = FindClusters(data,DENS=FALSE, OR2=0,OR1=1.2,minArea=10,maxArea=1000)
  
  LeukTree = tree(100*cases/population ~ x+y,data)
  
  xy=TreePartition(LeukTree,ordvars = c("x","y"), verbose=0)
  polys=Rect2PBSpolys(xy)
  ColorMap(100*data$cases/data$population, mapNY, polys, add = FALSE,
           alpha = 0.35, log = TRUE, location = "topleft")
  
  crimeTree <- tree(CRIME ~ X+Y, columbus)
  xy=TreePartition(crimeTree,verbose=0)
  PlotPartition(xy,lab=TRUE)
  polys=Rect2PBSpolys(xy)
  mapOH <- GetMap(center=c(lat=mean(columbus$Y),lon=mean(columbus$X)), destfile = "OHcrime.png", 
                  maptype = "mobile", zoom=7)
  ColorMap(xy[,"yval"], mapOH, polys, add = FALSE,
           alpha = 0.35, log = TRUE, location = "topleft")
}

