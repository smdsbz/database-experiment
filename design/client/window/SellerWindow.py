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

        self.ui.add_item_button.clicked.connect(self.handle_add_item_button_clicked)
        self.ui.remove_selected_button.clicked.connect(self.handle_remove_selected_button_clicked)
        self.ui.clear_button.clicked.connect(self.handle_clear_button_clicked)
        self.ui.is_vip_checkbox.clicked.connect(self.handle_is_vip_checkbox_clicked)
        self.ui.submit_button.clicked.connect(self.handle_submit_button_clicked)

        self.ui.vipreg_cardid_input.clear()
        self.ui.vipreg_submit_button.clicked.connect(self.handle_vipreg_submit_button_clicked)
        self.ui.vipreg_clear_button.clicked.connect(self.handle_vipreg_clear_button_clicked)

        self.ui.exit_action.triggered.connect(self.close)

        self.user_data = {}
        self.user_data['vip_id'] = None     # used if using VIP card

    def handle_add_item_button_clicked(self):
        # get the only matching merchandise
        merch_name, ok = W.QInputDialog.getText(self, '添加商品', '请输入商品名称：')
        if not ok:
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
        try:
            ret = ret.json()
            if not ret:
                W.QMessageBox.information(self, '提示', '无法找到匹配的商品！')
                return
            elif len(ret) > 1:
                merch_name, ok = W.QInputDialog.getItem(
                    self, '选择商品', '在数据库中查找到以下匹配的商品：',
                    [f"{row['merch_id']}.{row['name']}" for row in ret])
                if not ok:
                    return
                merch_id = int(merch_name.split('.')[0])
                for row in ret:
                    if row['merch_id'] == merch_id:
                        ret = row
                        break
            elif len(ret) == 1:
                ret = ret[0]
            merch_id = ret['merch_id']      # type: int
            merch_name = ret['name']        # type: str
            orig_price = ret['orig_price']  # type: float
            # get count of item to purchase
            count, ok = W.QInputDialog.getInt(self, '选择数量', '请输入购买数量：')
            if not ok or count <= 0:
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
        except Exception as e:
            W.QMessageBox.warning(self, '警告', '服务端通信协议已升级！')
            return

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

    def update_calculated_price(self) -> float:
        # iterate over table and get sum
        table = self.ui.trans_table
        rows = table.rowCount()
        is_vip = self.ui.is_vip_checkbox.isChecked()
        discount = CONFIG['transaction']['vip-discount'] if is_vip else 1.0     # type: float
        sum = 0.0
        for row in range(rows):
            orig_price = float(table.item(row, 2).text())
            count = int(table.item(row, 4).text())
            actual_price = round(orig_price * discount, 2)
            table.setItem(row, 3, W.QTableWidgetItem(f'{actual_price:.2f}'))
            sum += round(actual_price * count, 2)
        sum = round(sum, 2)
        self.ui.sum_display_label.setText(f'总金额：￥{sum:.2f}')
        return sum

    def handle_is_vip_checkbox_clicked(self):
        # NOTE: the clicked signal is emitted AFTER checkbox being checked / unchecked!
        # if unchecked
        if not self.ui.is_vip_checkbox.isChecked():
            self.user_data['vip_id'] = None
            self.update_calculated_price()
            return
        # get vip card ID from user
        vip_id, ok = W.QInputDialog.getInt(self, '使用会员卡', '请输入会员卡卡号：')
        if not ok:
            self.ui.is_vip_checkbox.setChecked(False)
            return
        try:
            ret = requests.get(
                f'{URL}/api/list/vip/{vip_id}/1',
                auth=self.user_data['auth']
            )
            assert ret.status_code == 200
        except Exception as e:
            qmessage_critical_with_detail('错误', '服务端发生错误！', str(e), self)
            self.ui.is_vip_checkbox.setChecked(False)
            return
        try:
            ret = [row['id'] for row in ret.json()]
            if vip_id in ret:
                self.user_data['vip_id'] = vip_id
                self.ui.is_vip_checkbox.setChecked(True)
            else:
                W.QMessageBox.information(self, '提示', '无效的会员卡卡号！')
                self.user_data['vip_id'] = None
                self.ui.is_vip_checkbox.setChecked(False)
        except Exception as e:
            W.QMessageBox.warning(self, '警告', '服务端通信协议升级！')
            self.ui.is_vip_checkbox.setChecked(False)
            return
        self.update_calculated_price()

    def handle_submit_button_clicked(self):
        # prompt for VIP Card give-away
        if not self.ui.is_vip_checkbox.isChecked():
            trans_sum = self.update_calculated_price()  # NOTE: may not be precise
            if trans_sum >= CONFIG['transaction']['vip-give-away-valve']:
                choice = W.QMessageBox.information(self, '提示',
                    f"预计消费满 ￥{CONFIG['transaction']['vip-give-away-valve']}，"
                    '是否免费注册会员？',
                    W.QMessageBox.Ok | W.QMessageBox.Cancel,
                    W.QMessageBox.Ok)
                if choice == W.QMessageBox.Ok:
                    return
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
                    'vip_id': self.user_data['vip_id'],
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
                    if ret['reason'] == 'Not enough in storage':
                        W.QMessageBox.information(self, '错误', f"商品 ID {ret['merch_id']} 库存不足！")
                        return
                    W.QMessageBox.warning(self, '错误', '服务端无法正确处理该请求！')
                    return
                if 'vip_id' in ret:
                    if ret['reason'] == 'Invalid VIP ID':
                        W.QMessageBox.information(self, '提示', '无效的 VIP 卡号！')
                        return
                    if ret['reason'] == 'VIP card timeout':
                        W.QMessageBox.information(self, '提示', 'VIP 卡过期！')
                        return
                qmessage_critical_with_detail('错误', '服务端出现了错误！', ret['reason'], self)
                return
            qmessage_critical_with_detail('错误', '无法完成请求！', str(e), self)
            return
        W.QMessageBox.information(self, '成功', '订单提交成功！')
        self.ui.is_vip_checkbox.setChecked(False)
        self.user_data['vip_id'] = None
        self.ui.clear_button.click()

    def handle_vipreg_submit_button_clicked(self):
        vip_id = self.ui.vipreg_cardid_input.text()
        name = self.ui.vipreg_name_input.text()
        tel = self.ui.vipreg_tel_input.text()
        try:
            ret = requests.put(
                f'{URL}/api/list/vip',
                json={
                    'vip_id': vip_id if vip_id else None,
                    'name': name if name else None,
                    'tel': tel if tel else None
                },
                auth=self.user_data['auth']
            )
            if ret.status_code == 406:
                ret = ret.json()
                if 'reason' not in ret:
                    W.QMessageBox.warning(self, '警告', '服务端通信协议已升级！')
                    return
                if ret['reason'] == 'No need for renew':
                    W.QMessageBox.information(self, '提示', '该卡不需要续期！')
                    return
            assert ret.status_code == 200
        except Exception as e:
            qmessage_critical_with_detail('错误', '服务端出现了错误！', str(e), self)
            return
        try:
            ret = ret.json()
            W.QMessageBox.information(self, '成功', f"您的 VIP 卡号为 {ret['vip_id']}！")
        except Exception as e:
            W.QMessageBox.warning(self, '警告', '服务端通信协议已升级！')
            return
        self.ui.vipreg_clear_button.click()

    def handle_vipreg_clear_button_clicked(self):
        self.ui.vipreg_cardid_input.clear()
        self.ui.vipreg_name_input.clear()
        self.ui.vipreg_tel_input.clear()

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
