use DBEXP

declare @_cnt integer = 0
-- create test env
insert into USERS (UID, NAME, BYEAR) values
	(1, 'aaa', 1990), (2, 'bbb', 2000), (3, 'ccc', 2000)
--- create blogs
insert into MBLOG values
	(1, 'AAA', 1, 2010, 1, 1, ''),
	(2, 'BBB', 2, 2010, 1, 1, ''),
	(3, 'CCC', 3, 2010, 1, 1, '')
--- create topdays
---  #1 'AAA' has been selected as topday for 25 times
set @_cnt = 0
while @_cnt < 25 begin
	insert into TOPDAY values (2010, 1, @_cnt, 1, 1)
	set @_cnt = @_cnt + 1
end
---  #2 'BBB' has been selected as topday for 9 times
set @_cnt = 0
while @_cnt < 9 begin
	insert into TOPDAY values (2010, 1, @_cnt, 2, 2)
	set @_cnt = @_cnt + 1
end
---  #3 'CCC' has been selected as topday for 10 times
set @_cnt = 0
while @_cnt < 10 begin
	insert into TOPDAY values (2010, 1, @_cnt, 3, 3)
	set @_cnt = @_cnt + 1
end

go
------------------ Experiment Code --------------------

drop function if exists getUserTopdayCount

go
create function getUserTopdayCount (
			@uid as integer
		) returns integer as begin
	declare @cnt integer
	select @cnt = count(*)
		from TOPDAY, MBLOG
		where TOPDAY.BID = MBLOG.BID
			and MBLOG.UID = @uid
	return @cnt
end
go

-- NOTE 为测试方便，这里设置条件为上头条天数大于等于 10 天
select USERS.UID
from USERS
where USERS.BYEAR >= 2000
	and dbo.getUserTopdayCount(USERS.UID) >= 10

-- expecting: #3

------------------ Experiment Code --------------------
go

-- tear down test env
delete from TOPDAY
delete from MBLOG
delete from USERS