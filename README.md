UTM5 Spare IPs
--------------

В данном файле будет коротко описан процесс использования данного скрипта
и установка пакетов, необходимых для его нормальной работы в разных системах.

1. Для того чтобы скрипт мог получить данные из БД, необходимо установить
   драйвер базы данных. Для этого нужно скачать файл, соответствующий вашему
   типу, версии и битности ОС по данному адресу:
   https://dev.mysql.com/downloads/connector/python/

2. Для корректного подключения к БД, нужно внести изменения в файл конфигурации.
   Он расположен в корневом каталоге проекта и называется config.ini

3. На сервере БД необходимо открыть доступ на файрволе для удаленного подключения
   по порту 3306 (или иному используемому вами) и протоколу tcp.

4. В файле конфигурации сервера БД разрешить подключения с удаленных хостов.

5. На сервере БД создать учетную запись с правами только для чтения к таблице
   ip_groups базы данных UTM5 (или иной в зависимости какое имя было указано
   при создании базы). Для выполнения этого можно воспользоваться примером:

    grant select on UTM5.ip_groups to 'user'@'%' identified by 'pass';  
    flush privileges;

6. Для корректного отображения диалоговых окон нужно поставить библиотеку PyQt5.
   Для примера в дистрибутиве Ubuntu Linux это можно сделать введя следующую
   команду в консоли: sudo apt-get install python3-pyqt5
   Информацию о том, как выполнить установку для других систем, можно найти по
   адресу https://www.riverbankcomputing.com/software/pyqt/intro

Формат запуска скрипта:

   Можно создать на рабочем столе кнопку запуска и указать ей в качестве команды

    python spareips.pyw 10.10.0.0/20 [all]

Если в системе установлено несколько версий интерпретатора python, то нужно будет
указать его точно. Например так: python3

Если путь до интерпретатора не добавлен в соответствующую переменную окружения, то
нужно будет указать полный путь. Например так: /usr/bin/python3

Если скрипт не находится в текущем каталоге, то нужно будет указать полный путь до него.
Например вот так: /home/user/scripts/spareips/spareips.py

Параметр all является опциональным. Если не указать его, то будет выведен только
первый неиспользуемый адрес, иначе будет выведен список всех неиспользуемых адресов.
Регистр букв параметра all не имеет значения.
