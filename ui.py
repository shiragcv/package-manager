import os
import sys

from PySide2 import QtWidgets
from PySide2 import QtCore
from PySide2 import QtUiTools

import core
import settings
import tree


_MAIN_UI = os.path.join(settings.RESOURCE_PATH, "main.ui")


class MainWidget(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWidget, self).__init__()

        self.input_dir = ""
        self.output_dir = ""

        self.ui = None

        self.build()

    def build(self):
        self.setWindowTitle("Package Manager")
        self.setLayout(QtWidgets.QHBoxLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.layout().setSpacing(0)

        qfile = QtCore.QFile(_MAIN_UI)
        qfile.open(QtCore.QFile.ReadOnly)
        self.ui = QtUiTools.QUiLoader().load(qfile, self)
        qfile.close()

        # Connections
        self.ui.pbt_browse_input.clicked.connect(self.browse_input)
        self.ui.pbt_browse_output.clicked.connect(self.browse_output)

        self.ui.pbt_execute.clicked.connect(self.execute)
        self.ui.pbt_cancel.clicked.connect(self.cancel)

    def browse(self):
        return QtWidgets.QFileDialog(self).getExistingDirectory()

    def browse_input(self):
        directory = self.browse()

        if directory:
            self.input_dir = directory
            self.ui.lne_input_directory.setText(self.input_dir)

    def browse_output(self):
        directory = self.browse()

        if directory:
            self.output_dir = directory
            self.ui.lne_output_directory.setText(self.output_dir)

    def get_context(self):
        return core.Context(
            project=self.ui.lne_project.text(),
            shot=self.ui.lne_shot.text(),
            task=self.ui.lne_task.text()
        )

    def execute(self):
        context = self.get_context()

        if not context.isvalid():
            raise Exception("Invalid context")

        if not self.input_dir or not os.path.exists(self.input_dir):
            raise Exception("Input directory not found")

        if not self.output_dir or not os.path.exists(self.output_dir):
            raise Exception("Output directory not found")

        result = tree.create(
            template=tree.get(context=context, directory=self.input_dir),
            directory=self.output_dir
        )

        if result["status"]:
            QtWidgets.QMessageBox.information(
                self,
                "Success",
                "Package created successfully"
            )

    def cancel(self):
        self.close()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    widget = MainWidget()
    widget.show()
    sys.exit(app.exec_())
