# -*- coding: utf-8 -*-
DEFAULT_IMG_NAME = 'test.jpg'

import os
isWindows = os.name == 'nt'

if not isWindows:
    print('К сожалению, скрипт можно запустить только на Windows.')
    input('Нажмите Enter для завершения\n')
    exit()

from random import random

from shutil import rmtree

try:
    from seticon import seticon
except ImportError:
    print('Отсутствует обязательный файл seticon.py')
    print('Этот файл содержит код для добавления папкам иконок')
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

def moddedInput(prompt):
    print(prompt)
    return input('>>> ')

#######################################################################

def mkdir(path, alert=True):
    # Обёртка над функцией создания папки
    try:
        os.makedirs(path)
    except OSError:
        print(f'Создать директорию {path} не удалось')
        input('Завершите программу, иначе дальнейшая корректная работа не будет гарантирована\n')
    else:
        if alert:
            print(f'Успешно создана директория {path} \n')

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

def createConvertedListOfPrimeFactors(number):
    '''
    Разбиваем на все простые множители и попутно преобразуем для следующего этапа.
    Выход имеет вид [[1,2,4,8],[1,3],[1,7,49]].
    '''
    num = number # Ищем все простые множители этого числа
    powersOfPrimeNumbers = [] # Список рядов степеней простых чисел
    if num % 2 == 0: # Если 2 делитель, формируем начало и работаем по двойке
        powersOfPrimeNumbers = [ [ 1, 2 ] ]
        num //= 2
        lastMultInLastRow = 2 # Последний множитель в ряду (2, 4, 8 и т д)
        while num % 2 == 0: # Если ещё есть 2ки, то их тоже добавляем
            lastMultInLastRow *= 2
            powersOfPrimeNumbers[ 0 ].append( lastMultInLastRow ) # Наполняем наполняем список в powersOfPrimeNumbers новыми множителями
            num //= 2
    d = 3 # Тестируемый простой множитель (цикл начинающийся с 3 ускоряет поиск простых в 2 раза)
    while d * d <= num:
        if num % d == 0:
            powersOfPrimeNumbers.append( [ 1, d ] ) # Обьявляем новый ряд
            lastMultInLastRow = d
            num //= d
            break
        else:
            d += 2
    while d * d <= num:
        # Перебираем все возможные простые числа
        if num % d == 0:
            if d == powersOfPrimeNumbers[ -1 ][ 1 ]: # Если тестируемый множитель принадлежит текущему ряду
                lastMultInLastRow *= d
                powersOfPrimeNumbers[ -1 ].append( lastMultInLastRow )
            else:
                powersOfPrimeNumbers.append( [ 1, d ] ) # Обьявляем новый ряд
                lastMultInLastRow = d
            num //= d
        else:
            d += 2
    if num > 1: # Если есть остатки
        if (len(powersOfPrimeNumbers)) and ( num == powersOfPrimeNumbers[ -1 ][ 1 ] ):
            powersOfPrimeNumbers[ -1 ].append( num * lastMultInLastRow )
        else:
            powersOfPrimeNumbers.append( [ 1, num ] )
    return powersOfPrimeNumbers # имеет вид [[1,2,4,8],[1,3],[1,7,49]]

def createListOfAllMultipliers(number):
    # Находим список всех делителей числа
    arr = createConvertedListOfPrimeFactors( number )
    nextarr = arr[ 0 ]
    for arrnow in arr[ 1 : ]:
        nextarr = [ k * j for j in nextarr for k in arrnow ]
    nextarr.sort()
    return nextarr

#######################################################################

dir_for_icons = 'C:\\PleaseDontDeleteMe\\'

# Чистка предыдущих временных файлов
if os.path.isdir(dir_for_icons):
    print('Обнаружены временные файлы с предыдущих запусков. Очистка...\n')
    rmtree(dir_for_icons, ignore_errors = True)

# Создание временной папки для иконок
dir_for_icons += f'dir_for_icons{random()}\\'
mkdir(dir_for_icons)

# Ввод, проверка имени, открытие исходной картинки
isExists = False
while not isExists:
    imgName = moddedInput('Введите имя файла картинки, которая лежит в одной папке с программой:')
    if imgName and os.path.isfile(imgName):
        print('Файл найден.')
    elif not imgName and os.path.isfile(DEFAULT_IMG_NAME):
        print(f'По заданному пути файл не найден, кроме заданного по умолчанию: {DEFAULT_IMG_NAME}\n')
        imgName = DEFAULT_IMG_NAME
    else:
        print('Файл с картинкой по указанному пути не найден! Попробуйте снова...\n')
        continue

    try:
        img = Image.open(imgName).convert('RGBA')
    except:
        print(f'Файл {imgName} скорее всего не является картинкой. Попробуйте другую картинку.\n')
    else:
        imgWidth = img.size[0]
        imgHeight = img.size[1]
        print(f'Картинка с разрешением {imgWidth} * {imgHeight} успешно открыта.\n')
        isExists = True

# Обнаружение рабочего стола пользователя
try:
    env = dict(os.environ)
    deskPath = f"{env['HOMEDRIVE'] + env['HOMEPATH']}\\Desktop\\"
except NameError:
    user = moddedInput('Введите имя вашего пользователя: ')
    deskPath = f'C:\\Users\\{user}\\Desktop\\'
    if not user and os.path.isdir(deskPath):
        deskPath = 'C:\\Users\\User\\Desktop\\'

# Создание списка доступных разрешний мозаик
listOfAllMultipliers = createListOfAllMultipliers(NOD(imgWidth,imgHeight))
listOfAllMultipliers.sort()
stringForChoose = ', '.join(map(str,listOfAllMultipliers))

# Выбор размера мозайки
mode = moddedInput('''Выберете режим ввода:
Вы задаёте разрешение иконки в пикселях[1](по умолчанию)
Вы задаёте разрешение мозаики в ячейках[2]''')

if not mode in ['1','2']:
    print('Вы ввели недопустимое значение! Будет установлен режим по умолчанию: 1')
    mode = '1'

if mode == '1':
    print('Список разрешений иконок, при которых исходная картинка не обрежется:')
    print('\n', stringForChoose, '\n')
    maxStep = min(imgWidth, imgHeight)

oldImgWidth = imgWidth
oldImgHeight = imgHeight

changeChoice = True
while changeChoice:
    if mode == '1':
        step = int(moddedInput('Введите свой размер иконки либо из предложенного выше списка:'))
        if step < 1 or step > maxStep:
            print('Вы ввели недопустимые значения!')
            continue
        cellX = imgWidth // step
        cellY = imgHeight // step
    else:
        cellX = int(moddedInput('Введите ширину в ячейках:'))
        cellY = int(moddedInput('Введите высоту в ячейках:'))
        if cellX < 1 or cellX > imgWidth or cellY < 1 or cellY > imgHeight:
            print('Вы ввели недопустимые значения!')
            continue
        step = min(imgWidth // cellX, imgHeight // cellY)
    allCells = cellX * cellY
    print(f'У вас получится мозайка состоящая из {allCells} ячеек: {cellX} в ширину и {cellY} в высоту, при размере иконки {step}')
    imgWidth = cellX * step
    imgHeight = cellY * step
    (imgWidth, imgHeight) != (oldImgWidth, oldImgHeight) and print(f'Картинка обрежется до: {imgWidth} в ширину и {imgHeight} в высоту')

    if moddedInput('Изменить выбор? [д\\Н]') in ['да','ДА','Да','Д','д','Yes','yes','YES','Y','y','l','L']:
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

moddedInput('Нажмите Enter для завершения')
