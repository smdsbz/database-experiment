use DBEXP

----------------- Experiment Code --------------------

set transaction isolation level read committed

begin transaction
select count(*) from USERS
insert into USERS (UID, NAME) values (1, 'aaa')
select count(*) from USERS
commit transaction

select count(*) from USERS

----------------- Experiment Code --------------------
go

delete from USERS