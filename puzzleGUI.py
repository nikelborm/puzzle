#######################################################################

import os
import ctypes
from ctypes import POINTER, Structure, c_wchar, c_int, sizeof, byref
if os.name == 'not':
    from ctypes.wintypes import BYTE, WORD, DWORD, LPWSTR, LPSTR
    try:
        import win32api
    except:
        print('Библиотека win32api не найдена. Вы можете её установить следующей коммандой в консоли с правами администратора: ')
        print('pip install pywin32')
        input('Нажмите Enter для завершения\n')
        exit()

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

        hr = shell32.SHGetSetFolderCustomSettings(byref(fcs), folderpath,
                                                  FCS_FORCEWRITE)
        if hr:
            raise WindowsError(win32api.FormatMessage(hr))

        sfi = SHFILEINFO()
        hr = shell32.SHGetFileInfoW(folderpath, 0, byref(sfi), sizeof(sfi), SHGFI_ICONLOCATION)

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
    def setupUi(s, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.resize(382, 552)
        s.centralwidget = QtWidgets.QWidget(MainWindow)
        s.centralwidget.setObjectName("centralwidget")
        s.verticalLayout_2 = QtWidgets.QVBoxLayout(s.centralwidget)
        s.verticalLayout_2.setObjectName("verticalLayout_2")
        s.label = QtWidgets.QLabel(s.centralwidget)
        s.label.setObjectName("label")
        s.verticalLayout_2.addWidget(s.label, 0, QtCore.Qt.AlignHCenter)
        s.line = QtWidgets.QFrame(s.centralwidget)
        s.line.setFrameShape(QtWidgets.QFrame.HLine)
        s.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        s.line.setObjectName("line")
        s.verticalLayout_2.addWidget(s.line)
        s.label_2 = QtWidgets.QLabel(s.centralwidget)
        s.label_2.setObjectName("label_2")
        s.verticalLayout_2.addWidget(s.label_2)
        s.horizontalLayout = QtWidgets.QHBoxLayout()
        s.horizontalLayout.setObjectName("horizontalLayout")
        s.imgPath_field = QtWidgets.QLineEdit(s.centralwidget)
        s.imgPath_field.setObjectName("imgPath_field")
        s.horizontalLayout.addWidget(s.imgPath_field)
        s.selectImgPath_button = QtWidgets.QPushButton(s.centralwidget)
        s.selectImgPath_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        s.selectImgPath_button.setObjectName("selectImgPath_button")
        s.horizontalLayout.addWidget(s.selectImgPath_button)
        s.verticalLayout_2.addLayout(s.horizontalLayout)
        s.aboutImgPath_label = QtWidgets.QLabel(s.centralwidget)
        s.aboutImgPath_label.setText("")
        s.aboutImgPath_label.setObjectName("aboutImgPath_label")
        s.verticalLayout_2.addWidget(s.aboutImgPath_label)
        s.label_3 = QtWidgets.QLabel(s.centralwidget)
        s.label_3.setObjectName("label_3")
        s.verticalLayout_2.addWidget(s.label_3)
        s.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        s.horizontalLayout_2.setObjectName("horizontalLayout_2")
        s.desktopPath_field = QtWidgets.QLineEdit(s.centralwidget)
        s.desktopPath_field.setText("")
        s.desktopPath_field.setObjectName("desktopPath_field")
        s.horizontalLayout_2.addWidget(s.desktopPath_field)
        s.selectDesktopPath_button = QtWidgets.QPushButton(s.centralwidget)
        s.selectDesktopPath_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        s.selectDesktopPath_button.setObjectName("selectDesktopPath_button")
        s.horizontalLayout_2.addWidget(s.selectDesktopPath_button)
        s.verticalLayout_2.addLayout(s.horizontalLayout_2)
        s.aboutDesktopPath_label = QtWidgets.QLabel(s.centralwidget)
        s.aboutDesktopPath_label.setText("")
        s.aboutDesktopPath_label.setObjectName("aboutDesktopPath_label")
        s.verticalLayout_2.addWidget(s.aboutDesktopPath_label)
        s.label_8 = QtWidgets.QLabel(s.centralwidget)
        s.label_8.setObjectName("label_8")
        s.verticalLayout_2.addWidget(s.label_8)
        s.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        s.horizontalLayout_3.setObjectName("horizontalLayout_3")
        s.verticalLayout = QtWidgets.QVBoxLayout()
        s.verticalLayout.setContentsMargins(-1, -1, -1, 45)
        s.verticalLayout.setObjectName("verticalLayout")
        s.label_4 = QtWidgets.QLabel(s.centralwidget)
        s.label_4.setObjectName("label_4")
        s.verticalLayout.addWidget(s.label_4)
        s.iconSize_field = QtWidgets.QSpinBox(s.centralwidget)
        s.iconSize_field.setMinimum(1)
        s.iconSize_field.setObjectName("iconSize_field")
        s.verticalLayout.addWidget(s.iconSize_field)
        s.horizontalLayout_3.addLayout(s.verticalLayout)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        s.horizontalLayout_3.addItem(spacerItem)
        s.line_2 = QtWidgets.QFrame(s.centralwidget)
        s.line_2.setFrameShape(QtWidgets.QFrame.VLine)
        s.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        s.line_2.setObjectName("line_2")
        s.horizontalLayout_3.addWidget(s.line_2)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        s.horizontalLayout_3.addItem(spacerItem1)
        s.verticalLayout_3 = QtWidgets.QVBoxLayout()
        s.verticalLayout_3.setObjectName("verticalLayout_3")
        s.label_5 = QtWidgets.QLabel(s.centralwidget)
        s.label_5.setObjectName("label_5")
        s.verticalLayout_3.addWidget(s.label_5)
        s.label_7 = QtWidgets.QLabel(s.centralwidget)
        s.label_7.setObjectName("label_7")
        s.verticalLayout_3.addWidget(s.label_7)
        s.cellX_field = QtWidgets.QSpinBox(s.centralwidget)
        s.cellX_field.setMinimum(1)
        s.cellX_field.setObjectName("cellX_field")
        s.verticalLayout_3.addWidget(s.cellX_field)
        s.label_6 = QtWidgets.QLabel(s.centralwidget)
        s.label_6.setObjectName("label_6")
        s.verticalLayout_3.addWidget(s.label_6)
        s.cellY_field = QtWidgets.QSpinBox(s.centralwidget)
        s.cellY_field.setMinimum(1)
        s.cellY_field.setObjectName("cellY_field")
        s.verticalLayout_3.addWidget(s.cellY_field)
        s.horizontalLayout_3.addLayout(s.verticalLayout_3)
        s.verticalLayout_2.addLayout(s.horizontalLayout_3)
        s.calculate_button = QtWidgets.QPushButton(s.centralwidget)
        s.calculate_button.setMaximumSize(QtCore.QSize(200, 16777215))
        s.calculate_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        s.calculate_button.setObjectName("calculate_button")
        s.verticalLayout_2.addWidget(s.calculate_button, 0, QtCore.Qt.AlignHCenter)
        s.line_3 = QtWidgets.QFrame(s.centralwidget)
        s.line_3.setFrameShape(QtWidgets.QFrame.HLine)
        s.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        s.line_3.setObjectName("line_3")
        s.verticalLayout_2.addWidget(s.line_3)
        s.textBrowser = QtWidgets.QTextBrowser(s.centralwidget)
        s.textBrowser.setEnabled(True)
        s.textBrowser.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
        s.textBrowser.setObjectName("textBrowser")
        s.verticalLayout_2.addWidget(s.textBrowser)
        s.progressBar = QtWidgets.QProgressBar(s.centralwidget)
        s.progressBar.setObjectName("progressBar")
        s.verticalLayout_2.addWidget(s.progressBar)
        s.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        s.horizontalLayout_4.setObjectName("horizontalLayout_4")
        s.createPuzzle_button = QtWidgets.QPushButton(s.centralwidget)
        s.createPuzzle_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        s.createPuzzle_button.setObjectName("createPuzzle_button")
        s.horizontalLayout_4.addWidget(s.createPuzzle_button)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        s.horizontalLayout_4.addItem(spacerItem2)
        s.clearParams_button = QtWidgets.QPushButton(s.centralwidget)
        s.clearParams_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        s.clearParams_button.setObjectName("clearParams_button")
        s.horizontalLayout_4.addWidget(s.clearParams_button)
        spacerItem3 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        s.horizontalLayout_4.addItem(spacerItem3)
        s.delPrevPuzzle_button = QtWidgets.QPushButton(s.centralwidget)
        s.delPrevPuzzle_button.setObjectName("delPrevPuzzle_button")
        s.horizontalLayout_4.addWidget(s.delPrevPuzzle_button)
        s.verticalLayout_2.addLayout(s.horizontalLayout_4)
        s.label.raise_()
        s.line.raise_()
        s.label_3.raise_()
        s.label_8.raise_()
        s.line_3.raise_()
        s.label_2.raise_()
        s.calculate_button.raise_()
        s.aboutImgPath_label.raise_()
        s.aboutDesktopPath_label.raise_()
        s.progressBar.raise_()
        s.textBrowser.raise_()
        MainWindow.setCentralWidget(s.centralwidget)

        s.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(s, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Создание мозаики"))
        s.label.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\">Эта программа создаёт мозаику папок с иконками, составленными из <br>вашей картинки. Вам остаётся лишь собрать получившийся пазл.</p></body></html>"))
        s.label_2.setText(_translate("MainWindow", "Выберите путь к картинке:"))
        s.selectImgPath_button.setText(_translate("MainWindow", "Выбрать"))
        s.label_3.setText(_translate("MainWindow", "Выберите путь к рабочему столу пользователя (если указан неверно):"))
        s.selectDesktopPath_button.setText(_translate("MainWindow", "Выбрать"))
        s.label_8.setText(_translate("MainWindow", "Заполните поля на одной из сторон:"))
        s.label_4.setText(_translate("MainWindow", "Ввод размера иконки:"))
        s.label_5.setText(_translate("MainWindow", "Ввод размера мозаики:"))
        s.label_7.setText(_translate("MainWindow", "Ширина:"))
        s.label_6.setText(_translate("MainWindow", "Высота:"))
        s.calculate_button.setText(_translate("MainWindow", "Расcчитать"))
        s.progressBar.setFormat(_translate("MainWindow", "%v/%m[%p%]"))
        s.createPuzzle_button.setText(_translate("MainWindow", "Создать мозаику"))
        s.clearParams_button.setText(_translate("MainWindow", "Сбросить значения"))
        s.delPrevPuzzle_button.setToolTip(_translate("MainWindow", "Не работает, так как фунционал этой кнопки не реализован"))
        s.delPrevPuzzle_button.setText(_translate("MainWindow", "Удалить мозаику"))


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
    def __init__(s):
        super().__init__()
        s.setupUi(s)
        
        # Подключение обработчиков кликов на кнопки
        s.clearParams_button.clicked.connect(s.clearAllFields)
        s.calculate_button.clicked.connect(s.calculate)
        s.createPuzzle_button.clicked.connect(s.createPuzzle)
        s.selectImgPath_button.clicked.connect(s.browseImgPath)
##        s.delPrevPuzzle_button.clicked.connect(s.delPreviousPuzzle)
        
        # Подключение обработчиков смены значений на поля ввода
        s.imgPath_field.textChanged.connect(s.onChangeImgPath)
        s.iconSize_field.valueChanged.connect(s.onChangeIconSize)
        s.cellX_field.valueChanged.connect(s.onChangeCellXorCellY)
        s.cellY_field.valueChanged.connect(s.onChangeCellXorCellY)
        
        # Отключение кнопки удаления мозаики, ведь функционал нереализован
        s.delPrevPuzzle_button.setEnabled(False)
        # Вычислено ли окончательное разрешение мозаики
        s.isCalculated = False
        # Заблокирован ли ввод значений в соседнем поле на 2-ом этапе
        # Блокировка нужна, чтобы не запускалась бесконечная рекурсия обработчиков
        # И чтобы поля не менялись в процессе их обработки
        s.blockEnteringData = False
        # Корректен ли путь к картинке
        s.isImgPathCorrect = False
        # Корректен ли путь к рабочему столу
        s.isDesktopPathCorrect = False
        # Путь к последней успешно открытой картинке (кэширование)
        s.lastSuccessOpenedImgPath = ''
        # Содержимое textBrowser
        s.baseHTML = '<html><head/><body><p></p></body></html>'
        s.lastHTML = s.baseHTML
        # Первоначальная блокировка 2-го этапа (ввод параметров мозаики)
        s.changeStateOf2ndStep(False)
        # Первоначальная блокировка 3-го этапа (само создание мозаики)
        s.changeStateOf3rdStep()
        if os.name != 'nt':
            s.desktopPath_field.setEnabled(False)
            s.selectDesktopPath_button.setEnabled(False)
            s.aboutDesktopPath_label.setStyleSheet("color: #900;")
            s.aboutDesktopPath_label.setText("К сожалению, ОС, отличные от Windows, не поддерживаются.")
        else:
            s.desktopPath_field.textChanged.connect(s.onChangeDesktopPath)
            s.selectDesktopPath_button.clicked.connect(s.browseDesktopPath)
            # Чистка предыдущих временных файлов
            dir_for_icons = 'C:/PleaseDontDeleteMe'
            if os.path.isdir(dir_for_icons):
                from shutil import rmtree
                rmtree(dir_for_icons, ignore_errors = True)
            
            # Создание временной папки для иконок
            from random import random
            dir_for_icons += f'/dir_for_icons{random()}'
            mkdir(dir_for_icons)
            s.dir_for_icons = dir_for_icons
    
    def onChangeImgPath(s):
        # Обработчик изменениия пути к картинке
        isSuccess = False
        imgPath = s.imgPath_field.text()
        s.clear2ndStepFields()
        isCashed = s.lastSuccessOpenedImgPath == imgPath
        if not imgPath:
            text = ''
        elif os.path.isfile(imgPath):
            try:
                if isCashed:
                    # Если это старое изображение, восстанавливаем значения полей ввода
                    if s.isCalculated:
                        cellX = s.confirmedCellX
                        cellY = s.confirmedCellY
                    else:
                        cellX = s.cellX
                        cellY = s.cellY
                    s.blockEnteringData = True
                    s.cellX_field.setValue(cellX)
                    s.cellY_field.setValue(cellY)
                    s.blockEnteringData = False
                    s.onChangeCellXorCellY()
                else:
                    # Если это новое изображение, обработать его
                    from PIL import Image
                    img = Image.open(imgPath).convert('RGBA')
                    s.isCalculated = False
                    s.imgWidth = imgWidth = img.size[0]
                    s.imgHeight = imgHeight = img.size[1]
                    s.img = img
                    maxIconSize = min(imgWidth, imgHeight)
                    s.iconSize_field.setMaximum(maxIconSize)
                    s.iconSize_field.setValue(maxIconSize)
                    s.cellX_field.setMaximum(imgWidth)
                    s.cellY_field.setMaximum(imgHeight)
                    s.lastSuccessOpenedImgPath = imgPath
                isSuccess = True
                text = f'Изображение с разрешением {s.imgWidth} * {s.imgHeight} успешно открыто.'
            except ImportError:
                text = 'Библиотека PIL не найдена. Команда для установки: pip install pillow'
            except:
                text = 'Данное изображение не поддерживается. Выберите другое.'
        else:
            text = 'По заданному пути нет изображения.'
        s.aboutImgPath_label.setStyleSheet(f"color: #{'07' if isSuccess else '90'}0;")
        s.aboutImgPath_label.setText(text)
        s.isImgPathCorrect = isSuccess
        s.progressBar.setTextVisible(s.isCalculated and isCashed)
        s.textBrowser.setHtml(s.lastHTML if s.isCalculated and isCashed else s.baseHTML)
        s.progressBar.setValue(0)
        s.changeStateOf2ndStep(isSuccess)
        s.changeStateOf3rdStep()
    
    def onChangeDesktopPath(s):
        # Обработчик изменениия пути к рабочему столу
        isSuccess = False
        desktopPath = s.desktopPath_field.text()
        if not desktopPath:
            text = ''
        elif os.path.isdir(desktopPath) and (desktopPath[-8:] == '/Desktop' or desktopPath[-9:] == '/Desktop/'):
            isSuccess = True
            text = 'Папка успешно задана.'
            s.desktopPath = desktopPath
        else:
            text = 'Это не рабочий стол.'
        s.aboutDesktopPath_label.setStyleSheet(f"color: #{'07' if isSuccess else '90'}0;")
        s.aboutDesktopPath_label.setText(text)
        s.isDesktopPathCorrect = isSuccess
        s.changeStateOf3rdStep()
    
    def browseImgPath(s):
        # Диалоговое окно выбора пути к картинке
        fileName = QtWidgets.QFileDialog.getOpenFileName(s, 'Выберите картинку', filter='Images (*.bmp *.png *.jpeg *.jpg *.ico *.webp)')[0]
        if fileName:
            s.imgPath_field.setText(fileName)
    
    def browseDesktopPath(s):
        # Диалоговое окно выбора пути к рабочему столу
        directory = QtWidgets.QFileDialog.getExistingDirectory(s, 'Выберите папку Desktop')
        if directory:
            s.desktopPath_field.setText(directory)
    
    def onChangeIconSize(s):
        # Обработчик изменениия размера иконки
        if not s.blockEnteringData:
            s.blockEnteringData = True
            iconSize = s.iconSize_field.value()
            s.cellX = s.imgWidth // iconSize
            s.cellY = s.imgHeight // iconSize
            s.cellX_field.setValue(s.cellX)
            s.cellY_field.setValue(s.cellY)
            s.blockEnteringData = False
    
    def onChangeCellXorCellY(s):
        # Обработчик изменениия разрешения мозаики
        if not s.blockEnteringData:
            s.blockEnteringData = True
            s.cellX = cellX = s.cellX_field.value()
            s.cellY = cellY = s.cellY_field.value()
            s.iconSize_field.setValue(min(s.imgWidth // cellX, s.imgHeight // cellY))
            s.blockEnteringData = False
    
    def calculate(s):
        # Расчёт параметров мозаики и вывод их на экран
        s.blockEnteringData = True
        
        s.confirmedCellX = cellX = s.cellX_field.value()
        s.confirmedCellY = cellY = s.cellY_field.value()
        
        s.confirmedIconSize = iconSize = min(s.imgWidth // cellX, s.imgHeight // cellY)
        
        oldIconSize = s.iconSize_field.value()
        imgWidth = cellX * iconSize
        imgHeight = cellY * iconSize
        message = ''
        if iconSize != oldIconSize:
            message += f'''Установлен неоптимальный размер иконки.
            Он будет изменён с {oldIconSize} на {iconSize}, для наименьшей обрезки картинки.
            Размер мозаики при этом останется неизменным. '''
        allCells = str(cellX * cellY)
        ending = 'ки' if allCells[-1] == '1' and (allCells == '1' or allCells[-2] != '1') else 'ок'
        message += f'У вас получится мозайка, состоящая из {allCells} ({cellX}*{cellY}) пап{ending}, при размере иконки {iconSize}*{iconSize}. '
        if (imgWidth, imgHeight) != (s.imgWidth, s.imgHeight):
            percentX = f'{(1 - imgWidth / s.imgWidth) * 100:.1f}'
            percentY = f'{(1 - imgHeight/s.imgHeight) * 100:.1f}'
            percentX = '' if percentX == '0.0' else f'(-{percentX}%)'
            percentY = '' if percentY == '0.0' else f'(-{percentY}%)'
            message += f'Разрешение картинки станет {imgWidth} {percentX} в ширину и {imgHeight} {percentY} в высоту. '
        message = f'<html><head/><body><p style="font-size:10pt;font-family:\'Verdana\';">{message}</p></body></html>'
        s.textBrowser.setHtml(message)
        s.lastHTML = message
        s.isCalculated = True
        s.progressBar.setTextVisible(True)
        s.progressBar.setMaximum(int(allCells))
        s.progressBar.setValue(0)
        s.changeStateOf3rdStep()
        s.blockEnteringData = False
    
    def createPuzzle(s):
        # Создание мозаики
        s.changeStateOfAllFields(False)
##        s.imgPath_field.setEnabled(False)
        dir_for_icons = s.dir_for_icons
        img = s.img
        desktopPath = s.desktopPath
        iconSize = s.confirmedIconSize
        cellX = s.confirmedCellX
        cellY = s.confirmedCellY
        numNow = 0
        x = 0
        for numx in range(cellX):
            y = 0
            for numy in range(cellY):
                numNow += 1
                canvasDir = desktopPath + '/' + ' ' * numNow + '/'
                if not os.path.isdir(canvasDir):
                    mkdir(canvasDir)
                newImg = s.img.crop( (x, y, x + iconSize, y + iconSize) )
                s.progressBar.setValue(numNow)
                iconDir = f'{dir_for_icons}/x{numx + 1}_y{numy + 1}.ico'
                newImg.save(iconDir)
                
                seticon(canvasDir, iconDir,0)
                y += iconSize
            x += iconSize
        s.changeStateOfAllFields(True)
    
    def clearAllFields(s):
        # Очистка всех полей
        s.imgPath_field.setText('')
        s.desktopPath_field.setText('')
        s.clear2ndStepFields()
    
    def delPreviousPuzzle(s):
        pass
    
    def changeStateOf2ndStep(s, isUnlocked):
        # Блокировка или разблокировка полей 2-го этапа
        s.calculate_button.setEnabled(isUnlocked)
        s.iconSize_field.setEnabled(isUnlocked)
        s.cellX_field.setEnabled(isUnlocked)
        s.cellY_field.setEnabled(isUnlocked)
    
    def changeStateOf3rdStep(s):
        # Блокировка или разблокировка кнопки создания мозаики
        s.createPuzzle_button.setEnabled(s.isImgPathCorrect and s.isDesktopPathCorrect and s.isCalculated)
    
    def clear2ndStepFields(s):
        # Очистка полей 2-го этапа
        s.blockEnteringData = True
        s.iconSize_field.setValue(1)
        s.cellX_field.setValue(1)
        s.cellY_field.setValue(1)
        s.blockEnteringData = False
    
    def changeStateOfAllFields(s, isUnlocked):
        # Блокировка или разблокировка всех полей
        s.changeStateOf2ndStep(isUnlocked)
        s.imgPath_field.setEnabled(isUnlocked)
        s.selectImgPath_button.setEnabled(isUnlocked)
        s.desktopPath_field.setEnabled(isUnlocked)
        s.selectDesktopPath_button.setEnabled(isUnlocked)
    
#######################################################################

# Открытие окна
window = QtWidgets.QApplication([])
window.setStyle('Fusion')
app = ExampleApp()
app.show()
if os.name == 'nt':
    # Попытка установки папки рабочего стола по умолчанию
    try:
        env = dict(os.environ)
        directory = (env['HOMEDRIVE'] + env['HOMEPATH']).replace('\\' , '/') + '/Desktop'
    except:
        directory = 'C:/Users/User/Desktop'
    app.desktopPath_field.setText(directory)
window.exec_()
