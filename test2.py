import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QFileDialog, QMessageBox
import qrcode
from PIL import Image
from PyQt5.QtGui import QPixmap, QImage
import numpy as np
from PyQt5.QtCore import Qt

class QRCodeApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('QR 코드 생성기')
        self.setFixedSize(350, 480)
        self.setStyleSheet('background-color: #f6f8fa;')
        layout = QVBoxLayout()
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(18)

        self.label = QLabel('QR 코드에 넣을 데이터를 입력하세요:')
        self.label.setStyleSheet('font-size: 15px; color: #222; font-weight: bold;')
        layout.addWidget(self.label)

        self.data_input = QLineEdit()
        self.data_input.setPlaceholderText('예: https://github.com')
        self.data_input.setStyleSheet('padding: 8px; font-size: 14px; border-radius: 6px; border: 1px solid #bbb;')
        layout.addWidget(self.data_input)

        self.gen_btn = QPushButton('QR 코드 생성')
        self.gen_btn.setStyleSheet('background-color: #2ea44f; color: white; font-size: 15px; padding: 10px; border-radius: 6px; font-weight: bold;')
        self.gen_btn.clicked.connect(self.generate_qr)
        layout.addWidget(self.gen_btn)

        self.qr_label = QLabel()
        self.qr_label.setFixedSize(220, 220)
        self.qr_label.setStyleSheet('background: white; border: 1px solid #ddd; border-radius: 10px;')
        self.qr_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.qr_label, alignment=Qt.AlignCenter)

        self.save_btn = QPushButton('QR 코드 저장')
        self.save_btn.setStyleSheet('background-color: #0366d6; color: white; font-size: 15px; padding: 10px; border-radius: 6px; font-weight: bold;')
        self.save_btn.clicked.connect(self.save_qr)
        layout.addWidget(self.save_btn)

        self.setLayout(layout)
        self.qr_img = None

    def generate_qr(self):
        data = self.data_input.text()
        if not data:
            QMessageBox.warning(self, '경고', '데이터를 입력하세요!')
            return
        try:
            img = qrcode.make(data)
            self.qr_img = img
            img_rgb = img.convert('RGB')
            arr = np.array(img_rgb)
            h, w, ch = arr.shape
            bytes_per_line = ch * w
            qimg = QImage(arr.data, w, h, bytes_per_line, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(qimg)
            self.qr_label.setPixmap(pixmap.scaled(200, 200))
        except Exception as e:
            QMessageBox.critical(self, '오류', f'QR 코드 생성 중 오류 발생: {e}')

    def save_qr(self):
        if self.qr_img is None:
            QMessageBox.warning(self, '경고', '먼저 QR 코드를 생성하세요!')
            return
        fname, _ = QFileDialog.getSaveFileName(self, 'QR 코드 저장', 'qr.png', 'PNG Files (*.png)')
        if fname:
            self.qr_img.save(fname)
            QMessageBox.information(self, '저장 완료', f'QR 코드가 {fname} 파일로 저장되었습니다.')

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = QRCodeApp()
    window.show()
    sys.exit(app.exec_())