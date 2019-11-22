#######################################################################

import os
import ctypes
from ctypes import POINTER, Structure, c_wchar, c_int, sizeof, byref
isWindows = os.name == 'nt'
if isWindows:
    from ctypes.wintypes import BYTE, WORD, DWORD, LPWSTR, LPSTR

    HICON = c_int
    LPTSTR = LPWSTR
    TCHAR = c_wchar
    MAX_PATH = 260
    FCSM_ICONFILE = 0x00000010
    FCS_FORCEWRITE = 0x00000002
    SHGFI_ICONLOCATION = 0x000001000

    class GUID(Structure):
        _fields_ = [
            ('Data1', DWORD),
            ('Data2', WORD),
            ('Data3', WORD),
            ('Data4', BYTE * 8)]

    class SHFOLDERCUSTOMSETTINGS(Structure):
        _fields_ = [
            ('dwSize', DWORD),
            ('dwMask', DWORD),
            ('pvid', POINTER(GUID)),
            ('pszWebViewTemplate', LPTSTR),
            ('cchWebViewTemplate', DWORD),
            ('pszWebViewTemplateVersion', LPTSTR),
            ('pszInfoTip', LPTSTR),
            ('cchInfoTip', DWORD),
            ('pclsid', POINTER(GUID)),
            ('dwFlags', DWORD),
            ('pszIconFile', LPTSTR),
            ('cchIconFile', DWORD),
            ('iIconIndex', c_int),
            ('pszLogo', LPTSTR),
            ('cchLogo', DWORD)]

    class SHFILEINFO(Structure):
        _fields_ = [
            ('hIcon', HICON),
            ('iIcon', c_int),
            ('dwAttributes', DWORD),
            ('szDisplayName', TCHAR * MAX_PATH),
            ('szTypeName', TCHAR * 80)]

    def seticon(folderpath, iconpath, iconindex):
        """Set folder icon.

        >>> seticon(".", "C:\\Windows\\system32\\SHELL32.dll", 10)

        """
        shell32 = ctypes.windll.shell32

        folderpath = os.path.abspath(folderpath)
        iconpath = os.path.abspath(iconpath)

        fcs = SHFOLDERCUSTOMSETTINGS()
        fcs.dwSize = sizeof(fcs)
        fcs.dwMask = FCSM_ICONFILE
        fcs.pszIconFile = iconpath
        fcs.cchIconFile = 0
        fcs.iIconIndex = iconindex

        sfi = SHFILEINFO()

        index = shell32.Shell_GetCachedImageIndexW(sfi.szDisplayName, sfi.iIcon, 0)

        shell32.SHUpdateImageW(sfi.szDisplayName, sfi.iIcon, 0, index)

#######################################################################

def mkdir(path):
    # Обёртка над функцией создания папки
    try:
        os.makedirs(path)
    except OSError:
        print('Создать директорию %s не удалось' % path)

#######################################################################

try:
    from PyQt5 import QtCore, QtGui, QtWidgets
except:
    print('Библиотека PyQt5 не найдена. Вы можете её установить следующей коммандой в консоли с правами администратора: ')
    print('pip install pyqt5')
    input('Нажмите Enter для завершения\n')
    exit()

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.resize(382, 552)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setObjectName("label")
        self.verticalLayout_2.addWidget(self.label, 0, QtCore.Qt.AlignHCenter)
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout_2.addWidget(self.line)
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_2.addWidget(self.label_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.imgPath_field = QtWidgets.QLineEdit(self.centralwidget)
        self.imgPath_field.setObjectName("imgPath_field")
        self.horizontalLayout.addWidget(self.imgPath_field)
        self.selectImgPath_button = QtWidgets.QPushButton(self.centralwidget)
        self.selectImgPath_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.selectImgPath_button.setObjectName("selectImgPath_button")
        self.horizontalLayout.addWidget(self.selectImgPath_button)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.aboutImgPath_label = QtWidgets.QLabel(self.centralwidget)
        self.aboutImgPath_label.setText("")
        self.aboutImgPath_label.setObjectName("aboutImgPath_label")
        self.verticalLayout_2.addWidget(self.aboutImgPath_label)
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setObjectName("label_3")
        self.verticalLayout_2.addWidget(self.label_3)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.desktopPath_field = QtWidgets.QLineEdit(self.centralwidget)
        self.desktopPath_field.setText("")
        self.desktopPath_field.setObjectName("desktopPath_field")
        self.horizontalLayout_2.addWidget(self.desktopPath_field)
        self.selectDesktopPath_button = QtWidgets.QPushButton(self.centralwidget)
        self.selectDesktopPath_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.selectDesktopPath_button.setObjectName("selectDesktopPath_button")
        self.horizontalLayout_2.addWidget(self.selectDesktopPath_button)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.aboutDesktopPath_label = QtWidgets.QLabel(self.centralwidget)
        self.aboutDesktopPath_label.setText("")
        self.aboutDesktopPath_label.setObjectName("aboutDesktopPath_label")
        self.verticalLayout_2.addWidget(self.aboutDesktopPath_label)
        self.label_8 = QtWidgets.QLabel(self.centralwidget)
        self.label_8.setObjectName("label_8")
        self.verticalLayout_2.addWidget(self.label_8)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setContentsMargins(-1, -1, -1, 45)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setObjectName("label_4")
        self.verticalLayout.addWidget(self.label_4)
        self.iconSize_field = QtWidgets.QSpinBox(self.centralwidget)
        self.iconSize_field.setMinimum(1)
        self.iconSize_field.setObjectName("iconSize_field")
        self.verticalLayout.addWidget(self.iconSize_field)
        self.horizontalLayout_3.addLayout(self.verticalLayout)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        self.horizontalLayout_3.addItem(spacerItem)
        self.line_2 = QtWidgets.QFrame(self.centralwidget)
        self.line_2.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.horizontalLayout_3.addWidget(self.line_2)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        self.horizontalLayout_3.addItem(spacerItem1)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setObjectName("label_5")
        self.verticalLayout_3.addWidget(self.label_5)
        self.label_7 = QtWidgets.QLabel(self.centralwidget)
        self.label_7.setObjectName("label_7")
        self.verticalLayout_3.addWidget(self.label_7)
        self.cellX_field = QtWidgets.QSpinBox(self.centralwidget)
        self.cellX_field.setMinimum(1)
        self.cellX_field.setObjectName("cellX_field")
        self.verticalLayout_3.addWidget(self.cellX_field)
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setObjectName("label_6")
        self.verticalLayout_3.addWidget(self.label_6)
        self.cellY_field = QtWidgets.QSpinBox(self.centralwidget)
        self.cellY_field.setMinimum(1)
        self.cellY_field.setObjectName("cellY_field")
        self.verticalLayout_3.addWidget(self.cellY_field)
        self.horizontalLayout_3.addLayout(self.verticalLayout_3)
        self.verticalLayout_2.addLayout(self.horizontalLayout_3)
        self.calculate_button = QtWidgets.QPushButton(self.centralwidget)
        self.calculate_button.setMaximumSize(QtCore.QSize(200, 16777215))
        self.calculate_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.calculate_button.setObjectName("calculate_button")
        self.verticalLayout_2.addWidget(self.calculate_button, 0, QtCore.Qt.AlignHCenter)
        self.line_3 = QtWidgets.QFrame(self.centralwidget)
        self.line_3.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.verticalLayout_2.addWidget(self.line_3)
        self.textBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser.setEnabled(True)
        self.textBrowser.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
        self.textBrowser.setObjectName("textBrowser")
        self.verticalLayout_2.addWidget(self.textBrowser)
        self.progressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar.setObjectName("progressBar")
        self.verticalLayout_2.addWidget(self.progressBar)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.createPuzzle_button = QtWidgets.QPushButton(self.centralwidget)
        self.createPuzzle_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.createPuzzle_button.setObjectName("createPuzzle_button")
        self.horizontalLayout_4.addWidget(self.createPuzzle_button)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        self.horizontalLayout_4.addItem(spacerItem2)
        self.clearParams_button = QtWidgets.QPushButton(self.centralwidget)
        self.clearParams_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.clearParams_button.setObjectName("clearParams_button")
        self.horizontalLayout_4.addWidget(self.clearParams_button)
        spacerItem3 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        self.horizontalLayout_4.addItem(spacerItem3)
        self.delPrevPuzzle_button = QtWidgets.QPushButton(self.centralwidget)
        self.delPrevPuzzle_button.setObjectName("delPrevPuzzle_button")
        self.horizontalLayout_4.addWidget(self.delPrevPuzzle_button)
        self.verticalLayout_2.addLayout(self.horizontalLayout_4)
        self.label.raise_()
        self.line.raise_()
        self.label_3.raise_()
        self.label_8.raise_()
        self.line_3.raise_()
        self.label_2.raise_()
        self.calculate_button.raise_()
        self.aboutImgPath_label.raise_()
        self.aboutDesktopPath_label.raise_()
        self.progressBar.raise_()
        self.textBrowser.raise_()
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Создание мозаики"))
        self.label.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\">Эта программа создаёт мозаику папок с иконками, составленными из <br>вашей картинки. Вам остаётся лишь собрать получившийся пазл.</p></body></html>"))
        self.label_2.setText(_translate("MainWindow", "Выберите путь к картинке:"))
        self.selectImgPath_button.setText(_translate("MainWindow", "Выбрать"))
        self.label_3.setText(_translate("MainWindow", "Выберите путь к рабочему столу пользователя (если указан неверно):"))
        self.selectDesktopPath_button.setText(_translate("MainWindow", "Выбрать"))
        self.label_8.setText(_translate("MainWindow", "Заполните поля на одной из сторон:"))
        self.label_4.setText(_translate("MainWindow", "Ввод размера иконки:"))
        self.label_5.setText(_translate("MainWindow", "Ввод размера мозаики:"))
        self.label_7.setText(_translate("MainWindow", "Ширина:"))
        self.label_6.setText(_translate("MainWindow", "Высота:"))
        self.calculate_button.setText(_translate("MainWindow", "Расcчитать"))
        self.progressBar.setFormat(_translate("MainWindow", "%v/%m[%p%]"))
        self.createPuzzle_button.setText(_translate("MainWindow", "Создать мозаику"))
        self.clearParams_button.setText(_translate("MainWindow", "Сбросить значения"))
        self.delPrevPuzzle_button.setToolTip(_translate("MainWindow", "Не работает, так как фунционал этой кнопки не реализован"))
        self.delPrevPuzzle_button.setText(_translate("MainWindow", "Удалить мозаику"))



#######################################################################

##from design import Ui_MainWindow

##Твои рабочие элементы:

##imgPath_field
##selectImgPath_button
##desktopPath_field
##selectDesktopPath_button
##iconSize_field
##cellX_field
##cellY_field
##calculate_button
##createPuzzle_button
##clearParams_button
##aboutDesktopPath_label
##aboutImgPath_label
##delPrevPuzzle_button
##progressBar
##textBrowser

class ExampleApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # Подключение обработчиков кликов на кнопки
        self.clearParams_button.clicked.connect(self.clearAllFields)
        self.calculate_button.clicked.connect(self.calculate)
        self.selectImgPath_button.clicked.connect(self.browseImgPath)
##        self.delPrevPuzzle_button.clicked.connect(self.delPreviousPuzzle)

        # Подключение обработчиков смены значений на поля ввода
        self.imgPath_field.textChanged.connect(self.onChangeImgPath)
        self.iconSize_field.valueChanged.connect(self.onChangeIconSize)
        self.cellX_field.valueChanged.connect(self.onChangeCellXorCellY)
        self.cellY_field.valueChanged.connect(self.onChangeCellXorCellY)

        # Отключение кнопки удаления мозаики, ведь функционал нереализован
        self.delPrevPuzzle_button.setEnabled(False)
        # Вычислено ли окончательное разрешение мозаики
        self.isCalculated = False
        # Заблокирован ли ввод значений в соседнем поле на 2-ом этапе
        # Блокировка нужна, чтобы не запускалась бесконечная рекурсия обработчиков
        # И чтобы поля не менялись в процессе их обработки
        self.blockEnteringData = False
        # Корректен ли путь к картинке
        self.isImgPathCorrect = False
        # Корректен ли путь к рабочему столу
        self.isDesktopPathCorrect = False
        # Путь к последней успешно открытой картинке (кэширование)
        self.lastSuccessOpenedImgPath = ''
        # Содержимое textBrowser
        self.baseHTML = '<html><head/><body><p></p></body></html>'
        self.lastHTML = self.baseHTML
        # Первоначальная блокировка 2-го этапа (ввод параметров мозаики)
        self.changeStateOf2ndStep(False)
        # Первоначальная блокировка 3-го этапа (само создание мозаики)
        self.changeStateOf3rdStep()
        if isWindows:
            self.desktopPath_field.textChanged.connect(self.onChangeDesktopPath)
            self.selectDesktopPath_button.clicked.connect(self.browseDesktopPath)
            self.createPuzzle_button.clicked.connect(self.createPuzzle)
            # Чистка предыдущих временных файлов
            dir_for_icons = 'C:/PleaseDontDeleteMe'
            if os.path.isdir(dir_for_icons):
                from shutil import rmtree
                rmtree(dir_for_icons, ignore_errors = True)

            # Создание временной папки для иконок
            from random import random
            dir_for_icons += f'/dir_for_icons{random()}'
            mkdir(dir_for_icons)
            self.dir_for_icons = dir_for_icons
        else:
            self.desktopPath_field.setEnabled(False)
            self.selectDesktopPath_button.setEnabled(False)
            self.aboutDesktopPath_label.setStyleSheet('color: #900;')
            self.aboutDesktopPath_label.setText('К сожалению, ОС, отличные от Windows, не поддерживаются.')
            self.createPuzzle_button.setToolTip('ОС, отличные от Windows, не поддерживаются')

    def onChangeImgPath(self):
        # Обработчик изменениия пути к картинке
        isSuccess = False
        imgPath = self.imgPath_field.text()
        self.clear2ndStepFields()
        isCashed = self.lastSuccessOpenedImgPath == imgPath
        if not imgPath:
            text = ''
        elif os.path.isfile(imgPath):
            try:
                if isCashed:
                    # Если это старое изображение, восстанавливаем значения полей ввода
                    if self.isCalculated:
                        cellX = self.confirmedCellX
                        cellY = self.confirmedCellY
                    else:
                        cellX = self.cellX
                        cellY = self.cellY
                    self.blockEnteringData = True
                    self.cellX_field.setValue(cellX)
                    self.cellY_field.setValue(cellY)
                    self.blockEnteringData = False
                    self.onChangeCellXorCellY()
                else:
                    # Если это новое изображение, обработать его
                    from PIL import Image
                    img = Image.open(imgPath).convert('RGBA')
                    self.isCalculated = False
                    self.imgWidth = imgWidth = img.size[0]
                    self.imgHeight = imgHeight = img.size[1]
                    self.img = img
                    maxIconSize = min(imgWidth, imgHeight)
                    self.iconSize_field.setMaximum(maxIconSize)
                    self.iconSize_field.setValue(maxIconSize)
                    self.cellX_field.setMaximum(imgWidth)
                    self.cellY_field.setMaximum(imgHeight)
                    self.lastSuccessOpenedImgPath = imgPath
                isSuccess = True
                text = f'Изображение с разрешением {self.imgWidth} * {self.imgHeight} успешно открыто.'
            except ImportError:
                text = 'Библиотека PIL не найдена. Команда для установки: pip install pillow'
            except:
                text = 'Данное изображение не поддерживается. Выберите другое.'
        else:
            text = 'По заданному пути нет изображения.'
        self.aboutImgPath_label.setStyleSheet(f"color: #{'07' if isSuccess else '90'}0;")
        self.aboutImgPath_label.setText(text)
        self.isImgPathCorrect = isSuccess
        self.progressBar.setTextVisible(self.isCalculated and isCashed)
        self.textBrowser.setHtml(self.lastHTML if self.isCalculated and isCashed else self.baseHTML)
        self.progressBar.setValue(0)
        self.changeStateOf2ndStep(isSuccess)
        self.changeStateOf3rdStep()

    def onChangeDesktopPath(self):
        # Обработчик изменениия пути к рабочему столу
        isSuccess = False
        desktopPath = self.desktopPath_field.text()
        if not desktopPath:
            text = ''
        elif os.path.isdir(desktopPath) and (desktopPath[-8:] == '/Desktop' or desktopPath[-9:] == '/Desktop/'):
            isSuccess = True
            text = 'Папка успешно задана.'
            self.desktopPath = desktopPath
        else:
            text = 'Это не рабочий стол.'
        self.aboutDesktopPath_label.setStyleSheet(f"color: #{'07' if isSuccess else '90'}0;")
        self.aboutDesktopPath_label.setText(text)
        self.isDesktopPathCorrect = isSuccess
        self.changeStateOf3rdStep()

    def browseImgPath(self):
        # Диалоговое окно выбора пути к картинке
        fileName = QtWidgets.QFileDialog.getOpenFileName(self, 'Выберите картинку', filter='Images (*.bmp *.png *.jpeg *.jpg *.ico *.webp)')[0]
        if fileName:
            self.imgPath_field.setText(fileName)

    def browseDesktopPath(self):
        # Диалоговое окно выбора пути к рабочему столу
        directory = QtWidgets.QFileDialog.getExistingDirectory(self, 'Выберите папку Desktop')
        if directory:
            self.desktopPath_field.setText(directory)

    def onChangeIconSize(self):
        # Обработчик изменениия размера иконки
        if not self.blockEnteringData:
            self.blockEnteringData = True
            iconSize = self.iconSize_field.value()
            self.cellX = self.imgWidth // iconSize
            self.cellY = self.imgHeight // iconSize
            self.cellX_field.setValue(self.cellX)
            self.cellY_field.setValue(self.cellY)
            self.blockEnteringData = False

    def onChangeCellXorCellY(self):
        # Обработчик изменениия разрешения мозаики
        if not self.blockEnteringData:
            self.blockEnteringData = True
            self.cellX = cellX = self.cellX_field.value()
            self.cellY = cellY = self.cellY_field.value()
            self.iconSize_field.setValue(min(self.imgWidth // cellX, self.imgHeight // cellY))
            self.blockEnteringData = False

    def calculate(self):
        # Расчёт параметров мозаики и вывод их на экран
        self.blockEnteringData = True

        self.confirmedCellX = cellX = self.cellX_field.value()
        self.confirmedCellY = cellY = self.cellY_field.value()

        self.confirmedIconSize = iconSize = min(self.imgWidth // cellX, self.imgHeight // cellY)

        oldIconSize = self.iconSize_field.value()
        imgWidth = cellX * iconSize
        imgHeight = cellY * iconSize
        message = ''
        if iconSize != oldIconSize:
            message += f'''Установлен неоптимальный размер иконки.
            Он будет изменён с {oldIconSize} на {iconSize}, для наименьшей обрезки картинки.
            Размер мозаики при этом останется неизменным. '''
        allCells = str(cellX * cellY)
        ending1 = f' ({cellX}*{cellY})' if allCells != '1' else ''
        ending2 = 'ки' if allCells[-1] == '1' and (allCells == '1' or allCells[-2] != '1') else 'ок'

        message += f'У вас получится мозайка, состоящая из {allCells + ending1} пап{ending2}, при размере иконки {iconSize}*{iconSize}. '
        if (imgWidth, imgHeight) != (self.imgWidth, self.imgHeight):
            percentX = f'{(1 - imgWidth / self.imgWidth) * 100:.1f}'
            percentY = f'{(1 - imgHeight/self.imgHeight) * 100:.1f}'
            percentX = '' if percentX == '0.0' else f'(-{percentX}%)'
            percentY = '' if percentY == '0.0' else f'(-{percentY}%)'
            message += f'Разрешение картинки станет {imgWidth} {percentX} в ширину и {imgHeight} {percentY} в высоту. '
        message = f'<html><head/><body><p style="font-size:10pt;font-family:\'Verdana\';">{message}</p></body></html>'
        self.textBrowser.setHtml(message)
        self.lastHTML = message
        self.isCalculated = True
        self.progressBar.setTextVisible(True)
        self.progressBar.setMaximum(int(allCells))
        self.progressBar.setValue(0)
        self.changeStateOf3rdStep()
        self.blockEnteringData = False

    def createPuzzle(self):
        # Создание мозаики
        self.changeStateOfAllFields(False)
##        self.imgPath_field.setEnabled(False)
        dir_for_icons = self.dir_for_icons
        img = self.img
        desktopPath = self.desktopPath
        iconSize = self.confirmedIconSize
        cellX = self.confirmedCellX
        cellY = self.confirmedCellY
        numNow = 0
        x = 0
        for numx in range(cellX):
            y = 0
            for numy in range(cellY):
                numNow += 1
                canvasDir = desktopPath + '/' + ' ' * numNow + '/'
                if not os.path.isdir(canvasDir):
                    mkdir(canvasDir)
                newImg = img.crop( (x, y, x + iconSize, y + iconSize) )
                self.progressBar.setValue(numNow)
                iconDir = f'{dir_for_icons}/x{numx + 1}_y{numy + 1}.ico'
                newImg.save(iconDir)

                seticon(canvasDir, iconDir,0)
                y += iconSize
            x += iconSize
        self.changeStateOfAllFields(True)

    def clearAllFields(self):
        # Очистка всех полей
        self.imgPath_field.setText('')
        self.desktopPath_field.setText('')
        self.clear2ndStepFields()

    def delPreviousPuzzle(self):
        pass

    def changeStateOf2ndStep(self, isUnlocked):
        # Блокировка или разблокировка полей 2-го этапа
        self.calculate_button.setEnabled(isUnlocked)
        self.iconSize_field.setEnabled(isUnlocked)
        self.cellX_field.setEnabled(isUnlocked)
        self.cellY_field.setEnabled(isUnlocked)

    def changeStateOf3rdStep(self):
        # Блокировка или разблокировка кнопки создания мозаики
        self.createPuzzle_button.setEnabled(self.isImgPathCorrect and self.isDesktopPathCorrect and self.isCalculated)

    def clear2ndStepFields(self):
        # Очистка полей 2-го этапа
        self.blockEnteringData = True
        self.iconSize_field.setValue(1)
        self.cellX_field.setValue(1)
        self.cellY_field.setValue(1)
        self.blockEnteringData = False

    def changeStateOfAllFields(self, isUnlocked):
        # Блокировка или разблокировка всех полей
        self.changeStateOf2ndStep(isUnlocked)
        self.imgPath_field.setEnabled(isUnlocked)
        self.selectImgPath_button.setEnabled(isUnlocked)
        self.desktopPath_field.setEnabled(isUnlocked)
        self.selectDesktopPath_button.setEnabled(isUnlocked)

#######################################################################

# Открытие окна
window = QtWidgets.QApplication([])
window.setStyle('Fusion')
app = ExampleApp()
app.show()
if isWindows:
    # Попытка установки папки рабочего стола по умолчанию
    try:
        env = dict(os.environ)
        directory = (env['HOMEDRIVE'] + env['HOMEPATH']).replace('\\' , '/') + '/Desktop'
    except:
        directory = 'C:/Users/User/Desktop'
    app.desktopPath_field.setText(directory)
window.exec_()
