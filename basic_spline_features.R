require(splines)
require(stats)
require(graphics)
 
x = women$height;
knot_quantiles = c(0.03,0.25,0.5,0.75,0.97);
mySpline = ns(x,knots=quantile(x, knot_quantiles));
 
# This is to get spline values (6 since we have 5 knots) for a new
    # x=65.1
predict(mySpline, 65.1, nseg = 50)
 
# Create plots of splines
colors <- c("Orange", "Gray", "tomato2", "deepskyblue3","green","black")
plot(range(x), range(mySpline), type="n", main="R Version",
     xlab="x", ylab="Spline value")
for (k in attr(mySpline, "knots")) abline(v=k, col="Gray", lty=2)
for (j in 1:ncol(mySpline)) {
    lines(x, mySpline[,j], col=colors[j], lwd=2)
}
 
#
# Export this basis in Excel-readable format.
# , where n is the spline
ns.formula <- function(n, ref="A1") {
    ref.p <- paste("I(", ref, sep="")
    knots <- sort(c(attr(n, "Boundary.knots"), attr(n, "knots")))
    d <- attr(n, "degree")
    f <- sapply(2:length(knots), function(i) {
        s.pre <- paste("IF(AND(", knots[i-1], "<=", ref, ", ", ref, "<", knots[i], "), ",
                       sep="")
        x <- seq(knots[i-1], knots[i], length.out=d+1)
        y <- predict(n, x)
        apply(y, 2, function(z) {
            s.f <- paste("z ~ x+", paste("I(x", 2:d, sep="^", collapse=")+"), ")", sep="")
            f <- as.formula(s.f)
            b.hat <- coef(lm(f))
            s <- paste(c(b.hat[1],
                         sapply(1:d, function(j) paste(b.hat[j+1], "*", ref, "^", j, sep=""))),
                       collapse=" + ")
            paste(s.pre, s, ", 0)", sep="")
        })
    })
    apply(f, 1, function(s) paste(s, collapse=" + "))
}
 
# fit regression
summary(fm1 <- lm(weight ~ ns(x,knots=quantile(x, knot_quantiles)), data = women))
## To see what knots were selected
attr(terms(fm1), "predvars")
 
## example of safe prediction
plot(women, xlab = "Height (in)", ylab = "Weight (lb)")
ht <- seq(57, 73, length.out = 200)
lines(ht, predict(fm1, newdata=data.frame(x = ht)))
