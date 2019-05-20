use DBEXP

-- create test env
--- create users
insert into USERS (UID, NAME) values
	(1, 'aaa'), (2, 'bbb'), (3, 'ccc'),
	(4, 'ddd'), (5, 'eee')
--- create follows
insert into FOLLOW values
	-- 1 ==> 2, 3, 4, 5
	(1, 2), (1, 3), (1, 4), (1, 5),
	-- 2 ==> 1, 3, 4, 5
	(2, 1), (2, 3), (2, 4), (2, 5),
	-- 3 ==> nil
	-- 4 ==> 1, 2, 3
	(4, 1), (4, 2), (4, 3),
	-- 5 ==> 1, 3, 4
	(5, 1), (5, 3), (5, 4)

go
------------------ Experiment Code ------------------

select U1.UID, U2.UID
from USERS as U1, USERS as U2
where U1.UID != U2.UID
	and (select distinct count(F1.UIDFLED)
			from FOLLOW as F1 inner join FOLLOW as F2 on F1.UIDFLED = F2.UIDFLED
			where F1.UID = U1.UID and F2.UID = U2.UID) >= 3

-- expecting:
--  1 <==> 2, 2 <==> 5

------------------ Experiment Code ------------------
go

-- tear down test env
delete from FOLLOW
delete from USERS