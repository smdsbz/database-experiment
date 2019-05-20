use DBEXP

-- create test env
--- create user
insert into USERS (UID, NAME) values (1, 'aaa')
--- create blogs
insert into MBLOG values
	(1, 'AAA', 1, 1970, 1, 1, ''),
	(2, 'BBB', 1, 1970, 1, 1, ''),
	(3, 'CCC', 1, 1970, 1, 1, '')
--- create labels
insert into LABEL values
	(1, 'L1'), (2, 'L2')
--- create B_Ls
insert into B_L values
	-- 'AAA' labeled 'L1', 'L2'
	(1, 1), (1, 2),
	-- 'BBB' labeled 'L2'
	(2, 2)
	-- 'CCC' has no label
--- create topdays
insert into TOPDAY values
	(2019, 4, 20, 1, 1),
	(2019, 4, 20, 2, 2),
	(2019, 4, 20, 3, 3)

go
------------------- Experiment Code -------------------

select MBLOG.BID, MBLOG.TITLE, T_L.LID, LABEL.LNAME
from MBLOG, (
		select TOPDAY.*, B_L.LID
		from TOPDAY left outer join B_L
				on TOPDAY.BID = B_L.BID
	) as T_L left outer join LABEL on T_L.LID = LABEL.LID
where T_L.TYEAR = 2019 and T_L.TMONTH = 4 and T_L.TDAY = 20
	and T_L.BID = MBLOG.BID

------------------- Experiment Code -------------------
go

-- tear down test env
delete from TOPDAY
delete from B_L
delete from LABEL
delete from MBLOG
delete from USERS