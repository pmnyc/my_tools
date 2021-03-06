use [Gas_Growth]
go

/************ This is to define which variable to manipulate *************/
declare @ListOfField table (id int identity, Field varchar(100), primary key (id));
insert into @ListOfField(Field) values('CDE_FUEL_TYPE_TRW');
insert into @ListOfField(Field) values('CDE_HEAT_SYSTEM_TRW');
insert into @ListOfField(Field) values('CDE_LAND_USE_TRW');
insert into @ListOfField(Field) values('CDE_PROPERTY_TYPE_TRW');
insert into @ListOfField(Field) values('CDE_EXT_WALL_TRW_NL');
insert into @ListOfField(Field) values('CDE_BLDG_COND_TRW_NL');
insert into @ListOfField(Field) values('CDE_BLDG_STYLE_TRW_NL');
insert into @ListOfField(Field) values('CDE_ROOF_MTRL_TRW_NL');
insert into @ListOfField(Field) values('CDE_ROOF_TRW_NL');

declare @sourcetable_name varchar(100) = '[dbo].[TRW_STEP01]';
declare @MainField varchar(100) = 'ADDRESS_BUILDING_LEV1'; ---- This is to specify level data is aggregated on, such as building address
declare @rank_reference varchar(100) = 'AMT_TOT_VALUE_TRW'; ----This is to specify which field is used to rank other variables within the same address
declare @NumOfTopFieldValues int = 5; ----This is to specify we select top 5 values of certain variable by address;

/************** Below are generic codes **************/
declare @MyField varchar(50);
declare @cmd varchar(max);
declare @OutputTable_name varchar(100);
declare @MyTable_1 table (rowid int identity, MainField varchar(150), RefField float, MyField varchar(100), primary key(rowid));
declare @loop varchar(150);
declare @MyTable_2 table (rowid int identity, MainField varchar(150), RefField float, MyField varchar(150), primary key(rowid));
declare @MyTable_3 table (rowid int identity, MainField varchar(150), RefField float, MyField varchar(150), Rank int, primary key(rowid));
declare @MyTable_4 table (rowid int identity, MainField varchar(150), RefField float, MyField varchar(150), Rank int, MaxRank int, primary key(rowid));
declare @MyTable_7 table (rowid int identity, MainField varchar(150),
                          MyField_1 varchar(100), MyField_2 varchar(100), MyField_3 varchar(100), MyField_4 varchar(100), MyField_5 varchar(100),
                          primary key (rowid));
declare @MyTable_7_2 table (rowid int identity, MainField varchar(150),
                          MyField_1 varchar(100), MyField_2 varchar(100), MyField_3 varchar(100), MyField_4 varchar(100), MyField_5 varchar(100),
                          primary key (rowid)); 
------------Above is to declare variables
declare @ii int=1;
while @ii <= (select count(*) from @ListOfField)
begin
select @MyField = Field from @ListOfField where id = @ii;
print @MyField;

set @OutputTable_name = 'aux.' + @MyField;

if OBJECT_ID('dbo.temp') is not null
             drop table [dbo].[temp];

set @cmd = '
SELECT ' + @MainField + ' , sum(' + @rank_reference + ') ' + @rank_reference + '
       ,' + @MyField + '
   into dbo.temp
  FROM ' + @sourcetable_name + ' 
  group by ' + @MainField +', ' + @MyField
  + ' order by ' + @MainField;
exec(@cmd);

delete from @MyTable_1;
insert into @MyTable_1 select * from dbo.temp;

delete from @MyTable_7_2;
insert into @MyTable_7_2
select a.MainField, a.MyField MyField_1 , a.MyField MyField_2,
       a.MyField MyField_3, a.MyField MyField_4, a.MyField MyField_5
    from @MyTable_1 a
    join (select MainField from @MyTable_1 group by MainField having COUNT(1) = 1) b
    on a.MainField = b.MainField;

delete a
from @MyTable_1 a
    join (select MainField from @MyTable_1 group by MainField having COUNT(1) = 1) b
    on a.MainField = b.MainField;

if OBJECT_ID('dbo.temp_table1') is not null
             drop table [dbo].[temp_table1];
select * into [dbo].[temp_table1] from @MyTable_1;

alter table [dbo].[temp_table1]
add constraint pk_temp_table1 primary key (rowid);

/****** Select top 5 records for certain field, like fuel type, etc, by Address*****/
if OBJECT_ID('dbo.temp') is not null
             drop table [dbo].[temp];
select @loop = min(MainField) from @MyTable_1;
delete from @MyTable_2;
while @loop is not null
begin
	 set @cmd = 'select top ' + convert(varchar(100),@NumOfTopFieldValues) + ' MainField, RefField, MyField
				into [dbo].[temp] from [dbo].[temp_table1] where MainField = ''' + @loop + ''' order by MainField, RefField desc';
	 exec(@cmd);
	 insert into @MyTable_2
	 select MainField, RefField, MyField from dbo.temp;
	 drop table dbo.temp;
	 select @loop = min(MainField) from @MyTable_1 where MainField > @loop;
end;

if OBJECT_ID('dbo.temp') is not null
             drop table [dbo].[temp];

if OBJECT_ID('dbo.temp_table1') is not null
             drop table [dbo].[temp_table1];

delete from @MyTable_3;
insert into @MyTable_3
select MainField, RefField, MyField, RANk() OVER (Partition By MainField order by RefField desc) Rank
from @MyTable_2;

/********* Replicate records with lowest rank to make up 5 records in total **********/
/*****@NumOfTopFieldValues=5 means we select top 5 values of a certain variable by address *******/
delete from @MyTable_4;
insert into @MyTable_4
select a.MainField, a.RefField, a.MyField, a.Rank, b.maxrank
from @MyTable_3 a
join (select MainField, max(RANK) maxrank from @MyTable_3 group by MainField) b
on a.MainField = b.MainField
order by a.mainfield;

delete from @MyTable_7;
insert into @MyTable_7
select MainField, null, null, null, null, null from @MyTable_4 group by MainField;

select @loop = MIN(MainField) from @MyTable_7;
while @loop is not null
begin
     update m 
     set MyField_1 = b.MyField
     from @MyTable_7 m join (select * from @MyTable_4 where MainField = @loop) b
     on m.MainField = b.MainField and b.Rank = (case when b.MaxRank >= 1 then 1 else b.MaxRank end);
     
     update m 
     set MyField_2 = b.MyField
     from @MyTable_7 m join (select * from @MyTable_4 where MainField = @loop) b
     on m.MainField = b.MainField and b.Rank = (case when b.MaxRank >= 2 then 2 else b.MaxRank end);
    
     update m 
     set MyField_3 = b.MyField
     from @MyTable_7 m join (select * from @MyTable_4 where MainField = @loop) b
     on m.MainField = b.MainField and b.Rank = (case when b.MaxRank >= 3 then 3 else b.MaxRank end);

     update m 
     set MyField_4 = b.MyField
     from @MyTable_7 m join (select * from @MyTable_4 where MainField = @loop) b
     on m.MainField = b.MainField and b.Rank = (case when b.MaxRank >= 4 then 4 else b.MaxRank end);

     update m 
     set MyField_5 = b.MyField
     from @MyTable_7 m join (select * from @MyTable_4 where MainField = @loop) b
     on m.MainField = b.MainField and b.Rank = (case when b.MaxRank >= 5 then 5 else b.MaxRank end);
     
select @loop = MIN(MainField) from @MyTable_7 where MainField > @loop;
end;

if OBJECT_ID('dbo.temp') is not null
             drop table [dbo].[temp];
if object_id(@OutputTable_name) is not null
             exec('drop table ' + @OutputTable_name);

select * into [dbo].[temp] from @MyTable_7;
insert into [dbo].[temp]
select MainField, MyField_1, MyField_2, MyField_3, MyField_4, MyField_5 from @MyTable_7_2;

update [dbo].[temp]
set MyField_1 = coalesce(MyField_1, MyField_2, MyField_3, MyField_4, MyField_5),
    MyField_2 = coalesce(MyField_2, MyField_1, MyField_3, MyField_4, MyField_5),
    MyField_3 = coalesce(MyField_3, MyField_2, MyField_1, MyField_4, MyField_5),
    MyField_4 = coalesce(MyField_4, MyField_3, MyField_2, MyField_1, MyField_5),
    MyField_5 = coalesce(MyField_5, MyField_4, MyField_3, MyField_2, MyField_1);

alter table [dbo].[temp]
add constraint pk_temptemp primary key (rowid asc);
set @cmd = 'select MainField as MainField@, MyField_1 as MyField@_1, 
            MyField_2 as MyField@_2, MyField_3 as MyField@_3, MyField_4 as MyField@_4, MyField_5 as MyField@_5
            into ' + @OutputTable_name + '
            from [dbo].[temp]';
set @cmd = REPLACE(@cmd,'MainField@', @MainField);
set @cmd = REPLACE(@cmd,'MyField@_', @MyField + '_Top');
print @cmd;
exec(@cmd);
if OBJECT_ID('dbo.temp') is not null
             drop table [dbo].[temp];

set @cmd = 'alter table ' + @OutputTable_name + '
           alter column ' + @MainField + ' varchar(150) not null';
exec(@cmd);
/***
set @cmd = 'alter table ' + @OutputTable_name + '
           add constraint pk_' + replace(@OutputTable_name,'dbo.','') + ' primary key ('
           + @MainField + ')'; ***/
set @cmd = 'alter table ' + @OutputTable_name + '
           add constraint pk_' + convert(varchar(20),convert(bigint,round(rand()* 1e18,0))) + ' primary key ('
           + @MainField + ')';
print @cmd;
exec(@cmd);

   set @ii += 1;
end