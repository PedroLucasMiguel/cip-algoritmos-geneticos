from PyQt6.QtWidgets import QWidget, QMessageBox
 
class AlertBox(QWidget):
    def __init__(self, message:str = "Lorem ipsum"):
        super().__init__()
        self.setWindowTitle("Alerta")
 
        dialog = QMessageBox(parent=self, text=message)
        dialog.setWindowTitle("Alerta")
        ret = dialog.exec()