use DBEXP

-- create test env
--- create users
insert into USERS (UID, NAME) values
	(1, '����'), (2, '����'), (3, '����'), (4, '����')
--- create follow relations
insert into FOLLOW values
	(2, 1),	-- ���� <- ����
	(3, 1)	-- ���� <- ����

go
------------------ Experiment Code --------------------

select USERS.*
from USERS, FOLLOW
where USERS.UID = FOLLOW.UID
	and FOLLOW.UIDFLED = (
			select UID from USERS as U2 where U2.NAME = '����'
		)
order by USERS.UID asc

go
------------------ Experiment Code --------------------

-- tear down test env
delete from FOLLOW
delete from USERS