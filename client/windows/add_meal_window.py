from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QComboBox,
    QDoubleSpinBox,
    QTableWidget,
    QTableWidgetItem,
    QMessageBox,
    QHeaderView,
)
from PyQt6.QtCore import Qt


class AddMealWindow(QWidget):
    def __init__(self, api_client, current_date, on_save_callback):
        super().__init__()
        self.api = api_client
        self.current_date = current_date
        self.on_save = on_save_callback
        self.selected_items = []

        self.setWindowTitle("Добавить приём пищи")
        self.setMinimumSize(500, 500)
        self.init_ui()
        self.load_products()

    def init_ui(self):
        layout = QVBoxLayout()

        # Тип приёма
        type_layout = QHBoxLayout()
        type_layout.addWidget(QLabel("Тип:"))
        self.meal_type_combo = QComboBox()
        self.meal_type_combo.addItems(["breakfast", "lunch", "dinner", "snack"])
        type_layout.addWidget(self.meal_type_combo)
        layout.addLayout(type_layout)

        # Поиск
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Поиск продукта...")
        self.search_input.textChanged.connect(self.load_products)
        layout.addWidget(self.search_input)

        # Таблица продуктов
        self.products_table = QTableWidget()
        self.products_table.setColumnCount(5)
        self.products_table.setHorizontalHeaderLabels(["Название", "Ккал", "Б", "Ж", "У"])
        self.products_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.products_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        layout.addWidget(self.products_table)

        # Вес + кнопка
        add_layout = QHBoxLayout()
        add_layout.addWidget(QLabel("Вес (г):"))
        self.weight_input = QDoubleSpinBox()
        self.weight_input.setRange(1, 5000)
        self.weight_input.setValue(100)
        add_layout.addWidget(self.weight_input)

        btn_add = QPushButton("Добавить в список")
        btn_add.clicked.connect(self.add_item_to_list)
        add_layout.addWidget(btn_add)
        layout.addLayout(add_layout)

        # Выбранные
        layout.addWidget(QLabel("Выбранные продукты:"))
        self.selected_table = QTableWidget()
        self.selected_table.setColumnCount(3)
        self.selected_table.setHorizontalHeaderLabels(["Продукт", "Вес (г)", "Убрать"])
        self.selected_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        layout.addWidget(self.selected_table)

        # Сохранить
        btn_save = QPushButton("Сохранить приём пищи")
        btn_save.setStyleSheet(
            "padding: 10px; font-size: 14px; " "background-color: #4CAF50; color: white;"
        )
        btn_save.clicked.connect(self.save_meal)
        layout.addWidget(btn_save)

        self.setLayout(layout)

    def load_products(self):
        try:
            resp = self.api.get_products(search=self.search_input.text())
            if resp.status_code != 200:
                return

            products = resp.json()
            self.products_table.setRowCount(0)

            for p in products:
                row = self.products_table.rowCount()
                self.products_table.insertRow(row)

                item_name = QTableWidgetItem(p["name"])
                item_name.setData(Qt.ItemDataRole.UserRole, p["id"])

                self.products_table.setItem(row, 0, item_name)
                self.products_table.setItem(row, 1, QTableWidgetItem(str(p["calories"])))
                self.products_table.setItem(row, 2, QTableWidgetItem(str(p["proteins"])))
                self.products_table.setItem(row, 3, QTableWidgetItem(str(p["fats"])))
                self.products_table.setItem(row, 4, QTableWidgetItem(str(p["carbs"])))
        except Exception as e:
            print(f"Ошибка: {e}")

    def add_item_to_list(self):
        selected = self.products_table.currentRow()
        if selected < 0:
            QMessageBox.warning(self, "Ошибка", "Выберите продукт")
            return

        product_id = self.products_table.item(selected, 0).data(Qt.ItemDataRole.UserRole)
        product_name = self.products_table.item(selected, 0).text()
        weight = self.weight_input.value()

        self.selected_items.append(
            {
                "product_id": product_id,
                "weight_grams": weight,
            }
        )

        row = self.selected_table.rowCount()
        self.selected_table.insertRow(row)
        self.selected_table.setItem(row, 0, QTableWidgetItem(product_name))
        self.selected_table.setItem(row, 1, QTableWidgetItem(str(weight)))

        btn_remove = QPushButton("X")
        btn_remove.clicked.connect(lambda checked, r=row: self.remove_item(r))
        self.selected_table.setCellWidget(row, 2, btn_remove)

    def remove_item(self, row):
        if row < len(self.selected_items):
            self.selected_items.pop(row)
            self.selected_table.removeRow(row)

    def save_meal(self):
        if not self.selected_items:
            QMessageBox.warning(self, "Ошибка", "Добавьте хотя бы один продукт")
            return

        resp = self.api.add_meal(
            date=str(self.current_date),
            meal_type=self.meal_type_combo.currentText(),
            items=self.selected_items,
        )

        if resp.status_code == 200:
            QMessageBox.information(self, "Успех", "Сохранено!")
            self.on_save()
            self.close()
        else:
            QMessageBox.warning(self, "Ошибка", "Не удалось сохранить")
