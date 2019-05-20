# -*- coding: utf-8 -*-

'''
Drops all data table definitions and recreate new ones.

NOTE You will lost all your data!
'''

import toml
import MySQLdb

dbconfig = toml.load('../config/db.toml')

conn = MySQLdb.connect(
    host=dbconfig['connection']['host'],
    user=dbconfig['connection']['user'],
    passwd=dbconfig['connection']['passwd'],
    db=dbconfig['connection']['db'],
    charset='utf8'
)


with conn.cursor() as cur:

    cur.execute('drop table if exists Shifts')
    cur.execute('drop table if exists VIPTransRecord')
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
            count       integer                         comment '库存数量（0 为不限量）',
            primary key (id),
            check (price >= 0.00),
            index (name)
        )
    ''')
    # 会员卡为常驻商品
    cur.execute('''
        insert into Merchandise (name, price) values (%s, %s)
    ''', ('会员卡', 50.0))

    # 店员职务信息表
    cur.execute('''
        create table if not exists Jobs (
            id          integer         auto_increment  comment '职务编号',
            name        varchar(64)     not null        comment '职务名称',
            ac_merch    boolean         default false   comment '商品信息表操作权限',
            primary key (id),
            index (name)
        )
    ''')

    # 店员信息表
    cur.execute('''
        create table if not exists Employee (
            id          integer         auto_increment  comment '店员编号',
            login       varchar(64)     not null        comment '登录名',
            passwd      char(128)       not null        comment '登陆密码（MD5）',
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
