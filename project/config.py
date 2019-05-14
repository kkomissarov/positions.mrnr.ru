

import os

#yandex xml settings
main_link = 'https://yandex.ru/search/xml'

#Эти два поля в реальности заполнены :) 
user = ''  
api_key = ''

lang = 'ru'
sortby = 'rlv'
add_filt = 'none'
group = 'attr="".mode=flat.groups-on-page=100.docs-in-group='
page = '0'

#database settings
bd_path = 'sqlite:///'+os.path.dirname(__file__)+'/database.db'