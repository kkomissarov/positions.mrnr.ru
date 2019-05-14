import requests
import re
import datetime
import time
import config

def log_time():
    date = str(datetime.datetime.now().date())
    hour = str(datetime.datetime.now().hour)
    min = str(datetime.datetime.now().minute)
    return date + ' ' + hour + ':' + min


def get_position():
    from model.project import get_one_today_phrase, get_phrase_by_id, delete_phrase_after_get_pos, add_position
    #Получить xml c результатами
    def get_xml(query, city):

        req_result = requests.get(config.main_link, params={
            'user': config.user,
            'key': config.api_key,
            'query': query,
            'lr': city,
            'l10n': config.lang,
            'sortby':  config.sortby,
            'filter': config.add_filt,
            'groupby': config.group,
            'page': config.page
        })

        xml = req_result.text
        return xml

    def parse_rel_pages(xml):
        rel_pages = re.findall(r'<url>(.*?)</url>', xml)
        return rel_pages

    def parse_domains(xml):
        domains = re.findall(r'<domain>(.*?)</domain>', xml)
        return domains


    def get_position(site, domains):
        pos = 101

        for domain in domains:
            if domain[-len(site):] == site:
                pos = domains.index(domain) + 1
                break


        return pos

    def validate_xml(xml):
        if '<error' in xml:
            err = 'Ошибка в XML'
        else:
            err = False

        return err


    with open('project/log.txt', 'a') as log:
        log.write('\n' + log_time() + ' Запущен сбор позиций')

    work_status = True
    while work_status == True and int(datetime.datetime.now().minute) < 50:

        #Берем id первой фразы из списка фраз на сегодя
        current_query_id = get_one_today_phrase()

        #Если в базе что-то есть, пытаемся снять позиции
        if current_query_id != 'error':

            #Получаем словарь с информацией о запросе
            current_query = get_phrase_by_id(current_query_id)

            #Получаем xml c позициями  и смотрим, что он не содержит сообщение об ошибке
            yandex_xml = get_xml(current_query['text'], current_query['city'])
            xml_error = validate_xml(yandex_xml)

            #Если ошибки в xml нет - продолжаем
            if xml_error == False:

                #Парсим все домены
                domains = parse_domains(yandex_xml)

                #Определяем позицию нашего сайта
                pos = get_position(current_query['domain'], domains)

                #Парсим релевантные страницы и берем нашу
                rel_pages = parse_rel_pages(yandex_xml)
                if pos < 101:
                    rel_page = rel_pages[pos-1]
                else:
                    rel_page = '-'


                #Пишем результат в базу
                add_position(current_query_id, datetime.datetime.today(), pos, rel_page)

                #Удаляем собраную фразу из базы
                delete_phrase_after_get_pos(current_query['id'])

                #ждем
                time.sleep(2)

            #Если есть ошибка в xml, печатаем сообщение и останавливаем процесс
            else:
                with open('project/log.txt', 'a') as log:
                    log.write('\n'+log_time()+ xml_error)

                #Прекратить выполнение скрипта
                work_status = False




        #Если id запроса получить не удалось (база пустая), то прерываем скрипт
        else:
            with open('project/log.txt', 'a') as log:
                log.write('\n'+log_time()+' Запросы на сегодня закончились')

            #Прекратить выполнение скрипта
            work_status = False


    with open('project/log.txt', 'a') as log:
        log.write('\n'+log_time()+' Сбор позиций прерван')



