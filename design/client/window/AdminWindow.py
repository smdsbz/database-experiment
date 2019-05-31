# -*- coding: utf-8 -*-

from typing import *
from decimal import Decimal

from PyQt5 import QtCore as C
from PyQt5 import QtGui as G
from PyQt5 import QtWidgets as W
import requests

from . import CONFIG, qmessage_critical_with_detail
from ui import Ui_AdminWindow

URL = CONFIG['remote']['url']


class MerchTableModel(C.QAbstractTableModel):
    pass


class AdminWindow(W.QMainWindow):

    def __init__(self):
        super().__init__()
        self.ui = Ui_AdminWindow()
        self.ui.setupUi(self)

        self.ui.refresh_merch_action.triggered.connect(self.handle_refresh_merch_action)
        self.ui.refresh_employee_action.triggered.connect(self.handle_refresh_employee_action)
        self.ui.refresh_trans_action.triggered.connect(self.handle_refresh_trans_action)
        self.ui.refresh_all_action.triggered.connect(self.handle_refresh_all_action)
        self.ui.merch_table.cellDoubleClicked.connect(self.handle_merch_table_cellDoubleClick)
        self.ui.trans_tree.clicked.connect(self.handle_trans_tree_clicked)
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
                new_name, not_empty = W.QInputDialog.getText(self, '更改商品名称', '请输入新的商品名称：')
                if not_empty:
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
                new_price, not_empty = W.QInputDialog.getDouble(self, '更改商品单价', '请输入新的单价：')
                if not_empty:
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
                action, not_empty = W.QInputDialog.getItem(self, '更改数量', '请输入更改方式：', choices, editable=False)
                if not_empty:
                    if action == choices[2]:
                        ret = requests.put(
                            f'{URL}/api/query/merchandise/{merch_id}',
                            json={'count': None},
                            auth=self.user_data['auth']
                        )
                        assert ret.status_code == 200
                    else:
                        amount, not_empty = W.QInputDialog.getInt(self, '更改数量', '请输入数量：')
                        if not_empty:
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
        if not_empty:
            W.QMessageBox.information(self, '提示', '更改已生效！')
            self.handle_refresh_merch_action()
        else:
            W.QMessageBox.information(self, '提示', '更改未生效！')

    def handle_refresh_employee_action(self):
        pass

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
                    row['time'], f"{Decimal(row['sum']).quantize(Decimal('1.00'))}",
                    f"{row['cashier_id']}", row['cashier_login']
                ])
                for row in ret
            ])
        except Exception as e:
            W.QMessageBox.warning(self, '警告', '服务端通信协议升级！')
            return

    def handle_trans_tree_clicked(self, index: C.QModelIndex):
        # set sub-items, i.e. transdetails, on expanding top-level
        trans_toplevel = self.ui.trans_tree.topLevelItem(index.row())
        # if expanded, hide
        if trans_toplevel.isExpanded():
            trans_toplevel.setExpanded(False)
            return
        # short-cut if already have data
        if trans_toplevel.childCount() != 0:
            trans_toplevel.setExpanded(True)
            return
        trans_toplevel.takeChildren()
        # get trans ID
        trans_id = trans_toplevel.text(0)
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
            trans_toplevel.addChildren([
                W.QTreeWidgetItem([
                    '', f"{row['merch_id']}", row['name'],
                    f"{Decimal.from_float(row['actual_price']).quantize(Decimal('1.00'))}",
                    f"{row['count']}", '',
                    f"{(Decimal.from_float(row['actual_price']).quantize(Decimal('1.00')) * Decimal(row['count'])).quantize(Decimal('1.00'))}", '', ''
                ])
                for row in ret
            ])
            trans_toplevel.setExpanded(True)
        except Exception as e:
            W.QMessageBox.warning(self, '警告', '服务端通信协议升级！')
            return


    def handle_refresh_all_action(self):
        self.handle_refresh_merch_action()
        self.handle_refresh_employee_action()
        self.handle_refresh_trans_action()

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
