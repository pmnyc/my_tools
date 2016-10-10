jitterLatLon = function(incidents, sd=0.00025) {
  n = nrow(incidents)
  incidents$X = incidents$X + rnorm(n,sd=sd)
  incidents$Y = incidents$Y + rnorm(n,sd=sd)
  return(incidents)
}