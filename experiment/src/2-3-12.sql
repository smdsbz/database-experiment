use DBEXP

-- create test env
--- create users
insert into USERS (UID, NAME) values (1, 'aaa')
--- create blogs
insert into MBLOG values
	(1, '����û�йؼ���', 1, 1970, 1, 1, ''),
	(2, '������վ', 1, 1970, 1, 1, ''),
	(3, '���пƼ���ѧ', 1, 1970, 1, 1, ''),
	(4, '��ӵ������վ�Ļ��пƼ���ѧ', 1, 1970, 1, 1, '')

go
--------------------- Experiment Code ------------------------

select *
from MBLOG
where TITLE like '%������վ%'
	or TITLE like '%���пƼ���ѧ%'

--------------------- Experiment Code ------------------------
go

-- tear down test env
delete from MBLOG
delete from USERS