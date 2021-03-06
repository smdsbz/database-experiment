# 数据库系统原理实践

## 超市收银系统

### 任务书

假设一家小型超市的收银台（前台）要完成下列日常工作：

- 收银：收银员输入顾客的会员卡卡号（若有卡）、所购商品的货号等信息，系统根据这些信息获取相应的价格信息并计算应收取的总金额。完成收银后，记录交易信息，修改有关种类商品的剩余量以及该持卡顾客的消费情况。
- 发卡：顾客可交纳一定的费用（如 50 元）办理一张会员卡，以后在该商场购物可凭卡享受 9 折优惠。如果一个未持卡顾客一次购物满 1000 元，可为其免费发放一张会员卡，每张卡的优惠期为一年，一年内消费达到一定金额的可继续享受下一年的优惠。
- 款项盘存：收银员下班或交接班前对本收银台中本班次收取的款额进行盘存，明确责任。

此外，还应提供下列后台功能：

- 商品信息的录入、修改、删除和查询等。
- 收银员身份及口令管理。

设计一个 C/S 模式的系统实现上述功能。

### 使用方法

#### 运行方法

0. 进入源码目录 `src/`。
1. 手动在 MySQL 中创建数据库，并更新 `config/db.toml` 中数据库名称及其他各项设置。
2. （在服务端源码根目录 `server/` 下）运行脚本 `scripts/drop-and-create-tables.py`，创建数据表结构并注入 `config/*.toml` 中描述的数据。
3. `python app.py` 启动服务端。
4. `python app.py` 启动客户端。

#### 测试

所有单元测试都位于 `server/test/` 中，使用命令

```console
$ python -m unittest test.[PKG] -v
```

运行包 `PKG` 的单元测试。

> NOTE
>
> - 单元测试可能会改动数据库，请在单元测试后运行 `scripts/drop-and-create-tables.py` 脚本重建数据表。
> - API 单元测试 `test.api` 仅为 `curl` 工具的替代方案，所有测试 endpoint 均不做任何断言，需要使用者根据自己测试时数据库中数据状态，自行判断测试结果的正确性。
> - 由于加入了身份验证，所有 API 单元测试现均不可使用。若需要测试，可以修改 `api/Auth.py` 中 `auth.verify_password` 的实现。

#### 环境依赖

- Python 3
- MySQL

__Python 包__

Server-side:

- toml
- [mysqlclient](https://github.com/PyMySQL/mysqlclient-python) 1.4.2
- flask
    - itsdangerous (default package in flask)
    - Flask-HTTPAuth
    - flask-restul
- [requests](https://2.python-requests.org/en/master/) (only used in tests)

Client-side:

- toml
- PyQt5
- requests
