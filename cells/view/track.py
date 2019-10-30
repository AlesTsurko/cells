from PySide2.QtCore import Qt
from PySide2.QtGui import QColor
from PySide2.QtWidgets import QVBoxLayout, QWidget, QLabel

from cells.observation import Observation


class Track(Observation, QWidget):
    def __init__(self, subject, name):
        Observation.__init__(self, subject)
        QWidget.__init__(self)

        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(self.backgroundRole(), QColor("red"))
        self.setPalette(palette)

        self.setFixedWidth(200)

        self.setLayout(QVBoxLayout())
        self.header = Header()
        self.layout().addWidget(self.header)
        self.layout().setSpacing(0)
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.layout().setAlignment(Qt.AlignTop)

        self.setName(name)

    def setName(self, name):
        self.header.setName(name)


class Header(QWidget):
    def __init__(self):
        super().__init__()

        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(self.backgroundRole(), QColor("blue"))
        self.setPalette(palette)

        self.setFixedHeight(100)

        self.setLayout(QVBoxLayout())
        self.layout().setSpacing(0)
        self.layout().setContentsMargins(0, 0, 0, 0)

        self.nameLabel = QLabel(self)
        self.nameLabel.setAlignment(Qt.AlignCenter)
        self.layout().addWidget(self.nameLabel)

    def setName(self, name):
        self.nameLabel.setText(name)