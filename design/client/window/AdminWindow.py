# -*- coding: utf-8 -*-

from typing import *
from decimal import Decimal
import hashlib

from PyQt5 import QtCore as C
from PyQt5 import QtGui as G
from PyQt5 import QtWidgets as W
import requests

from . import CONFIG, qmessage_critical_with_detail
from ui import Ui_AdminWindow

URL = CONFIG['remote']['url']


class AdminWindow(W.QMainWindow):

    def __init__(self):
        super().__init__()
        self.ui = Ui_AdminWindow()
        self.ui.setupUi(self)

        self.ui.refresh_merch_action.triggered.connect(self.handle_refresh_merch_action)
        self.ui.refresh_employee_action.triggered.connect(self.handle_refresh_employee_action)
        self.ui.refresh_trans_action.triggered.connect(self.handle_refresh_trans_action)
        self.ui.refresh_vip_action.triggered.connect(self.handle_refresh_vip_action)
        self.ui.refresh_all_action.triggered.connect(self.handle_refresh_all_action)

        self.ui.insert_merch_action.triggered.connect(self.handle_insert_merch_action)
        self.ui.insert_employee_action.triggered.connect(self.handle_insert_employee_action)

        self.ui.merch_table.cellDoubleClicked.connect(self.handle_merch_table_cellDoubleClick)
        self.ui.employ_tree.itemClicked.connect(self.handle_employ_tree_itemClicked)
        self.ui.trans_tree.itemClicked.connect(self.handle_trans_tree_itemClicked)
        self.ui.vip_tree.itemClicked.connect(self.handle_vip_tree_itemClicked)

        self.ui.exit_action.triggered.connect(self.handle_exit_action)

        self.user_data = {}

    def showEvent(self, evt):
        self.handle_refresh_all_action()
        return super().showEvent(evt)

    @staticmethod
    def clear_table(table):
        while table.rowCount() != 0:
            table.removeRow(0)

    def handle_refresh_merch_action(self):
        table = self.ui.merch_table
        while table.rowCount() != 0:
            table.removeRow(0)
        try:
            ret = requests.get(
                f'{URL}/api/list/merchandise/0/0',
                auth=self.user_data['auth']
            )
            assert ret.status_code == 200
        except Exception as e:
            warn = qmessage_critical_with_detail('连接错误', '无法从服务端获取数据！', str(e), self)
            return
        ret = ret.json()
        for idx, row in enumerate(ret):
            if 'id' not in row or 'name' not in row or 'price' not in row or 'count' not in row:
                warn = qmessage_critical_with_detail('数据错误', '服务端数据格式升级！', str(e), self)
                return
            table.insertRow(idx)
            table.setItem(idx, 0, W.QTableWidgetItem(f"{row['id']}"))
            table.setItem(idx, 1, W.QTableWidgetItem(row['name']))
            table.setItem(idx, 2, W.QTableWidgetItem(f"{row['price']:.2f}"))
            table.setItem(idx, 3, W.QTableWidgetItem(f"{row['count']}" if row['count'] is not None else '---'))

    def handle_merch_table_cellDoubleClick(self, row, col):
        table = self.ui.merch_table
        if table.item(row, 1).text() == '会员卡':
            warn = W.QMessageBox.information(self, '提示', '会员卡信息不可随意更改！')
            return
        if col == 0:
            warn = W.QMessageBox.information(self, '提示', '商品 ID 不可更改！')
            return
        try:
            merch_id = table.item(row, 0).text()
            if col == 1:        # renaming merchandise
                new_name, ok = W.QInputDialog.getText(self, '更改商品名称', '请输入新的商品名称：')
                if ok:
                    if not new_name:
                        W.QMessageBox.information(self, '提示', '名称不能为空！')
                        return
                    ret = requests.put(
                        f'{URL}/api/query/merchandise/{merch_id}',
                        json={'name': new_name},
                        auth=self.user_data['auth']
                    )
                    assert ret.status_code == 200
            elif col == 2:      # modifying count
                new_price, ok = W.QInputDialog.getDouble(self, '更改商品单价', '请输入新的单价：')
                if ok:
                    if new_price < 0.0:
                        W.QMessageBox.information(self, '提示', '单价不能为负！')
                        return
                    ret = requests.put(
                        f'{URL}/api/query/merchandise/{merch_id}',
                        json={'price': new_price},
                        auth=self.user_data['auth']
                    )
                    assert ret.status_code == 200
            elif col == 3:
                choices = ['增加库存', '减少库存', '设为不限量']
                action, ok = W.QInputDialog.getItem(self, '更改数量', '请输入更改方式：', choices, editable=False)
                if ok:
                    if action == choices[2]:
                        ret = requests.put(
                            f'{URL}/api/query/merchandise/{merch_id}',
                            json={'count': None},
                            auth=self.user_data['auth']
                        )
                        assert ret.status_code == 200
                    else:
                        amount, ok = W.QInputDialog.getInt(self, '更改数量', '请输入数量：')
                        if ok:
                            if amount <= 0:
                                W.QMessageBox.information(self, '提示', '更改数量必须为正数！')
                                return
                            ret = requests.put(
                                f'{URL}/api/query/merchandise/{merch_id}',
                                json={'add' if action == choices[0] else 'minus': amount},
                                auth=self.user_data['auth']
                            )
                            assert ret.status_code == 200
        except Exception as e:
            warn = qmessage_critical_with_detail('连接错误', '无法更新数据！', str(e), self)
            return
        if ok:
            W.QMessageBox.information(self, '提示', '更改已生效！')
            self.handle_refresh_merch_action()
        else:
            W.QMessageBox.information(self, '提示', '更改未生效！')

    def handle_refresh_employee_action(self):
        tree = self.ui.employ_tree
        while tree.topLevelItemCount() != 0:
            tree.takeTopLevelItem(0)
        try:
            ret = requests.get(
                f'{URL}/api/list/employee/0/0',
                auth=self.user_data['auth']
            )
            assert ret.status_code == 200
        except Exception as e:
            qmessage_critical_with_detail('错误', '服务端发生错误！', str(e), self)
            return
        try:
            ret = ret.json()
            tree.insertTopLevelItems(0, [
                W.QTreeWidgetItem([
                    f"{row['employee_id']}", row['name'], '', '', '',
                    row['job'], row['tel']
                ])
                for row in ret
            ])
        except Exception as e:
            W.QMessageBox.warning(self, '警告', '服务端通信协议升级！')
            return

    def handle_employ_tree_itemClicked(self, employee: W.QTreeWidgetItem, col: int):
        if employee.parent() is not None:
            return
        if employee.isExpanded():
            employee.setExpanded(False)
            return
        if employee.childCount() != 0:
            employee.setExpanded(True)
            return
        employee.takeChildren()
        employee_id = employee.text(0)
        try:
            ret = requests.get(
                f'{URL}/api/query/shifts/{employee_id}',
                auth=self.user_data['auth']
            )
            assert ret.status_code == 200
        except Exception as e:
            qmessage_critical_with_detail('错误', '服务端发生错误！', str(e), self)
            return
        try:
            ret = ret.json()
            employee.addChildren([
                W.QTreeWidgetItem([
                    '', '', row['start'], row['end'] if row['end'] is not None else '---',
                    f"{row['sum']:.2f}", '', ''
                ])
                for row in ret
            ])
            employee.setExpanded(True)
        except Exception as e:
            W.QMessageBox.warning(self, '警告', '服务端通信协议升级！')
            return

    def handle_refresh_trans_action(self):
        tree = self.ui.trans_tree
        while tree.topLevelItemCount() != 0:
            tree.takeTopLevelItem(0)
        # get top-level, i.e. transactions
        try:
            ret = requests.get(
                f'{URL}/api/list/trans/0/0',
                auth=self.user_data['auth']
            )
            assert ret.status_code == 200
        except Exception as e:
            qmessage_critical_with_detail('错误', '服务端发生错误！', str(e), self)
            return
        # push to tree widget
        try:
            ret = ret.json()
            tree.insertTopLevelItems(0, [
                W.QTreeWidgetItem([
                    f"{row['trans_id']}", '', '', '', '',
                    row['time'], f"{row['sum']:.2f}",
                    f"{row['cashier_id']}", row['cashier_login']
                ])
                for row in ret
            ])
        except Exception as e:
            W.QMessageBox.warning(self, '警告', '服务端通信协议升级！')
            return

    def handle_trans_tree_itemClicked(self, trans: W.QTreeWidgetItem, col: int):
        if trans.parent() is not None:
            return
        # if expanded, hide
        if trans.isExpanded():
            trans.setExpanded(False)
            return
        # short-cut if already have data
        if trans.childCount() != 0:
            trans.setExpanded(True)
            return
        # clear all children
        trans.takeChildren()
        # get trans ID
        trans_id = trans.text(0)
        # get transdetail
        try:
            ret = requests.get(
                f'{URL}/api/query/trans-detail/{trans_id}',
                auth=self.user_data['auth']
            )
            assert ret.status_code == 200
        except Exception as e:
            qmessage_critical_with_detail('错误', '服务端发生错误！', str(e), self)
            return
        # append detail as sub-items
        try:
            ret = ret.json()
            trans.addChildren([
                W.QTreeWidgetItem([
                    '', f"{row['merch_id']}", row['name'],
                    f"{row['actual_price']:.2f}",
                    f"{row['count']}", '',
                    f"{row['actual_price'] * row['count']:.2f}", '', ''
                ])
                for row in ret
            ])
            trans.setExpanded(True)
        except Exception as e:
            W.QMessageBox.warning(self, '警告', '服务端通信协议升级！')
            return

    def handle_refresh_vip_action(self):
        tree = self.ui.vip_tree
        while tree.topLevelItemCount() != 0:
            tree.takeTopLevelItem(0)
        try:
            ret = requests.get(
                f'{URL}/api/list/vip/0/0',
                auth=self.user_data['auth']
            )
            assert ret.status_code == 200
        except Exception as e:
            qmessage_critical_with_detail('错误', '服务端发生错误！', str(e), self)
            return
        try:
            ret = ret.json()
            tree.insertTopLevelItems(0, [
                W.QTreeWidgetItem([
                    f"{row['id']}", row['register-date'],
                    row['name'] if row['name'] is not None else '---',
                    '', '',
                    row['tel'] if row['tel'] is not None else '---',
                ])
                for row in ret
            ])
        except Exception as e:
            W.QMessageBox.warning(self, '警告', '服务端通信协议升级！')
            return

    def handle_vip_tree_itemClicked(self, vip: W.QTreeWidgetItem, col: int):
        if vip.parent() is not None:
            return
        if vip.isExpanded():
            vip.setExpanded(False)
            return
        if vip.childCount() != 0:
            vip.setExpanded(True)
            return
        vip.takeChildren()
        vip_id = vip.text(0)
        try:
            ret = requests.get(
                f'{URL}/api/query/vip-trans-record/{vip_id}',
                auth=self.user_data['auth']
            )
            assert ret.status_code == 200
        except Exception as e:
            qmessage_critical_with_detail('错误', '服务端发生错误！', str(e), self)
            return
        try:
            ret = ret.json()
            vip.addChildren([
                W.QTreeWidgetItem([
                    '', '', '', row['start-date'], f"{row['acc-consume']}", ''
                ])
                for row in ret
            ])
            vip.setExpanded(True)
        except Exception as e:
            W.QMessageBox.warning(self, '警告', '服务端通信协议升级！')
            return

    def handle_refresh_all_action(self):
        self.ui.refresh_merch_action.trigger()
        self.ui.refresh_employee_action.trigger()
        self.ui.refresh_trans_action.trigger()
        self.ui.refresh_vip_action.trigger()

    def handle_insert_merch_action(self):
        # get name
        name, ok = W.QInputDialog.getText(self, '添加商品', '请输入商品名称：')
        if not ok:
            return
        if not name:
            W.QMessageBox.information(self, '提示', '商品名不能为空！')
            return
        # get price
        price, ok = W.QInputDialog.getDouble(self, '添加商品', '请输入商品单价：', decimals=2)
        if not ok:
            return
        if price < 0.00:
            W.QMessageBox.information(self, '提示', '单价不能为负数！')
        # get count
        count, ok = W.QInputDialog.getInt(self, '添加商品', '请输入商品库存（0 表示不限量）：')
        if not ok:
            return
        if count < 0:
            W.QMessageBox.information(self, '提示', '商品库存不能为负数！')
        count = None if count == 0 else count
        # make request
        try:
            ret = requests.post(
                f'{URL}/api/list/merchandise',
                json={
                    'name': name,
                    'price': round(price, 2),
                    'count': count
                },
                auth=self.user_data['auth']
            )
            assert ret.status_code == 200
        except Exception as e:
            qmessage_critical_with_detail('错误', '服务端发生错误！', str(e), self)
            return
        W.QMessageBox.information(self, '成功', '成功添加商品！')
        self.ui.refresh_merch_action.trigger()

    def handle_insert_employee_action(self):
        # get login
        login, ok = W.QInputDialog.getText(self, '添加店员', '请输入店员姓名：')
        if not ok:
            return
        if not login:
            W.QMessageBox.information(self, '提示', '店员姓名不能为空！')
            return
        # get passwd, raw to md5
        passwd, ok = W.QInputDialog.getText(self, '添加店员', '请输入登陆密码：',
            echo=W.QLineEdit.Password)
        if not ok:
            return
        passwd = hashlib.md5(passwd.encode('utf-8')).hexdigest()
        # get jobs (from remote)
        try:
            ret = requests.get(
                f'{URL}/api/list/jobs',
                auth=self.user_data['auth']
            )
            assert ret.status_code == 200
        except Exception as e:
            qmessage_critical_with_detail('错误', '服务端发生错误！', str(e), self)
            return
        try:
            ret = ret.json()
            job, ok = W.QInputDialog.getItem(self, '添加店员', '请输入店员职务：', [
                f"{row['job_id']}.{row['name']}"
                for row in ret
            ], editable=False)
            job_id = int(job.split('.')[0])
        except Exception as e:
            W.QMessageBox.warning(self, '警告', '服务端通信协议已升级！')
            return
        # get tel
        tel, ok = W.QInputDialog.getText(self, '添加店员', '请输入店员联系方式：')
        if not ok:
            return
        if len(tel) > 11:
            W.QMessageBox.information(self, '提示', '电话号码长度不得超过 11 位！')
            return
        # make request
        try:
            ret = requests.post(
                f'{URL}/api/list/employee',
                json={
                    'login': login,
                    'passwd': passwd,
                    'job': job_id,
                    'tel': tel
                },
                auth=self.user_data['auth']
            )
            assert ret.status_code == 200
        except Exception as e:
            qmessage_critical_with_detail('错误', '服务端发生错误！', str(e), self)
            return
        W.QMessageBox.information(self, '成功', '成功添加店员！')
        self.ui.refresh_employee_action.trigger()

    def handle_exit_action(self):
        self.close()

    def closeEvent(self, evt):
        try:
            ret = requests.delete(
                f"{URL}/api/auth/logout/{self.user_data['login']}",
                auth=self.user_data['auth']
            )
            assert ret.status_code == 200
        except Exception as e:
            ret = qmessage_critical_with_detail('连接错误', '无法从服务端注销！', str(e), self)
        return super().closeEvent(evt)
