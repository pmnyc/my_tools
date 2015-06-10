# -*- coding: utf-8 -*-
#COPYRIGHT 2013 ESRI
#
#TRADE SECRETS: ESRI PROPRIETARY AND CONFIDENTIAL
#Unpublished material - all rights reserved under the
#Copyright Laws of the United States.
#
#For additional information, contact:
#Environmental Systems Research Institute, Inc.
#Attn: Contracts Dept
#380 New York Street
#Redlands, California, USA 92373
#
#email: contracts@esri.com
"""The Analysis toolbox contains a powerful set of tools that perform the most
fundamental GIS operations. With the tools in this toolbox, you can perform
overlays, create buffers, calculate statistics, perform proximity analysis, and
much more. Whenever you need to solve a spatial or statistical problem, you
should always look in the Analysis toolbox."""
__all__ = ['Buffer', 'Clip', 'Erase', 'Identity', 'Intersect', 'SymDiff', 'Update', 'Split', 'Near', 'PointDistance', 'Select', 'TableSelect', 'Frequency', 'Statistics', 'CreateThiessenPolygons', 'SpatialJoin', 'MultipleRingBuffer', 'GenerateNearTable', 'Union', 'TabulateIntersection', 'PolygonNeighbors']
__alias__ = u'analysis'
from arcpy.geoprocessing._base import gptooldoc, gp, gp_fixargs
from arcpy.arcobjects.arcobjectconversion import convertArcObjectToPythonObject

# Extract toolset
@gptooldoc('Clip_analysis', None)
def Clip(in_features=None, clip_features=None, out_feature_class=None, cluster_tolerance=None):
    """Clip_analysis(in_features, clip_features, out_feature_class, {cluster_tolerance})

        Extracts input features that overlay the clip features.Use this tool to cut out
        a piece of one feature class using one or more of the
        features in another feature class as a cookie cutter. This is particularly
        useful for creating a new feature class—also referred to as study area or area
        of interest (AOI)—that contains a geographic subset of the features in another,
        larger feature class.

     INPUTS:
      in_features (Feature Layer):
          The features to be clipped.
      clip_features (Feature Layer):
          The features used to clip the input features.
      cluster_tolerance {Linear unit}:
          The minimum distance separating all feature coordinates as well as the distance
          a coordinate can move in X or Y (or both). Set the value to be higher for data
          with less coordinate accuracy and lower for data with extremely high accuracy.

     OUTPUTS:
      out_feature_class (Feature Class):
          The feature class to be created."""
    from arcpy.geoprocessing._base import gp, gp_fixargs
    from arcpy.arcobjects.arcobjectconversion import convertArcObjectToPythonObject
    try:
        retval = convertArcObjectToPythonObject(gp.Clip_analysis(*gp_fixargs((in_features, clip_features, out_feature_class, cluster_tolerance), True)))
        return retval
    except Exception, e:
        raise e

@gptooldoc('Select_analysis', None)
def Select(in_features=None, out_feature_class=None, where_clause=None):
    """Select_analysis(in_features, out_feature_class, {where_clause})

        Extracts features from an input feature class or input feature layer, typically
        using a select or Structured Query Language (SQL) expression and stores them in
        an output feature class.

     INPUTS:
      in_features (Feature Layer):
          The input feature class or layer from which features are selected.
      where_clause {SQL Expression}:
          An SQL expression used to select a subset of features. The syntax for the
          expression differs slightly depending on the data source. For example, if you're
          querying file or ArcSDE geodatabases, shapefiles, or coverages, enclose field
          names in double quotes: "MY_FIELD" If you're querying personal geodatabases,
          enclose fields in square brackets: [MY_FIELD] In Python, strings are enclosed in
          matching single or double quotes. To create
          a string that contains quotes (as is common with a WHERE clause in SQL
          expressions), you can escape the quotes (using a backslash) or triple quote the
          string. For example, if the intended WHERE clause is "CITY_NAME" = 'Chicago'you
          could enclose the entire string in double quotes, then escape the interior
          double quotes like this: " \"CITY_NAME\" = 'Chicago' " Or you could enclose the
          entire string in single quotes, then escape the
          interior single quotes like this: ' "CITY_NAME" = \'Chicago\' 'Or you could
          enclose the entire string in triple quotes without escaping: ''' "CITY_NAME" =
          'Chicago' ''' For more information on SQL syntax and how it differs between data
          sources, see
          the help topic SQL reference for query expressions used in ArcGIS.

     OUTPUTS:
      out_feature_class (Feature Class):
          The output feature class to be created. If no expression is used, it contains
          all input features."""
    from arcpy.geoprocessing._base import gp, gp_fixargs
    from arcpy.arcobjects.arcobjectconversion import convertArcObjectToPythonObject
    try:
        retval = convertArcObjectToPythonObject(gp.Select_analysis(*gp_fixargs((in_features, out_feature_class, where_clause), True)))
        return retval
    except Exception, e:
        raise e

@gptooldoc('Split_analysis', None)
def Split(in_features=None, split_features=None, split_field=None, out_workspace=None, cluster_tolerance=None):
    """Split_analysis(in_features, split_features, split_field, out_workspace, {cluster_tolerance})

        Splitting the Input Features creates a subset of multiple output feature
        classes.The Split Field's unique values form the names of the output feature
        classes.
        These are saved in the target workspace.

     INPUTS:
      in_features (Feature Layer):
          The features to be split.
      split_features (Feature Layer):
          The features containing a tabular field whose unique values are used to split
          the Input Features and provide the output feature classes' names.
      split_field (Field):
          The character field used to split the Input Features. This field's values
          identify the Split Features used to create each output feature class. The Split
          Field's unique values provide the output feature classes' names.
      out_workspace (Workspace / Feature Dataset):
          The workspace where the output feature classes are stored.
      cluster_tolerance {Linear unit}:
          The minimum distance separating all feature coordinates (nodes and vertices) as
          well as the distance a coordinate can move in X or Y (or both). Set the value to
          be higher for data that has less coordinate accuracy and lower for datasets with
          extremely high accuracy."""
    from arcpy.geoprocessing._base import gp, gp_fixargs
    from arcpy.arcobjects.arcobjectconversion import convertArcObjectToPythonObject
    try:
        retval = convertArcObjectToPythonObject(gp.Split_analysis(*gp_fixargs((in_features, split_features, split_field, out_workspace, cluster_tolerance), True)))
        return retval
    except Exception, e:
        raise e

@gptooldoc('TableSelect_analysis', None)
def TableSelect(in_table=None, out_table=None, where_clause=None):
    """TableSelect_analysis(in_table, out_table, {where_clause})

        Selects table records matching a Structured Query Language (SQL) expression and
        writes them to an output table.

     INPUTS:
      in_table (Table View / Raster Layer):
          The table whose records matching the specified expression will be written to the
          output table.
      where_clause {SQL Expression}:
          An SQL expression used to select a subset of records. The syntax for the
          expression differs slightly depending on the data source. For example, if you're
          querying file or ArcSDE geodatabases, shapefiles, coverages, or dBASE or INFO
          tables, enclose field names in double quotes: "MY_FIELD" If you're querying
          personal geodatabases, enclose fields in square brackets: [MY_FIELD] In Python,
          strings are enclosed in matching single or double quotes. To create
          a string that contains quotes (as is common with a WHERE clause in SQL
          expressions), you can escape the quotes (using a backslash) or triple quote the
          string. For example, if the intended WHERE clause is "CITY_NAME" = 'Chicago'you
          could enclose the entire string in double quotes, then escape the interior
          double quotes like this: " \"CITY_NAME\" = 'Chicago' " Or you could enclose the
          entire string in single quotes, then escape the
          interior single quotes like this: ' "CITY_NAME" = \'Chicago\' 'Or you could
          enclose the entire string in triple quotes without escaping: ''' "CITY_NAME" =
          'Chicago' ''' For more information on SQL syntax and how it differs between data
          sources, see
          the help topic SQL reference for query expressions used in ArcGIS.

     OUTPUTS:
      out_table (Table):
          The output table containing records from the input table that match the
          specified expression."""
    from arcpy.geoprocessing._base import gp, gp_fixargs
    from arcpy.arcobjects.arcobjectconversion import convertArcObjectToPythonObject
    try:
        retval = convertArcObjectToPythonObject(gp.TableSelect_analysis(*gp_fixargs((in_table, out_table, where_clause), True)))
        return retval
    except Exception, e:
        raise e


# Overlay toolset
@gptooldoc('Erase_analysis', None)
def Erase(in_features=None, erase_features=None, out_feature_class=None, cluster_tolerance=None):
    """Erase_analysis(in_features, erase_features, out_feature_class, {cluster_tolerance})

        Creates a feature class by overlaying the Input Features with the polygons of
        the Erase Features. Only those portions of the input features falling outside
        the erase features outside boundaries are copied to the output feature class.

     INPUTS:
      in_features (Feature Layer):
          The input feature class or layer.
      erase_features (Feature Layer):
          The features to be used to erase coincident features in the input.
      cluster_tolerance {Linear unit}:
          The minimum distance separating all feature coordinates (nodes and vertices) as
          well as the distance a coordinate can move in X or Y (or both).

     OUTPUTS:
      out_feature_class (Feature Class):
          The feature class that will contain only those Input Features that are not
          coincident with the Erase Features."""
    from arcpy.geoprocessing._base import gp, gp_fixargs
    from arcpy.arcobjects.arcobjectconversion import convertArcObjectToPythonObject
    try:
        retval = convertArcObjectToPythonObject(gp.Erase_analysis(*gp_fixargs((in_features, erase_features, out_feature_class, cluster_tolerance), True)))
        return retval
    except Exception, e:
        raise e

@gptooldoc('Identity_analysis', None)
def Identity(in_features=None, identity_features=None, out_feature_class=None, join_attributes=None, cluster_tolerance=None, relationship=None):
    """Identity_analysis(in_features, identity_features, out_feature_class, {join_attributes}, {cluster_tolerance}, {relationship})

        Computes a geometric intersection of the input features and identity features.
        The input features or portions thereof that overlap identity features will get
        the attributes of those identity features.

     INPUTS:
      in_features (Feature Layer):
          The input feature class or layer.
      identity_features (Feature Layer):
          The identity feature class or layer. Must be polygons or the same geometry type
          as the input features.
      join_attributes {String}:
          Determines what attributes will be transferred to the output feature class.

          * ALL—All the attributes (including FIDs) from the input features, as well as
          the identity features, will be transferred to the output features. If no
          intersection is found the identity feature values will not be transferred to the
          output (their values will be set to empty strings or 0) and the identity feature
          FID will be -1. This is the default.

          * NO_FID—All the attributes except the FID from the input features and identity
          features will be transferred to the output features. If no intersection is found
          the identity feature values will not be transferred to the output (their values
          will be set to empty strings or 0).

          * ONLY_FID—All the attributes from the input features but only the FID from the
          identity features will be transferred to the output features. The identity
          features FID attribute in the output will be -1 if no intersection is found.
      cluster_tolerance {Linear unit}:
          The minimum distance separating all feature coordinates (nodes and vertices) as
          well as the distance a coordinate can move in X or Y (or both).
      relationship {Boolean}:
          Determines if additional spatial relationships between the in_features and the
          identity_features are to be written to the output. This only applies when the
          in_features are lines and the identity_features are polygons.

          * NO_RELATIONSHIPS—No additional spatial relationship will be determined.

          * KEEP_RELATIONSHIPS—The output line features will contain two additional
          fields, LEFT_poly and RIGHT_poly. These fields contain the feature ID of the
          identity_features on the left and right side of the line feature.

     OUTPUTS:
      out_feature_class (Feature Class):
          The feature class that will be created and to which the results will be written."""
    from arcpy.geoprocessing._base import gp, gp_fixargs
    from arcpy.arcobjects.arcobjectconversion import convertArcObjectToPythonObject
    try:
        retval = convertArcObjectToPythonObject(gp.Identity_analysis(*gp_fixargs((in_features, identity_features, out_feature_class, join_attributes, cluster_tolerance, relationship), True)))
        return retval
    except Exception, e:
        raise e

@gptooldoc('Intersect_analysis', None)
def Intersect(in_features=None, out_feature_class=None, join_attributes=None, cluster_tolerance=None, output_type=None):
    """Intersect_analysis(in_features;in_features..., out_feature_class, {join_attributes}, {cluster_tolerance}, {output_type})

        Computes a geometric intersection of the input features. Features or portions of
        features which overlap in all layers and/or feature classes will be written to
        the output feature class.

     INPUTS:
      in_features (Value Table):
          A list of the input feature classes or layers. When the distance between
          features is less than the cluster tolerance, the features with the lower rank
          will snap to the feature with the higher rank. The highest rank is one. For more
          information, see Priority ranks and Geoprocessing tools.
      join_attributes {String}:
          Determines which attributes from the Input Features will be transferred to the
          Output Feature Class.

          * ALL—All the attributes from the Input Features will be transferred to the
          Output Feature Class. This is the default.

          * NO_FID—All the attributes except the FID from the Input Features will be
          transferred to the Output Feature Class.

          * ONLY_FID—Only the FID field from the Input Features will be transferred to the
          Output Feature Class.
      cluster_tolerance {Linear unit}:
          The minimum distance separating all feature coordinates (nodes and vertices) as
          well as the distance a coordinate can move in X or Y (or both).
      output_type {String}:
          Choose what type of intersection you want to find.

          * INPUT—The intersections returned will be the same geometry type as the Input
          Features with the lowest dimension geometry. If all inputs are polygons, the
          output feature class will contain polygons. If one or more of the inputs are
          lines and none of the inputs are points, the output will be line. If one or more
          of the inputs are points, the output feature class will contain points. This is
          the default.

          * LINE—Line intersections will be returned. This is only valid if none of the
          inputs are points.

          * POINT—Point intersections will be returned. If the inputs are line or polygon,
          the output will be a multipoint feature class.

     OUTPUTS:
      out_feature_class (Feature Class):
          The output feature class."""
    from arcpy.geoprocessing._base import gp, gp_fixargs
    from arcpy.arcobjects.arcobjectconversion import convertArcObjectToPythonObject
    try:
        retval = convertArcObjectToPythonObject(gp.Intersect_analysis(*gp_fixargs((in_features, out_feature_class, join_attributes, cluster_tolerance, output_type), True)))
        return retval
    except Exception, e:
        raise e

@gptooldoc('SpatialJoin_analysis', None)
def SpatialJoin(target_features=None, join_features=None, out_feature_class=None, join_operation=None, join_type=None, field_mapping=None, match_option=None, search_radius=None, distance_field_name=None):
    """SpatialJoin_analysis(target_features, join_features, out_feature_class, {join_operation}, {join_type}, {field_mapping}, {match_option}, {search_radius}, {distance_field_name})

        Joins attributes from one feature to another based on the spatial relationship.
        The target features and the joined attributes from the join features are written
        to the output feature class.

     INPUTS:
      target_features (Feature Layer):
          Attributes of the target features and the attributes from the joined features
          are transferred to the output feature class. However, a subset of attributes can
          be defined in the field map parameter. The target features can be any spatial
          data source supported by ArcGIS.
      join_features (Feature Layer):
          The attributes from the join features are joined to the attributes of the target
          features. See the explanation of the Join Operation parameter for details on how
          the aggregation of joined attributes are affected by the type of join operation.
      join_operation {String}:
          Determines how joins between the target features and join features will be
          handled in the output feature class if multiple join features are found that
          have the same spatial relationship with a single target feature.

          * JOIN_ONE_TO_ONE—If multiple join features are found that have the same spatial
          relationship with a single target feature, the attributes from the multiple join
          features will be aggregated using a field map merge rule. For example, if a
          point target feature is found within two separate polygon join features, the
          attributes from the two polygons will be aggregated before being transferred to
          the output point feature class. If one polygon has an attribute value of 3 and
          the other has a value of 7, and a Sum merge rule is specified, the aggregated
          value in the output feature class will be 10. The JOIN_ONE_TO_ONE option is the
          default.

          * JOIN_ONE_TO_MANY—If multiple join features are found that have the same
          spatial relationship with a single target feature, the output feature class will
          contain multiple copies (records) of the target feature. For example, if a
          single point target feature is found within two separate polygon join features,
          the output feature class will contain two copies of the target feature: one
          record with the attributes of one polygon, and another record with the
          attributes of the other polygon.
      join_type {Boolean}:
          Determines if all target features will be maintained in the output feature class
          (known as outer join), or only those that have the specified spatial
          relationship with the join features (inner join).

          * KEEP_ALL—All target features will be maintained in the output (outer join).
          This is the default.

          * KEEP_COMMON— Only those target features that have the specified spatial
          relationship with the join features will be maintained in the output feature
          class (inner join). For example, if a point feature class is specified for the
          target features, and a polygon feature class is specified for the join features,
          with a  Match Option of WITHIN, the output feature class will only contain those
          target features that are within a polygon join feature; any target features not
          within a join feature will be excluded from the output.
      field_mapping {Field Mappings}:
          Controls what attribute fields will be in the output feature class. The initial
          list contains all the fields from both the target features and the join
          features. Fields can be added, deleted, renamed, or have their properties
          changed. The selected fields from the target features are transferred as is, but
          selected fields from the join features can be aggregated by a merge rule. For
          details on field mapping, see Using the field mapping control and Mapping input
          fields to output fields. Multiple fields and statistic combination may be
          specified.
      match_option {String}:
          Defines the criteria used to match rows. The match options are:

          * INTERSECT—The features in the join features will be matched if they intersect
          a target feature. This is the default.

          * INTERSECT_3D— The features in the join features will be matched if they
          intersect a target feature in three-dimensional space (x, y, and z).

          * WITHIN_A_DISTANCE—The features in the join features will be matched if they
          are within a specified distance of a target feature. Specify a distance in the
          Search Radius parameter.

          * WITHIN_A_DISTANCE_3D—The features in the join features will be matched if they
          are within a specified distance of a target feature in three-dimensional space.
          Specify a distance in Search Radius parameter.

          * CONTAINS—The features in the join features will be matched if a target feature
          contains them. The target features must be polygons or polylines. For this
          option, the target features cannot be points, and the join features can only be
          polygons when the target features are also polygons.

          * COMPLETELY_CONTAINS—The features in the join features will be matched if a
          target feature completely contains them. Polygon can completely contain any
          feature. Point cannot completely contain any feature, not even a point. Polyline
          can completely contain only polyline and point.

          * CONTAINS_CLEMENTINI—This spatial relationship yields the same results as
          COMPLETELY_CONTAINS with the exception that if the join feature is entirely on
          the boundary of the target feature (no part is properly inside or outside) the
          feature will not be matched. CLEMENTINI defines the boundary polygon as the line
          separating inside and outside, the boundary of a line is defined as its end
          points, and the boundary of a point is always empty.

          * WITHIN—The features in the join features will be matched if a target feature
          is within them. It is opposite to CONTAINS. For this option, the target features
          can only be polygons when the join features are also polygons. Point can be join
          feature only if point is target.

          * COMPLETELY_WITHIN—The features in the join features will be matched if a
          target feature is completely within them. This is opposite to
          COMPLETELY_CONTAINS.

          * WITHIN_CLEMENTINI—The result will be identical to WITHIN except if the
          entirety of the feature in the join features is on the boundary of the target
          feature, the feature will not be matched. CLEMENTINI defines the boundary
          polygon as the line separating inside and outside, the boundary of a line is
          defined as its end points, and the boundary of a point is always empty.

          * ARE_IDENTICAL_TO—The features in the join features will be matched if they are
          identical to a target feature. Both join and target feature must be of same
          shape type—point-to-point, line-to-line, and polygon-to-polygon.

          * BOUNDARY_TOUCHES—The features in the join features will be matched if they
          have a boundary that touches a target feature. The join and target features must
          be lines or polygons. Additionally, the feature in the join features must be
          either outside or completely inside of the target polygon.

          * SHARE_A_LINE_SEGMENT_WITH—The features in the join features will be matched if
          they share a line segment with a target feature. The join and target features
          must be lines or polygons.

          * CROSSED_BY_THE_OUTLINE_OF—The features in the join features will be matched if
          a target feature is crossed by their outline. The join and target features must
          be lines or polygons. If polygons are used for the join or target features, the
          polygon's boundary (line) will be used. Lines that cross at a point will be
          matched, not lines that share a line segment.

          * HAVE_THEIR_CENTER_IN—The features in the join features will be matched if a
          target feature's center falls within them. The center of the feature is
          calculated as follows: for polygon and multipoint the geometry's centroid is
          used, and for line input the geometry's midpoint is used.

          * CLOSEST—The feature in the join features that is closest to a target feature
          is matched. See the usage tip for more information.
      search_radius {Linear unit}:
          Join features within this distance of a target feature will be considered for
          the spatial join. A search radius is only valid when the spatial relationship
          (Match Option) INTERSECT or CLOSEST is specified. Using a search radius of 100
          meters with the spatial relationship INTERSECT is the equivalent of saying: if a
          join feature is within 100 meters of a target feature, consider the join feature
          to be a match.
      distance_field_name {String}:
          The name of a field to be added to the output feature class, which contains the
          distance between the target feature and the closest join feature. This option is
          only valid when the spatial relationship (Match Option) CLOSEST is specified.
          The value of this field is -1 if no feature is matched within a search radius.
          If no field name is specified, the field will not be added to the output feature
          class.

     OUTPUTS:
      out_feature_class (Feature Class):
          A new feature class containing the attributes of the target and join features.
          By default, all attributes of target features and the attributes of the joined
          features are written to the output. However, the set of attributes to be
          transferred can be controlled by the field map parameter."""
    from arcpy.geoprocessing._base import gp, gp_fixargs
    from arcpy.arcobjects.arcobjectconversion import convertArcObjectToPythonObject
    try:
        retval = convertArcObjectToPythonObject(gp.SpatialJoin_analysis(*gp_fixargs((target_features, join_features, out_feature_class, join_operation, join_type, field_mapping, match_option, search_radius, distance_field_name), True)))
        return retval
    except Exception, e:
        raise e

@gptooldoc('SymDiff_analysis', None)
def SymDiff(in_features=None, update_features=None, out_feature_class=None, join_attributes=None, cluster_tolerance=None):
    """SymDiff_analysis(in_features, update_features, out_feature_class, {join_attributes}, {cluster_tolerance})

        Features or portions of features in the input and update features that do not
        overlap will be written to the output feature class.

     INPUTS:
      in_features (Feature Layer):
          The input feature class or layer.
      update_features (Feature Layer):
          The update feature class or layer. Geometry type must be the same geometry type
          as the input feature class or layer.
      join_attributes {String}:
          Determines which attributes will be transferred to the output feature class.

          * ALL—All the attributes from the input features and update features will be
          transferred to the output. This is the default.

          * NO_FID—All the attributes except the FID input features and update features
          will be transferred to the output.

          * ONLY_FID—Only the FID from the input features and update features will be
          transferred to the output.
      cluster_tolerance {Linear unit}:
          The minimum distance separating all feature coordinates (nodes and vertices) as
          well as the distance a coordinate can move in x or y (or both).

     OUTPUTS:
      out_feature_class (Feature Class):
          The feature class to which the results will be written."""
    from arcpy.geoprocessing._base import gp, gp_fixargs
    from arcpy.arcobjects.arcobjectconversion import convertArcObjectToPythonObject
    try:
        retval = convertArcObjectToPythonObject(gp.SymDiff_analysis(*gp_fixargs((in_features, update_features, out_feature_class, join_attributes, cluster_tolerance), True)))
        return retval
    except Exception, e:
        raise e

@gptooldoc('Union_analysis', None)
def Union(in_features=None, out_feature_class=None, join_attributes=None, cluster_tolerance=None, gaps=None):
    """Union_analysis(in_features;in_features..., out_feature_class, {join_attributes}, {cluster_tolerance}, {gaps})

        Computes a geometric union of the input features. All features and their
        attributes will be written to the output feature class.

     INPUTS:
      in_features (Value Table):
          A list of the input feature classes or layers. When the distance between
          features is less than the cluster tolerance, the features with the lower rank
          will snap to the feature with the higher rank. The highest rank is one. All of
          the input features must be polygons.
      join_attributes {String}:
          Determines which attributes from the input features will be transferred to the
          output feature class.

          * ALL—All of the attributes from the input features will be transferred to the
          output feature class.This is the default.

          * NO_FID—All of the attributes except the FID from the input features will be
          transferred to the output feature class.

          * ONLY_FID—Only the FID field from the input features will be transferred to the
          output feature class.
      cluster_tolerance {Linear unit}:
          The minimum distance separating all feature coordinates (nodes and vertices) as
          well as the distance a coordinate can move in X or Y (or both).
      gaps {Boolean}:
          Gaps are areas in the output feature class that are completely enclosed by other
          polygons. This is not invalid, but it may be desirable to identify these for
          analysis. To find the gaps in the output, set this option to NO_GAPS, and a
          feature will be created in these areas. To select these features, query the
          output feature class based on all the input feature's FID values being equal to
          -1.

          * GAPS—No feature will be created for areas in the output that are completely
          enclosed by polygons. This is the default.

          * NO_GAPS—A feature will be created for the areas in the output that are
          completely enclosed by polygons. This feature will have blank attributes.

     OUTPUTS:
      out_feature_class (Feature Class):
          The feature class that will contain the results."""
    from arcpy.geoprocessing._base import gp, gp_fixargs
    from arcpy.arcobjects.arcobjectconversion import convertArcObjectToPythonObject
    try:
        retval = convertArcObjectToPythonObject(gp.Union_analysis(*gp_fixargs((in_features, out_feature_class, join_attributes, cluster_tolerance, gaps), True)))
        return retval
    except Exception, e:
        raise e

@gptooldoc('Update_analysis', None)
def Update(in_features=None, update_features=None, out_feature_class=None, keep_borders=None, cluster_tolerance=None):
    """Update_analysis(in_features, update_features, out_feature_class, {keep_borders}, {cluster_tolerance})

        Computes a geometric intersection of the Input Features and Update Features. The
        attributes and geometry of the input features are updated by the update features
        in the output feature class.

     INPUTS:
      in_features (Feature Layer):
          The input feature class or layer. Geometry type must be polygon.
      update_features (Feature Layer):
          The features that will be used to update the Input Features. Geometry type must
          be polygon.
      keep_borders {Boolean}:
          Specifies whether the boundary of the update polygon features will be kept.

          * BORDERS—The outside border of the Update Features will be kept in the Output
          Feature Class. This is the default option.

          * NO_BORDERS—The outside border of the Update Features are dropped after they
          are inserted into the Input Features. Item values of the Update Features take
          precedence over Input Features attributes.
      cluster_tolerance {Linear unit}:
          The minimum distance separating all feature coordinates (nodes and vertices) as
          well as the distance a coordinate can move in X or Y (or both).

     OUTPUTS:
      out_feature_class (Feature Class):
          The feature class to contain the results. Do not set this to be the same as the
          Input Features."""
    from arcpy.geoprocessing._base import gp, gp_fixargs
    from arcpy.arcobjects.arcobjectconversion import convertArcObjectToPythonObject
    try:
        retval = convertArcObjectToPythonObject(gp.Update_analysis(*gp_fixargs((in_features, update_features, out_feature_class, keep_borders, cluster_tolerance), True)))
        return retval
    except Exception, e:
        raise e


# Proximity toolset
@gptooldoc('Buffer_analysis', None)
def Buffer(in_features=None, out_feature_class=None, buffer_distance_or_field=None, line_side=None, line_end_type=None, dissolve_option=None, dissolve_field=None):
    """Buffer_analysis(in_features, out_feature_class, buffer_distance_or_field, {line_side}, {line_end_type}, {dissolve_option}, {dissolve_field;dissolve_field...})

        Creates buffer polygons around input features to a specified distance.

     INPUTS:
      in_features (Feature Layer):
          The input point, line, or polygon features to be buffered.
      buffer_distance_or_field (Linear unit / Field):
          The distance around the input features that will be buffered. Distances can be
          provided as either a value representing a linear distance or as a field from the
          input features that contains the distance to buffer each feature.If linear units
          are not specified or are entered as Unknown, the linear unit of
          the input features' spatial reference is used.When specifying a distance in
          scripting, if the desired linear unit has two
          words, like Decimal Degrees, combine the two words into one (for example, '20
          DecimalDegrees').
      line_side {String}:
          The side(s) of the input features that will be buffered.

          * FULL—For line input features, buffers will be generated on both sides of the
          line. For polygon input features, buffers will be generated around the polygon
          and will contain and overlap the area of the input features. For point input
          features, buffers will be generated around the point. This is the default.

          * LEFT—For line input features, buffers will be generated on the topological
          left of the line. This option is not valid for polygon input features.

          * RIGHT—For line input features, buffers will be generated on the topological
          right of the line. This option is not valid for polygon input features.

          * OUTSIDE_ONLY—For polygon input features, buffers will be generated only
          outside the input polygon (the area inside the input polygon will be erased from
          the output buffer). This option is not valid for line input features.
          This optional parameter is not available with a Basic or Standard license.
      line_end_type {String}:
          The shape of the buffer at the end of line input features. This parameter is not
          valid for polygon input features.

          * ROUND—The ends of the buffer will be round, in the shape of a half circle.
          This is the default.

          * FLAT—The ends of the buffer will be flat, or squared, and will end at the
          endpoint of the input line feature.
          This optional parameter is not available with a Basic or Standard license.
      dissolve_option {String}:
          Specifies the dissolve to be performed to remove buffer overlap.

          * NONE—An individual buffer for each feature is maintained, regardless of
          overlap. This is the default.

          * ALL—All buffers are dissolved together into a single feature, removing any
          overlap.

          * LIST—Any buffers sharing attribute values in the listed fields (carried over
          from the input features) are dissolved.
      dissolve_field {Field}:
          The list of field(s) from the input features on which to dissolve the output
          buffers. Any buffers sharing attribute values in the listed fields (carried over
          from the input features) are dissolved.

     OUTPUTS:
      out_feature_class (Feature Class):
          The feature class containing the output buffers."""
    from arcpy.geoprocessing._base import gp, gp_fixargs
    from arcpy.arcobjects.arcobjectconversion import convertArcObjectToPythonObject
    try:
        retval = convertArcObjectToPythonObject(gp.Buffer_analysis(*gp_fixargs((in_features, out_feature_class, buffer_distance_or_field, line_side, line_end_type, dissolve_option, dissolve_field), True)))
        return retval
    except Exception, e:
        raise e

@gptooldoc('CreateThiessenPolygons_analysis', None)
def CreateThiessenPolygons(in_features=None, out_feature_class=None, fields_to_copy=None):
    """CreateThiessenPolygons_analysis(in_features, out_feature_class, {fields_to_copy})

        Creates Thiessen polygons from point input features.Each Thiessen polygon
        contains only a single point input feature. Any location
        within a Thiessen polygon is closer to its associated point than to any other
        point input feature.

     INPUTS:
      in_features (Feature Layer):
          The point input features from which Thiessen polygons will be generated.
      fields_to_copy {String}:
          Determines which attributes from the point input features will be transferred to
          the output feature class.

          * ONLY_FID—Only the FID field from the input features will be transferred to the
          output feature class. This is the default.

          * ALL—All attributes from the input features will be transferred to the output
          feature class.

     OUTPUTS:
      out_feature_class (Feature Class):
          The output feature class containing the Thiessen polygons that are generated
          from the point input features."""
    from arcpy.geoprocessing._base import gp, gp_fixargs
    from arcpy.arcobjects.arcobjectconversion import convertArcObjectToPythonObject
    try:
        retval = convertArcObjectToPythonObject(gp.CreateThiessenPolygons_analysis(*gp_fixargs((in_features, out_feature_class, fields_to_copy), True)))
        return retval
    except Exception, e:
        raise e

@gptooldoc('GenerateNearTable_analysis', None)
def GenerateNearTable(in_features=None, near_features=None, out_table=None, search_radius=None, location=None, angle=None, closest=None, closest_count=None):
    """GenerateNearTable_analysis(in_features, near_features;near_features..., out_table, {search_radius}, {location}, {angle}, {closest}, {closest_count})

        Determines the distances from each feature in the input features to one or more
        nearby features in the near features, within the search radius. The results are
        recorded in the output table.

     INPUTS:
      in_features (Feature Layer):
          The input features that can be point, polyline, polygon, or multipoint type.
      near_features (Feature Layer):
          Value used to find the nearest features from input features. There can be one or
          more entries of near features; each entry can be of point, polyline, polygon, or
          multipoint type. When multiple entries of near features are specified, a new
          field, NEAR_FC, is added to the input table to store the paths of the source
          feature class that contains the nearest features.
      search_radius {Linear unit}:
          Specifies the radius used to search for candidate near features. The near
          features within this radius are considered for calculating the nearest feature.
          If no value is specified, that is, the default (empty) radius is used, all near
          features are considered for calculation. The unit of the search radius defaults
          to the units of the coordinate system of the input features. The units can be
          changed to any other unit. However, this has no impact on the units of NEAR_DIST
          which is based on the units of the coordinate system of the input features.
      location {Boolean}:
          Specifies whether x- and y-coordinates of the nearest location of the near
          feature will be written to new fields NEAR_X and NEAR_Y, respectively.

          * NO_LOCATION—Specifies that the x- and y-coordinates of the nearest location
          will not be written. This is the default.

          * LOCATION—Specifies that the x- and y-coordinates of the nearest location will
          be written to NEAR_X and NEAR_Y fields.
      angle {Boolean}:
          Specifies whether the near angle values in decimal degrees will be calculated
          and written to a new field, NEAR_ANGLE. A near angle measures from the x-axis
          (horizontal axis) to the direction of the line connecting an input feature to
          its nearest feature at their closest locations, and it is within the range of 0
          to 180 or 0 to -180 decimal degrees - 0 to the east, 90 to the north, 180
          (-180°) to the west, and -90 to the south.

          * NO_ANGLE—Specifies that the near angle values will not be written. This is the
          default.

          * ANGLE—Specifies that the near angle values will be written to the NEAR_ANGLE
          field.
      closest {Boolean}:
          Determines whether to locate and return only the closest features or all the
          features within the search radius.

          * CLOSEST—Locate and return only the closest features from the near features to
          the input features within the search radius. This is the default.

          * ALL—Locate and return all features from the near features to the input
          features within the search radius.
      closest_count {Long}:
          Find only the specified number of closest features. This parameter will not be
          used if the Find only closest feature option is checked.

     OUTPUTS:
      out_table (Table):
          The output table that will contain the proximity information—such as IN_FID,
          NEAR_FID, and NEAR_DIST—and other attributes—such as location (NEAR_X, NEAR_Y)
          and angle (NEAR_ANGLE)—of the near feature and the NEAR_FC, if necessary."""
    from arcpy.geoprocessing._base import gp, gp_fixargs
    from arcpy.arcobjects.arcobjectconversion import convertArcObjectToPythonObject
    try:
        retval = convertArcObjectToPythonObject(gp.GenerateNearTable_analysis(*gp_fixargs((in_features, near_features, out_table, search_radius, location, angle, closest, closest_count), True)))
        return retval
    except Exception, e:
        raise e

@gptooldoc('MultipleRingBuffer_analysis', None)
def MultipleRingBuffer(Input_Features=None, Output_Feature_class=None, Distances=None, Buffer_Unit=None, Field_Name=None, Dissolve_Option=None, Outside_Polygons_Only=None):
    """MultipleRingBuffer_analysis(Input_Features, Output_Feature_class, Distances;Distances..., {Buffer_Unit}, {Field_Name}, {Dissolve_Option}, {Outside_Polygons_Only})

        Creates multiple buffers at specified distances around the input features. These
        buffers can optionally be merged and dissolved using the buffer distance values
        to create non-overlapping buffers.

     INPUTS:
      Input_Features (Feature Layer):
          The input point, line, or polygon features to be buffered.
      Distances (Double):
          The list of buffer distances.
      Buffer_Unit {String}:
          The linear unit to be used with the Distance values. If the units are not
          specified, or entered as 'Default', the linear unit of the input features'
          spatial reference is used. If the Buffer Unit is specified as 'Default' and the
          Output Coordinate System geoprocessing environment has been set, its linear unit
          will be used.
      Field_Name {String}:
          The name of the field in the output feature class that stores the buffer
          distance used to create each buffer feature. If no name is specified, the
          default field name is 'distance'. This field will be of type Double.
      Dissolve_Option {String}:
          Determines if buffers will be dissolved to resemble rings around the input
          features.

          * ALL—Buffers will be rings around the input features that do not overlap (think
          of these as rings or donuts around the input features). The smallest buffer will
          cover the area of its input feature plus the buffer distance, and subsequent
          buffers will be rings around the smallest buffer which do not cover the area of
          the input feature or smaller buffers. All buffers of the same distance will be
          dissolved into a single feature. This is the default.

          * NONE—All buffer areas will be maintained regardless of overlap. Each buffer
          will cover its input feature plus the area of any smaller buffers.
      Outside_Polygons_Only {Boolean}:
          Valid only for polygon input features.

          * FULL—Buffers will overlap or cover the input features. This is the default.

          * OUTSIDE_ONLY—Buffers will be rings around the input features, and will not
          overlap or cover the input features (the area inside the input polygon will be
          erased from the buffer).

     OUTPUTS:
      Output_Feature_class (Feature Class):
          The output feature class that will contain multiple buffers."""
    from arcpy.geoprocessing._base import gp, gp_fixargs
    from arcpy.arcobjects.arcobjectconversion import convertArcObjectToPythonObject
    try:
        retval = convertArcObjectToPythonObject(gp.MultipleRingBuffer_analysis(*gp_fixargs((Input_Features, Output_Feature_class, Distances, Buffer_Unit, Field_Name, Dissolve_Option, Outside_Polygons_Only), True)))
        return retval
    except Exception, e:
        raise e

@gptooldoc('Near_analysis', None)
def Near(in_features=None, near_features=None, search_radius=None, location=None, angle=None):
    """Near_analysis(in_features, near_features;near_features..., {search_radius}, {location}, {angle})

        Determines the distance from each feature in the input features to the nearest
        feature in the near features, within the search radius.

     INPUTS:
      in_features (Feature Layer):
          The input features that can be point, polyline, polygon, or multipoint type.
      near_features (Feature Layer):
          Value used to find the nearest features from input features. There can be one or
          more entries of near features; each entry can be of point, polyline, polygon, or
          multipoint type. When multiple entries of near features are specified, a new
          field, NEAR_FC, is added to the input table to store the paths of the source
          feature class that contains the nearest features.
      search_radius {Linear unit}:
          Specifies the radius used to search for candidate near features. The near
          features within this radius are considered for calculating the nearest feature.
          If no value is specified, that is, the default (empty) radius is used, all near
          features are considered for calculation. The unit of the search radius defaults
          to the units of the coordinate system of the input features. The units can be
          changed to any other unit. However, this has no impact on the units of NEAR_DIST
          which is based on the units of the coordinate system of the input features.
      location {Boolean}:
          Specifies whether x- and y-coordinates of the nearest location of the near
          feature will be written to new fields NEAR_X and NEAR_Y, respectively.

          * NO_LOCATION—Specifies that the x- and y-coordinates of the nearest location
          will not be written. This is the default.

          * LOCATION—Specifies that the x- and y-coordinates of the nearest location will
          be written to NEAR_X and NEAR_Y fields.
      angle {Boolean}:
          Specifies whether the near angle values in decimal degrees will be calculated
          and written to a new field, NEAR_ANGLE. A near angle measures from the x-axis
          (horizontal axis) to the direction of the line connecting an input feature to
          its nearest feature at their closest locations, and it is within the range of 0
          to 180 or 0 to -180 decimal degrees - 0 to the east, 90 to the north, 180
          (-180°) to the west, and -90 to the south.

          * NO_ANGLE—Specifies that the near angle values will not be written. This is the
          default.

          * ANGLE—Specifies that the near angle values will be written to the NEAR_ANGLE
          field."""
    from arcpy.geoprocessing._base import gp, gp_fixargs
    from arcpy.arcobjects.arcobjectconversion import convertArcObjectToPythonObject
    try:
        retval = convertArcObjectToPythonObject(gp.Near_analysis(*gp_fixargs((in_features, near_features, search_radius, location, angle), True)))
        return retval
    except Exception, e:
        raise e

@gptooldoc('PointDistance_analysis', None)
def PointDistance(in_features=None, near_features=None, out_table=None, search_radius=None):
    """PointDistance_analysis(in_features, near_features, out_table, {search_radius})

        Determines the distances from input point features to all points in the near
        features within a specified search radius.

     INPUTS:
      in_features (Feature Layer):
          The point features from which distances to the near features will be calculated.
      near_features (Feature Layer):
          The points to which distances from the input features will be calculated.
          Distances between points within the same feature class or layer can be
          determined by specifying the same feature class or layer for the input and near
          features.
      search_radius {Linear unit}:
          Specifies the radius used to search for candidate near features. The near
          features within this radius are considered for calculating the nearest feature.
          If no value is specified (that is, the default (empty) radius is used) all near
          features are considered for calculation. The unit of search radius defaults to
          units of the input features. The units can be changed to any other unit.
          However, this has no impact on the units of the output DISTANCE field which is
          based on the units of the coordinate system of the input features.

     OUTPUTS:
      out_table (Table):
          The table containing the list of input features and information about all near
          features within the search radius. If a search radius is not specified,
          distances from all input features to all near features are calculated."""
    from arcpy.geoprocessing._base import gp, gp_fixargs
    from arcpy.arcobjects.arcobjectconversion import convertArcObjectToPythonObject
    try:
        retval = convertArcObjectToPythonObject(gp.PointDistance_analysis(*gp_fixargs((in_features, near_features, out_table, search_radius), True)))
        return retval
    except Exception, e:
        raise e

@gptooldoc('PolygonNeighbors_analysis', None)
def PolygonNeighbors(in_features=None, out_table=None, in_fields=None, area_overlap=None, both_sides=None, cluster_tolerance=None, out_linear_units=None, out_area_units=None):
    """PolygonNeighbors_analysis(in_features, out_table, {in_fields;in_fields...}, {area_overlap}, {both_sides}, {cluster_tolerance}, {out_linear_units}, {out_area_units})

        Creates a table with statistics based on polygon contiguity (overlaps,
        coincident edges, or nodes).

     INPUTS:
      in_features (Feature Layer):
          The input polygon features.
      in_fields {Field}:
          Input attribute field or fields used to identify unique polygons or polygon
          groups and represent them in the output.
      area_overlap {Boolean}:
          Determines if overlapping polygons will be analyzed and reported in the output.

          * NO_AREA_OVERLAP—Overlapping relationships will not be analyzed and included in
          the output. This is the default.

          * AREA_OVERLAP—Overlapping relationships will be analyzed and included in the
          output.
      both_sides {Boolean}:
          Determines if both sides of neighbor relationships will be included in the
          output.

          * BOTH_SIDES— For a pair of neighboring polygons, report both neighboring
          information of one polygon being the source and the other being the neighbor and
          vice versa. This is the default.

          * NO_BOTH_SIDES— For a pair of neighboring polygons, only report neighboring
          information of one polygon being the source and the other being the neighbor. Do
          not include the reciprocal relationship.
      cluster_tolerance {Linear unit}:
          The minimum distance between coordinates before they are considered equal. By
          default, this is the XY Tolerance of the input features.
      out_linear_units {String}:
          Units used to report the total length of the coincident edge between
          neighboring polygons. The default is the input feature units.
      out_area_units {String}:
          Units used to report the area overlap of neighboring polygons. The default is
          the input feature units. This parameter is only enabled when the area_overlap
          parameter is set to AREA_OVERLAP.

     OUTPUTS:
      out_table (Table):
          The output table."""
    from arcpy.geoprocessing._base import gp, gp_fixargs
    from arcpy.arcobjects.arcobjectconversion import convertArcObjectToPythonObject
    try:
        retval = convertArcObjectToPythonObject(gp.PolygonNeighbors_analysis(*gp_fixargs((in_features, out_table, in_fields, area_overlap, both_sides, cluster_tolerance, out_linear_units, out_area_units), True)))
        return retval
    except Exception, e:
        raise e


# Statistics toolset
@gptooldoc('Frequency_analysis', None)
def Frequency(in_table=None, out_table=None, frequency_fields=None, summary_fields=None):
    """Frequency_analysis(in_table, out_table, frequency_fields;frequency_fields..., {summary_fields;summary_fields...})

        Reads a table and a set of fields and creates a new table containing unique
        field values and the number of occurrences of each unique field value.

     INPUTS:
      in_table (Table View / Raster Layer):
          The table containing the field(s) that will be used to calculate frequency
          statistics. This table can be an INFO or OLE DB table, a dBASE or a VPF table,
          or a             feature class table.
      frequency_fields (Field):
          The attribute field or fields that will be used to calculate frequency
          statistics.
      summary_fields {Field}:
          The attribute field or fields to sum and add to the output table. Null values
          are excluded from this calculation.

     OUTPUTS:
      out_table (Table):
          The table that will store the calculated frequency statistics."""
    from arcpy.geoprocessing._base import gp, gp_fixargs
    from arcpy.arcobjects.arcobjectconversion import convertArcObjectToPythonObject
    try:
        retval = convertArcObjectToPythonObject(gp.Frequency_analysis(*gp_fixargs((in_table, out_table, frequency_fields, summary_fields), True)))
        return retval
    except Exception, e:
        raise e

@gptooldoc('Statistics_analysis', None)
def Statistics(in_table=None, out_table=None, statistics_fields=None, case_field=None):
    """Statistics_analysis(in_table, out_table, statistics_fields;statistics_fields..., {case_field;case_field...})

        Calculates summary statistics for field(s) in a table.

     INPUTS:
      in_table (Table View / Raster Layer):
          The input table containing the field(s) that will be used to calculate
          statistics. The input can be an INFO table, a dBASE table, an OLE DB table, a
          VPF table, or a feature class.
      statistics_fields (Value Table):
          The numeric field containing attribute values used to calculate the specified
          statistic. Multiple statistic and field combinations may be specified. Null
          values are excluded from all statistical calculations.The Add Field button,
          which is used only in ModelBuilder, allows you to add
          expected field(s) so you can complete the dialog box and continue to build your
          model.Available statistics types are:

          * SUM—Adds the total value for the specified field.

          * MEAN—Calculates the average for the specified field.

          * MIN—Finds the smallest value for all records of the specified field.

          * MAX—Finds the largest value for all records of the specified field.

          * RANGE—Finds the range of values (MAX minus MIN) for the specified field.

          * STD—Finds the standard deviation on values in the specified field.

          * COUNT—Finds the number of values included in statistical calculations. This
          counts each value except null values. To determine the number of null values in
          a field, use the COUNT statistic on the field in question, and a COUNT statistic
          on a different field which does not contain nulls (for example, the OID if
          present), then subtract the two values.

          * FIRST—Finds the first record in the Input Table and uses its specified field
          value.

          * LAST—Finds the last record in the Input Table and uses its specified field
          value.
      case_field {Field}:
          The fields in the Input Table used to calculate statistics separately for each
          unique attribute value (or combination of attribute values when multiple fields
          are specified).

     OUTPUTS:
      out_table (Table):
          The output dBASE or geodatabase table that will store the calculated statistics."""
    from arcpy.geoprocessing._base import gp, gp_fixargs
    from arcpy.arcobjects.arcobjectconversion import convertArcObjectToPythonObject
    try:
        retval = convertArcObjectToPythonObject(gp.Statistics_analysis(*gp_fixargs((in_table, out_table, statistics_fields, case_field), True)))
        return retval
    except Exception, e:
        raise e

@gptooldoc('TabulateIntersection_analysis', None)
def TabulateIntersection(in_zone_features=None, zone_fields=None, in_class_features=None, out_table=None, class_fields=None, sum_fields=None, xy_tolerance=None, out_units=None):
    """TabulateIntersection_analysis(in_zone_features, zone_fields;zone_fields..., in_class_features, out_table, {class_fields;class_fields...}, {sum_fields;sum_fields...}, {xy_tolerance}, {out_units})

        Computes the intersection between two feature classes and cross-tabulates the
        area, length, or count of the intersecting features.

     INPUTS:
      in_zone_features (Feature Layer):
          The features used to identify zones.
      zone_fields (Field):
          The attribute field or fields that will be used to define zones.
      in_class_features (Feature Layer):
          The features used to identify classes.
      class_fields {Field}:
          The attribute field or fields used to define classes.
      sum_fields {Field}:
          The fields to sum from the Input Class Features.
      xy_tolerance {Linear unit}:
          The distance that determines the range in which features or their vertices are
          considered equal. By default, this is the XY Tolerance of the Input Zone
          Features.
      out_units {String}:
          Units to be used to calculate area or length measurements. Setting Output Units
          when the Input Class Features are points is not supported.

     OUTPUTS:
      out_table (Table):
          The table that will contain the cross-tabulation of intersections between zones
          and classes."""
    from arcpy.geoprocessing._base import gp, gp_fixargs
    from arcpy.arcobjects.arcobjectconversion import convertArcObjectToPythonObject
    try:
        retval = convertArcObjectToPythonObject(gp.TabulateIntersection_analysis(*gp_fixargs((in_zone_features, zone_fields, in_class_features, out_table, class_fields, sum_fields, xy_tolerance, out_units), True)))
        return retval
    except Exception, e:
        raise e


# End of generated toolbox code
del gptooldoc, gp, gp_fixargs, convertArcObjectToPythonObject