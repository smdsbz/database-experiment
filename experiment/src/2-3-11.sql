use DBEXP

-- create test env
--- create users
insert into USERS (UID, NAME) values
	(1, 'aaa'), (2, 'bbb')
--- create labels
insert into LABEL values
	(1, '文学'), (2, '科技')
--- create subs
insert into SUB values
	(1, 1), (2, 2)

go
--------------------- Experiment Code -----------------------

select SUB.UID
from SUB, LABEL
where SUB.LID = LABEL.LID
	and LABEL.LNAME in ('文学', '艺术', '哲学', '音乐')

-- expecting: #1 'aaa'

--------------------- Experiment Code -----------------------
go

-- tear down test env
delete from SUB
delete from LABEL
delete from USERS