from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QTableWidget, QTableWidgetItem,
    QProgressBar, QMessageBox, QHeaderView
)
from datetime import date, timedelta

from client.windows.add_meal_window import AddMealWindow


class MainWindow(QMainWindow):
    def __init__(self, api_client):
        super().__init__()
        self.api = api_client
        self.setWindowTitle("Nutrition Tracker — Главная")
        self.setMinimumSize(800, 600)
        self.current_date = date.today()
        self.init_ui()
        self.load_daily_data()

    def init_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout()

        # Шапка
        header = QHBoxLayout()
        user = self.api.current_user
        welcome = QLabel(
            f"Пользователь: {user['username']}  |  "
            f"Цель: {user['daily_goal_kcal']} ккал/день"
        )
        welcome.setStyleSheet("font-size: 16px; font-weight: bold;")
        header.addWidget(welcome)
        header.addStretch()

        btn_prev = QPushButton("< Вчера")
        btn_prev.clicked.connect(self.prev_day)
        header.addWidget(btn_prev)

        self.date_label = QLabel(str(self.current_date))
        self.date_label.setStyleSheet(
            "font-size: 16px; font-weight: bold;"
        )
        header.addWidget(self.date_label)

        btn_next = QPushButton("Завтра >")
        btn_next.clicked.connect(self.next_day)
        header.addWidget(btn_next)

        layout.addLayout(header)

        # Прогресс калорий
        cal_layout = QHBoxLayout()
        cal_layout.addWidget(QLabel("Калории:"))
        self.cal_progress = QProgressBar()
        self.cal_progress.setMaximum(int(user["daily_goal_kcal"]))
        self.cal_progress.setFormat("%v / %m ккал")
        cal_layout.addWidget(self.cal_progress)
        layout.addLayout(cal_layout)

        # БЖУ
        bju_layout = QHBoxLayout()
        self.prot_label = QLabel("Белки: 0 г")
        self.prot_label.setStyleSheet("font-size: 14px; color: #2196F3;")
        bju_layout.addWidget(self.prot_label)

        self.fat_label = QLabel("Жиры: 0 г")
        self.fat_label.setStyleSheet("font-size: 14px; color: #FF9800;")
        bju_layout.addWidget(self.fat_label)

        self.carb_label = QLabel("Углеводы: 0 г")
        self.carb_label.setStyleSheet("font-size: 14px; color: #F44336;")
        bju_layout.addWidget(self.carb_label)

        layout.addLayout(bju_layout)

        # Таблица
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels([
            "Приём пищи", "Продукт", "Вес (г)",
            "Ккал", "Б/Ж/У", "Удалить"
        ])
        self.table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )
        layout.addWidget(self.table)

        # Кнопки
        btn_layout = QHBoxLayout()

        btn_add = QPushButton("Добавить приём пищи")
        btn_add.setStyleSheet(
            "padding: 10px; font-size: 14px; "
            "background-color: #4CAF50; color: white;"
        )
        btn_add.clicked.connect(self.open_add_meal)
        btn_layout.addWidget(btn_add)

        btn_refresh = QPushButton("Обновить")
        btn_refresh.clicked.connect(self.load_daily_data)
        btn_layout.addWidget(btn_refresh)

        layout.addLayout(btn_layout)
        central.setLayout(layout)

    def prev_day(self):
        self.current_date -= timedelta(days=1)
        self.date_label.setText(str(self.current_date))
        self.load_daily_data()

    def next_day(self):
        self.current_date += timedelta(days=1)
        self.date_label.setText(str(self.current_date))
        self.load_daily_data()

    def load_daily_data(self):
        try:
            resp = self.api.get_daily_summary(str(self.current_date))
            if resp.status_code != 200:
                return

            data = resp.json()

            self.cal_progress.setValue(int(data["total_calories"]))
            self.prot_label.setText(
                f"Белки: {data['total_proteins']} г"
            )
            self.fat_label.setText(
                f"Жиры: {data['total_fats']} г"
            )
            self.carb_label.setText(
                f"Углеводы: {data['total_carbs']} г"
            )

            self.table.setRowCount(0)
            meal_names = {
                "breakfast": "Завтрак",
                "lunch": "Обед",
                "dinner": "Ужин",
                "snack": "Перекус",
            }

            for meal in data["meals"]:
                for item in meal["items"]:
                    row = self.table.rowCount()
                    self.table.insertRow(row)

                    self.table.setItem(row, 0, QTableWidgetItem(
                        meal_names.get(
                            meal["meal_type"], meal["meal_type"]
                        )
                    ))
                    self.table.setItem(
                        row, 1,
                        QTableWidgetItem(item["product_name"])
                    )
                    self.table.setItem(
                        row, 2,
                        QTableWidgetItem(str(item["weight_grams"]))
                    )
                    self.table.setItem(
                        row, 3,
                        QTableWidgetItem(str(item["calories"]))
                    )
                    self.table.setItem(row, 4, QTableWidgetItem(
                        f"{item['proteins']}/"
                        f"{item['fats']}/"
                        f"{item['carbs']}"
                    ))

                    btn_del = QPushButton("Удалить")
                    btn_del.clicked.connect(
                        lambda checked, mid=meal["id"]:
                        self.delete_meal(mid)
                    )
                    self.table.setCellWidget(row, 5, btn_del)

        except Exception as e:
            QMessageBox.warning(
                self, "Ошибка",
                f"Не удалось загрузить данные:\n{e}"
            )

    def delete_meal(self, meal_id):
        resp = self.api.delete_meal(meal_id)
        if resp.status_code == 200:
            self.load_daily_data()

    def open_add_meal(self):
        self.add_window = AddMealWindow(
            self.api, self.current_date, self.load_daily_data
        )
        self.add_window.show()