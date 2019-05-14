from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from config import bd_path
from model.project import Phrase, Position
from datetime import datetime, timedelta
from controller.dates import decode_date

#Соединяемся с БД
engine = create_engine(bd_path)

def get_top10(project_id, days_count):
    session = Session(bind=engine)

    #Количество активных запросов у данного проекта на текущий момент
    phrases_in_project_count = session.query(Phrase).filter(Phrase.project == project_id).filter(Phrase.enable == 1).count()

    #Конечная дата - сегодня (если надо, можно сделать выбор в будущем)
    target_day = datetime.today().date() - timedelta(days=days_count-1)

    #Проценты в топе - пока пустой массив
    per_in_top_arr = []
    dates_arr = []

    #Прокручиваем этот цикл столько раз, сколько дней нам нужно показать
    for d in range(0, days_count):
        #Количество фраз проекта в топе за запрашиваемую дату
        phrases_in_top_count = session.query(Position).filter(Position.keyword.has(Phrase.project == project_id)).filter(Position.keyword.has(Phrase.enable == 1)).filter(Position.date == target_day).filter(Position.pos <= 10).count()

        #Расчитываем, сколько это будет в процентах от общего количества фраз проекта
        percent_in_top = round(phrases_in_top_count/phrases_in_project_count*100, 1)
        per_in_top_arr.append(percent_in_top)
        dates_arr.append(decode_date(str(target_day)))
        target_day += timedelta(days=1)

    data_frame = list(zip(dates_arr, per_in_top_arr))
    top_data = '["Дата", "% в ТОП-10"], '
    for elem in data_frame:
        data_el = str('["'+elem[0]) +'", '+ str(elem[1]) +'], '
        top_data += data_el

    session.close()

    return top_data


def get_average_position(project_id, days_count):
    session = Session(bind=engine)

    #Количество активных запросов у данного проекта на текущий момент
    phrases_in_project_count = session.query(Phrase).filter(Phrase.project == project_id).filter(Phrase.enable == 1).count()

    #Конечная дата - сегодня (если надо, можно сделать выбор в будущем)
    target_day = datetime.today().date() - timedelta(days=days_count-1)

    #Среднее значение - пока пустой массив
    average_positions_arr = []
    dates_arr = []

    #Прокручиваем этот цикл столько раз, сколько дней нам нужно показать
    for d in range(0, days_count):

        #Вытаскиваем все позиции за эту дату
        all_position_of_day = session.query(Position).filter(
            Position.keyword.has(Phrase.project == project_id)).filter(
            Position.keyword.has(Phrase.enable == 1)).filter(
            Position.date == target_day).all()

        #Расчитываем, сколько это будет в процентах от общего количества фраз проекта
        if all_position_of_day:
            average_position = round(sum([x.pos for x in all_position_of_day])/len(all_position_of_day), 1)
        else:
            average_position = 100

        average_positions_arr.append(average_position)
        dates_arr.append(decode_date(str(target_day)))
        target_day += timedelta(days=1)

    data_frame = list(zip(dates_arr, average_positions_arr))
    average_position_data = '["Дата", "Средняя позиция"], '
    for elem in data_frame:
        data_el = str('["'+elem[0]) +'", '+ str(elem[1]) +'], '
        average_position_data += data_el

    session.close()

    print(average_position_data)
    return average_position_data


if __name__ == '__main__':
    pass