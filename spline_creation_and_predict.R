#############################################
#   This function is for creating natural cubic spline
#   functions and export it out
#############################################

require(splines)

# This is for creating data with adding spline info
    # given knot and knot quantiles
createSplinesFromData = function(data,
                                 knot_quantiles,
                                 columns_to_spline,
                                 spline_output_folder){
    #columns_to_spline = c("height","weight");
    #data = women;
    #spline_output_folder = "C:/Tempfile"
    #knot_quantiles = c(0.03,0.25,0.5,0.75,0.97);
    for (column in columns_to_spline){
        mySpline = splines::ns(data[,column],knots=quantile(data[,column], knot_quantiles));
        splineMatrix = as.data.frame(mySpline);
        col_names = sapply(c(1:ncol(splineMatrix)), FUN=function(t){paste(column,"__spline",t,sep="")});
        names(splineMatrix) = col_names;
        data = cbind(data,splineMatrix);
        spline_name = paste(column,"_spline",sep="");
        eval(parse(text=paste(spline_name, "<- mySpline", sep="")))
        cmd = paste('save(', spline_name, ', file=file.path("',spline_output_folder,'", "',spline_name,'.RData"))', sep='');
        eval(parse(text=cmd))
        rm(splineMatrix);
    }
    return(data)
}


# This is for recreating the spline matrix given a new
# column and spline that was created before for the data
predictWithSpline = function(data, column, spline){
    # data=women;
    # column = "height";
    # spline = mySpline;
    splineMatrix = as.data.frame(predict(spline, data[,column], nseg = 50));
    col_names = sapply(c(1:ncol(splineMatrix)), FUN=function(t){paste(column,"__spline",t,sep="")});
    names(splineMatrix) = col_names;
    data = cbind(data,splineMatrix);
    rm(splineMatrix)
    return(data)
}

####### Test ##########
if (FALSE){
    data_spline = createSplinesFromData(data=women,
                         knot_quantiles=c(0.03,0.25,0.5,0.75,0.97),
                         columns_to_spline=c("height","weight"),
                         spline_output_folder="C:/Tempfile");
    
    data_new = predictWithSpline(data=women, column="height", spline=mySpline);
}

