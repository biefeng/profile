# -*- coding:utf-8 -*-
# author : BieFeNg
# date_time 2020/06/21 13:36
# file_name : MysqlUtil.py

import getopt
import sys
from csv import DictWriter, DictReader

import pymysql

DEV = {'host': '10.128.62.33', 'user': 'root', 'password': 'root', 'database': 'jy_catering'}
CATERING_PROD = {'host': '172.16.1.106', 'user': 't11developer', 'password': 'JYwl@2019', 'database': 'jy_catering'}
ORDER_PROD = {'host': '172.16.1.154', 'user': 't11developer', 'password': 'JYwl@2019', 'database': 'jy_order'}

BASE_WIN_OUTPUT_PATH = 'd:/'
profiles = {'dev': DEV, 'cateringProd': CATERING_PROD, "orderProd": ORDER_PROD}


class Export:
    def export_to_csv(self, **kwargs):
        print("--------args:" + str(kwargs))
        limit = 10000
        count = self.get_data_scale(**kwargs)['count']
        print("***************************************共计：d%条", count)
        times = (count + limit - 1) // limit

        add_header = False
        dict_writer = None
        output_file = "result.csv"
        try:
            if 'output' in kwargs:
                output_file = kwargs['output']
            elif 'table' in kwargs:
                output_file = kwargs['table'] + ".csv"
        except Exception as e:
            print(e)
        print(output_file)
        with open(output_file, 'w') as csvfile:
            for i in range(times):
                kwargs["startIndex"] = i * limit + 1
                # kwargs['endIndex'] =(i + 1) * limit
                kwargs['endIndex'] = limit
                print("第%d条至第%d条", kwargs["startIndex"], (i + 1) * limit)

                records = self.get_data(**kwargs)
                column_names = []
                for data in records:
                    if not add_header:
                        for column_name in data.keys():
                            column_names.append(column_name)
                        add_header = True
                        dict_writer = DictWriter(csvfile, fieldnames=column_names, delimiter=" ")
                        dict_writer.writeheader()
                    dict_writer.writerow(data)

    def export_to_inserts(self, **kwargs):
        prop = {'host': '192.168.186.135', 'user': 'root', 'password': 'Biefeng123!', 'database': 'recosys'}
        insert_connection = pymysql.connect(host=prop['host'], user=prop['user'], password=prop['password'],
                                            database=prop['database'])
        insert_cursor = insert_connection.cursor(cursor=pymysql.cursors.DictCursor)

        limit = 10000
        count = self.get_data_scale(**kwargs)['count']
        print("***************************************共计：d%条", count)
        times = (count + limit - 1) // limit

        init = False
        insert_sql = ""

        with open('result.sql', 'w', encoding="utf-8") as sqlfile:
            for i in range(times):
                kwargs["startIndex"] = i * limit + 1
                # kwargs['endIndex'] =(i + 1) * limit
                kwargs['endIndex'] = limit
                print("第%d条至第%d条", kwargs["startIndex"], (i + 1) * limit)

                records = self.get_data(**kwargs)
                column_names = []
                for data in records:
                    if not init:
                        insert_sql = "insert into " + kwargs['tableName'] + "("
                        for column_name in data.keys():
                            insert_sql = insert_sql + column_name + ","
                        init = True
                        insert_sql = insert_sql[:len(insert_sql) - 1] + ") values ("
                        print(insert_sql)
                    temp = insert_sql
                    for (key, value) in data.items():

                        if value is None:
                            temp = temp + "NULL" + ","
                        else:
                            temp = temp + "'" + str(value) + "'" + ","
                    temp = temp[:len(temp) - 1] + ");\r\n"
                    # print(temp)
                    insert_cursor.execute(temp)
                    insert_connection.commit()
                    try:
                        sqlfile.write(temp)
                    except Exception as e:
                        print(e)

    @staticmethod
    def get_cursor(**kwargs):
        # connection = pymysql.connect(host="10.128.62.33", usser="root", password="root", database="jy_catering")
        connection = pymysql.connect(host=kwargs['host'], user=kwargs['user'], password=kwargs['password'],
                                     database=kwargs['database'])
        cursor = connection.cursor(cursor=pymysql.cursors.DictCursor)
        return cursor

    def get_data(self, **kwargs):
        cursor = self.get_cursor(**kwargs)
        # sql = "select * from " + kwargs['table'] + ' limit ' + str(kwargs['startIndex']) + "," + str(kwargs['endIndex'])
        sql = ' select * from (' + kwargs['sql'] + ')tmp limit ' + str(
            kwargs['startIndex']) + "," + str(kwargs['endIndex'])
        cursor.execute(sql)
        return cursor.fetchall()

    def get_data_scale(self, **kwargs):
        cursor = self.get_cursor(**kwargs)
        sql = "select count(1) count from (" + kwargs['sql'] + ") tmp"
        cursor.execute(sql)
        return cursor.fetchone()

    def export(self):
        args = sys.argv[1:]
        opts, args = getopt.getopt(args, "hd:s:p:t:")
        print(opts)
        props = {"profiles": "dev"}
        for opt, arg in opts:
            if opt == '-h':
                print("python export_to_excel.py -d <database> -s <sql> -p <profile> ")
                sys.exit(1)
            elif opt == '-d':
                print(props)
                props['database'] = profiles[props['profiles']]['database']
            elif opt == '-s':
                props['sql'] = arg
            elif opt == '-t':
                props['table'] = arg
            elif opt == '-p':
                props['profiles'] = arg
            elif opt == '-o':
                props['output_path'] = arg

        profiles[props['profiles']]['sql'] = props['sql']
        profiles[props['profiles']]['database'] = props['database']
        profiles[props['profiles']]['table'] = props['table']

        self.export_to_csv(**profiles[props['profiles']])


class Import():
    def __init__(self, host, database, user, password):
        self._connect = pymysql.connect(host=host, password=password, user=user, database=database)
        self._cursor = self._connect.cursor(cursor=pymysql.cursors.Cursor)
        self.database = database
        self.user = user
        self.password = password

    def import_csv(self, fn, table_name, delimiter=" "):
        with open(fn, mode='r') as cf:
            reader = DictReader(cf, delimiter=delimiter)
            sql = "insert into {0}({1})values ({2});"
            for row in reader:
                keys = row.keys()
                keys.remove('id')
                colums = str(keys)[1:len(str(keys)) - 1].replace("'", "")
                value_arr = []
                for key in keys:
                    value_arr.append(row[key])
                values = str(value_arr)[1:len(str(value_arr)) - 1]
                tmp = sql.format(table_name, colums, values)
                try:
                    self._cursor.execute(tmp)
                except Exception as e:
                    print(tmp)
        self._connect.commit()


if "__main__" == __name__:
    im = Import("baiduyun", "blog_mini", "root", "Biefeng123!")
    im.import_csv("D:\\Download\chromePlugin\\2020-6-20\\chrome_plugin_url.csv", "chrome_plugin")
