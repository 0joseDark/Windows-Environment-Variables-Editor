import sys
import os
import winreg
from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QVBoxLayout,
    QHBoxLayout, QLabel, QLineEdit, QListWidget, QMessageBox, QMenuBar, QMenu
)

class EnvEditor(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Editor de Variáveis de Ambiente")
        self.setGeometry(100, 100, 600, 400)

        # Layout principal
        self.layout = QVBoxLayout()

        # Menu
        self.menu_bar = QMenuBar(self)
        menu = self.menu_bar.addMenu("Ficheiro")
        menu.addAction("Sair", self.close)
        self.layout.setMenuBar(self.menu_bar)

        # Lista de variáveis
        self.var_list = QListWidget()
        self.var_list.itemClicked.connect(self.load_variable)
        self.layout.addWidget(QLabel("Variáveis do Utilizador:"))
        self.layout.addWidget(self.var_list)

        # Campos para editar
        self.name_edit = QLineEdit()
        self.value_edit = QLineEdit()
        self.layout.addWidget(QLabel("Nome da Variável:"))
        self.layout.addWidget(self.name_edit)
        self.layout.addWidget(QLabel("Valor da Variável:"))
        self.layout.addWidget(self.value_edit)

        # Botões
        btn_layout = QHBoxLayout()

        self.edit_btn = QPushButton("Editar")
        self.edit_btn.clicked.connect(self.edit_variable)
        btn_layout.addWidget(self.edit_btn)

        self.add_btn = QPushButton("Escrever")
        self.add_btn.clicked.connect(self.add_variable)
        btn_layout.addWidget(self.add_btn)

        self.delete_btn = QPushButton("Apagar")
        self.delete_btn.clicked.connect(self.delete_variable)
        btn_layout.addWidget(self.delete_btn)

        self.ok_btn = QPushButton("OK")
        self.ok_btn.clicked.connect(self.load_env_vars)
        btn_layout.addWidget(self.ok_btn)

        self.exit_btn = QPushButton("Sair")
        self.exit_btn.clicked.connect(self.close)
        btn_layout.addWidget(self.exit_btn)

        self.layout.addLayout(btn_layout)

        self.setLayout(self.layout)
        self.load_env_vars()

    def load_env_vars(self):
        """Carrega variáveis do utilizador"""
        self.var_list.clear()
        try:
            reg_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                                     "Environment", 0, winreg.KEY_READ)
            i = 0
            while True:
                try:
                    name, value, _ = winreg.EnumValue(reg_key, i)
                    self.var_list.addItem(f"{name} = {value}")
                    i += 1
                except OSError:
                    break
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao ler variáveis: {e}")

    def load_variable(self, item):
        """Preenche os campos com a variável selecionada"""
        try:
            name, value = item.text().split(" = ", 1)
            self.name_edit.setText(name)
            self.value_edit.setText(value)
        except Exception as e:
            QMessageBox.warning(self, "Erro", f"Erro ao carregar variável: {e}")

    def add_variable(self):
        """Adiciona nova variável"""
        name = self.name_edit.text().strip()
        value = self.value_edit.text().strip()
        if not name:
            QMessageBox.warning(self, "Aviso", "O nome da variável não pode estar vazio.")
            return
        try:
            reg_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Environment", 0, winreg.KEY_SET_VALUE)
            winreg.SetValueEx(reg_key, name, 0, winreg.REG_EXPAND_SZ, value)
            winreg.CloseKey(reg_key)
            self.load_env_vars()
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao adicionar variável: {e}")

    def edit_variable(self):
        """Edita variável selecionada"""
        self.add_variable()  # Mesmo procedimento de adicionar

    def delete_variable(self):
        """Remove variável selecionada"""
        name = self.name_edit.text().strip()
        if not name:
            QMessageBox.warning(self, "Aviso", "Selecione uma variável para apagar.")
            return
        try:
            reg_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Environment", 0, winreg.KEY_SET_VALUE)
            winreg.DeleteValue(reg_key, name)
            winreg.CloseKey(reg_key)
            self.name_edit.clear()
            self.value_edit.clear()
            self.load_env_vars()
        except FileNotFoundError:
            QMessageBox.warning(self, "Aviso", f"A variável '{name}' não existe.")
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao apagar variável: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = EnvEditor()
    window.show()
    sys.exit(app.exec_())
