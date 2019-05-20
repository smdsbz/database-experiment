use DBEXP

-- create test env
declare @_cnt integer = 0
--- create users
while @_cnt < 15 begin
	insert into USERS (UID, NAME) values (@_cnt+1, cast(@_cnt as varchar(8)))
	set @_cnt = @_cnt + 1
end
--- create blogs
insert into MBLOG values
	(1, 'AAA', 1, 1970, 1, 1, 'fdjaskl'),
	(2, 'BBB', 2, 1970, 1, 1, 'fhdjklsa')
--- create thumbs
set @_cnt = 0

while @_cnt < 12 begin
	insert into THUMB values (@_cnt+2, 1)
	set @_cnt = @_cnt + 1
end
set @_cnt = 0
while @_cnt < 5 begin
	insert into THUMB values (@_cnt+3, 2)
	set @_cnt = @_cnt + 1
end

go
--------------------- Experiment Code ----------------------

select MBLOG.BID, MBLOG.TITLE
from MBLOG
where MBLOG.BID in (
			select THUMB.BID
			from THUMB
			group by THUMB.BID
			having count(*) > 10
		)

-- expecting: #1 'AAA'

--------------------- Experiment Code ----------------------
go

-- tear down test env
delete from THUMB
delete from MBLOG
delete from USERS