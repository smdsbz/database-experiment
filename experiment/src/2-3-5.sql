use DBEXP

-- create test env
--- create users
insert into USERS (UID, NAME, BYEAR) values
	(1, '1969', 1969), (2, '2011', 2011),
	(3, '1970', 1970), (4, '2010', 2010)

go
------------------------- Experiment Code ------------------------

--select USERS.UID, USERS.BYEAR, USERS.CITY
--from USERS
--where USERS.UID not in (
--			select U2.UID
--			from USERS as U2
--			where U2.BYEAR between 1970 and 2010
--		)

select USERS.UID, USERS.BYEAR, USERS.CITY
from USERS
where USERS.BYEAR not between 1970 and 2010

-- expecting:
--  #1 '1969'
--  #2 '2011'

------------------------- Experiment Code ------------------------
go

-- tear down test env
delete from USERS