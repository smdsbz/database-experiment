# -*- coding: utf-8 -*-

from typing import *
from decimal import Decimal

from PyQt5 import QtCore as C
from PyQt5 import QtGui as G
from PyQt5 import QtWidgets as W
import requests

from . import CONFIG, qmessage_critical_with_detail
from ui import Ui_SellerWindow

URL = CONFIG['remote']['url']


class SellerWindow(W.QMainWindow):

    def __init__(self):
        super().__init__()
        self.ui = Ui_SellerWindow()
        self.ui.setupUi(self)
        self.ui.exit_action.triggered.connect(self.close)
        self.ui.add_item_button.clicked.connect(self.handle_add_item_button_clicked)
        self.ui.remove_selected_button.clicked.connect(self.handle_remove_selected_button_clicked)
        self.ui.clear_button.clicked.connect(self.handle_clear_button_clicked)
        self.ui.is_vip_checkbox.clicked.connect(self.handle_is_vip_checkbox_checked)
        self.ui.submit_button.clicked.connect(self.handle_submit_button_clicked)

        self.user_data = {}

    def handle_add_item_button_clicked(self):
        # get the only matching merchandise
        merch_name, not_empty = W.QInputDialog.getText(self, '添加商品', '请输入商品名称：')
        if not not_empty:
            return
        try:
            ret = requests.get(
                f'{URL}/api/byname/merchandise/{merch_name}',
                auth=self.user_data['auth']
            )
            assert ret.status_code == 200
        except Exception as e:
            qmessage_critical_with_detail('错误', '服务端发生错误！', str(e), self)
            return
        ret = ret.json()
        if not ret:
            W.QMessageBox.information(self, '提示', '无法找到该商品！')
            return
        elif len(ret) == 1:
            ret = ret[0]
        elif len(ret) > 1:
            merch_name, not_empty = W.QInputDialog.getItem(
                self, '选择商品', '在数据库中查找到以下匹配的商品：',
                [f"{row['merch_id']}.{row['name']}" for row in ret])
            if not not_empty:
                return
            merch_id = int(merch_name.split('.')[0])
            for row in ret:
                if row['merch_id'] == merch_id:
                    ret = row
                    break
        merch_id = ret['merch_id']
        merch_name = ret['name']
        orig_price = Decimal.from_float(ret['orig_price']).quantize(Decimal('1.00'))
        # get count of item to purchase
        count, not_empty = W.QInputDialog.getInt(self, '选择数量', '请输入购买数量：')
        if not not_empty or count <= 0:
            return
        table = self.ui.trans_table
        row = table.rowCount()
        # merge if already in table
        for rowidx in range(row):
            if int(table.item(rowidx, 0).text()) == merch_id:
                table.setItem(rowidx, 4, W.QTableWidgetItem(
                        f'{int(table.item(rowidx, 4).text()) + count}'))
                self.update_calculated_price()
                return
        # else add to bottom of table
        table.insertRow(row)
        table.setItem(row, 0, W.QTableWidgetItem(f'{merch_id}'))
        table.setItem(row, 1, W.QTableWidgetItem(merch_name))
        table.setItem(row, 2, W.QTableWidgetItem(f'{orig_price}'))
        table.setItem(row, 4, W.QTableWidgetItem(f'{count}'))
        self.update_calculated_price()

    def handle_remove_selected_button_clicked(self):
        # get selected row
        model = self.ui.trans_table.selectionModel()
        if not model.hasSelection():
            W.QMessageBox.information(self, '提示', '请选择要删除的商品！')
            return
        row = model.selectedRows()[0].row()
        self.ui.trans_table.removeRow(row)
        self.update_calculated_price()

    def handle_clear_button_clicked(self):
        while self.ui.trans_table.rowCount() != 0:
            self.ui.trans_table.removeRow(0)
        self.update_calculated_price()

    def update_calculated_price(self):
        # iterate over table and get sum
        table = self.ui.trans_table
        rows = table.rowCount()
        is_vip = self.ui.is_vip_checkbox.isChecked()
        discount = CONFIG['transaction']['vip-discount'] if is_vip else 1.0
        discount = Decimal.from_float(discount)
        sum = Decimal('0.00')
        for row in range(rows):
            orig_price = Decimal(table.item(row, 2).text())
            count = Decimal(table.item(row, 4).text())
            actual_price = (orig_price * discount).quantize(Decimal('1.00'))
            table.setItem(row, 3, W.QTableWidgetItem(f'{actual_price:.2f}'))
            sum += (actual_price * count).quantize(Decimal('1.00'))
        self.ui.sum_display_label.setText(f'总金额：￥{sum}')

    def handle_is_vip_checkbox_checked(self):
        # TODO: pop to ask for VIP card ID
        # self.ui.is_vip_checkbox.setChecked(False)
        self.update_calculated_price()

    def handle_submit_button_clicked(self):
        # get transaction list
        table = self.ui.trans_table
        trans_list = [
            (
                int(table.item(row, 0).text()),
                float(table.item(row, 3).text()),
                int(table.item(row, 4).text())
            )
            for row in range(table.rowCount())
        ]
        if not trans_list:
            W.QMessageBox.information(self, '提示', '订单为空，请添加商品！')
            return
        try:
            ret = requests.post(
                f'{URL}/api/trans',
                json={
                    'cashier': self.user_data['employee_id'],
                    'trans': trans_list
                },
                auth=self.user_data['auth']
            )
            assert ret.status_code == 200
        except Exception as e:
            if ret.status_code == 406:
                ret = ret.json()
                if 'reason' not in ret:
                    W.QMessageBox.warning(self, '警告', '服务端通信协议已升级！')
                    return
                if 'merch_id' in ret:
                    if ret['reason'] == 'Illegal ID':
                        W.QMessageBox.warning(self, '错误', f"商品 ID {ret['merch_id']} 非法！")
                        return
                    elif ret['reason'] == 'Not enough in storage':
                        W.QMessageBox.information(self, '错误', f"商品 ID {ret['merch_id']} 库存不足！")
                        return
                    W.QMessageBox.warning(self, '错误', '服务端无法正确处理该请求！')
                    return
                qmessage_critical_with_detail('错误', '服务端出现了错误！', ret['reason'], self)
                return
            qmessage_critical_with_detail(self, '错误', '无法完成请求！', str(e))
            return
        W.QMessageBox.information(self, '成功', '订单提交成功！')
        self.handle_clear_button_clicked()

    def closeEvent(self, evt):
        # unregister from session
        try:
            ret = requests.delete(
                f"{URL}/api/auth/logout/{self.user_data['login']}",
                auth=self.user_data['auth']
            )
            assert ret.status_code == 200
        except Exception as e:
            ret = qmessage_critical_with_detail('连接错误', '无法从服务端注销！', str(e), self)
        return super().closeEvent(evt)

