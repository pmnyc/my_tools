require(dplyr)
require(lattice)
require(sqldf)
require(plotrix)


addBreaks2DataFrame = function(ds, xvar, num_cuts, cut_method=NULL){
    ####
    # This function adds another column of cuts for xvar by cut_method
    # cut method has to be one of 
    # equidistant, equal_probablity, log_equidistant
    ####
    x_series = ds[,xvar];
    
    if (typeof(x_series) %in% c("character","factor")){
        ds$varcuts = x_series
    } else{
        unqiue_x_values = unique(x_series);
        if (length(unqiue_x_values) <= num_cuts+1){
            breaks = sort(unqiue_x_values);
        } else{
            # cut_method in c("equidistant", "equal_probablity", "log_equidistant");
            if (is.null(cut_method)){cut_method = "equidistant"};
            # make sure number of bins is even number
            if (as.integer(num_cuts/2) != num_cuts/2){stop("Number of bins has to be EVEN")};
            
            if (cut_method == "equal_probablity"){
                breaks = quantile(x_series, probs=seq(0,1, 1/num_cuts)) ;
            } else if(cut_method == "equidistant"){
                breaks = seq(min(x_series), max(x_series), length.out=(num_cuts+1)) ;
            } else if (cut_method == "log_equidistant"){
                if (min(x_series)<1){stop(paste(xvar,"values need to be >=1"))} else{
                    breaks = exp(seq(min(log(x_series)), max(log(x_series)), length.out=(num_cuts+1)));
                }
            } else {stop(paste("cut_method is not one of ","equidistant, equal_probablity, log_equidistant"))}
        }
        
        ds = dplyr::mutate(ds, varcuts = cut(x_series, breaks = breaks, include.lowest=TRUE));
    }
    
    return(ds)
}


hisogramPlotsbyBlocks = function(ds,
                                 xvar,
                                 yvar,
                                 num_cuts,
                                 title,
                                 cut_method=NULL){
    title_ <- title;
    ds = addBreaks2DataFrame(ds=ds, xvar=xvar, num_cuts=num_cuts, cut_method=cut_method);
    cmd = paste("lattice::histogram( ~ ",yvar," | varcuts,  main='",title_,"', index.cond=list(c(",
                paste(c(c((num_cuts/2+1):num_cuts),c(1:(num_cuts/2))),collapse=","),
                ")), data=ds)",sep="");
    eval(parse(text=cmd));
}

## Test Code ##
if (FALSE){
    ds = read.csv("http://www.amherst.edu/~nhorton/r2/datasets/help.csv")
    xvar = "mcs"
    yvar = "pcs"
    num_cuts = 6;
    title = "Histogram";
    cut_method=NULL;
    hisogramPlotsbyBlocks(ds, xvar, yvar, num_cuts, title="Histograms of PCS by sextile of MCS");
}


##########################################################
##########################################################

plotRelativities = function(ds,
                            xvar,
                            actual_vs_predict,
                            xvar_factor,
                            wgt_column,
                            num_cuts,
                            cut_method=NULL,
                            relativity_scale_max = 10,
                            output_folder=NULL,
                            output_image_prefix=NULL){
    # This function plots the relativity curves of factors of predictor, relativity
    # of actual target values, and predicted values / actual values
    # the pred / actual is used as kind of indicator for factors of predictors
    
    # ds is the data frame containing factor of predictor, actual target and predicted values of target
    # xvar is the predictor
    # actual_vs_predict , first is the actual target field, and predict is the field for predicted value
    # xvar_factor is the field for factor of precdictor
    # wgt_column is the weight field
    # num_cuts specifices how many cuts we have. If the predictor is a categorical variable, this number
    # will automatically disabled
    # cut_method is the method for making breaks for bins. Must be one of equidistant, equal_probablity, log_equidistant
    
    # relativity_scale_max is upper limit for the relativity curve to be drawn on plot
    # output_image_prefix is prefix of image files produced. If NULL, then no image will be produced
    
    if (is.null(output_folder)){output_folder =getwd()}
    currworkdir = getwd();
    
    ds = addBreaks2DataFrame(ds=ds, xvar=xvar, num_cuts=num_cuts, cut_method=cut_method);
    sql_cmd = paste("select varcuts, 1.0 * sum(",actual_vs_predict[1],"*",wgt_column,")/sum(",wgt_column,") as actual, ",
                    "1.0 * sum(",actual_vs_predict[2],"*",wgt_column,")/sum(",wgt_column,") as predict, ",
                    "1.0 * sum(",xvar_factor,"*",wgt_column,")/sum(",wgt_column,") as xvar_factor, ",
                    "sum(",wgt_column,") as weight ",
                    "from ds group by varcuts", sep="");
    ds_aggregate = sqldf(sql_cmd);
    
    ds_aggregate2 = sqldf("select varcuts, 1.0 *actual / (select sum(actual * weight)/sum(weight)
                          from ds_aggregate) as actual_rel,
                          1.0 * predict / (select sum(predict * weight)/sum(weight)
                          from ds_aggregate) as predict_rel,
                          1.0 * xvar_factor / (select sum(xvar_factor * weight)/sum(weight)
                          from ds_aggregate) as xvar_factor_rel,
                          weight
                          from ds_aggregate order by varcuts");
    ds_aggregate2$predict_div_actual = 1.0 * ds_aggregate2$predict_rel / ds_aggregate2$actual_rel;
    ds_aggregate2 = ds_aggregate2[order(ds_aggregate2$varcuts),];
    
    ## plots of three relativity curves
    colors <- rainbow(3)
    
    setwd(output_folder);
    image_name = paste(output_image_prefix,"_",xvar,".png",sep="");
    if(!is.null(output_image_prefix)){
        png(image_name, width = 10, height = 9/(16/10), pointsize = 1/300, units = 'in', res = 300)
    }

    # barplot can be multiple columns instead of one variable like weight here
    mp <- barplot(as.matrix(t(ds_aggregate2[,"weight"])),beside=TRUE,ann=FALSE,
                  xlab = xvar, ylab=wgt_column, ylim=c(0,1.1*max(ds_aggregate2[,"weight"])),
                  col = c("lightcyan")); #xlim=c(0,40)
    par(new=TRUE)
    plot(mp[1,],ds_aggregate2$xvar_factor_rel,type="l",col=colors[1],
         axes=FALSE ,ann=FALSE,
         ylim=pmin(relativity_scale_max,c(0,quantile(ds_aggregate2$xvar_factor_rel,0.99) * 1.5)),
         lwd=2) #xlim=c(0,40)
    lines(mp[1,],ds_aggregate2$actual_rel,col=colors[2], lwd=2);
    lines(mp[1,],ds_aggregate2$predict_div_actual,col=colors[3], lwd=3);
    lines(mp[1,], rep(1,nrow(ds_aggregate2)), col='gray70')
    axis(1,at=mp[1,],labels=ds_aggregate2$varcuts)
    axis(4,at=c(0:10))
    box()
    
    # add a title and subtitle 
    #title(paste("Relativity Curves by ",xvar,sep=""), "Relativity of Actual vs Relativity of Actual/Predited")
    title(paste("Relativity Curves by ",xvar,sep=""));
    
    # add a legend 
    #legend(xrange[1], yrange[2], 1:ntrees, cex=0.8, col=colors,
    #   pch=plotchar, lty=linetype, title="Tree")
    
    legend('topright', lty=c(1,1), title = "Relativity", 
           legend= c(paste(xvar_factor,"",sep=""),
                     paste(actual_vs_predict[1],"",sep=""),
                     paste("predict / actual",sep="")),
           col=colors, bty='n', cex=.75);
    
    if(!is.null(output_image_prefix)){
        dev.off()
    }
    setwd(currworkdir);
}


## Test Code ##
if (FALSE){
    
    ds = read.csv("http://www.amherst.edu/~nhorton/r2/datasets/help.csv")
    xvar = "mcs"
    actual_vs_predict = c("pcs", "cesd")
    xvar_factor = "cesd"
    wgt_column = "pss_fr"
    num_cuts = 6;
    cut_method=NULL;
    
    plotRelativities(ds=ds,
                     xvar=xvar,
                     actual_vs_predict=actual_vs_predict,
                     xvar_factor=xvar_factor,
                     wgt_column=wgt_column,
                     num_cuts=num_cuts,
                     cut_method=NULL,
                     output_image_prefix=NULL);
}
