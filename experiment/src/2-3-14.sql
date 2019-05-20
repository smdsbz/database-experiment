use DBEXP

-- create test env
--- create users
insert into USERS (UID, NAME) values
	(1, 'aaa'), (2, 'bbb'), (3, 'ccc'), (5, 'eee')
--- create follows
insert into FOLLOW values
	-- 5 ==> 1, 2
	(5, 1), (5, 2),
	-- 1 ==> 2 (, 1 self)
	(1, 2),
	-- 2 ==> 3
	(2, 3),
	-- 3 ==> 1, 2, 5
	(3, 1), (3, 2), (3, 5)

go
---------------- Experiment Code -----------------

declare @target_user integer = 5

select USERS.UID
from USERS
where not exists (
			select F2.UIDFLED	-- users followed by @target_user
			from (select UIDFLED from FOLLOW where UID = @target_user) as F2
			where F2.UIDFLED not in (
						select F1.UIDFLED
						from FOLLOW as F1
						where F1.UID = USERS.UID
					)
				and F2.UIDFLED != USERS.UID
		)
	and USERS.UID != @target_user

-- expecting: #1, #3

---------------- Experiment Code -----------------
go

-- tear down test env
delete from FOLLOW
delete from USERS