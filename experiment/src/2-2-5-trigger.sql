use DBEXP
set nocount on

-- set up test env
--- create user
insert into USERS (UID, NAME) values
	(1, '²©Ö÷'), (2, '¶ÁÕß1')
--- create blogs
insert into MBLOG values
	(1, 'Mein First Blog', 1, 1970, 1, 1, 'Hello, World!')

print 'Running experiment code...'
print ''
--------------------- EXPERIMENT CODE ----------------------------

drop trigger if exists self_thumb_check
go
create trigger self_thumb_check on THUMB instead of insert, update as begin
	declare @uid integer, @bid integer
	select @uid = UID, @bid = BID from inserted
	if @uid = (select UID from MBLOG where BID = @bid) begin
		;throw 51000, 'Cannot thumb youself!', 1
	end else begin
		select @uid = UID, @bid = BID from deleted
		delete from THUMB where UID = @uid and BID = @bid
		select @uid = UID, @bid = BID from inserted
		insert into THUMB values (@uid, @bid)
	end
end
go

-- legal insertion
begin try
	insert into THUMB values (2, 1)
	print 'Legal insertion success!'
end try
begin catch
	print 'Legal insertion failed!'
	print error_message()
end catch

print ''

-- illegal insertion
begin try
	insert into THUMB values (1, 1)
	print 'Illegal insertion success!'
end try
begin catch
	print 'Illegal insertion failed!'
	print error_message()
end catch

print ''

-- illegal udpate
begin try
	update THUMB set UID = 1 where UID = 2 and BID = 1
	print 'Illegal update success!'
end try
begin catch
	print 'Illegal update failed!'
	print error_message()
end catch

--------------------- EXPERIMENT CODE ----------------------------
print ''
print 'Out of experiment code...'

-- tear down test env
delete from THUMB
delete from MBLOG
delete from USERS