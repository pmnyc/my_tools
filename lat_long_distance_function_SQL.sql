create or replace FUNCTION latlon_distance_mile(Lat1 IN NUMBER, Lon1 IN NUMBER,
                                Lat2 IN NUMBER, Lon2 IN NUMBER,
                                Radius IN NUMBER DEFAULT 3963)
    RETURN NUMBER IS
-- Convert degrees to radians and make declaration
DegToRad NUMBER := 57.29577951;
ReturnValue NUMBER;
ACOS_Param NUMBER;
BEGIN
    -- nvl function is to replace null value if seen
    ACOS_Param := (sin(NVL(Lat1,0) / DegToRad) * SIN(NVL(Lat2,0) / DegToRad)) +
        (COS(NVL(Lat1,0) / DegToRad) * COS(NVL(Lat2,0) / DegToRad) *
        COS(NVL(Lon2,0) / DegToRad - NVL(Lon1,0)/ DegToRad));
    -- Check if greater than 1 due to floating point errors
    IF ACOS_Param > 1 THEN
        ACOS_Param := 1;
    END IF;
    -- Check if less than -1 due to floating point errors
    IF ACOS_Param < -1 THEN
        ACOS_Param := -1;
    END IF;
    ReturnValue := NVL(Radius,0) * ACOS(ACOS_Param);
    IF NVL(Lat1,99999) = 99999 or NVL(Lon1,99999) = 99999
        or NVL(Lat2,99999) = 99999 or NVL(Lon2,99999) = 99999 THEN
        ReturnValue := 0;
    END IF;
    RETURN ReturnValue;
END;

------------------------------------------
-- ANOTHER EXAMPLE USING QUERIES
------------------------------------------
-- create or replace FUNCTION search_partition (partval VARCHAR2, ptable_name VARCHAR2)
--     RETURN VARCHAR2
-- IS
--     temporary_varchar   LONG;
-- BEGIN
--     select high_value INTO temporary_varchar from user_tab_partitions where
--     partition_name = partval
--     AND table_name = ptable_name;

--     RETURN temporary_varchar;
-- END;


--------------------------------------------------------------------------------
-- Sample of SQL Queries for Running it --
--------------------------------------------------------------------------------
-- select /*+ PARALLEL(a,30) */ a.*,
--     lag(LONGITUDE, 1,null) over (partition by JOURNEY_ID order by TIMESTAMP) as lon2,
--     lag(LATITUDE, 1,null) over (partition by JOURNEY_ID order by TIMESTAMP) as lat2,
--     LATLON_DISTANCE_MILE(LATITUDE,
--                 LONGITUDE,
--                 lag(LATITUDE, 1,null) over (partition by JOURNEY_ID order by TIMESTAMP),
--                 lag(LONGITUDE, 1,null) over (partition by JOURNEY_ID order by TIMESTAMP)) as distance
--     from trip a
--     where rownum <= 2000;

--------------------------------------------------------------------------------
-- There are many other Optimizer hints and SQL methods. You can find few topics we discussed today in the below URL. I will find some more useful docs and provide next week.
-- http://www.dba-oracle.com/art_sql_tune.htm
-- Sample Code
--------------------------------------------------------------------------------
-- alter session enable parallel DML

-- insert into /*+ APPEND PARALLEL(a,15) */ mytemptable
-- select /*+ PARALLEL(route,10) */
        -- cast(JOURNEY_ID as varchar(255)) JOURNEY_ID,
        -- cast(LATITUDE as float) LATITUDE,
        -- cast(LONGITUDE as float) LONGITUDE,
        -- (timestamp '1970-01-01 00:00:00 GMT' + numtodsinterval(TIMESTAMP/1000, 'SECOND')) AS datetime,
-- from trip a
-- where LATITUDE in (select LATITUDE from table_list_of_ids)
