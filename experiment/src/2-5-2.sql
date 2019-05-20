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

drop table if exists TODAY_TOP_TEN
drop procedure if exists UPDATE_TOP_TEN

go
-- REQURIE view TOP_TEN exists
-- SIDE-EFFECT creates table TODAY_TOP_TEN
create procedure UPDATE_TOP_TEN as begin
	if not exists (select * from sysobjects where name='TOP_TEN' and xtype='U') begin
		create table TODAY_TOP_TEN (
			BID			integer		not null,
			NUM_THUMBS	integer		not null,
			foreign key (BID) references MBLOG
		)
	end
	delete from TODAY_TOP_TEN
	insert into TODAY_TOP_TEN (BID, NUM_THUMBS) (
			select BID, NUM_THUMBS from TOP_TEN
		)
end
go

exec UPDATE_TOP_TEN
select * from TODAY_TOP_TEN

-------------------- Experiment Code ---------------------
go

-- tear down test env
drop table if exists TODAY_TOP_TEN
delete from THUMB
delete from MBLOG
delete from USERS