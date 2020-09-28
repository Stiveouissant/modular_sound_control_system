import sounddevice
from scipy.io.wavfile import write
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QLabel, QGridLayout
from PyQt5.QtWidgets import QLineEdit, QPushButton, QHBoxLayout
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import Qt


class Recorder(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.interfejs()

    def interfejs(self):

        # etykiety
        etykieta1 = QLabel("Naciśnij przycisk, aby rozpocząć nagrywanie:", self)


        # przypisanie widgetów do układu tabelarycznego
        ukladT = QGridLayout()
        ukladT.addWidget(etykieta1, 0, 0)

        # przyciski
        koniecBtn = QPushButton("&Koniec", self)
        recordBtn = QPushButton("&Nagraj", self)
        koniecBtn.resize(koniecBtn.sizeHint())

        ukladH = QHBoxLayout()
        ukladH.addWidget(recordBtn)

        ukladT.addLayout(ukladH, 2, 0, 1, 3)
        ukladT.addWidget(koniecBtn, 3, 0, 1, 3)

        # przypisanie utworzonego układu do okna
        self.setLayout(ukladT)

        koniecBtn.clicked.connect(self.koniec)
        recordBtn.clicked.connect(self.voice_recording)


        # self.liczba1Edt.setFocus()
        self.setGeometry(20, 20, 300, 100)
        # self.setWindowIcon(QIcon('icon.png'))
        self.setWindowTitle("Voice recording")
        self.show()

    def voice_recording(self):
        fs = 44100
        second = 3
        print("recording......")
        record_voice = sounddevice.rec(int(second * fs), samplerate=fs, channels=1)
        sounddevice.wait()
        write("output.wav", fs, record_voice)

    def koniec(self):
        self.close()

    def closeEvent(self, event):

        odp = QMessageBox.question(
            self, 'Komunikat',
            "Czy na pewno koniec?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if odp == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            self.close()


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    okno = Recorder()
    sys.exit(app.exec_())