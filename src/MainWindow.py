import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QFileDialog,\
        QLabel, QStatusBar, QVBoxLayout, QHBoxLayout, \
        QMessageBox, QTextEdit, QWidget, QSpinBox, QPushButton, QLineEdit
from PyQt5.QtGui import QPixmap, QPalette
from PyQt5.QtCore import Qt
from src.TextRead import TextRead
from src.TrainModelDialog import TrainModelDialog


class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        #set geometry
        self.setGeometry(50, 50, 900, 600)
        #set title
        self.setWindowTitle('Text Reader From Image')
        #sets necessary variables
        self.pixmap = None
        self.imagePath = None
        self.textRead = None
        self.modelPath = None
        #create user interface
        self.initUI()
        #connect functionality with methods
        self.setupQtConnections()
        #showing all widgets
        self.show()

    def initUI(self):
        """
        Initialization of the User Interface
        """
        #set the horizontal layout
        self.layout = QVBoxLayout()
        widget = QWidget()
        widget.setLayout(self.layout)

        self.layout.addWidget(QLabel('Model Panel'))

        layoutModel1 = QHBoxLayout()
        self.labelModel1 = QLabel('Load Model  (the model is not loaded)!')
        layoutModel1.addWidget(self.labelModel1)

        self.loadModelButton = QPushButton('Load Model', self)
        self.loadModelButton.setToolTip('This button load a model file!')
        layoutModel1.addWidget(self.loadModelButton)
        self.layout.addLayout(layoutModel1)

        layoutModel2 = QHBoxLayout()
        labelModel2 = QLabel('Characters that are learned in the model:  ')
        layoutModel2.addWidget(labelModel2)
        self.textLineModel = QLineEdit('0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ')
        layoutModel2.addWidget(self.textLineModel)
        self.layout.addLayout(layoutModel2)

        self.layoutBot = QHBoxLayout()
        #adding space for image
        self.label = QLabel('Place to display the loaded image!')
        self.label.setBackgroundRole(QPalette.Base)
        self.layoutBot.addWidget(self.label,1)
        #adding space for the text read
        self.textEdit =  QTextEdit()
        self.textEdit.setReadOnly(True)
        self.textEdit.clear()
        self.textEdit.insertPlainText("Load a image to read the content!")
        self.layoutBot.addWidget(self.textEdit,1)

        self.layout.addLayout(self.layoutBot)
        self.setCentralWidget(widget)

        #prepare closing app button
        self.exitButton = QAction("Exit", self)
        self.exitButton.setStatusTip("CLOSE APPLICATION!")
        self.exitButton.setShortcut('Ctrl+Q')
        #prepare load image button
        self.loadButton = QAction("Load Image", self)
        self.loadButton.setStatusTip("Opens a dialog for browsing files in order to select an image!")
        self.loadButton.setShortcut('Ctrl+O')
        #prepare save text button
        self.copyTextButton = QAction("Copy content", self)
        self.copyTextButton.setStatusTip("Copies content from the text window!")
        self.copyTextButton.setShortcut('Ctrl+C')
        #prepare save text button
        self.extractTextButton = QAction("Extract Text", self)
        self.extractTextButton.setStatusTip("Extract Text from Image!")
        self.extractTextButton.setShortcut('Ctrl+E')
        #prepare save text button
        self.saveTextButton = QAction("Save Text", self)
        self.saveTextButton.setStatusTip("Save Text To File")
        self.saveTextButton.setShortcut('Ctrl+S')
        #prepare spinbox for change size text
        self.fontSizeSpinBox = QSpinBox()
        self.fontSizeSpinBox.setStatusTip('Set Text Size!')
        self.fontSizeSpinBox.setFocusPolicy(Qt.NoFocus)
        self.fontSizeSpinBox.setValue(20)
        #prepare reset app button
        self.resetButton = QAction("Reset", self)
        self.resetButton.setStatusTip("Restores the input setting of the application")
        self.resetButton.setShortcut('Ctrl+R')
        #prepare train app button
        self.trainButton = QAction("Train Model", self)
        self.trainButton.setStatusTip("Open a dialog to train model!")
        self.trainButton.setShortcut('Ctrl+T')

        #Toolbar
        #file toolbar
        fileToolBar = self.addToolBar("File")
        fileToolBar.addAction(self.exitButton)
        fileToolBar.addAction(self.loadButton)
        fileToolBar.addAction(self.saveTextButton)
        fileToolBar.addAction(self.resetButton)
        fileToolBar.addAction(self.trainButton)
        #edit toolbar
        editToolBar = self.addToolBar("Edit")
        editToolBar.addAction(self.copyTextButton)
        editToolBar.addAction(self.extractTextButton)
        editToolBar.addWidget(self.fontSizeSpinBox)
        #Menu bar
        menubar = self.menuBar()
        #file menu
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(self.exitButton)
        fileMenu.addAction(self.loadButton)
        fileMenu.addAction(self.saveTextButton)
        fileMenu.addAction(self.resetButton)
        fileMenu.addAction(self.trainButton)
        #edit menu
        editMenu = menubar.addMenu('&Edit')
        editMenu.addAction(self.copyTextButton)
        editMenu.addAction(self.extractTextButton)
        #status bar
        self.setStatusBar(QStatusBar(self))
        #Set font size
        self.onChangedSizeSpinBox()

    def setupQtConnections(self):
        """
        A method that combines events with appropriate methods
        """
        self.exitButton.triggered.connect(self.onClickedButtonExitApp)
        self.loadButton.triggered.connect(self.onClickedButtonLoadImage)
        self.copyTextButton.triggered.connect(self.onClickedButtonCopyText)
        self.extractTextButton.triggered.connect(self.onClickedButtonExtractText)
        self.saveTextButton.triggered.connect(self.onClickedButtonSaveText)
        self.fontSizeSpinBox.valueChanged.connect(self.onChangedSizeSpinBox)
        self.resetButton.triggered.connect(self.onClickReset)
        self.loadModelButton.clicked.connect(self.onClickLoadModelButton)
        self.trainButton.triggered.connect(self.onClickTrainButton)

    def resizeEvent(self, event):
        """
        Override of the method that runs when the size of the main window is changed.
        """
        QMainWindow.resizeEvent(self, event)
        self.printImageWithCorrectSize()

    def printImageWithCorrectSize(self):
        """
        Method displaying the loaded image with the correct size.
        """
        if self.pixmap:
            x=self.label.width()
            y=self.label.height()
            rel=x/y
            if self.relation > rel:
                showPixmap = self.pixmap.scaledToWidth(self.label.width()-5)
            else:
                showPixmap = self.pixmap.scaledToHeight(self.label.height()-5)
            self.label.setPixmap(QPixmap(showPixmap))

    def onClickedButtonLoadImage(self):
        """
        Method calling the window to select and load an image.
        """
        fname = QFileDialog.getOpenFileName(self, 'Open file','\\', "Image files (*.jpg *.png)")
        self.imagePath = fname[0]
        self.pixmap = QPixmap(self.imagePath)
        if self.pixmap.isNull():
            QMessageBox.information(self, "Image Viewer", "Cannot load image!.")
            return
        x=self.pixmap.width()
        y=self.pixmap.height()
        self.relation=x/y
        self.printImageWithCorrectSize()
        self.textEdit.clear()
        self.textEdit.insertPlainText('Push extract button to get text from image!')

    def onClickedButtonExitApp(self):
        """
        Method to close the application.
        """
        choice =  QMessageBox.question(self, 'Exit',
                    "Do you want leave app?",
                    QMessageBox.Yes |  QMessageBox.No)
        if choice ==  QMessageBox.Yes:
            self.close()
        else:
            pass

    def onClickedButtonCopyText(self):
        """
        Copy Context to Clipboard
        """
        cb = QApplication.clipboard()
        cb.clear(mode=cb.Clipboard)
        cb.setText(self.textEdit.toPlainText(),mode=cb.Clipboard)

    def onClickedButtonExtractText(self):
        """
        Extract text from Image
        """
        if self.imagePath:
            self.textRead = TextRead(self.imagePath,list(self.textLineModel.text()),self.modelPath)
            self.textEdit.clear()
            self.textEdit.insertPlainText(str(self.textRead))
            self.pixmap = self.textRead.getImg()
            self.printImageWithCorrectSize()

    def onClickedButtonSaveText(self):
        """
        Save text from text edit
        """
        name = QFileDialog.getSaveFileName(self, 'Save File')
        if not name[0]:
            QMessageBox.information(self, "Image Viewer", "Set correct name with directory!.")
            return
        file = open(name[0],'w')
        text = self.textEdit.toPlainText()
        file.write(text)
        file.close()

    def onChangedSizeSpinBox(self):
        """
        Change Size in text edit box
        """
        self.textEdit.selectAll()
        self.textEdit.setFontPointSize(self.fontSizeSpinBox.value())
        self.textEdit.setTextCursor( self.textEdit.textCursor() )

    def onClickReset(self):
        self.close()
        self.__init__()

    def onClickLoadModelButton(self):
        """
        Method calling the window to select and load an model file.
        """
        fname = QFileDialog.getOpenFileName(self, 'Open file','\\', "Image files (*.h5)")
        if not fname[0]:
            QMessageBox.information(self, "Model", "Set correct name with model directory!.")
            return
        self.modelPath = fname[0]
        self.labelModel1.setText(f'Load Model  (the model {os.path.basename(self.modelPath)} is loaded)!')

    def onClickTrainButton(self):
        TrainModelDialog().exec()
