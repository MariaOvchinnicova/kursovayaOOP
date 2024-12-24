import requests
import datetime

class Shedule:

    def __init__(self):
        self.group = None
        self.week_day = datetime.datetime.today().weekday()
        self.next_week = False
        self.method = None
        self.parity_week = self.dict_parity_week[bool(datetime.datetime.today().isocalendar().week % 2)]

    def add_group(self, group):
        while(True):
            self.group = group
            payload = {'groupNumber': self.group}
            check = len(requests.get(self.url, params=payload).json())

            if check > 0:
                return 0
            
            else:
                print("Такой группы не существует!")
                self.group = input("Введите номер группы: ")
                return 1

    def check_week_day(self):
        if  self.week_day == 6: 
                self.week_day = 0
                self.parity_week = not self.parity_week
                self.next_week = True

    def print_schedule(self, lessons):
        print_data = ''

        for i in range(len(lessons) // 2):
            print_data += lessons['name'] + '\n'

            for j in lessons['lessons']:
                print_data += j['start_time'] + '-' + j['end_time'] + ' ' + j['room'] + ' ' + j['name'] + ' ' + j['teacher'] + '\n'
            
        return print_data

    def get_schedule(self, method, week_day = None):

        match self.dict_method[method]:

            case 0:
                    next_day = False

                    while(True):

                        self.check_week_day()
                        payload = {'groupNumber': self.group, 'week' : self.parity_week, "weekDay": self.dict_day_week[self.week_day]}

                        lessons = requests.get(self.url, params=payload).json()
                        lessons = lessons[self.group]['days'][str(self.week_day)]
                        
                        if self.next_week == True or next_day == True:
                            lessons['lessons'] = [lessons['lessons'][0]]
                            
                            return self.print_schedule(lessons)

                        else:
                            time_now =  datetime.time.fromisoformat(datetime.datetime.now().strftime("%H:%M"))
                            
                            for i in lessons['lessons']:
                                time_lesson = datetime.time.fromisoformat(i['end_time'])

                                if time_now < time_lesson:
                                    lessons['lessons'] = [i]
                                    
                                    return self.print_schedule(lessons) 
                            
                            self.week_day += 1
                            next_day = True


            case 1:
                payload = {'groupNumber': self.group, 'week' : self.parity_week, "weekDay": self.dict_day_week[week_day]}
                lessons = requests.get(self.url, params=payload).json()
                lessons = lessons[self.group]['days'][str(week_day)]
               
                return self.print_schedule(lessons)

            case 2:
                self.week_day += 1
                self.check_week_day()
                payload = {'groupNumber': self.group, 'week' : self.parity_week, "weekDay": self.dict_day_week[self.week_day]}
                lessons = requests.get(self.url, params=payload).json()
                lessons = lessons[self.group]['days'][str(self.week_day)]
                
                return self.print_schedule(lessons)


            case 3:
                print_data = ''
                payload = {'groupNumber': self.group, 'week' : self.parity_week}
                lessons = requests.get(self.url, params=payload).json()

                for i in range(6):
                    print_data += self.print_schedule(lessons[self.group]['days'][str(i)])

                    if i != 5:
                        print_data += '\n'

                return print_data

    url = 'https://digital.etu.ru/api/mobile/schedule'   

    dict_day_week = {
        0 : "MON",
        1 : "TUE",
        2 : "WED",
        3 : "THU",
        4 : "FRI",
        5 : "SAT"
    }

    dict_method = {
        'near_lesson' : 0,
        'day_week_number': 1,
        'tommorrow' : 2,
        'all_week' : 3
    }

    dict_parity_week = {
        True : "2",
        False : "1"
    }