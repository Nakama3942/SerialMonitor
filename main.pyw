"""
WTFPL license
Copyright © 2023 Kalynovsky Valentin
\n
A simple dialog window where you can select a COM connection and listen to it.
"""

import sys

from PyQt6.QtWidgets import QApplication, QDialog, QVBoxLayout, QHBoxLayout, QSizePolicy, QLabel, QComboBox, QPushButton, QTextEdit
from PyQt6.QtSerialPort import QSerialPort, QSerialPortInfo
from PyQt6.QtCore import QIODevice

class SerialDialog(QDialog):
	"""
	A class that describes the dialog box for reading a COM port.
	"""

	def __init__(self):
		super(SerialDialog, self).__init__()

		# Adding layouts
		self.main_layout = QVBoxLayout()
		self.combo_layout = QHBoxLayout()
		self.rate_layout = QHBoxLayout()

		# Adding a COM Ports ComboBox
		self.combo_label = QLabel("Select COM Port:", self)
		self.combo_label.setMinimumSize(120, 0)
		self.combo_label.setSizePolicy(QSizePolicy.Policy.Minimum, self.combo_label.sizePolicy().verticalPolicy())
		self.port_combo = QComboBox(self)
		self.port_combo.setSizePolicy(QSizePolicy.Policy.Expanding, self.port_combo.sizePolicy().verticalPolicy())
		self.update_list = QPushButton("Update list", self)
		self.update_list.setSizePolicy(QSizePolicy.Policy.Maximum, self.update_list.sizePolicy().verticalPolicy())
		self.update_list.clicked.connect(self.update_list_clicked)
		self.combo_layout.addWidget(self.combo_label)
		self.combo_layout.addWidget(self.port_combo)
		self.combo_layout.addWidget(self.update_list)
		self.main_layout.addLayout(self.combo_layout)

		# Adding a baud rates ComboBox
		self.rate_label = QLabel("Select baud rate:", self)
		self.rate_label.setMinimumSize(120, 0)
		self.rate_label.setSizePolicy(QSizePolicy.Policy.Minimum, self.rate_label.sizePolicy().verticalPolicy())
		self.rate_combo = QComboBox(self)
		self.rate_combo.setSizePolicy(QSizePolicy.Policy.Expanding, self.rate_combo.sizePolicy().verticalPolicy())
		self.rate_combo.addItems([
			"110 baud",
			"300 baud",
			"600 baud",
			"1200 baud",
			"2400 baud",
			"4800 baud",
			"9600 baud",
			"14400 baud",
			"19200 baud",
			"28800 baud",
			"38400 baud",
			"57600 baud"
		])
		self.rate_combo.setCurrentIndex(6)
		self.rate_layout.addWidget(self.rate_label)
		self.rate_layout.addWidget(self.rate_combo)
		self.main_layout.addLayout(self.rate_layout)

		# Adding a monitoring on/off button
		self.monitoring_butt = QPushButton("Monitoring", self)
		self.monitoring_butt.setMinimumSize(35, 35)
		self.monitoring_butt.setCheckable(True)
		self.monitoring_butt.clicked.connect(self.monitoring_butt_clicked)
		self.main_layout.addWidget(self.monitoring_butt)

		# Adding a text output field intercepted from the COM port
		self.text = QTextEdit(self)
		self.text.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
		self.text.setReadOnly(True)
		self.main_layout.addWidget(self.text)

		# Dialog window customization
		self.setLayout(self.main_layout)
		self.setWindowTitle("Serial Monitor")
		self.setMinimumSize(600, 480)

		# Creating a COM port object
		self.com = QSerialPort()
		self.com.setBaudRate(int(self.rate_combo.currentText().split(" ")[0]))
		self.com.readyRead.connect(self.serial_write)
		self.string_data: bytes = b''

	def update_list_clicked(self) -> None:
		"""
		Button for updating the list of available COM ports.
		"""
		self.port_combo.clear()
		for port in QSerialPortInfo().availablePorts():
			self.port_combo.addItem(f"{str(port.portName())} - {str(port.description())}")

	def monitoring_butt_clicked(self) -> None:
		"""
		If the monitoring button is pressed - turns monitoring on/off.
		"""
		if self.monitoring_butt.isChecked():
			self.monitoring_butt.setText(f"Monitoring of {self.port_combo.currentText().split(' - ')[1]}")
			self.com.setPortName(self.port_combo.currentText().split(" ")[0])
			self.com.open(QIODevice.OpenModeFlag.ReadOnly)
		else:
			self.monitoring_butt.setText(f"Monitoring")
			self.com.close()

	def serial_write(self) -> None:
		"""
		When data arrives at the COM port, it saves them in the program.
		"""
		self.string_data += self.com.readLine().data()
		if b'\n' in self.string_data:
			self.text.append(self.string_data.decode().rstrip())
			self.string_data = b''

	def close(self) -> bool:
		"""
		Closes the COM port if it is open.

		:return: See the Qt documentation
		"""
		if self.com.isOpen():
			self.com.close()
		return super().close()

if __name__ == '__main__':
	app = QApplication(sys.argv)
	ui = SerialDialog()
	ui.show()
	sys.exit(app.exec())
