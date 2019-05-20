use DBEXP

-- create test env
--- create users
insert into USERS (UID, NAME, CITY, BYEAR) values
	(1, 'aaa', '�人', 1970),
	(2, 'bbb', '�人', 1970),
	(3, 'ccc', '�人', 1971),
	(4, 'ddd', '����', 1971),
	(5, 'eee', '����', 1972)

go
--------------------- Expeirment Code --------------------------

select USERS.CITY, USERS.BYEAR, count(*) as '�û���'
from USERS
group by USERS.CITY, USERS.BYEAR
order by USERS.CITY asc, USERS.BYEAR desc

-- expecting:
--  ����  1972  1
--  ����  1971  1
--  �人  1971  1
--  �人  1970  2

--------------------- Expeirment Code --------------------------
go

-- tear down test env
delete from USERS