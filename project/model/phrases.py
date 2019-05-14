def del_phrases():
    #Тестовый пример массива айдишников записей, которые прислал пользователь

    session = Session(bind=engine)

    for q in deleted_phrases:
        session.query(Phrase).filter_by(query_id=q).delete()

    session.commit()
    session.close()

def get_phrases():
    #Допустим хотим получить все фразы для проета с id 2
    proj = 2

    session = Session(bind=engine)

    proj_phrases = session.query(Phrase).filter_by(project=proj).all()

    for q in proj_phrases:
        #Пока печатаем их в консоль, а там будет видно
        print(q.query_text)

    session.close()

def upd_phrases():
    #Допустим, нужно поменять что-то в 2х фразах

    upd_ph = (
        {'id': 1, 'query': 'Подключить виртуальную АТС в СПб', 'project': 1, 'city': 2},
        {'id': 2, 'query': 'Купить пластиковые окна в СПб', 'project': 2, 'city': 2},
    )

    session = Session(bind=engine)

    for ph in upd_ph:
        session.query(Phrase).filter(Phrase.query_id == ph['id']).\
            update({Phrase.query_text: ph['query'], Phrase.project: ph['project'], Phrase.city: ph['city']}, synchronize_session=False)

    session.commit()


if __name__ == '__main__':
    add_phrases()


