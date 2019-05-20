use DBEXP

-- create test env
--- create users
insert into USERS (UID, NAME, SEX, BYEAR, CITY) values
	(1, 'aaa', '男', 1998, '武汉'),
	(2, 'bbb', '男', 1999, '北京'),
	(3, 'ccc', '女', 2000, '上海'),
	(4, 'ddd', '男', 1996, '深圳')
--- create relation graph
insert into FOLLOW (UID, UIDFLED) values
	(2, 3), (4, 3)

------------------- Experiment Code -----------------------

drop procedure if exists GEN_FANS_3
go
create procedure GEN_FANS_3 as begin
-- create FANS_3
drop table if exists FANS_3
create table FANS_3 (
	UID		integer		not null,
	NAME	text		not null,
	SEX		char(2)		not null,
	BYEAR	integer		not null,
	CITY	text		not null,
	foreign key (UID) references USERS,
)
-- insert data to FANS_3
insert into FANS_3 (UID, NAME, SEX, BYEAR, CITY) (
	select USERS.* from USERS, FOLLOW
	where USERS.UID = FOLLOW.UID
		and FOLLOW.UIDFLED = 3
)
end
go

execute GEN_FANS_3
select * from FANS_3

------------------- Experiment Code -----------------------
go

-- tear down all tests
drop table if exists FANS_3
delete from FOLLOW
delete from USERS
