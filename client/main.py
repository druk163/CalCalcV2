import sys
from PyQt6.QtWidgets import QApplication

from client.api_client import ApiClient
from client.windows.login_window import LoginWindow
from client.windows.main_window import MainWindow


class App:
    def __init__(self):
        self.qt_app = QApplication(sys.argv)
        self.api = ApiClient()
        self.login_window = None
        self.main_window = None

    def show_login(self):
        self.login_window = LoginWindow(
            self.api, self.on_login_success
        )
        self.login_window.show()

    def on_login_success(self):
        if self.login_window:
            self.login_window.close()
        self.main_window = MainWindow(self.api)
        self.main_window.show()

    def run(self):
        self.show_login()
        sys.exit(self.qt_app.exec())


if __name__ == "__main__":
    app = App()
    app.run()