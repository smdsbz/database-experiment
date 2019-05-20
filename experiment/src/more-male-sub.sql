use DBEXP

-- init test set --

delete from SUB
delete from LABEL
delete from USERS

insert into USERS (UID, NAME, SEX) values (1, 'aaa', '��')
insert into USERS (UID, NAME, SEX) values (2, 'bbb', 'Ů')
insert into USERS (UID, NAME, SEX) values (3, 'ccc', '��')
select * from USERS

insert into LABEL values (1, '1')
insert into LABEL values (2, '2')
select * from LABEL

-- TODO: tune this
insert into SUB values (1, 1)	-- m
insert into SUB values (2, 1)	-- f
insert into SUB values (3, 1)	-- m
select USERS.NAME, LABEL.LNAME from SUB, USERS, LABEL
	where SUB.UID = USERS.UID and SUB.LID = LABEL.LID

-- 
select LABEL.LNAME from LABEL
	where (select COUNT(*) from SUB, USERS
				where SUB.LID = LABEL.LID
					and SUB.UID = USERS.UID
					and USERS.SEX='��') >
			(select COUNT(*) from SUB, USERS
				where SUB.LID = LABEL.LID
					and SUB.UID = USERS.UID
					and USERS.sex='Ů')