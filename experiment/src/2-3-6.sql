use DBEXP

-- create test env
--- create users
insert into USERS (UID, NAME, CITY) values
	(1, 'aaa', '武汉'), (2, 'bbb', '北京'),
	(3, 'ccc', '上海'), (4, 'ddd', '武汉')

go
--------------------- Experiment Code ----------------------

select USERS.CITY, count(*) as '用户数'
from USERS
group by USERS.CITY

--------------------- Experiment Code ----------------------
go

-- tear down test env
delete from USERS