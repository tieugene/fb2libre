# fb2libre
Web-based FB2 library.
Django (?) powered
Howto: tipython/branches/librusec

*.inpx - zip-архив *.inp
*.inp - описание архива (1 архив - 1 файл)
Структура строки *.inp (1 строка - 1 файл; разделитель полей - <04>; разделитель значений - :; разделитель подзначений - ,):
AUTHOR*.GENRE*.TITLE.SERIES?.SERNO?.FILE.SIZE.LIBID.DEL?.EXT.DATE.LANG?.LIBRATE?.KEYWORDS*.

AUTHOR:	Автор[ы] - Фамилия,Имя,[Отчество]
GENRE:	жанр[ы]
TITLE:	Название
SERIES:	Серия
SERNO:	Номер в серии (может быть при отсутсв. серии)
FILE:	имя файла (без расширения)
SIZE:	размер файла (байт)
LIBID:	идентификатор (чего?) == FILE
DEL:	?
EXT:	расширение файла (fb2)
DATE:	Дата (публикации?) YYYY-MM-DD
LANG:	язык (ISO 639-1 ?)
LIBRATE:	рейтинг (?..?)
KEYWORDS:	ключевые слова

= Plan =
* 0.0.1: parsing
** parsing; lib (*.inpx) > arch (*.inp) > file (line)
** output (txt, uniq):
*** lang
*** genres
*** authors
*** books

* 0.0.2: sql
** load:
*** genres - as is, plain
*** lang - as is
** view:
*** Authors
*** ...
** features:
*** filter:
*** sorting:
*** order:
*** search:
** mk patches (per line/file.fb2)

* 0.0.3: tuning
** "проверено"
** genre: preload, 2-level (?)
** lang: preload
** html view
** download

= TODO =

* per-line patches (lib>file)
* book:file == m:m
* ru-RU patch
* user_file.read - читал
* user_book.read - читал
* online view
* descr (on demand)
* pic (on demand)
* URL

= Future =
* объединение книг (1 книга - * файлов)
* разъединение (1 файл - * книг)
* md5?
* genre - согласно библиотекарству
* text-based git-powered plain-text-only repo lib
* Json?

= ToTeach =
http://diss.rsl.ru/datadocs/doc_291wu.pdf
http://psyjournals.ru/files/59161/gost_r_7.0.4-2006.pdf
