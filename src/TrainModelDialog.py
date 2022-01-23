import sys
from PyQt5.QtGui import QTextCursor
from PyQt5.QtCore import QProcess, QObject, pyqtSignal
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QHBoxLayout, \
    QLineEdit, QPushButton, QFileDialog, QMessageBox, QWidget, QTextEdit
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D, Dense, Flatten, Dropout
from keras.preprocessing.image import ImageDataGenerator
import math


class Stream(QObject):
    newText = pyqtSignal(str)

    def write(self, text):
        self.newText.emit(str(text))

    def flush(self):
        pass

class TrainModelDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Train Model')
        self.training_data=''
        self.validation_data=''
        self.model = None
        self.initUI()
        self.setupQtConnections()

    def initUI(self):
        """
        Initialization of the Dialog User Interface
        """
        self.layout = QVBoxLayout()

        layoutModel1 = QHBoxLayout()
        self.labelModel1 = QLabel('Training Data Directory (load data):')
        layoutModel1.addWidget(self.labelModel1)
        self.loadTrainingButton = QPushButton('Load Training Data', self)
        self.loadTrainingButton.setToolTip('This button load a training data!')
        layoutModel1.addWidget(self.loadTrainingButton)
        self.layout.addLayout(layoutModel1)

        layoutModel2 = QHBoxLayout()
        self.labelModel2 = QLabel('Validation Data Directory (load data):')
        layoutModel2.addWidget(self.labelModel2)
        self.loadValidationButton = QPushButton('Load Validation Data', self)
        self.loadValidationButton.setToolTip('This button load a validation data!')
        layoutModel2.addWidget(self.loadValidationButton)
        self.layout.addLayout(layoutModel2)

        layoutModel3 = QHBoxLayout()
        labelModel3 = QLabel('Number of characters that will be learned:  ')
        layoutModel3.addWidget(labelModel3)
        self.numOfChar = QLineEdit('9')
        layoutModel3.addWidget(self.numOfChar)
        self.layout.addLayout(layoutModel3)

        layoutModel4 = QHBoxLayout()
        labelModel4 = QLabel('Number of epochs in neuron network:  ')
        layoutModel4.addWidget(labelModel4)
        self.epoch = QLineEdit('6')
        layoutModel4.addWidget(self.epoch)
        self.layout.addLayout(layoutModel4)

        layoutModel5 = QHBoxLayout()
        labelModel5 = QLabel('Number of elements in training dataset:  ')
        layoutModel5.addWidget(labelModel5)
        self.trainingDataSize = QLineEdit('720')
        layoutModel5.addWidget(self.trainingDataSize)
        self.layout.addLayout(layoutModel5)

        layoutModel6 = QHBoxLayout()
        labelModel6 = QLabel('Number of elements in validation dataset:  ')
        layoutModel6.addWidget(labelModel6)
        self.validationDataSize = QLineEdit('180')
        layoutModel6.addWidget(self.validationDataSize)
        self.layout.addLayout(layoutModel6)

        layoutModel7 = QHBoxLayout()
        labelModel7 = QLabel('Batch Size:  ')
        layoutModel7.addWidget(labelModel7)
        self.batchSize = QLineEdit('18')
        layoutModel7.addWidget(self.batchSize)
        self.layout.addLayout(layoutModel7)

        self.startTrainData = QPushButton('Start Train Model', self)
        self.layout.addWidget(self.startTrainData)

        self.process  = QTextEdit()
        self.process.moveCursor(QTextCursor.Start)
        self.process.ensureCursorVisible()
        self.process.setLineWrapColumnOrWidth(500)
        self.process.setLineWrapMode(QTextEdit.FixedPixelWidth)
        self.layout.addWidget(self.process)

        self.saveToFile = QPushButton('Save Model', self)
        self.layout.addWidget(self.saveToFile)

        self.setLayout(self.layout)

    def setupQtConnections(self):
        """
        A method that combines events with appropriate methods
        """
        self.loadTrainingButton.clicked.connect(self.onClickLoadTrainingButton)
        self.loadValidationButton.clicked.connect(self.onClickLoadValidationButton)
        self.saveToFile.clicked.connect(self.onClickSaveToFile)
        self.startTrainData.clicked.connect(self.onClickStartTrainData)
        sys.stdout = Stream(newText=self.onUpdateText)

    def onUpdateText(self, text):
        cursor = self.process.textCursor()
        cursor.movePosition(QTextCursor.End)
        cursor.insertText(text)
        self.process.setTextCursor(cursor)
        self.process.ensureCursorVisible()

    def onClickLoadTrainingButton(self):
        fname = QFileDialog.getExistingDirectory(self, "Choose Training Directory")
        if not fname:
            QMessageBox.information(self, "Model", "Set correct directory to training data!")
            return
        self.training_data = fname
        self.labelModel1.setText('Training Data Directory (Directory Loaded):')

    def onClickLoadValidationButton(self):
        fname = QFileDialog.getExistingDirectory(self, "Choose Validation Directory")
        if not fname:
            QMessageBox.information(self, "Model", "Set correct directory to validation data!")
            return
        self.validation_data = fname
        self.labelModel2.setText('Validation Data Directory (Directory Loaded):')

    def onClickStartTrainData(self):
        print("Training started (wait a while)")
        self.train()
        print("Training finished")

    def onClickSaveToFile(self):
        name = QFileDialog.getSaveFileName(self, 'Save Model','model.h5')
        self.model.save(name[0])

    def train(self):
        self.model=Sequential()
        self.model.add(Conv2D(32,(3,3),input_shape=(64,64,1),activation='relu'))
        self.model.add(MaxPooling2D(pool_size=(2,2)))
        self.model.add(Conv2D(32,(3,3),activation='relu'))
        self.model.add(MaxPooling2D(pool_size=(2,2)))
        self.model.add(Flatten())
        self.model.add(Dense(units=128,activation='relu'))
        self.model.add(Dropout(0.5))
        self.model.add(Dense(units=int(self.numOfChar.text()),activation='sigmoid'))
        self.model.compile(optimizer='adam',loss='sparse_categorical_crossentropy',metrics=['accuracy'])

        train_datagen=ImageDataGenerator(rescale = 1./255,
                                   shear_range = 0.2,
                                   zoom_range = 0.2,
                                    horizontal_flip = False)

        test_datagen=ImageDataGenerator(rescale = 1./255)

        training_set=train_datagen.flow_from_directory(directory = self.training_data,
                                                 target_size = (64, 64),
                                                 color_mode='grayscale',
                                                 batch_size = int(self.batchSize.text()),
                                                 class_mode = 'sparse')

        test_set=test_datagen.flow_from_directory(directory = self.validation_data,
                                            target_size = (64, 64),
                                            color_mode='grayscale',
                                            batch_size = int(self.batchSize.text()),
                                            class_mode = 'sparse')

        compute_steps_per_epoch = lambda x: int(math.ceil(1. * x / int(self.batchSize.text())))
        steps_per_epoch = compute_steps_per_epoch(int(self.trainingDataSize.text()))
        val_steps = compute_steps_per_epoch(int(self.validationDataSize.text()))
        self.model.fit(training_set,
            epochs = int(self.epoch.text()),
            steps_per_epoch=steps_per_epoch,
            validation_data = test_set,
            validation_steps=val_steps,
            shuffle=True
            )