import sys
from PyQt5.QtCore import QUrl, QProcess
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QMessageBox
from PyQt5.QtWebEngineWidgets import QWebEngineView

class SnapcraftWebView(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Snapcraft')
        self.resize(1000, 600)

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.web_view = QWebEngineView(self)
        self.web_view.load(QUrl('https://snapcraft.io/'))
        self.layout.addWidget(self.web_view)

        url_actual = self.web_view.url().toString()
        if url_actual == "https://snapcraft.io/":
            boton_instalar = QPushButton("Instalar")
            self.layout.addWidget(boton_instalar)
            boton_instalar.clicked.connect(self.instalar_paquete)
        else:
            self.boton_instalar = None

        self.web_view.urlChanged.connect(self.verificar_url)

        self.show()

    def verificar_snap(self):
        proceso = QProcess()
        proceso.start('snap', ['version'])
        proceso.waitForFinished()

        exit_code = proceso.exitCode()
        if exit_code != 0:
            mensaje = "Instale Snap en su sistema y vuelva a intentarlo más tarde, por favor."
            QMessageBox.critical(self, "Error", mensaje, QMessageBox.StandardButton.Ok)
            sys.exit(1)

    def verificar_url(self, url):
        if url.toString() == "https://snapcraft.io/":
            for i in reversed(range(self.layout.count())):
                widget = self.layout.itemAt(i).widget()
                if isinstance(widget, QPushButton):
                    widget.deleteLater()
        else:
            if not self.boton_instalar:
                boton_instalar = QPushButton("Instalar")
                self.layout.addWidget(boton_instalar)
                boton_instalar.clicked.connect(self.instalar_paquete)
                self.boton_instalar = boton_instalar

    def instalar_paquete(self):
        url_actual = self.web_view.url().toString()
        if url_actual.startswith("https://snapcraft.io/"):
            paquete = url_actual.replace("https://snapcraft.io/", "")
            comando = f"sudo snap install --classic {paquete}"

            terminal = QProcess()
            terminal.startDetached('x-terminal-emulator', ['-e', 'bash', '-c', comando])
            terminal.finished.connect(self.comando_terminado)

    def comando_terminado(self):
        QMessageBox.information(self, "Éxito", "El paquete se instaló correctamente.", QMessageBox.StandardButton.Ok)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    proceso_verificacion = QProcess()
    proceso_verificacion.start('snap', ['version'])
    proceso_verificacion.waitForFinished()
    
    exit_code_verificacion = proceso_verificacion.exitCode()
    if exit_code_verificacion != 0:
        mensaje = "Instale Snap en su sistema y vuelva a intentarlo más tarde, por favor."
        QMessageBox.critical(None, "Error", mensaje, QMessageBox.StandardButton.Ok)
        sys.exit(1)

    view = SnapcraftWebView()
    sys.exit(app.exec_())
