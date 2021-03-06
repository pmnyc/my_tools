use mydb
go

-------------------- Define initial parameters ------------------------
declare @regular_tablename varchar(max) = 'dbo.source';
declare @output_tablename varchar(max) = 'dbo.myoutput';

------------ Load Source Regular Data ---------
if object_id('tempdb..#reg_scd') is not null
		drop table #reg_scd;
declare @cmd varchar(max);
set @cmd = 'select * into dbo.ZZZ from '+@regular_tablename;
exec(@cmd)
select * into #reg_scd from dbo.ZZZ;
drop table dbo.ZZZ;

------------ Create special schedule that goes full calendar month ---------
if object_id('tempdb..#spec_scd') is not null
		drop table #spec_scd;
select mycalendar, YYYY, Period, 20 as Cycle,
		mycalendar as BiaoStartDay,
		DATEADD(DAY, -(DAY(DATEADD(MONTH, 1, mycalendar))), DATEADD(MONTH, 1, mycalendar)) BiaoEndDay,
		myid, 'Special' as ScheduleType, BiaoSys, ver
	into #spec_scd
	from #reg_scd
	group by mycalendar, YYYY, Period, myid, BiaoSys, ver
	order by ver desc, myid, mycalendar;
	
------------ Create Cut schedule that ends on the end of month ---------
if object_id('tempdb..#cut_scd') is not null
		drop table #cut_scd;
select a.mycalendar, a.YYYY, a.Period, a.Cycle, 
		a.BiaoStartDay,
		case when a.BiaoEndDay <= (cast(DATEADD(day,-1,a.mycalendar) as DATE)) then a.BiaoEndDay
			else (cast(DATEADD(day,-1,a.mycalendar) as DATE)) end as BiaoEndDay,
		a.myid,
		'Cut' as ScheduleType,
		a.BiaoSys, a.ver
	into #cut_scd
	from #reg_scd a
	order by ver desc, a.myid, a.mycalendar, a.Cycle;

------------ Append Regular, Special and Cut schedules together ------------
set @cmd = 'if object_id('''+@output_tablename+''') is not null
		drop table '+@output_tablename;
exec(@cmd)
select * into dbo.ZZZ
		from (
		(select mycalendar, YYYY, Period, Cycle, BiaoStartDay, BiaoEndDay, myid, ScheduleType, BiaoSys, ver from #reg_scd)
		union all
		(select mycalendar, YYYY, Period, Cycle, BiaoStartDay, BiaoEndDay, myid, ScheduleType, BiaoSys, ver from #spec_scd)
		union all
		(select mycalendar, YYYY, Period, Cycle, BiaoStartDay, BiaoEndDay, myid, ScheduleType, BiaoSys, ver from #cut_scd)
) m ;

set @cmd = 'select * into ' + @output_tablename +' from dbo.ZZZ	order by ver desc, myid, mycalendar, cycle, ScheduleType';
exec(@cmd)
drop table dbo.ZZZ;
---------------- Drop temp tables ----------------
drop table #reg_scd;
drop table #spec_scd;
drop table #cut_scd;