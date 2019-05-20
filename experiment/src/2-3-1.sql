use DBEXP

-- create test env
--- create users
insert into USERS (UID, NAME) values
	(1, '张三'), (2, '李四'), (3, '王五'), (4, '赵六')
--- create follow relations
insert into FOLLOW values
	(2, 1),	-- 张三 <- 李四
	(3, 1)	-- 张三 <- 王五

go
------------------ Experiment Code --------------------

select USERS.*
from USERS, FOLLOW
where USERS.UID = FOLLOW.UID
	and FOLLOW.UIDFLED = (
			select UID from USERS as U2 where U2.NAME = '张三'
		)
order by USERS.UID asc

go
------------------ Experiment Code --------------------

-- tear down test env
delete from FOLLOW
delete from USERS