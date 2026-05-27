from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QMessageBox,
)


class AddProductWindow(QWidget):
    def __init__(self, api):
        super().__init__()

        self.api = api

        self.setWindowTitle("Добавить продукт")
        self.resize(400, 350)

        layout = QVBoxLayout()

        title = QLabel("Добавление нового продукта")
        title.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(title)

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Название продукта")

        self.calories_input = QLineEdit()
        self.calories_input.setPlaceholderText("Калории на 100 г")

        self.proteins_input = QLineEdit()
        self.proteins_input.setPlaceholderText("Белки на 100 г")

        self.fats_input = QLineEdit()
        self.fats_input.setPlaceholderText("Жиры на 100 г")

        self.carbs_input = QLineEdit()
        self.carbs_input.setPlaceholderText("Углеводы на 100 г")

        btn_save = QPushButton("Добавить продукт")
        btn_save.clicked.connect(self.save_product)

        layout.addWidget(self.name_input)
        layout.addWidget(self.calories_input)
        layout.addWidget(self.proteins_input)
        layout.addWidget(self.fats_input)
        layout.addWidget(self.carbs_input)
        layout.addWidget(btn_save)

        self.setLayout(layout)

    def save_product(self):
        try:
            name = self.name_input.text().strip()

            if not name:
                QMessageBox.warning(
                    self,
                    "Ошибка",
                    "Введите название продукта",
                )
                return

            response = self.api.add_product(
                name=name,
                calories=float(self.calories_input.text()),
                proteins=float(self.proteins_input.text()),
                fats=float(self.fats_input.text()),
                carbs=float(self.carbs_input.text()),
            )

            if response.status_code == 200:
                QMessageBox.information(
                    self,
                    "Успех",
                    f"Продукт '{name}' добавлен",
                )
                self.close()
            else:
                QMessageBox.warning(
                    self,
                    "Ошибка",
                    response.text,
                )

        except ValueError:
            QMessageBox.warning(
                self,
                "Ошибка",
                "Калории, белки, жиры и углеводы должны быть числами",
            )

        except Exception as e:
            QMessageBox.warning(
                self,
                "Ошибка",
                str(e),
            )
