#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# Этот скрипт предназначен для поиска неиспользуемых
# ip адресов в биллинговой системе UTM5 от NetUp
#
# Скрипт принимает в качестве параметра командной
# строки подсеть в формате a.b.c.d/e
# Каждый хост в этой подсети будет проверен на
# присутствие в БД
# На экран выводится первый неиспользуемый адрес
# либо список всех неиспользуемых адресов в базе
# в зависимости от того задан второй параметр
# all или нет
#

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QListWidget, QMessageBox
import ipaddress
from configparser import ConfigParser
from mysql.connector import MySQLConnection, Error


class Form(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(171, 231)
        self.setMinimumSize(171, 231)
        self.setMaximumSize(171, 231)
        self.setWindowTitle("Spare IPs")
        self.lst_addresses = QListWidget(self)
        self.lst_addresses.setGeometry(10, 10, 151, 211)
        self.lst_addresses.setObjectName("lst_addresses")
        self.show()


def main():
    """ Точка входа в программу """

    # Строка запроса на языке sql для получения списка
    # ip адресов из базы данных биллинговой системы
    SQL_QUERY = "SELECT ip FROM ip_groups WHERE is_deleted=0"

    def read_db_config(filename="config.ini", section="mysql"):
        """ Функция считывает настройки подключенния к БД
        :параметр filename: имя файла конфигурации
        :параметр section: раздел конфигурации
        :возвращает словарь с настройками подключения """

        # Создаем парсер и считываем данные кофигурации
        parser = ConfigParser()
        if sys.platform.startswith("win32"):
            full_name = sys.path[0] + "\\" + filename
        else:
            full_name = sys.path[0] + "/" + filename
        parser.read(full_name)
        # Получаем раздел
        db = {}
        if parser.has_section(section):
            items = parser.items(section)
            for item in items:
                db[item[0]] = item[1]
        else:
            raise Exception(
                "Раздел {0} в файле {1} не найден".format(section, filename))
        return db

    def connect_to_db():
        """ Функция подключения к базе данных """

        db_config = read_db_config()
        try:
            conn = MySQLConnection(**db_config)
            if conn.is_connected():
                return conn
        except Error as e:
            print(e)

    def get_ips_from_db():
        """ Функция получает список ip адресов из БД """

        ips_from_db = []
        conn = connect_to_db()
        if conn:
            cursor = conn.cursor()
            cursor.execute(SQL_QUERY)
            db_data = cursor.fetchall()
            if len(db_data) > 0:
                for ip in db_data:
                    if ip[0] > 0:
                        ips_from_db.append(ipaddress.ip_address(ip[0]))
                conn.close()
            return ips_from_db

    def show_message(title="Default", msg="Default text message"):
        """ Функция выводит диалоговое окно с текстовым
        сообщением, заданным в качестве параметра для функции """

        # Проверка на случай, если в качестве параметров
        # заданы пробелы или другие символы разделители
        if title.strip() == "":
            title = "Default title"
        if msg.strip() == "":
            msg = "Default text message"
        msgbox = QMessageBox()
        msgbox.setIcon(QMessageBox.Information)
        msgbox.setWindowTitle(title)
        msgbox.setText(msg)
        msgbox.exec()

    # Основной код
    if len(sys.argv) > 1:
        app = QApplication(sys.argv)
        subnet = ipaddress.ip_network(sys.argv[1])
        ips_from_db = get_ips_from_db()
        if len(ips_from_db) > 0:
            if len(sys.argv) > 2 and sys.argv[2].upper() == "ALL":
                frm = Form()
            for ip in subnet.hosts():
                if ip not in ips_from_db:
                    if len(sys.argv) < 3 or sys.argv[2].upper() != "ALL":
                        show_message("Spare IPs",
                                     "Свободный адрес: " + str(ip))
                        sys.exit(0)
                    else:
                        frm.lst_addresses.addItem(str(ip))
            sys.exit(app.exec_())
    else:
        print("Пример использования: ")
        print("python spareips.pyw 192.168.0.0/24 [all]")


if __name__ == "__main__":
    main()
