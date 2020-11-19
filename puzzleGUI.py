#######################################################################
# Установка иконки на папку
import os
isWindows = os.name == 'nt'
if isWindows:
    try:
        from seticon import seticon
    except ImportError:
        print('Отсутствует обязательный файл seticon.py')
        print('Этот файл содержит код для добавления папкам иконок')
        input('Нажмите Enter для завершения\n')
        exit()

try:
    from PyQt5 import QtWidgets
except ImportError:
    print('Библиотека PyQt5 не найдена. Вы можете её установить следующей коммандой в консоли с правами администратора: ')
    print('pip install pyqt5')
    input('Нажмите Enter для завершения\n')
    exit()

try:
    from design import Ui_MainWindow
except ImportError:
    print('Отсутствует обязательный файл design.py')
    print('Этот файл содержит весь дизайн окна приложения')
    input('Нажмите Enter для завершения\n')
    exit()

try:
    from PIL import Image
except ImportError:
    print('Библиотека PIL не найдена. Вы можете её установить следующей коммандой в консоли с правами администратора: ')
    print('pip install pillow')
    input('Нажмите Enter для завершения\n')
    exit()

#######################################################################

def mkdir(path):
    # Обёртка над функцией создания папки
    try:
        os.makedirs(path)
    except OSError:
        print('Создать директорию %s не удалось' % path)

#######################################################################

##Твои рабочие элементы:

##imgPath_field                 Поле ввода пути к картинке
##selectImgPath_button          Кнопка вызова окна выбора пути к картинке
##desktopPath_field             Поле ввода пути к рабочему столу пользователя
##selectDesktopPath_button      Кнопка вызова окна выбора пути к рабочему столу пользователя
##iconSize_field                Поле ввода какой ширины и высоты будет каждая иконка
##cellX_field                   Поле ввода ширины мозаики
##cellY_field                   Поле ввода высоты мозаики
##calculate_button              Кнопка расчёта всех параметров мозаики
##createPuzzle_button           Кнопка создания мозаики
##clearParams_button            Кнопка очистки всех полей ввода
##aboutDesktopPath_label        Текстовое поле с информацией о возможных ошибках при выборе пути к рабочему столу пользователя
##aboutImgPath_label            Текстовое поле с информацией о возможных ошибках при выборе пути к картинке
##delPrevPuzzle_button          Кнопка удаления предыдущей мозаики
##progressBar                   Прогресс бар создания мозаики
##textBrowser                   Текстовое поле со всеми параметрами мозаики

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        '''
        Класс, содержащий всю логику окна приложения.
        '''
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

                seticon(canvasDir, iconDir, 0)
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
app = QtWidgets.QApplication([])
app.setStyle('Fusion')
window = MainWindow()
window.show()
if isWindows:
    # Попытка установки папки рабочего стола по умолчанию
    try:
        env = dict(os.environ)
        directory = (env['HOMEDRIVE'] + env['HOMEPATH']).replace('\\' , '/') + '/Desktop'
    except NameError:
        directory = 'C:/Users/User/Desktop'
    window.desktopPath_field.setText(directory)
app.exec_()
