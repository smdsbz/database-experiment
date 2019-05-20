use DBEXP

-- create test env
--- create users
insert into USERS (UID, NAME) values
	(1, 'aaa'),	-- only sub 'L1'
	(2, 'bbb'),	-- only sub 'L2'
	(3, 'ccc')	-- subs 'L1' and 'L2'
--- create labels
insert into LABEL values
	(1, 'L1'), (2, 'L2')
--- create subs
insert into SUB values
	(1, 1), (2, 2), (3, 1), (3, 2)

go
-------------------- Experiment Code -------------------

--    \any LABEL.LID \in (SUB_{SUB.UID = USERS.UID}.LID)
-- => \not \exists LABEL.LID \notin (SUB_{SUB.UID = USERS.UID}.LID)

select USERS.UID, USERS.NAME
from USERS
where USERS.UID not in (
			select SUB.UID
			from SUB, LABEL
			where LABEL.LID not in (
						select SUB.LID
						from SUB
						where SUB.UID = USERS.UID
					)
		)

-- expecting: #3 'ccc'

-------------------- Experiment Code -------------------
go

-- tear down test env
delete from SUB
delete from LABEL
delete from USERS