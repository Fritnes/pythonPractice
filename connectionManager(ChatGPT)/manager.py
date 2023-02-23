#This program created by using chatgpt.
import sys
import os
import sqlite3
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QTableView, QPushButton, QLineEdit, QLabel, QMessageBox, QFileDialog
from PyQt5.QtSql import QSqlDatabase, QSqlTableModel
import yaml

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.db = None
        self.table = 'mytable'
        self.setGeometry(100, 100, 800, 500)
        self.setWindowTitle('SSH Manager')
        self.create_widgets()
        self.show()
        self.open_db_if_exists()

    def create_widgets(self):
        # create widgets
        self.open_db_button = QPushButton('Open Database')
        self.open_db_button.clicked.connect(self.open_db)

        self.create_db_button = QPushButton('Create Database')
        self.create_db_button.clicked.connect(self.create_db)

        self.add_button = QPushButton('Add Record')
        self.add_button.clicked.connect(self.add_record)

        self.remove_button = QPushButton('Remove Record')
        self.remove_button.clicked.connect(self.remove_record)

        self.connect_button = QPushButton('Connect')
        self.connect_button.clicked.connect(self.connect_record)

        self.table_view = QTableView()

        # create layout
        top_hbox = QHBoxLayout()
        top_hbox.addWidget(self.open_db_button)
        top_hbox.addWidget(self.create_db_button)

        button_hbox = QHBoxLayout()
        button_hbox.addWidget(self.add_button)
        button_hbox.addWidget(self.remove_button)
        button_hbox.addWidget(self.connect_button)

        vbox = QVBoxLayout()
        vbox.addLayout(top_hbox)
        vbox.addLayout(button_hbox)
        vbox.addWidget(self.table_view)

        central_widget = QWidget()
        central_widget.setLayout(vbox)
        self.setCentralWidget(central_widget)

    def open_db_if_exists(self):
        # check if database and table exist
        db_name = config["database"]["name"]
        if os.path.isfile(db_name):
            self.db = QSqlDatabase.addDatabase('QSQLITE')
            self.db.setDatabaseName(db_name)
            if not self.db.open():
                QMessageBox.warning(self, 'Error', 'Could not open database.')
                self.db = None
                return
            if self.db.tables().count(self.table) > 0:
                self.load_table()

    def open_db(self):
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.AnyFile)
        file_dialog.setNameFilter("Database files (*.db)")
        if file_dialog.exec_():
            db_name = file_dialog.selectedFiles()[0]
            if not db_name:
                QMessageBox.warning(self, 'Error', 'Please select a database file.')
                return
            if self.db:
                self.db.close()
            self.db = QSqlDatabase.addDatabase('QSQLITE')
            self.db.setDatabaseName(db_name)
            if not self.db.open():
                QMessageBox.warning(self, 'Error', 'Could not open database.')
                self.db = None
                return
            self.db_name = db_name  # update default database name
            self.load_table()

    def create_db(self):
        db_name, _ = QFileDialog.getSaveFileName(self, 'Create Database', '', 'SQLite Database (*.db)')
        if not db_name:
            QMessageBox.warning(self, 'Error', 'Please enter a database name.')
            return
        if self.db:
            self.db.close()
        self.db = QSqlDatabase.addDatabase('QSQLITE')
        self.db.setDatabaseName(db_name)
        if not self.db.open():
            QMessageBox.warning(self, 'Error', 'Could not create database.')
            self.db = None
            return
        self.db_name = db_name  # update default database name
        self.create_table()
        self.load_table()

    def create_table(self):
        query = f'CREATE TABLE {self.table} (id INTEGER PRIMARY KEY AUTOINCREMENT, hostname TEXT, username TEXT, port INTEGER)'
        self.db.exec(query)

    def load_table(self):
        model = QSqlTableModel()
        model.setTable(self.table)
        model.select()
        self.table_view.setModel(model)

    def add_record(self):
        model = self.table_view.model()
        row_count = model.rowCount()
        model.insertRow(row_count)

    def remove_record(self):
        model = self.table_view.model()
        selected_indexes = self.table_view.selectedIndexes()
        if not selected_indexes:
            return
        row = selected_indexes[0].row()
        model.removeRow(row)
        model.select()

    def connect_record(self):
        model = self.table_view.model()
        selected_indexes = self.table_view.selectedIndexes()
        if not selected_indexes:
            return
        row = selected_indexes[0].row()
        record = model.record(row)
        id = record.value('id')
        hostname = record.value('hostname')
        username = record.value('username')
        port = record.value('port')
        command = f"xterm -e 'bash -c \"ssh {username}@{hostname} -p {port}\"'"
        os.system(command)

if __name__ == '__main__':
    # Load YUML configuration file
    with open("config.yml", "r") as f:
        config = yaml.safe_load(f)
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())
