## 数据库系统原理实践记录

### 软件功能学习部分

#### 创建数据库

1. Databases (right click) -> New Databases... -> Database name (fill) -> OK

<img src="img/New Database.png" style="zoom:70%" />

#### 1. 两种完全备份

##### 脱机备份

1. _Take offline..._
2. _Detach..._

> 注意文件权限！应设置为允许继承权限！ [ref](https://stackoverflow.com/questions/18286765/sql-server-operating-system-error-5-5access-is-denied/18286808)

##### 系统备份功能

1. Object Explorer / Databases / 需要备份的数据库 (right) -> Tasks / Back up...
2. Backup type: Full
3. OK

<img src="img/Back Up Database.png" style="zoom:70%" />

##### Ref

- [Create a Full Database Backup (SQL Server)](https://docs.microsoft.com/en-us/sql/relational-databases/backup-restore/create-a-full-database-backup-sql-server?view=sql-server-2017)

--------------------------------------

#### 创建对 `test` 数据库只读的用户

1. Right click on _Object Explorer / Security / Logins_
2. Click _New Login..._
3. Fill _General / Login name_ and _Password_

    <img src="img/New Login - General.png" style="zoom:70%" />

4. Choose `test` in _User Mapping_, check `db_datareader`

    <img src="img/New Login - User Mapping.png" style="zoom:70%" />

5. Choose a valid _Securables_

    <img src="img/New Login - Securables.png" style="zoom:70%" />

6. OK

> 删除用户前，需要确保没有已该用户登陆的会话：
> 
> ```sql
> SELECT login_name, session_id FROM sys.dm_exec_sessions
> ```
> 
> 用 `KILL {session_id}` 强制关闭该会话。

> 删除用户后，要记得删除对应数据库中同名的用户！
> 
> ```sql
> use {database}
> drop user {login_name}
> ```

#### 尝试用新创建的用户操作 `test.table`

1. `select` 正常

    <img src="img/rdonly select.png" style="zoom:80%" />

2. `update` 出错

    <img src="img/rdonly update.png" style="zoom:80%" />


