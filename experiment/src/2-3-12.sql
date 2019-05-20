use DBEXP

-- create test env
--- create users
insert into USERS (UID, NAME) values (1, 'aaa')
--- create blogs
insert into MBLOG values
	(1, '这里没有关键字', 1, 1970, 1, 1, ''),
	(2, '最多地铁站', 1, 1970, 1, 1, ''),
	(3, '华中科技大学', 1, 1970, 1, 1, ''),
	(4, '坐拥最多地铁站的华中科技大学', 1, 1970, 1, 1, '')

go
--------------------- Experiment Code ------------------------

select *
from MBLOG
where TITLE like '%最多地铁站%'
	or TITLE like '%华中科技大学%'

--------------------- Experiment Code ------------------------
go

-- tear down test env
delete from MBLOG
delete from USERS