# -*- coding: utf-8 -*-
def create_success_message(arg):

    if arg == 'add':
        success_message = 'Проект успешно добавлен!'

    elif arg == 'edit':
        success_message = 'Проект успешно изменен!'

    elif arg == 'del':
        success_message = 'Проект успшно удален!'

    else:
        success_message = None

    return success_message