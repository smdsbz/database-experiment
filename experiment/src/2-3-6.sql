use DBEXP

-- create test env
--- create users
insert into USERS (UID, NAME, CITY) values
	(1, 'aaa', '�人'), (2, 'bbb', '����'),
	(3, 'ccc', '�Ϻ�'), (4, 'ddd', '�人')

go
--------------------- Experiment Code ----------------------

select USERS.CITY, count(*) as '�û���'
from USERS
group by USERS.CITY

--------------------- Experiment Code ----------------------
go

-- tear down test env
delete from USERS