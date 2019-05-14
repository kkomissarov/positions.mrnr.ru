# -*- coding: utf-8 -*-
import sys, os
sys.path.append('/home/k/kvognc/positions.mrnr.ru/project') # указываем директорию с проектом
sys.path.append('/home/k/kvognc/.local/Python-3.7.0/virtualenv/positions.mrnr.ru/lib/python3.7/site-packages') # указываем директорию с библиотеками, куда поставили Flask
from project import app as application # когда Flask стартует, он ищет application. Если не указать 'as application', сайт не заработает
from werkzeug.debug import DebuggedApplication # Опционально: подключение модуля отладки
application.wsgi_app = DebuggedApplication(application.wsgi_app, True) # Опционально: включение модуля отадки
application.debug = True  # Опционально: True/False устанавливается по необходимости в отладке