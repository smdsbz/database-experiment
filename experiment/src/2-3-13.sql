use DBEXP

-- create test env
--- create users
insert into USERS (UID, NAME) values
	(1, 'aaa'), (2, 'bbb'), (3, 'ccc')
--- create follows
insert into FOLLOW values
	-- 1 <==> 2
	(2, 1), (1, 2),
	-- 1 <==> 3
	(3, 1), (1, 3),
	-- 2 <== 3
	(3, 2)

go
--------------------- Experiment Code ----------------------

select F1.UID, F1.UIDFLED
from FOLLOW as F1, FOLLOW as F2
where F1.UID = F2.UIDFLED
	and F1.UIDFLED = F2.UID

--------------------- Experiment Code ----------------------
go

-- tear down test env
delete from FOLLOW
delete from USERS