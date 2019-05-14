from flask import Flask, render_template, request, session, redirect
from model.project import get_login_by_login_key
import os
from controller.auth import check_auth, validate_password

app = Flask(__name__)
app.secret_key = os.urandom(21)

#Правила проверки авторизации
@app.before_request
def login_check():
    if request.path == '/collect' or request.path == '/get_positions':
        pass

    elif '/static' in request.path:
        pass

    elif request.path != '/login':
        if check_auth() == True:
            pass

        else:
            return redirect('/login')

    elif request.path == 'login':
        if check_auth() == True:
            return redirect('/')

        else:
            pass

@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    elif request.method == 'POST':
        login = request.form['login']
        password = request.form['pass']

        if validate_password(login, password) == True:
            return redirect('/')

        else:
            return render_template('login.html', error='Неправильный логин и/или пароль')

@app.route('/logout')
def logout():
    session['login_key'] = ''
    return redirect('/login')


@app.route('/')
def project_list():
    from model.project import get_project_list
    from model.messages import create_success_message

    projects = get_project_list()

    if 'success' in request.args:
        success = request.args['success']
        message = create_success_message(success)

    else:
        message = None

    return render_template('home.html',
                           projects=projects,
                           message = message,
                           page_title = 'Список проектов',
                           username = get_login_by_login_key(session['login_key']))


@app.route('/new-project', methods=['GET', 'POST'])
def new_project():
    if request.method == 'GET':
        return render_template('new-project.html',
            page_title = 'Добавить новый проект',
            username=get_login_by_login_key(session['login_key']))

    if request.method == "POST":
        from controller.form import AddProjectForm

        name = request.form['name']
        domain = request.form['domain']
        queries = request.form['queries']

        add_project_form = AddProjectForm(name=name, domain=domain, queries=queries)

        form_validation_info = add_project_form.validate()

        if form_validation_info['form validate status']==True:
            add_project_form.to_fix_values()

            from model.project import add_project
            add_project(add_project_form.name, add_project_form.domain, add_project_form.queries, 2)

            return redirect('/?success=add')

        else:
            return render_template('new-project.html',
                error=True,
                name_error=form_validation_info['name error message'],
                domain_error=form_validation_info['domain error message'],
                queries_error=form_validation_info['queries error message'],
                project_name=request.form['name'],
                project_domain=request.form['domain'],
                project_queries=request.form['queries'],
                username=get_login_by_login_key(session['login_key'])

            )


#Редактирование существующего проекта
@app.route('/edit-project', methods=['GET', 'POST'])
def edit_project():
    from model.project import is_project_id_in_base, get_project_by_id, update_project_info

    proj_id = request.args['id']
    project_info = get_project_by_id(proj_id)

    #Если такой айди есть в базе, возвращаем инфу о проекте
    if is_project_id_in_base(proj_id) == True:

        if request.method == 'GET':
            return render_template('edit-project.html',
             project_id = project_info['id'],
             project_name = project_info['name'],
             project_domain = project_info['domain'],
             project_queries = project_info['queries'],
             page_title = 'Редактировать проект ' + project_info['name'],
             username = get_login_by_login_key(session['login_key'])
            )

        elif request.method == 'POST':
            #Если метод post - получаем из формы содержимое полей и создаем из них питон-форму
            from controller.form import AddProjectForm
            name = request.form['name']
            domain = project_info['domain'] #Домен берем не из формы, т.к. поле домен отключено
            queries = request.form['queries']
            add_project_form = AddProjectForm(name=name, domain=domain, queries=queries)

            #Валидируем содержимое полей
            form_validation_info = add_project_form.validate()

            #Если валидацияпрошла успешно, проверяем поля на косяки и исправляем их
            if form_validation_info['form validate status'] == True:
                add_project_form.to_fix_values()


                update_project_info(proj_id, add_project_form.name, add_project_form.queries, 2)
                return redirect('/?success=edit')

            else:
                return render_template('edit-project.html',
                    error=True,
                    name_error = form_validation_info['name error message'],
                    domain_error = form_validation_info['domain error message'],
                    queries_error=form_validation_info['queries error message'],
                    project_name = project_info['name'],
                    project_domain = project_info['domain'],
                    project_queries = request.form['queries'],
                    page_title='Редактировать проект ' + project_info['name'],
                    username=get_login_by_login_key(session['login_key'])
                 )



    #Если айди в базе нет - возвращаем страницу 404
    else:
        return render_template('404.html', proj_id=proj_id), 404




@app.route('/del_project', methods=['GET'])
def del_project():
    from model.project import delete_project_by_id
    delete_project_by_id(request.args['id'])
    return redirect('/?success=del')


@app.route('/view', methods=['GET', 'POST'])
def view_project():
    from model.project import is_project_id_in_base, get_project_by_id, get_all_project_positions_by_id
    from controller.dates import get_default_dates, encode_date
    from model.visual import get_top10, get_average_position
    proj_id = request.args['id']

    if is_project_id_in_base(proj_id) == True and request.method == 'GET':
        project_info = get_project_by_id(proj_id)
        default_dates = get_default_dates()
        top_chart_data = get_top10(proj_id, 30)
        average_chart_data = get_average_position(proj_id, 30)

        return render_template('view.html',
            project_name = project_info['name'],
            project_id = project_info['id'],
            default_start_date = default_dates['start_date'],
            default_finish_date = default_dates['finish_date'],
            page_title = 'Позиции ' + project_info['name'],
            top_chart_data = top_chart_data,
            average_chart_data = average_chart_data,
            username=get_login_by_login_key(session['login_key']))

    elif is_project_id_in_base(proj_id) == True and request.method == 'POST':
        project_info = get_project_by_id(proj_id)
        top_chart_data = get_top10(proj_id, 30)
        average_chart_data = get_average_position(proj_id, 30)

        try:
            export_file = get_all_project_positions_by_id(proj_id, encode_date(request.form['s_date']), encode_date(request.form['f_date']))
            error = False

        except Exception as err:
            import traceback
            export_file = False
            error = traceback.format_exc()

        return render_template('view.html',
            project_name = project_info['name'],
            project_id = project_info['id'],
            default_start_date = request.form['s_date'],
            default_finish_date = request.form['f_date'],
            export_file = export_file,
            error = error,
            top_chart_data=top_chart_data,
            average_chart_data = average_chart_data,
            username=get_login_by_login_key(session['login_key']))

    else:
        return render_template('404.html', proj_id=proj_id), 404

@app.route('/collect', methods=['GET'])
def collecting_query_ip():
    if 'secret_key' in request.args:
        if request.args['secret_key'] == 'xCaBcZyXaBcZ':
            from model.project import collect_daily_list
            collect_daily_list()

            msg = 'Список для сбора позиций сформирован'
        else:
            msg = 'шел бы ты отсюда, петушок'
    else:
        msg = 'шел бы ты отсюда петушок'

    return msg

@app.route('/get_positions', methods=['GET'])
def getpos():
    if 'secret_key' in request.args:
        if request.args['secret_key'] == 'xCaBcZyXaBcZ':
            import crontab.get_positions as gp
            gp.get_position()
            msg = 'ок'
        else:
            msg = 'не ок'

    else:
        msg = 'не ок'
    return msg


@app.route('/log')
def log():
    with open(os.path.dirname(__file__)+'/log.txt', 'r', encoding='utf-8') as f:
        log = [logstring for logstring in f]


    return render_template('log.html', log=log)

if __name__ == '__main__':
    app.run(debug=True)