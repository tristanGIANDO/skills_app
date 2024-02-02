import os
import sys
import webbrowser
from skills_app.Qt import QtWidgets, QtGui, QtCore
from skills_app import envs

HEADERS = ["Soft / Skill", "Level"]


class CustomTreeItem(QtWidgets.QTreeWidgetItem):
    def __init__(self, data: dict):
        super(CustomTreeItem, self).__init__()
        if not data:
            return
        self._data = data
        if data:
            self._name = data[0]
            for i in range(len(HEADERS)):
                self.setText(i, str(data[i]))
                # self.setTextAlignment(i, QtCore.Qt.AlignCenter)
                if i % 2 == 0:
                    if STANDALONE:
                        self.setBackground(i, QtGui.QColor(240,240,240))
                    else:
                        self.setBackground(i, QtGui.QColor(50,50,50))

            # color type
            self.setIcon(1, QtGui.QIcon(self.type_color(data[1])))

        self.setSizeHint(2,QtCore.QSize(20,20))


class MainUI(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(MainUI, self).__init__(parent)

        self._title = "SKILZAP"
        self._version = "1.0"
        self._builder = None
        self.setWindowTitle(f"{self._title} v-{self._version}")
        # self.setWindowIcon(ICONS.get("logo"))
        self.setGeometry(100, 100, 600, 400)
        central_widget = QtWidgets.QWidget()
        self.setCentralWidget(central_widget)

        self._layout = QtWidgets.QVBoxLayout()
        central_widget.setLayout(self._layout)
        self._project_path = ""

        self.create_menubar()
        # title
        # title_label = QtWidgets.QLabel(self)
        # pixmap = QtGui.QPixmap(ICONS.get_title())
        # pixmap = pixmap.scaledToWidth(200, QtCore.Qt.SmoothTransformation)
        # title_label.setPixmap(pixmap)
        # title_label.setAlignment(QtCore.Qt.AlignCenter)
        # central_widget.layout().addWidget(title_label)
        # root

        self.tab_widget = QtWidgets.QTabWidget()
        self.database_tab()

        self.tab_db_idx = self.tab_widget.addTab(self.db_tab, "DATABASE")
        self._layout.addWidget(self.tab_widget)

        self._layout.addWidget(QtWidgets.QLabel("By Tristan Giandoriggio"))

        self.create_connections()

    def closeEvent(self, event):
        if self._builder:
            self._builder.close()
        event.accept()

    def database_tab(self) -> None:
        self.db_tab = QtWidgets.QWidget()
        # tree
        self.tree = QtWidgets.QTreeWidget() 
        self.tree.setColumnCount(len(HEADERS))
        self.tree.setHeaderLabels(HEADERS)
        for i in range(len(HEADERS)):
            self.tree.header().setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeToContents)
        self.tree.setRootIsDecorated(False)
        self.tree.setSortingEnabled(True)
        self.tree.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.tree.customContextMenuRequested.connect(self._show_context_menu)
        self.tree.header().sectionsMovable()
        
        select_tab_layout = QtWidgets.QVBoxLayout()
        select_tab_layout.addWidget(self.tree)

        self.db_tab.setLayout(select_tab_layout)

    def reload(self) -> None:
        self.reload_tree()


    def reload_tree(self) ->None:
        self.tree.clear()
  
        for data in []:
            item = CustomTreeItem(data)
            self.tree.addTopLevelItem(item)

    def create_menubar(self):
        self.menu_bar = self.menuBar()

        self.about_menu = self.menu_bar.addMenu("About")
        self.action["help"] = QtWidgets.QAction("Help (?)", self)
        self.action["help"].triggered.connect(self.on_help_triggered)
        self.about_menu.addAction(self.action["help"])
        self.action["about"] = QtWidgets.QAction("About me", self)
        self.action["about"].triggered.connect(self.on_about_triggered)
        self.about_menu.addAction(self.action["about"])

    def on_help_triggered(self) -> None:
        QtWidgets.QMessageBox.question(
                    self,
                    "Need help ?", 
                    f"""
        Some important conventions:\n
    * The object name should not contain any special characters apart from '/' and spaces should be replaced by '_'.
    * Decimal numbers are written as 'xxx.x', no ',' is required.
    * Powers are written as 'xxex'.
    * The parent 'Origin' means that the object rotates around the barycentre of the system represented.

        Approximations :\n
    * It is difficult to find all the data, especially that concerning physical characteristics.
    However, always enter a value in all the boxes, even if it is 0.

    * To change the colours of the types, go to the 'envs.py' file.

    Have fun ! :)
                    """,
                    QtWidgets.QMessageBox.Ok)

    def on_about_triggered(self) -> None:
        webbrowser.open(envs.ME)

    def create_connections(self) -> None:
        pass

    def _show_context_menu(self, position):
        delete_action = QtWidgets.QAction("Delete")
        delete_action.triggered.connect(self.on_delete_triggered)
        modify_action = QtWidgets.QAction("Modify")
        modify_action.triggered.connect(self.on_modified_triggered)
        menu = QtWidgets.QMenu(self)
        menu.addAction(delete_action)
        menu.addAction(modify_action)
        menu.exec_(self.mapToGlobal(position))

    def on_delete_triggered(self) -> None:
        name = self.tree.currentItem()._name
        # self._builder.delete_element(name)
        self.reload()

    def on_modified_triggered(self) ->None:
        data = self.tree.currentItem()._data
        # set to creation tab
        # self.tab_widget.setCurrentIndex(self.tab_create_idx)

    def read(self) -> dict:
        pass

    def on_create_button_clicked(self) -> None:
        # self._builder.add_element(self.read())
        # message_box = QtWidgets.QMessageBox.information(
        #             self,
        #             "Success", 
        #             f"Object created with success !",
        #             QtWidgets.QMessageBox.Ok)
        # self.reload()
        pass


class Icons():
    def __init__(self):
        self._root = os.path.join(os.path.dirname(__file__), "icons")
        self._cache = {}
        self._icons = {
        }

    def get(self, key):
        if key in self._cache:
            return self._cache[key]

        path = os.path.join(self._root, self._icons.get(key))
        icon = QtGui.QIcon(path)
        self._cache[path] = icon
        return icon


ICONS = Icons()


def run_ui():
    try:
        app = QtWidgets.QApplication(sys.argv)
    except:
        try:
            ui.close()
        except:
            pass

    ui = MainUI()
    ui.show()

    try:
        sys.exit(app.exec_())
    except:
        pass


if __name__ == '__main__':
    run_ui()
