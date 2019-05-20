use DBEXP

-- create test env
--- create users
insert into USERS (UID, NAME, BYEAR, CITY) values
	(1, '2000wuhan', 2000, 'Œ‰∫∫'),
	(2, '2001beijing', 2001, '±±æ©'),
	(3, '2001wuhan', 2001, 'Œ‰∫∫'),
	(4, '2002wuhan', 2002, 'Œ‰∫∫')
--- create blogs
insert into MBLOG values
	(1, 'AAA', 1, 2005, 1, 1, 'aaa'),	-- 'AAA' by '2000wuhan' (user unsatisfy)
	(2, 'BBB', 2, 2005, 1, 1, 'bbb'),	-- 'BBB' by '2001beijing' (user unsatisfy)
	(3, 'CCC', 3, 2005, 1, 1, 'ccc'),	-- 'CCC' by '2001wuhan' (user staisfied, not in topday)
	(4, 'DDD', 4, 2005, 1, 1, 'ddd')	-- 'DDD' by '2002wuhan' (expected)
--- create topdays
insert into TOPDAY values
	(2005, 2, 2, 1, 1),	-- 'AAA' by '2000wuhan'
	(2005, 2, 2, 2, 2),	-- 'BBB' by '2001beijing'
	(2005, 2, 2, 4, 3)	-- 'DDD' by '2002wuhan'

go
------------------------- Experiment Code --------------------

select MBLOG.BID as '≤©ŒƒID', MBLOG.TITLE, USERS.NAME
from MBLOG, USERS
where MBLOG.UID = USERS.UID
	and USERS.BYEAR > 2000
	and USERS.CITY = 'Œ‰∫∫'
	and MBLOG.BID in (select TOPDAY.BID from TOPDAY)

-- expecting: #4 'DDD' by '2002wuhan'

------------------------- Experiment Code --------------------
go

delete from TOPDAY
delete from MBLOG
delete from USERS