use DBEXP

-- create test env
declare @_cnt integer = 0
--- create users
while @_cnt < 15 begin
	insert into USERS (UID, NAME, BYEAR) values (@_cnt+1, cast(@_cnt as varchar(8)), 2001)
	set @_cnt = @_cnt + 1
end
while @_cnt < 30 begin
	insert into USERS (UID, NAME, BYEAR) values (@_cnt+1, cast(@_cnt as varchar(8)), 2000)
	set @_cnt = @_cnt +1
end
--- create blogs
insert into MBLOG values
	(1, 'AAA', 1, 1970, 1, 1, 'fdjaskl'),
	(2, 'BBB', 2, 1970, 1, 1, 'fhdjklsa')
--- create thumbs
---- #1 'AAA': 12 subs by users born in 2001
set @_cnt = 0
while @_cnt < 12 begin
	insert into THUMB values (@_cnt+2, 1)
	set @_cnt = @_cnt + 1
end
---- #2 'BBB': 5 subs by users born in 2001, and 12 subs by users born in 2000
set @_cnt = 0
while @_cnt < 5 begin
	insert into THUMB values (@_cnt+3, 2)
	set @_cnt = @_cnt + 1
end
set @_cnt = 0
while @_cnt < 12 begin
	insert into THUMB values (@_cnt+16, 2)
	set @_cnt = @_cnt + 1
end
--- create topday
insert into TOPDAY values
	(1970, 1, 1, 1, 1),
	(1970, 1, 2, 1, 1)

go
--------------------- Experiment Code ----------------------

select TOPDAY.BID, count(*) as '上头条次数'
from TOPDAY, MBLOG
where TOPDAY.BID = MBLOG.BID
	and MBLOG.BID in (
			select THUMB.BID
			from THUMB, USERS
			where THUMB.UID = USERS.UID
				and USERS.BYEAR > 2000
			group by THUMB.BID
			having count(*) > 10
		)
group by TOPDAY.BID

-- expecting: #1 'AAA'

--------------------- Experiment Code ----------------------
go

-- tear down test env
delete from TOPDAY
delete from THUMB
delete from MBLOG
delete from USERS