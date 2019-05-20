use DBEXP

-- create dependency
--- create user
insert into USERS (UID, NAME, SEX, BYEAR, CITY) values (
	1, 'aaa', 'ÄÐ', 1998, 'Îäºº'
)

-------- Experiment Code ---------------

-- Task 1: insert
insert into MBLOG (BID, TITLE, UID, PYEAR, PMONTH, PDAY, CONT) values (
	1, 'AAA', 1, 2002, 6, 6, 'aaaaaaaaaaaaaa'
)
select * from MBLOG

-- Task 2: update
update MBLOG set CONT = 'bbbbbb'
	where BID = 1
select * from MBLOG

-- Task 3: delete
delete from MBLOG where BID = 1
select * from MBLOG

-------- Experiment Code ---------------

-- tear down all tests
delete from MBLOG
delete from USERS
