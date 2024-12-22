import datetime

from carcass.config import imp_data


def generate_duty_chart(data, duties, tomorrow, assigned_to_bot, day_period):
    weekdays = tomorrow not in ('Sun', 'Sat')
    if weekdays:
        data = [el for el in data if day_period in el.workshifts]
    lenght = len(data)
    actions = {"KK bot": 2,
               "Na Prv bot": 3 if lenght >= 15 else 2,
               "Correct/KM": 4 if lenght >= 16 else 3,
               "KK Online": 3 if lenght >= 14 else 2,
               "Zapros KK": 2 if lenght >= 17 else 1,
               "Na Prv Online": 5}

    assigned = []
    if weekdays:
        necess_bot_kk = ["Sabrina", "Behruz", "Yosuman", "Nuqra", "Nazira", "Parviz", "Anushervon", "Abdurauf"]

        bot_kk = [empl for empl in data if empl.name in necess_bot_kk
                  and empl.name not in assigned_to_bot]

        employee = sorted(bot_kk, key=lambda x: x.skills.index('KK bot'))[0]
        assigned.append(employee.name)
        assigned_to_bot.append(employee.name)
        employee.skills.remove('KK bot')
        employee.skills.append('KK bot')
        duties[employee.name] = duties.get(employee.name, {})
        duties[employee.name][day_period] = 'KK bot'

    for pos, num in actions.items():
        if weekdays:
            avail_emps = (empl for empl in data if empl.name not in assigned
                          and pos in empl.skills)

        else:
            avail_emps = (empl for empl in data if empl.name not in assigned
                          and pos in empl.skills)

        prior_emps = sorted(avail_emps, key=lambda x: x.skills.index(pos))

        if 'bot' in pos and day_period == 'PM':
            prior_emps = [e for e in prior_emps if e.name not in assigned_to_bot][:num]
        else:
            prior_emps = prior_emps[:num]

        for employee in prior_emps:
            employee.skills.remove(pos)
            employee.skills.append(pos)
            assigned.append(employee.name)
            if day_period:
                duties[employee.name] = duties.get(employee.name, {})
                duties[employee.name][day_period] = pos
            else:
                duties[employee.name] = {'AM': pos, 'PM': pos}
            if 'bot' in pos and weekdays:
                assigned_to_bot.append(employee.name)


def start_process():
    duties = dict()
    data = imp_data()
    tomorrow = (datetime.date.today() + datetime.timedelta(days=1)).strftime("%a")
    if tomorrow not in ('Sun', 'Sat'):
        assigned_to_bot = []
        for day_period in ('AM', 'PM'):
            generate_duty_chart(data, duties, tomorrow, assigned_to_bot, day_period)
    else:
        generate_duty_chart(data, duties, tomorrow, [], [])

    return duties, data
