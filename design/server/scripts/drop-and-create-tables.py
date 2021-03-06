# -*- coding: utf-8 -*-

'''
Drops all data table definitions and recreate new ones.

NOTE You will lost all your data!
'''

import sys
import toml
import MySQLdb

if len(sys.argv) == 1:
    dbconfig = toml.load('config/db.toml')
elif len(sys.argv) == 2:
    dbconfig = toml.load(sys.argv[1])
else:
    print('Usage: python scripts/drop-and-create-tables.py [DBCONFIG]')
    exit(0)

conn = MySQLdb.connect(**dbconfig['connection'])


# Create data tables
with conn.cursor() as cur:

    cur.execute('drop table if exists Shifts')
    cur.execute('drop table if exists VIPTransRecord')
    cur.execute('drop table if exists VIP')
    cur.execute('drop table if exists TransDetail')
    cur.execute('drop table if exists Transaction')
    cur.execute('drop table if exists Employee')
    cur.execute('drop table if exists Jobs')
    cur.execute('drop table if exists Merchandise')

    # 商品信息表
    cur.execute('''
        create table if not exists Merchandise (
            id          integer         auto_increment  comment '商品编号',
            name        varchar(64)     not null        comment '商品名称',
            price       decimal(6,2)    not null        comment '商品单价',
            count       integer                         comment '库存数量（NULL 为不限量）',
            primary key (id),
            check (price >= 0.00),
            index (name)
        )
    ''')

    # 店员职务信息表
    cur.execute('''
        create table if not exists Jobs (
            id          integer         auto_increment              comment '职务编号',
            name        varchar(64)     not null                    comment '职务名称',
            ac_merch    boolean         not null    default false   comment '商品信息表操作权限',
            primary key (id),
            index (name)
        )
    ''')

    # 店员信息表
    cur.execute('''
        create table if not exists Employee (
            id          integer         auto_increment  comment '店员编号',
            login       varchar(64)     not null        comment '登录名',
            passwd      char(32)        not null        comment '登陆密码（16进制 MD5）',
            job         integer                         comment '职务编号',
            tel         char(11)        not null        comment '联系电话',
            primary key (id),
            foreign key (job) references jobs(id),
            index (login)
        )
    ''')

    # 注册会员信息表
    cur.execute('''
        create table if not exists VIP (
            id          integer         auto_increment  comment '会员编号',
            date        date            not null        comment '注册日期',
            name        varchar(64)                     comment '会员姓名',
            tel         char(11)                        comment '联系电话',
            primary key (id)
        )
    ''')

    # 交易信息表
    cur.execute('''
        create table if not exists Transaction (
            id          integer         auto_increment  comment '交易编号',
            time        datetime        not null        comment '交易时间',
            cashier     integer         not null        comment '店员编号',
            primary key (id),
            foreign key (cashier) references Employee(id)
        )
    ''')

    # 交易明细表
    cur.execute('''
        create table if not exists TransDetail (
            trans_id    integer         not null        comment '所属交易编号',
            merch_id    integer         not null        comment '商品编号',
            price       decimal(6,2)    not null        comment '实际交易单价',
            count       integer         not null        comment '交易数量',
            primary key (trans_id, merch_id),
            check (price >= 0.00),
            check (count > 0)
        )
    ''')

    # 会员累计交易信息统计表
    cur.execute('''
        create table if not exists VIPTransRecord (
            vip_id      integer         not null                    comment '会员编号',
            start_date  date            not null                    comment '起始统计日期',
            acc_consume decimal(10,2)   not null    default 0.00    comment '累计消费（1 年内）',
            primary key (vip_id, start_date),
            foreign key (vip_id) references VIP(id),
            check (acc_consume >= 0.00)
        )
    ''')

    # 班次信息表
    cur.execute('''
        create table if not exists Shifts (
            start_time  datetime        not null                    comment '起始时间',
            end_time    datetime                                    comment '结束时间',
            employee_id integer         not null                    comment '店员编号',
            sum_consume decimal(10,2)   not null    default 0.00    comment '累计收银',
            primary key (employee_id, start_time),
            foreign key (employee_id) references Employee(id),
            check (sum_consume >= 0.00)
        )
    ''')

    conn.commit()


# Insert initial data
with conn.cursor() as cur:

    initial_data = dbconfig['initial-data']

    for table, datas in initial_data.items():
        for data in datas:
            cols = data.keys()
            cur.execute(f'''
                insert into `{table}`
                ({','.join(f'`{col}`' for col in cols)}) values
                ({','.join('%s' for _ in cols)})
            ''', tuple(data[col] for col in cols))

    conn.commit()
