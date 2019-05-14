from sqlalchemy import create_engine, Column, Integer, String, Boolean, ForeignKey, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, relationship
from crontab.get_positions import log_time
import os
import random
import string
from config import bd_path




#Соединяемся с БД
engine = create_engine(bd_path)

#Определяем БД
DataBase = declarative_base()

class Project(DataBase):
    __tablename__ = 'projects'

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    name = Column(String, nullable=False, unique=True)
    domain = Column(String, nullable=False)
    phrases = relationship("Phrase", backref='proj')

    def __init__(self, name, domain):
        self.name = name
        self.domain = domain


class Phrase(DataBase):
    __tablename__ = 'phrases'

    query_id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    query_text = Column(String, nullable=False)
    project = Column(Integer, ForeignKey('projects.id'), nullable=False)
    city = Column(Integer, nullable=False)
    enable = Column(Boolean, nullable=False, default=True)
    positions = relationship("Position", backref='keyword')


    def __init__(self, query_text, project, city):
        self.query_text = query_text
        self.project = project
        self.city = city


class Position(DataBase):
    __tablename__ = 'positions'

    id = Column(Integer, autoincrement=True, primary_key=True, nullable=False)
    query = Column(Integer, ForeignKey('phrases.query_id'))
    date = Column(Date, nullable=False)
    pos = Column(Integer, nullable=True)
    rel_page = Column(String, nullable=True)

    def __init__(self, query, date, pos, rel_page):
        self.query = query
        self.date = date
        self.pos = pos
        self.rel_page = rel_page


class DailyList(DataBase):
    __tablename__ = 'dailylist'

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    phrase_id = Column(Integer, nullable=False)


    def __init__(self, phrase_id):
        self.phrase_id = phrase_id

class User(DataBase):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    login = Column(String(30), nullable=False, unique=True)
    password = Column(String(50), nullable=False, unique=True)
    login_key = Column(String(255), nullable=False, unique=True)

    def keygen(self):
        symbols = string.ascii_letters + string.digits
        key = ''.join(random.choices(symbols, k=255))
        return key

    def __init__(self, login, password):
        self.login = login
        self.password = password
        self.login_key = self.keygen()


DataBase.metadata.create_all(engine)

def add_project(name, domain, queries, city_id):

    session = Session(bind=engine)
    new_project = Project(name=name, domain=domain)
    session.add(new_project)
    session.commit()

    added_phrases = queries

    for phrase in added_phrases:
        q = Phrase(query_text=phrase, project=new_project.id, city=city_id)
        session.add(q)

    session.commit()
    session.close()

def get_project_list():

    session = Session(bind=engine)
    project_query = session.query(Project).all()

    project_list = []
    for proj in project_query:
        count = get_phrases_count(proj.id)
        project_list.append({'id': proj.id, 'name': proj.name, 'domain': proj.domain, 'phrase_count': count})

    session.close()
    return project_list

def get_project_by_id(id):
    session = Session(bind=engine)
    project_data = session.query(Project).filter(Project.id == id).first()
    project_queries_in_list = session.query(Phrase).filter(Phrase.project == id, Phrase.enable == True).all()

    project_queries = ''
    for q in project_queries_in_list:
        project_queries = str(project_queries) + str(q.query_text) + '\n'


    project_info = {
        'id': project_data.id,
        'name': project_data.name,
        'domain': project_data.domain,
        'queries': project_queries}
    session.close()
    return project_info



def is_project_id_in_base(id):
    session = Session(bind=engine)

    if session.query(Project).filter(Project.id == id).count() > 0:
        r = True
    else:
        r = False
    session.close()
    return r


def get_phrases_count(proj_id):
    session = Session(bind=engine)
    phrases_count = session.query(Phrase).filter(Phrase.project == proj_id).count()
    session.close()

    return phrases_count


def update_project_info(id, name, queries, city_id):
    session = Session(bind=engine)
    session.query(Project).filter(Project.id == id).update({'name': name})
    session.commit()


    #Получаем список всех включенных фраз проекта из базы
    current_queries_selection = session.query(Phrase).filter(Phrase.project == id, Phrase.enable == True).all()


    #Получаем список всех отключенных фраз проекта из базы
    disabled_queries_selection = session.query(Phrase).filter(Phrase.project == id, Phrase.enable == False).all()

    #Создаем из выборки список текущих
    current_queries = []
    for ph in current_queries_selection:
        current_queries.append(ph.query_text)

    #Создаем из выборки список отключенных
    disabled_queries = []
    for ph in disabled_queries_selection:
        disabled_queries.append(ph.query_text)



    #Получаем список запросов, которые надо отключить (есть в базе, но нет в форме)
    phrase_to_disable = set(current_queries).difference(queries)
    for ph in phrase_to_disable:
        session.query(Phrase).filter(Phrase.query_text == ph).update({'enable': False})
        session.commit()

    #Получаем список запросов, которые надо включить (есть в форме, но отключены в базе)
    phrase_to_enable = set(queries).intersection(disabled_queries)
    for ph in phrase_to_enable:
        session.query(Phrase).filter(Phrase.query_text == ph).update({'enable': True})
        session.commit()

    #Получаем список запросов, которые надо добавить (есть в форме, но нет в базе)
    phrase_to_add = set(queries).difference(disabled_queries+current_queries)
    for ph in phrase_to_add:
        q = Phrase(query_text=ph, project=id, city=city_id)
        session.add(q)
        session.commit()





def delete_project_by_id(id):
    session = Session(bind=engine)
    session.query(Project).filter(Project.id == id).delete()
    session.query(Phrase).filter(Phrase.project == id).delete()
    session.commit()
    session.close()


def add_position(query_id, date, position, rel_page):
    session = Session(bind=engine)
    pos = Position(query=query_id, date=date, pos=position, rel_page=rel_page)
    session.add(pos)
    session.commit()
    session.close()

def collect_daily_list():
    session = Session(bind=engine)

    #На всякий случай очищаем таблицу, если в ней что-то есть
    session.query(DailyList).delete()

    #Собираем список запросов, по которым сегодня нужно снимать позиции
    daily_list = session.query(Phrase).filter(Phrase.enable == True).all()


    #Пишем все id запросов на сегодня в базу
    for ph in daily_list:
        q = DailyList(phrase_id=ph.query_id)
        session.add(q)
        session.commit()


    with open('project/log.txt', 'a') as log:
        log.write('\n' + log_time() + ' Собран список фраз на день')

    session.close()

def get_one_today_phrase():
    session = Session(bind=engine)

    try:
        q = session.query(DailyList).first()
        q_id = q.phrase_id

    except:
        q_id = 'error'
        print(q_id)

    session.close()

    return q_id

def delete_phrase_after_get_pos(phrase_id):
    session = Session(bind=engine)
    session.query(DailyList).filter(DailyList.phrase_id == phrase_id).delete()
    session.commit()
    session.close()

def get_phrase_by_id(id):
    session = Session(bind=engine)
    q = session.query(Phrase).filter(Phrase.query_id == id).first()
    q_prop = {'id': q.query_id, 'text': q.query_text, 'domain': q.proj.domain, 'city': q.city}
    session.close()
    return q_prop

def get_all_project_positions_by_id(project_id, start_date, finish_date):
    import pandas
    session = Session(bind=engine)

    #Получаем записи всех существующих позиций для каждой фразы
    all_proj_positions = session.query(Position).filter(Position.date.between(start_date, finish_date)).filter(Position.keyword.has(Phrase.proj.has(Project.id == project_id))).all()
    all_proj_positions_dict = [{'phrase': p.keyword.query_text, 'date': str(p.date), 'position': p.pos, 'rel': p.rel_page} for p in all_proj_positions]

    #Создаем датафрейм pandas
    df = pandas.DataFrame(all_proj_positions_dict)

    #Создаем сводную таблицу релевантных страниц по датам
    rel_pivot = df.pivot(index='phrase', columns='date', values ='rel')

    #Создаем сводную таблицу позиций по датам
    pos_pivot = df.pivot(index='phrase', columns='date', values='position')

    #Добавляем колонку с последними релевантными страницами как столбец в сводную таблицу позиций
    pos_pivot = pos_pivot.assign(rel_page = pandas.Series(rel_pivot[rel_pivot.columns[-1]]))

    #Меняем местами столбцы (релевантную страницу вперед)
    cols_range = list(pos_pivot.columns)
    new_cols_range = [cols_range[-1]]
    for col in range(0, len(cols_range) - 1):
        new_cols_range.append(cols_range[col])
    pos_pivot = pos_pivot[new_cols_range]
    #Формируем имя файла
    file_name = 'positions_id'+project_id+'_'+start_date+'_'+finish_date +'.csv'

    #Экспортируем csv
    pos_pivot.to_csv(os.path.dirname(__file__)+'/../static/export/'+file_name, ';', encoding='windows-1251')

    session.close()
    return file_name

def get_users():
    session = Session(bind=engine)
    users = session.query(User).all()
    users_dict = [{'id': user.id, 'login': user.login, 'password': user.password, 'login_key': user.login_key } for user in users]

    return users_dict

def get_password_by_login(login):
    session = Session(bind=engine)
    true_password = session.query(User).filter(User.login == login).first().password

    return true_password

def get_login_key_by_login(login):
    session = Session(bind=engine)
    login_key = session.query(User).filter(User.login == login).first().login_key

    return login_key

def get_login_by_login_key(login_key):
    session = Session(bind=engine)
    login = session.query(User).filter(User.login_key == login_key).first().login

    return login

if __name__ == '__main__':
    pass


