#######################################################################
# Декорирование функции input
oldinput = input
def input(prompt):
    print(prompt)
    return oldinput('>>> ')

#######################################################################

import os
import ctypes
from ctypes import POINTER, Structure, c_wchar, c_int, sizeof, byref
from ctypes.wintypes import BYTE, WORD, DWORD, LPWSTR, LPSTR
try:
    import win32api
except :
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

def NOD(A,B):
    # Находим наибольший общий делитель
    a,b = A,B
    while a != 0 and b != 0:
        if a > b:
            a %= b
        else:
            b %= a
    return a + b

def createListOfPrimeFactors(number):
    # Разбиваем на все простые множители
    num = number
    listOfPrimeFactors = []
    d = 2
    while d * d <= num:
        if num % d == 0:
            listOfPrimeFactors.append(d)
            num //= d
        else:
            d += 1
    if num > 1:
        listOfPrimeFactors.append(num)
    return listOfPrimeFactors

def createListOfAllMultipliers(inputNum):
    # Находим список всех делителей числа
    ls = createListOfPrimeFactors(inputNum)
    from collections import Counter
    kkk = dict(Counter(ls)).items()

    d, m = zip(*kkk)
    k = [0 for _ in range(len(set(ls)))]
    ln = range(len(m))
    arr = set()
    try:
        while True:
            r = 1
            for i1, i2 in zip(d, k):
                r *= i1 ** i2
            arr.add(r)
            k[0] += 1
            for i in ln:
                if k[i] > m[i]:
                    k[i] = 0
                    k[i+1] += 1  # IndexError
    except IndexError:
        pass
    arr = list(arr)
    arr.sort()
    return arr

#######################################################################

def mkdir(path, alert=True):
    # Обёртка над функцией создания папки
    try:
        os.makedirs(path)
    except OSError:
        print('Создать директорию %s не удалось' % path)
        oldinput('Завершите программу, иначе дальнейшая корректная работа не будет гарантирована\n')
    else:
        alert and print('Успешно создана директория %s \n' % path)

#######################################################################

# Подключение библиотеки pillow
try:
    from PIL import Image
except :
    print('Библиотека PIL не найдена. Вы можете её установить следующей коммандой в консоли с правами администратора: ')
    print('pip install pillow')
    input('Нажмите Enter для завершения\n')
    exit()

dir_for_icons = 'C:\\PleaseDontDeleteMe\\'

# Чистка предыдущих временных файлов
if os.path.isdir(dir_for_icons):
    print('Обнаружены временные файлы с предыдущих запусков. Очистка...\n')
    from shutil import rmtree
    rmtree(dir_for_icons, ignore_errors = True)

# Создание временной папки для иконок
from random import random
dir_for_icons += f'dir_for_icons{random()}\\'
mkdir(dir_for_icons)

# Ввод, проверка имени, открытие исходной картинки
isExists = False
while not isExists:
    imgName = input('Введите имя файла картинки, которая лежит в одной папке с программой:')
    if imgName and os.path.isfile(imgName):
        isExists = True
    elif os.path.isfile('input.jpg'):
        print('По заданному пути файл не найден, кроме заданного по умолчанию: input.jpg\n')
        isExists = True
        imgName = 'input.jpg'
    else:
        print('Файл с картинкой по указанному пути не найден! Попробуйте снова...\n')
    
    if isExists:
        try:
            img = Image.open(imgName).convert('RGBA')
        except:
            print(f'Файл {imgName} скорее всего не является картинкой. Попробуйте другую картинку.\n')
            isExists = False
        else:
            imgWidth = img.size[0]
            imgHeight = img.size[1]
            print(f'Картинка с разрешением {imgWidth} * {imgHeight} успешно открыта.\n')

# Обнаружение рабочего стола пользователя
try:
    env = dict(os.environ)
    deskPath = f"{env['HOMEDRIVE'] + env['HOMEPATH']}\\Desktop\\"
except:
    user = input('Введите имя вашего пользователя: ')
    deskPath = f'C:\\Users\\{user}\\Desktop\\'
    if not user and os.path.isdir(deskPath):
        deskPath = 'C:\\Users\\User\\Desktop\\'

# Создание списка доступных разрешний мозаик
listOfAllMultipliers = createListOfAllMultipliers(NOD(imgWidth,imgHeight))
listOfAllMultipliers.sort()
stringForChoose = ', '.join(map(str,listOfAllMultipliers))

# Выбор размера мозайки
mode = input('''Выберете режим ввода:
Вы задаёте разрешение иконки в пикселях[1](по умолчанию)
Вы задаёте разрешение мозаики в ячейках[2]''')

if not mode in ['1','2']:
    print('Вы ввели недопустимое значение! Будет установлен режим по умолчанию: 1')
    mode = '1'

if mode == '1':
    print('\n', stringForChoose, '\n')
    maxStep = min(imgWidth, imgHeight)

oldImgWidth = imgWidth
oldImgHeight = imgHeight

changeChoice = True
while changeChoice:
    try:
        if mode == '1':
            step = int(input('Введите размер иконки из предложенного выше списка:'))
            if step < 1 or step > maxStep:
                raise
            cellX = imgWidth // step
            cellY = imgHeight // step
        else:
            cellX = int(input('Введите ширину в ячейках:'))
            cellY = int(input('Введите высоту в ячейках:'))
            if cellX < 1 or cellX > imgWidth or cellY < 1 or cellY > imgHeight:
                raise
            step = min(imgWidth // cellX, imgHeight // cellY)
    except:
        print('Вы ввели недопустимые значения!')
        continue
    allCells = cellX * cellY
    print(f'У вас получится мозайка состоящая из {allCells} ячеек: {cellX} в ширину и {cellY} в высоту, при размере иконки {step}')
    imgWidth = cellX * step
    imgHeight = cellY * step
    (imgWidth, imgHeight) != (oldImgWidth, oldImgHeight) and print(f'Картинка обрежется до: {imgWidth} в ширину и {imgHeight} в высоту')
    
    if input('Изменить выбор? [д\Н]') in ['да','ДА','Да','Д','д','Yes','yes','YES','Y','y','l','L']:
        imgWidth = oldImgWidth
        imgHeight = oldImgHeight
        changeChoice = True
    else:
        changeChoice = False
print()

# Генерация папок, нарезка иконок, привязка иконок к папкам
imgWidth -= step - 1
imgHeight -= step - 1
numNow = 0

for numx, x in enumerate(range(0, imgWidth, step)):
    for numy, y in enumerate(range(0, imgHeight, step)):
        numNow += 1
        canvasDir = deskPath + ' ' * numNow + '\\'
        if os.path.isdir(canvasDir):
            print('Обнаружена ячейка с прошлой игры. Замена...')
        else:
            mkdir(canvasDir, False)
        
        print(f'Создаётся ячейка {numNow} из {allCells}.')
        
        newImg = img.crop( (x, y, x + step, y + step) )
        iconDir = f'{dir_for_icons}x{numx + 1}_y{numy + 1}.ico'
        newImg.save(iconDir)
        
        seticon(canvasDir, iconDir,0)

input('Нажмите Enter для завершения')
