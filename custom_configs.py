import sys, PyQt5, json, pathfinder_gen
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QWidget, QApplication, QComboBox, QLineEdit, QGroupBox, QGridLayout, QVBoxLayout, QHBoxLayout, QPushButton, QMessageBox)
from PyQt5.QtCore import pyqtSlot

class MainWin(QWidget):
	waypoints = {}
	
	def __init__(self):
		super().__init__()
		self.waypoints = self.load_json()
		self.main()

	def main(self):
		self.setWindowTitle('Pathfinder Generation Hub')
		self.setWindowIcon(QIcon('Resources\\pyqt_logo.png'))
		self.setGeometry(100, 100, 400, 400)

		self.new_path_name = QLineEdit(self)
		self.alliance_color = QComboBox(self)
		self.alliance_color.addItems(['Red', 'Blue'])
		self.new_path_submit = QPushButton('Add new path', self)
		self.new_path_submit.clicked.connect(lambda: self.create_new_gui(self.new_path_name.text(), self.alliance_color.currentText()))
		self.new_path = [self.new_path_name, self.alliance_color, self.new_path_submit]

		self.mod_entries = QComboBox(self)
		self.mod_entries.addItems(list(self.waypoints.keys()))
		self.mod_entry_button = QPushButton('Modify', self)
		self.mod_entry_button.clicked.connect(lambda: self.create_mod_gui(self.mod_entries.currentText()))
		self.mod_path = [self.mod_entries, self.mod_entry_button]

		self.save_all_changes = QPushButton('Save All Changes', self)
		self.save_all_changes.clicked.connect(self.dump_json)

		self.grid = QGridLayout()
		self.grid.addWidget(self.widget_group(self.new_path, 'Add new path configuration'), 0, 0)
		self.grid.addWidget(self.widget_group([self.save_all_changes], 'Save Changes'), 1, 0)
		self.grid.addWidget(self.widget_group(self.mod_path, 'Modify an existing path'), 0, 1)
		self.setLayout(self.grid)
		
		self.show()

	def load_json(self):
		with open('waypoints.json', 'r') as f:
			try:
				waypoints = json.load(f)
			except Exception as e:
				waypoints = {}
		return waypoints

	def dump_json(self):
		with open('waypoints.json', 'w') as f:
			json.dump(self.waypoints, f, indent=4)
		QMessageBox.about(self, 'Saving to JSON file', 'Successfuly saved to JSON file.')

	def widget_group(self, widgets, title):
		widget_group = QGroupBox(title)
		vbox = QVBoxLayout()

		for widget in widgets:
			vbox.addWidget(widget)
			vbox.addStretch()
		
		widget_group.setLayout(vbox)
		return widget_group
		
	def create_new_gui(self, title, alliance_color):
		if title.strip():
			if list(self.waypoints.keys()).count(title) == 0:
				path = pathfinder_gen.simulate(title, alliance_color=alliance_color)
				self.waypoints[title] = path
				self.mod_entries.clear()
				self.mod_entries.addItems(list(self.waypoints.keys()))
			else:
				QMessageBox.about(self, 'Error when making new path', 'That path already exists.')
		else: 
			QMessageBox.about(self, 'Error whem making new path', 'A name was not provided for this path.')
		

	def create_mod_gui(self, title):
		if len(list(self.waypoints.keys())) == 0:
			QMessageBox.about(self, 'Error when modifying path', 'There are no existing paths to modify.')
		else:
			path = pathfinder_gen.simulate(title, existing_waypoints=self.waypoints[title])
			self.waypoints[title] = path


app = QApplication(sys.argv)
win = MainWin()
sys.exit(app.exec_())