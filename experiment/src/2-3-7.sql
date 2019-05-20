use DBEXP

-- create test env
--- create users
insert into USERS (UID, NAME, CITY, BYEAR) values
	(1, 'aaa', '武汉', 1970),
	(2, 'bbb', '武汉', 1970),
	(3, 'ccc', '武汉', 1971),
	(4, 'ddd', '北京', 1971),
	(5, 'eee', '北京', 1972)

go
--------------------- Expeirment Code --------------------------

select USERS.CITY, USERS.BYEAR, count(*) as '用户数'
from USERS
group by USERS.CITY, USERS.BYEAR
order by USERS.CITY asc, USERS.BYEAR desc

-- expecting:
--  北京  1972  1
--  北京  1971  1
--  武汉  1971  1
--  武汉  1970  2

--------------------- Expeirment Code --------------------------
go

-- tear down test env
delete from USERS