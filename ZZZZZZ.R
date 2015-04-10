########################
### @author: pm
### It aligns shape file with point shape files based on elevations
########################

alignPtShpWithPolyShp <- function(pointshape, polyshape,
                                polyshape_polygon_area_fieldname="SHAPE_AREA",
                                pointshape_elev_fieldname="z",
                                buffer_distance=5){
    # Assume the point shape file size (in MB) is much bigger than polygon shape file
        # and the extent of point shape file is within that of polygon shape file

    # pointshape_elev_fieldname is the field name in the point shape file for the elevation
    # buffer_distance is used to buffer both point and polygon shape files
    #### Sample Inputs ####
    # pointshape = las_toPtShp_ss2;
    # polyshape = shpInput_ss1;
    # pointshape_elev_fieldname ="z";
    # polyshape_polygon_area_fieldname = "SHAPE_AREA";
    # buffer_distance =20;
    ###########################

    pointshape_raw = pointshape;

    smallExpendExtent = function(extent, distance_to_add=5){
        attributes(extent)$xmin = attributes(extent)$xmin - distance_to_add;
        attributes(extent)$xmax = attributes(extent)$xmax + distance_to_add;
        attributes(extent)$ymin = attributes(extent)$ymin - distance_to_add;
        attributes(extent)$ymax = attributes(extent)$ymax + distance_to_add;
        return(extent)
    }

    smallerXYRange = function(polyshape){
        x_diff = attributes(raster::extent(polyshape))$xmax - attributes(raster::extent(polyshape))$xmin;
        y_diff = attributes(raster::extent(polyshape))$ymax - attributes(raster::extent(polyshape))$ymin;
        return(c(min(x_diff,y_diff),max(x_diff,y_diff)))
    }

    commonExtent = smallExpendExtent(raster::extent(pointshape),distance_to_add=buffer_distance);
    polyshape = raster::crop(polyshape,commonExtent);

    polyshape@data[,polyshape_polygon_area_fieldname] = polyshape@data[,polyshape_polygon_area_fieldname] + runif(nrow(polyshape@data))*0.1; #This is to avoid ties
    areas = polyshape@data[,polyshape_polygon_area_fieldname];
    areas = unique(sort(unique(areas),decreasing=TRUE));
    top1areas = areas[1:min(length(areas),10)];
    max_area_totake = min(top1areas);

    #### Get the extent for the point shape file with extended extent around the polygon with max area
    polyshape = polyshape[polyshape@data[,polyshape_polygon_area_fieldname] >= max_area_totake - (1e-4),];
    polybuffer = rgeos::gBuffer(polyshape,width=buffer_distance);

    clipPointShp <- sp::over(pointshape,polybuffer);
    #clipPointShp <- sp::over(pointshape,polyshape);
    idx = which(!is.na(clipPointShp));
    pointshape = pointshape[idx,];

    pointPolyClip_varofElev = function(pointshape,polyshape, max_area_totake,
                                       pointshape_elev_fieldname_=pointshape_elev_fieldname,
                                       polyshape_polygon_area_fieldname_ =polyshape_polygon_area_fieldname){
        pt_clip <- sp::over(pointshape,polyshape);
        pt_clip[,pointshape_elev_fieldname_] = pointshape@data[,pointshape_elev_fieldname_];
        pt_clip = pt_clip[which(!is.na(pt_clip[,polyshape_polygon_area_fieldname_]) &  pt_clip[, polyshape_polygon_area_fieldname_] > max_area_totake - (1e-4)),];

        pt_clip$SHAPE_AREA = pt_clip[,polyshape_polygon_area_fieldname_];
        pt_clip$z = pt_clip[,pointshape_elev_fieldname_];

        df1 = aggregate(z ~ STRUCT_ID, data = pt_clip, min, na.rm=TRUE);
        names(df1)[2] = "z_min";
        df2 = aggregate(z ~ STRUCT_ID, data = pt_clip, mean, na.rm=TRUE);
        names(df2)[2] = "z_mean";
        df3 = merge(df1, df2, by="STRUCT_ID");

        smalldistance = 1.5; #this is assumed to be the smallest distance between roof and ground
        df3$dummy = rep(smalldistance,nrow(df3));
        df3$cut1 = (df3$z_mean - df3$z_min)/3.0;
        df3 = transform(df3, low_cutoff = pmin(dummy, cut1));

        df4 = merge(pt_clip, df3, by="STRUCT_ID");
        df5 = df4[df4$z <= (df4$z_min + df4$low_cutoff),]; # find the points that are far below the average height within polygon region
        df6 = df4[df4$z > (df4$z_min + df4$low_cutoff),]; #the points that are beyond the threshold

        #df1 = merge(aggregate(z ~ STRUCT_ID, data = pt_clip, min, na.rm=TRUE),
        #            aggregate(SHAPE_AREA ~ STRUCT_ID, data = pt_clip, mean, na.rm=TRUE),by="STRUCT_ID");
        #var = sum(df1$z  (times) (df1$SHAPE_AREA + 1e-5)) / sum(df1$SHAPE_AREA + 1e-5);
        var = sum(df5$z) - sum(df6$z);
                #smaller var is more preferable
        return(var)
    }

}