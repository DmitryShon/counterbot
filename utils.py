import requests
from datetime import datetime



async def check_acc_valid(acc_id):
    url = f'https://api.nearblocks.io/v1/account/{acc_id}'
    if len(requests.get(url).text) < 17:
        return False
    return True

def check_section(reward,coef1 = 1.1, coef2 = 1.5):
    if (0.1*coef1 <= reward <= 0.3*coef2):
        return 'Sunshine'
    if (0.5*coef1 <= reward <= 0.5*coef2):
        return 'Boardgames'
    if (0.7*coef1 <= reward <= 1*coef2):
        return 'Nightsky'
    return 'Unknown'

def form(cnt):
    if cnt < 21:
        if cnt == 1:
            return 'таска'
        elif 2 <= cnt <=4:
            return 'таски'
        else:
            return 'тасок'
    else:
        if str(cnt)[-1] == '1':
            return 'таска'
        elif str(cnt)[-1] =='2' or str(cnt)[-1] =='3' or str(cnt)[-1] =='4':
            return 'таски'
        else:
            return 'тасок'



async def beautiful_output(user):
    result = user.fill_result()
    output = f'Отчет по аккаунту: <b>{user.account}</b> \n\nСделано тасок на \n'
    total = 0
    n_total = 0
    for i in result['tasks']:
        task_cnt = len(result['tasks'][i])
        if task_cnt:
            output += f'<b>{i}</b>: {sorted(result["tasks"][i])}| {len(result["tasks"][i])} {form(task_cnt)} | Тотал: <b>{round(sum(result["tasks"][i]), 2)}</b>Ⓝ \n'
        total += sum(result['tasks'][i])
    output += '\nСделано ревью на\n'
    for i in result['reviews']:
        temp_sl = {}
        if len(result['reviews'][i]) != 0:
            output += f'<b>{i}</b>: '
            set_list = list(set(result["reviews"][i]))
            for j in range(len(set_list)):
                temp_sl[set_list[j]] = result["reviews"][i].count(set_list[j])
            output += f'{temp_sl} '
            output += f'| {len(result["reviews"][i])} ревью | Тотал: <b>{round(sum(result["reviews"][i]), 2)}</b>Ⓝ\n'
        total += sum(result['reviews'][i])
    n_total += (sum(result['reviews']['Nightsky']) + sum(result['tasks']['Nightsky']))
    output +=f'\nОбщий тотал : <b>{round(total, 2)}</b> Ⓝ | NightSky Тотал: <b>{round(n_total, 2)}</b> Ⓝ\n\n'
    output += f'Работа была проделана с <em>{datetime.utcfromtimestamp(user.time).strftime("%d.%m.%Y %H:%M")}</em>'

    return output
