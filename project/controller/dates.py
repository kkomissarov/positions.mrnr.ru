
def get_default_dates():
    from datetime import datetime, timedelta
    today = datetime.now().date()
    x_day_ago = today - timedelta(days=5)

    today_month = 'мес'
    if today.month == 1:
        today_month = 'янв'

    elif today.month == 2:
        today_month = 'фев'

    elif today.month == 3:
        today_month = 'мар'

    elif today.month == 4:
        today_month = 'апр'

    elif today.month == 5:
        today_month = 'май'

    elif today.month == 6:
        today_month = 'июн'

    elif today.month == 7:
        today_month = 'июл'

    elif today.month == 8:
        today_month = 'авг'

    elif today.month == 9:
        today_month = 'сен'

    elif today.month == 10:
        today_month = 'окт'

    elif today.month == 11:
        today_month = 'ноя'

    elif today.month == 12:
        today_month = 'дек'

    x_day_ago_month = 'мес'
    if x_day_ago.month == 1:
        x_day_ago_month = 'янв'

    elif x_day_ago.month == 2:
        x_day_ago_month = 'фев'

    elif x_day_ago.month == 3:
        x_day_ago_month = 'мар'

    elif x_day_ago.month == 4:
        x_day_ago_month = 'апр'

    elif x_day_ago.month == 5:
        x_day_ago_month = 'май'

    elif x_day_ago.month == 6:
        x_day_ago_month = 'июн'

    elif x_day_ago.month == 7:
        x_day_ago_month = 'июл'

    elif x_day_ago.month == 8:
        x_day_ago_month = 'авг'

    elif x_day_ago.month == 9:
        x_day_ago_month = 'сен'

    elif x_day_ago.month == 10:
        x_day_ago_month = 'окт'

    elif x_day_ago.month == 11:
        x_day_ago_month = 'ноя'

    elif x_day_ago.month == 12:
        x_day_ago_month = 'дек'

    finish_date = str(today.day) + ' ' + today_month + ' ' + str(today.year)
    start_date = str(x_day_ago.day) + ' ' + x_day_ago_month + ' ' + str(x_day_ago.year)

    return ({'start_date': start_date, 'finish_date': finish_date})


def decode_date(target_date):
    date_arr = target_date.split('-')
    month_list = ['янв', 'фев', 'мар', 'апр', 'май', 'июн', 'июл', 'авг', 'сен', 'окт', 'ноя', 'дек']

    month = month_list[int(date_arr[1]) - 1]

    decode_date = date_arr[2] + ' ' + month + ' ' + date_arr[0]

    return decode_date

def encode_date(target_date):
    date_in_list = target_date.split(' ')
    month_list = ['янв', 'фев', 'мар', 'апр', 'май', 'июн', 'июл', 'авг', 'сен', 'окт', 'ноя', 'дек']

    #Приводим дату к формату "01"
    day_num = date_in_list[0]
    if len(day_num) == 1:
        day_num = '0' + str(day_num)

    #Приводим месяц к формату "01"
    month_num = month_list.index(date_in_list[1])+1
    if month_num < 10:
        month_num = '0'+str(month_num)
    else:
        month_num = str(month_num)

    #Год
    year_num = date_in_list[2]

    result = year_num+'-'+month_num+'-'+day_num

    return result


if __name__ == '__main__':
    pass