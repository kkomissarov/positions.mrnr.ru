# -*- coding: utf-8 -*-
import re

#Форма добавления нового проекта
class AddProjectForm(object):
    def __init__(self, name, domain, queries):
        self.name = name
        self.domain = domain
        self.queries = queries

    #Валидация всех полей формы
    def validate(self):

        #Валидация поля name
        name_validate_status = True
        name_error_message = ''

        #Проверка длины
        if len(self.name) == 0:
            name_validate_status = False
            name_error_message = 'Название проекта на может быть пустым'



        elif len(self.name) < 3:
            name_validate_status = False
            name_error_message = 'Название не может быть короче 3х символов'

        elif len(self.name) > 40:
            name_validate_status = False
            name_error_message = 'Название не может быть длиннее 40 символов'

        #Проверка имени на запрещенные символы
        name_forbiden_simbols = re.search(r'[<>/^?;$@~=%#\']', self.name)
        if name_forbiden_simbols:
                name_validate_status = False
                name_error_message = 'Название проекта содержит запрещенные символы'


        #Валидация домена
        domain_validate_status = True
        domain_error_message = ''

        if len(self.domain) < 5:
            domain_validate_status = False
            domain_error_message = 'Слишком короткий домен'

        elif len(self.domain) > 40:
            domain_validate_status = False
            domain_error_message = 'Слишком длинный домен'

        #Проверка, что значение похоже на домен
        is_domain = re.search(r'^.*[.].*', self.domain)
        if is_domain==None :
            domain_validate_status = False
            domain_error_message = 'Введенное значение - не домен'

        #Проверка домена на запрещенные символы
        domain_forbidden_simbols = re.search(r'[<>&?;$@~=%#"()]', self.domain)
        if domain_forbidden_simbols!=None :
            domain_validate_status = False
            domain_error_message = 'Домен содержит недопустимые символы'

        if len(self.domain) == 0:
            domain_validate_status = False
            domain_error_message = 'Домен не может быть пустым'


        #Валидация поля запросов
        queries_validate_status = True
        queries_error_message = ''

        #Проверка на пустое поле запросов
        if len(self.queries) == 0:
            queries_validate_status = False
            queries_error_message = 'Проект должен содержать хотя бы один запрос'

        #Проверка запросов на запрещенные символы
        queries_forbidden_simbols = re.search(r'[<>&?;$@~=%#"()\-.!\']', self.queries)
        if queries_forbidden_simbols!=None :
            queries_validate_status = False
            queries_error_message = 'Запросы содержат недопустимые символы'




        #Вердикт валидации

        if name_validate_status==True and domain_validate_status==True and queries_validate_status==True:
            form_validate_status=True

        else:
            form_validate_status=False

        validate_result = {
            'name validate status': name_validate_status,
            'name error message':  name_error_message,
            'domain validate status': domain_validate_status,
            'domain error message': domain_error_message,
            'queries validate status': queries_validate_status,
            'queries error message': queries_error_message,
            'form validate status': form_validate_status,

        }

        return validate_result

    #Приведение содержимого полей к общему стандарту
    def to_fix_values(self):

        #Улучшайзеры названия
        self.name = self.name.lstrip()
        self.name = self.name.rstrip()


        #Улучшайзеры домена
        self.domain = self.domain.lstrip()
        self.domain = self.domain.rstrip()

        self.domain = str.lower(self.domain)

        if 'https://' in self.domain:
            self.domain = self.domain.replace('https://', '')

        elif 'http://' in self.domain:
            self.domain = self.domain.replace('http://', '')

        if self.domain[0:4] == 'www.':
            self.domain = self.domain[4:]

        #делаем массив из строки с запросами
        phrases = self.queries.split('\n')

        #в каждом запросе приводим все в нижний регистр и удаляем пробелы в начале и в конце
        valid_phrases = []
        for phrase in phrases:
            phrase = phrase.lstrip()
            phrase = phrase.rstrip()
            phrase = str.lower(phrase)
            if phrase:
                valid_phrases.append(phrase)

        #схлопываем дубли, если они есть
        uniq_valid_phrases = []
        for ph in valid_phrases:
            if ph not in uniq_valid_phrases:
                uniq_valid_phrases.append(ph)

        #перезаписываем строку с запросами как получившийся массив
        self.queries = uniq_valid_phrases




