# @author: pengma
# Simulation (5 million simulations) of Power Test by Comparing Six Different Groups in Parallel

library(parallel)
### Initial Parameters ###
p_0 <- 0.05;
p_1 <- 0.3;
simu = 5e+6;
nsize <- 25;

##########################

simuPower = function(X,nsize,p.critical,p_0,p_1){
    pwd = getwd();
    on.exit(setwd(pwd));
    seeds = as.integer(runif(6, -(2^31 - 1), 2^31));
    set.seed(seeds[1]);
    x_11 = sum(rbinom(nsize,1,p_0));
    set.seed(seeds[2]);
    x_21 = sum(rbinom(nsize,1,p_0));
    set.seed(seeds[3]);
    x_31 = sum(rbinom(nsize,1,p_0));
    set.seed(seeds[4]);
    x_12 = sum(rbinom(nsize,1,p_1));
    set.seed(seeds[5]);
    x_22 = sum(rbinom(nsize,1,p_1));
    set.seed(seeds[6]);
    x_32 = sum(rbinom(nsize,1,p_1));

    data <- array(c(x_11,x_12,nsize-x_11,nsize-x_12,x_21,x_22,nsize-x_21,nsize-x_22,x_31,x_32,nsize-x_31,nsize-x_32),dim  =  c(2,2,3));
    p.value = mantelhaen.test(data,correct = FALSE)$p.value;
    return(ifelse(p.value < p.critical,1,0))
}

stt = Sys.time();
simu = as.integer(simu);

### Parallel Computing ###
p.critical = 0.05;
cores <- parallel::detectCores();
clusters <- parallel::makeCluster(cores);
out = parallel::parLapplyLB(cl=clusters,X=1:simu, simuPower,
                          nsize,p.critical,p_0,p_1);
      # use parLapply for parallel computing without load balancing
out = unlist(out);
if (exists("clusters")){if(!is.null(clusters)){on.exit(parallel::stopCluster(clusters))}}
power = mean(out);
print(paste("Final Power for Type-I Error",toString(p.critical),"is",toString(power)));