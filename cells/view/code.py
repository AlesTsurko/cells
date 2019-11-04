import os
import time

from PySide2.QtWebEngineWidgets import QWebEngineView, QWebEnginePage
from PySide2.QtWidgets import QDialog, QBoxLayout, QShortcut
from PySide2.QtCore import Qt, QUrl
from PySide2.QtGui import QKeySequence
from cells.observation import Observation
from cells import events
import cells.utility as utility


class Code(Observation, QDialog):
    def __init__(self, cell, subject):

        self.cell = cell

        Observation.__init__(self, subject)
        QDialog.__init__(self)

        self.setModal(True)

        self.webView = QWebEngineView()
        self.webView.setContextMenuPolicy(Qt.NoContextMenu)

        page = Ace(cell, subject)
        self.webView.setPage(page)

        layout = QBoxLayout(QBoxLayout.TopToBottom)
        layout.addWidget(self.webView)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)
        QShortcut(QKeySequence("Alt+Esc"), self, self.close)

        self.setMinimumSize(500, 300)

        self.webView.page().loadFinished.connect(self.onLoadFinished)

    def onLoadFinished(self, ok):
        if len(self.cell.code()) < 1:
            self.setCodeAsync(self.tip())
            self.webView.page().runJavaScript("editor.selectAll();")
        else:
            self.setCodeAsync(self.cell.code())
        self.webView.page().runJavaScript("editor.focus();")

    def tip(self):
        return "Shift+Enter    - evaluate line or selection\\n" +\
               "Ctrl/Cmd+Enter - evaluate the whole buffer\\n" +\
               "Alt+Esc        - close the editor\\n" +\
               "Ctrl/Cmd+Alt+H - view all shortcuts"

    def setCodeAsync(self, code):
        self.webView.page().runJavaScript(
            f"editor.session.setValue('{code}');")

    def reject(self):
        self.close()

    def closeEvent(self, event):
        self.delete()
        return super().closeEvent(event)

    def delete(self):
        self.webView.page().setParent(None)
        self.webView.page().deleteLater()
        self.unregister()
        self.setParent(None)
        self.deleteLater()


class Ace(Observation, QWebEnginePage):
    def __init__(self, cell, subject):
        self.cell = cell

        QWebEnginePage.__init__(self)
        Observation.__init__(self, subject)

        aceUrl = QUrl.fromLocalFile(os.path.join(
            utility.viewResourcesDir(), "ace", "index.html"))
        self.load(aceUrl)
        # I'd like to move all the python<->js communication here
        # but when I'm starting to implement something more than just
        # virtual functions, I get:
        # ERROR:mach_port_broker.mm(193)] Unknown process  is sending Mach IPC messages!
        # so here is implementations of callbacks only

    def javaScriptConsoleMessage(self, level, message, lineNumber, sourceID):
        self.parseConsoleOutput(message)

    def parseConsoleOutput(self, message):
        print(message)
        if message.startswith(Token.evaluate):
            self.evaluate(message[len(Token.evaluate):])

    def evaluate(self, code):
        print("send evaluate")
        print(code)
        self.notify(events.view.code.Evaluate(code))


class Token:
    evaluate = "<-!code_evaluation_triggered!->"
