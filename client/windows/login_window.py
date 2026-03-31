from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit,
    QPushButton, QMessageBox, QTabWidget,
    QSpinBox, QDoubleSpinBox, QComboBox, QFormLayout
)
from PyQt6.QtCore import Qt


class LoginWindow(QWidget):
    def __init__(self, api_client, on_success):
        super().__init__()
        self.api = api_client
        self.on_success = on_success
        self.setWindowTitle("Nutrition Tracker — Вход")
        self.setFixedSize(400, 400)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        title = QLabel("Nutrition Tracker")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet(
            "font-size: 22px; font-weight: bold; margin: 10px;"
        )
        layout.addWidget(title)

        tabs = QTabWidget()

        # --- Вкладка ВХОД ---
        login_tab = QWidget()
        login_layout = QFormLayout()

        self.login_username = QLineEdit()
        self.login_username.setPlaceholderText("Логин")
        login_layout.addRow("Логин:", self.login_username)

        self.login_password = QLineEdit()
        self.login_password.setPlaceholderText("Пароль")
        self.login_password.setEchoMode(QLineEdit.EchoMode.Password)
        login_layout.addRow("Пароль:", self.login_password)

        btn_login = QPushButton("Войти")
        btn_login.clicked.connect(self.do_login)
        login_layout.addRow(btn_login)

        login_tab.setLayout(login_layout)
        tabs.addTab(login_tab, "Вход")

        # --- Вкладка РЕГИСТРАЦИЯ ---
        reg_tab = QWidget()
        reg_layout = QFormLayout()

        self.reg_username = QLineEdit()
        self.reg_username.setPlaceholderText("Придумайте логин")
        reg_layout.addRow("Логин:", self.reg_username)

        self.reg_password = QLineEdit()
        self.reg_password.setPlaceholderText("Придумайте пароль")
        self.reg_password.setEchoMode(QLineEdit.EchoMode.Password)
        reg_layout.addRow("Пароль:", self.reg_password)

        self.reg_age = QSpinBox()
        self.reg_age.setRange(10, 100)
        self.reg_age.setValue(25)
        reg_layout.addRow("Возраст:", self.reg_age)

        self.reg_weight = QDoubleSpinBox()
        self.reg_weight.setRange(30, 300)
        self.reg_weight.setValue(70)
        self.reg_weight.setSuffix(" кг")
        reg_layout.addRow("Вес:", self.reg_weight)

        self.reg_height = QDoubleSpinBox()
        self.reg_height.setRange(100, 250)
        self.reg_height.setValue(175)
        self.reg_height.setSuffix(" см")
        reg_layout.addRow("Рост:", self.reg_height)

        self.reg_gender = QComboBox()
        self.reg_gender.addItems(["male", "female"])
        reg_layout.addRow("Пол:", self.reg_gender)

        btn_register = QPushButton("Зарегистрироваться")
        btn_register.clicked.connect(self.do_register)
        reg_layout.addRow(btn_register)

        reg_tab.setLayout(reg_layout)
        tabs.addTab(reg_tab, "Регистрация")

        layout.addWidget(tabs)
        self.setLayout(layout)

    def do_login(self):
        resp = self.api.login(
            self.login_username.text().strip(),
            self.login_password.text().strip()
        )
        if resp.status_code == 200:
            self.on_success()
        else:
            QMessageBox.warning(
                self, "Ошибка",
                resp.json().get("detail", "Ошибка")
            )

    def do_register(self):
        resp = self.api.register(
            username=self.reg_username.text().strip(),
            password=self.reg_password.text().strip(),
            age=self.reg_age.value(),
            weight=self.reg_weight.value(),
            height=self.reg_height.value(),
            gender=self.reg_gender.currentText(),
        )
        if resp.status_code == 200:
            QMessageBox.information(
                self, "Успех", "Регистрация прошла успешно!"
            )
            self.on_success()
        else:
            QMessageBox.warning(
                self, "Ошибка",
                resp.json().get("detail", "Ошибка")
            )