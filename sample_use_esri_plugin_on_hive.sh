# The code eventually failed due to the compatability issue with Hadoop version. But this code gives some idea on how to use Hive in simple way
# Bash Sript Part
git clone https://github.com/cstanca1/hdp-hive-spatial.git
cd hdp-hive-spatial

hadoop fs -mkdir /user/hive/esri/
hadoop fs -put tmp/esri/* hdfs:///user/hive/esri/
hadoop fs -ls hdfs:///user/hive/esri

######################   Below are HIVE Script   #####################
# Now Launch Hive through command > hive

set mapreduce.map.memory.mb=10240;
set mapreduce.map.java.opts=-Xmx10240m;
set tez.am.resource.memory.mb=10240;
set tez.task.resource.memory.mb=10240;

set hive.tez.container.size=10240mb;
set hive.tez.java.opts=-Xmx8192m;


add jar hdfs:///user/hive/esri/esri-geometry-api.jar;
add jar hdfs:///user/hive/esri/spatial-sdk-hive-1.1.1-SNAPSHOT.jar;
add jar hdfs:///user/hive/esri/spatial-sdk-json-1.1.1-SNAPSHOT.jar;

create temporary function st_geomfromtext as 'com.esri.hadoop.hive.ST_GeomFromText';
create temporary function st_geometrytype as 'com.esri.hadoop.hive.ST_GeometryType';
create temporary function st_point as 'com.esri.hadoop.hive.ST_Point';
create temporary function st_asjson as 'com.esri.hadoop.hive.ST_AsJson';
create temporary function st_asbinary as 'com.esri.hadoop.hive.ST_AsBinary';
create temporary function st_astext as 'com.esri.hadoop.hive.ST_AsText';
create temporary function st_intersects as 'com.esri.hadoop.hive.ST_Intersects';
create temporary function st_x as 'com.esri.hadoop.hive.ST_X';
create temporary function st_y as 'com.esri.hadoop.hive.ST_Y';
create temporary function st_srid as 'com.esri.hadoop.hive.ST_SRID';
create temporary function st_linestring as 'com.esri.hadoop.hive.ST_LineString';
create temporary function st_pointn as 'com.esri.hadoop.hive.ST_PointN';
create temporary function st_startpoint as 'com.esri.hadoop.hive.ST_StartPoint';
create temporary function st_endpoint as 'com.esri.hadoop.hive.ST_EndPoint';
create temporary function st_numpoints as 'com.esri.hadoop.hive.ST_NumPoints';


CREATE TABLE `demo_shape_point`(`shape` string) STORED AS ORC;

INSERT INTO `demo_shape_point`(`shape`)
VALUES ("POINT (-74.140007019999985 39.650001530000054)"),
("POINT (-74.140007019999985 39.650001530000054)"),
("POINT (-74.140007019999985 39.650001530000054)"),
("POINT (-74.140007019999985 39.650001530000054)"),
("POINT (-74.140007019999985 39.650001530000054)"),
("POINT (-74.140007019999985 39.650001530000054)"),
("POINT (-74.140007019999985 39.650001530000054)"),
("POINT (-74.140007019999985 39.650001530000054)"),
("POINT (-74.140007019999985 39.650001530000054)");

CREATE TABLE `demo_shape_linestring`(`shape` string) STORED AS ORC;

INSERT INTO `demo_shape_linestring`(`shape`)
VALUES ("LINESTRING (-77.300002999999947 15.700000000000045, -77.100005999999951 17.900000000000034, -76.900001999999972 20.299999000000071, -76.900001999999972 22.7999990                                                                                                     00000071, -76.699996999999939 26.299999000000071, -73.499999999999943 29.500000000000057, -68.999999999999943 32.000000000000057)");

CREATE TABLE `demo_shape_polygon`(`shape` string) STORED AS ORC;

INSERT INTO `demo_shape_polygon`(`shape`)
VALUES ("POLYGON ((-78.011023999999964 13.102828000000045, -78.010642999999959 13.103308000000027, -78.717681999999968 12.728274000000056, -78.717681999999968 12.728264000000024, -78.718688999999983 12.727710000000059, -78.720138999999961 12.726795000000038, -78.721557999999959 12.725802000000044, -78.722899999999981 12.724729000000025, -78.724151999999947 12.723576000000037, -78.725303999999937 12.722371000000066, -78.72636399999999 12.721091000000058, -78.727378999999985 12.719742000000053, -78.728278999999986 12.718326000000047, -78.729125999999951 12.716850000000022, -78.729888999999957 12.715321000000074, -78.73054499999995 12.71374000000003, -78.731147999999962 12.712118000000032, -78.731666999999959 12.710457000000076, -78.732100999999943 12.708764000000031, -78.732459999999946 12.707044000000053, -78.73275799999999 12.705301000000077, -78.732947999999965 12.703543000000025, -78.733062999999959 12.70177300000006, -78.733115999999939 12.699998000000051, -78.733062999999959 12.698222000000044, -78.732947999999965 12.696453000000076, -78.73275799999999 12.694695000000024, -78.732459999999946 12.692952000000048, -78.732100999999943 12.69123200000007, -78.731666999999959 12.689539000000025, -78.731147999999962 12.687878000000069, -78.73054499999995 12.686255000000074, -78.729888999999957 12.684676000000024, -78.729125999999951 12.683146000000022, -78.728278999999986 12.681670000000054, -78.727378999999985 12.680255000000045, -78.72636399999999 12.678905000000043, -78.725303999999937 12.677626000000032, -78.102691999999934 11.99267100000003, -78.103476999999941 11.993669000000068, -78.094085999999947 11.982473000000027, -78.068755999999951 11.952874000000065, -78.044166999999959 11.924886000000072, -78.020286999999939 11.898667000000046, -77.997176999999965 11.874383000000023, -77.974769999999978 11.852190000000064, -77.95313299999998 11.832250000000045, -77.932204999999954 11.814722000000074, -77.912040999999988 11.799769000000026, -77.892615999999975 11.78754900000007, -77.873961999999949 11.778223000000025, -77.856032999999968 11.771952000000056, -77.838851999999974 11.768895000000043, -77.82243299999999 11.769215000000031, -77.806777999999952 11.773068000000023, -77.791884999999979 11.780619000000058, -77.777732999999955 11.792026000000021, -77.760848999999951 11.811623000000054, -77.745604999999955 11.835773000000074, -77.731917999999951 11.864168000000063, -77.719840999999974 11.896491000000026, -77.709296999999935 11.932430000000068, -77.700278999999966 11.971670000000074, -77.69279499999999 12.01389800000004, -77.686812999999972 12.058801000000074, -77.682303999999988 12.10606400000006, -77.679267999999979 12.155375000000049, -77.677657999999951 12.206418000000042, -77.677466999999979 12.258882000000028, -77.678695999999945 12.312451000000067, -77.68128999999999 12.366814000000034, -77.685225999999943 12.421657000000039, -77.690551999999968 12.476664000000028, -77.697165999999982 12.531522000000052, -77.705115999999975 12.585918000000049, -77.714324999999974 12.639541000000065, -77.724814999999978 12.69207300000005, -77.736533999999949 12.743203000000051, -77.749511999999982 12.792617000000064, -77.763663999999949 12.840000000000032, -77.77904499999994 12.885041000000058, -77.795577999999978 12.927423000000033, -77.81325499999997 12.966836000000058, -77.832046999999989 13.002964000000077, -77.851989999999944 13.035494000000028, -77.873000999999988 13.064113000000077, -77.895102999999949 13.088506000000052, -77.909911999999963 13.101058000000023, -77.924994999999967 13.11000800000005, -77.940375999999958 13.115515000000073, -77.956031999999936 13.117728000000056, -77.972014999999942 13.116804000000059, -77.988349999999969 13.112895000000037, -78.005019999999945 13.106156000000055, -78.011023999999964 13.102828000000045))");


//counts by geometry type -- assumes that other than ST_POINT values are possible
select st_geometrytype(st_geomfromtext(shape)), count(shape)
from demo_shape_point
group by st_geometrytype(st_geomfromtext(shape));

//counts by geometry type -- assumes that other than ST_LINESTRING values are possible
select st_geometrytype(st_geomfromtext(shape)), count(shape)
from demo_shape_linestring
group by st_geometrytype(st_geomfromtext(shape));

//counts by geometry type -- assumes that other than ST_POLYGON values are possible
select st_geometrytype(st_geomfromtext(shape)), count(shape)
from demo_shape_polygon
group by st_geometrytype(st_geomfromtext(shape));

// X and Y coordinates of the point
select st_x(st_point(shape)) AS X, st_y(st_point(shape)) AS Y
from demo_shape_point
where st_geometrytype(st_geomfromtext(shape)) = "ST_POINT"
limit 10;

// extract geometry from text shape
select st_geomfromtext(shape)
from demo_shape_point
where st_geometrytype(st_geomfromtext(shape)) = "ST_POINT"
limit 10;

// geometry type
select st_geometrytype(st_geomfromtext(shape))
from demo_shape_point
where st_geometrytype(st_geomfromtext(shape)) = "ST_POINT"
limit 10;

// point geometry as a binary - implicitly
select st_point(shape)
from demo_shape_point
where st_geometrytype(st_geomfromtext(shape)) = "ST_POINT"
limit 10;

// point geometry as a binary - explicitly
select st_asbinary(st_geomfromtext(shape))
from demo_shape_point
where st_geometrytype(st_geomfromtext(shape)) = "ST_POINT"
limit 10;

// point geometry as Json
select st_asjson(st_geomfromtext(shape))
from demo_shape_point
where st_geometrytype(st_geomfromtext(shape)) = "ST_POINT"
limit 10;

// point geometry as a text
select st_astext(st_point(shape))
from demo_shape_point
where st_geometrytype(st_geomfromtext(shape)) = "ST_POINT"
limit 1;

// SRID for a point
select distinct st_srid(st_point(shape))
from demo_shape_point
where st_geometrytype(st_geomfromtext(shape)) = "ST_POINT"
limit 1;

// line as text
select st_astext(st_linestring(shape))
from demo_shape_linestring
where st_geometrytype(st_geomfromtext(shape)) = "ST_LINESTRING"
limit 1;

// n point of a line
select st_astext(st_point(st_astext(st_pointn(st_linestring(shape), 2))))
from demo_shape_linestring
where st_geometrytype(st_geomfromtext(shape)) = "ST_LINESTRING"
limit 1;

// start and end points of a line
select st_astext(st_startpoint(st_linestring(shape))) AS StartPoint,
       st_astext(st_endpoint(st_linestring(shape))) AS EndPoint
from demo_shape_linestring
where st_geometrytype(st_geomfromtext(shape)) = "ST_LINESTRING"
limit 1;

// number of points in a polygon
select shape, st_numpoints(st_geomfromtext(shape)) as NumPoints
from demo_shape_polygon
where st_geometrytype(st_geomfromtext(shape)) = "ST_POLYGON"
limit 1;

// lines intersection - usually you would have two tables - this is just an example with a table with one row
select st_intersects(a.s1, b.s2)
from
   (select st_point(shape) AS  `s1`
      from demo_shape_point limit 1) a join
   (select st_point(shape) AS  `s2`
      from demo_shape_point limit 1) b
limit 1;

// lines intersection - usually you would have two tables - this is just an example with a table with one row
select st_intersects(a.s1, b.s2)
from
   (select st_linestring(0,0, 1,1) AS  `s1`
      from demo_shape_linestring limit 1) a join
   (select st_linestring(1,1, 0,0) AS  `s2`
      from demo_shape_linestring limit 1) b
limit 1;

