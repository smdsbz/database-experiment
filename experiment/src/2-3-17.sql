use DBEXP

-- create test env
--- create user
---  'U1' ~ 'U15'
declare @_cnt integer = 0
while @_cnt < 15 begin
	insert into USERS (UID, NAME) values (@_cnt+1, 'U'+cast(@_cnt+1 as varchar(8)))
	set @_cnt = @_cnt + 1
end
--- create blogs
---  'B1' ~ 'B15' by #1 'U1'
set @_cnt = 0
while @_cnt < 15 begin
	insert into MBLOG values (@_cnt, 'B'+cast(@_cnt+1 as varchar(8)), 1, 1970, 1, 1, '')
	set @_cnt = @_cnt + 1
end
--- create thumbs
---  'B1' ~'B11' all thumbed once (by 'U2' ~ 'U12')
set @_cnt = 0
while @_cnt < 11 begin
	insert into THUMB values (@_cnt+2, @_cnt+1)
	set @_cnt = @_cnt + 1
end
---  additionally, 'B{n}' thumbed one more time (by 'U{n+13]'), for n = [1..2]
set @_cnt = 0
while @_cnt < 2 begin
	insert into THUMB values (@_cnt+13, @_cnt+1)
	set @_cnt = @_cnt + 1
end
---  'B12' ~ 'B15' are not thumbed

go
-------------------- Experiment Code ---------------------

drop view if exists TOP_TEN

go
create view TOP_TEN as
select MBLOG.BID as BID, MBLOG.TITLE as BTITLE,
		USERS.UID as UID, USERS.NAME as UNAME,
		C.CNT as NUM_THUMBS
from MBLOG, USERS, (select top(10) THUMB.BID, count(*) as CNT
					from THUMB
					group by THUMB.BID
					order by CNT desc) as C
where C.BID = MBLOG.BID
	and USERS.UID = MBLOG.UID
go

select * from TOP_TEN

-------------------- Experiment Code ---------------------
go

-- tear down test env
delete from THUMB
delete from MBLOG
delete from USERS