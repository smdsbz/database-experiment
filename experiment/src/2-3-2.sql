use DBEXP

-- setup test env
--- create users
insert into USERS (UID, NAME) values
	(1, 'aaa'), (2, 'bbb')
--- create blogs
insert into MBLOG values
	(1, 'AAA', 1, 1970, 1, 1, 'aAA'),	-- 'AAA' by 'aaa'
	(2, 'BBB', 2, 1970, 1, 1, 'bBB')	-- 'BBB' by 'bbb'
--- create thumb relations
insert into THUMB values (2, 1)	-- 'bbb' thumbs 'AAA'

go
------------------ Experiment Code -------------------------

select MBLOG.BID, MBLOG.TITLE, USERS.NAME
from USERS, MBLOG
where MBLOG.BID not in (select distinct BID from THUMB)
	and MBLOG.UID = USERS.UID
order by MBLOG.TITLE asc

-- expecting: 'BBB' by 'bbb'

------------------ Experiment Code -------------------------
go

delete from THUMB
delete from MBLOG
delete from USERS
