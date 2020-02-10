from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import re
import pymysql
import geocoder
import datetime
import os


class Weather:
    def __init__(self, host, user, passwd, db, port):
        settings_file_path = 'weather.weather.settings'  # The path seen from root, ie. from main.py
        os.environ.setdefault('SCRAPY_SETTINGS_MODULE', settings_file_path)
        self.process = CrawlerProcess(get_project_settings())
        self.location = geocoder.ip('me').address
        self.date = datetime.date.today()

        self.text = ""
        self.data = {}
        self.conn = pymysql.connect(host=host, user=user, passwd=passwd, db=db, port=port)
        self.cursor = self.conn.cursor()

        self.renew_table()

    def renew_table(self):
        self._get_web_page()
        self._get_data()
        self._create_sql_table()

    def _get_web_page(self):
        """

        :return: the content of html file
        """
        self.process.crawl('weather')
        self.process.start()
        self.filename = 'weather.html'
        with open(self.filename, 'r') as f:
            data = f.readlines()
        self.text = ' '.join(data)

    def _get_data(self):
        """

        :return: data in dictionary format
        """
        dic = {}

        # description
        description = re.findall(r'<td class="twc-sticky-col" headers="day" title=(.*?) data-track-string', self.text)
        description = [val[1:-1] for val in description]
        dic['description'] = description

        # day_time
        day_time = re.findall(r'<span class="date-time">(.*?)</span>', self.text)
        dic['day_time'] = day_time

        # day_detail
        day_detail = re.findall(r'<span class="day-detail clearfix">(.*?)</span>', self.text)
        dic['day_detail'] = day_detail

        # simple_description
        simple_description = re.findall(r'<td class="description".*?<span>(.*?)</span></td>', self.text)
        dic['simple_description'] = simple_description

        # highest and lowest temperature
        highest_temperature = re.findall(
            r'<div><span>(.*?)</span><span class="slash"|<div><span class="">(.*?)<sup>°</sup></span><span class="slash"',
            self.text)
        lowest_temperature = re.findall(
            r'"slash"></span><span class="">(.*?)<sup>°</sup></span></div>|"slash"></span><span>(.*?)</span></div>',
            self.text)
        for i, val in enumerate(highest_temperature):
            if val[0]:
                highest_temperature[i] = val[0]
            else:
                highest_temperature[i] = val[1]
        for i, val in enumerate(lowest_temperature):
            if val[0]:
                lowest_temperature[i] = val[0]
            else:
                lowest_temperature[i] = val[1]

        dic['highest_temperature'] = highest_temperature
        dic['lowest_temperature'] = lowest_temperature

        # precip
        precip = re.findall(r'icon-drop-1"></span><span class=""><span>(.*?)<span', self.text)
        dic['precip'] = precip

        # wind
        wind = re.findall(r'"wind"><span class="">(.*?)</span></td>', self.text)
        dic['wind'] = wind

        # humidity
        humidity = re.findall(r'"humidity"><span class=""><span>(.*?)<span', self.text)
        dic['humidity'] = humidity

        self.data = dic

    def _create_sql_table(self):
        """

        create sql table and insert data
        """
        self.cursor.execute('SHOW TABLES')
        if ('weather',) in self.cursor:
            self.cursor.execute('DROP TABLE weather')
            self.conn.commit()

        sql_Q_create_table = "CREATE TABLE weather(date varchar(32) NOT NULL, date_week TEXT, description TEXT, simple_description TEXT, highest_temp TEXT, lowest_temp TEXT, precip TEXT, wind TEXT, humidity TEXT, PRIMARY KEY(date))"
        self.cursor.execute(sql_Q_create_table)
        self.conn.commit()

        for i in range(len(self.data['day_detail'])):
            sql_Q_insert = "INSERT INTO weather (date, date_week, description, simple_description, highest_temp, lowest_temp, precip, wind, humidity) values('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" % (self.data['day_detail'][i], self.data['day_time'][i], self.data['description'][i], self.data['simple_description'][i], self.data['highest_temperature'][i], self.data['lowest_temperature'][i], self.data['precip'][i], self.data['wind'][i], self.data['humidity'][i])

            self.cursor.execute(sql_Q_insert)
            self.conn.commit()

    def _transfer_date(self, value):
        temp = value.ctime().split(' ')
        if temp[2] == '':
            return temp[1].upper() + ' ' + temp[3]

        return temp[1].upper() + ' ' + temp[2]

    def select_data(self, content):
        if 'tomorrow' in content:
            date = self._transfer_date(value=self.date + datetime.timedelta(days=1))
            sql_Q_select = "SELECT description from weather WHERE date = \'%s\'" % date
            self.cursor.execute(sql_Q_select)
            rows = self.cursor.fetchall()
            return "Tomorrow in " + self.location + " : " + rows[0][0]
        else:
            date = self._transfer_date(value=self.date)
            sql_Q_select = "SELECT description from weather WHERE date = \'%s\'" % date
            self.cursor.execute(sql_Q_select)
            rows = self.cursor.fetchall()
            return "Today in " + self.location + " : " + rows[0][0]


# host = 'localhost'
# user = 'root'
# passwd = '123456'
# db = 'mydb'
# port = 3306
# w = Weather(host=host, user=user, passwd=passwd, db=db, port=port)
# print(w.select_data(content='today'))


