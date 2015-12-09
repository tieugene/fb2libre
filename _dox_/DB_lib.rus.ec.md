= Lib.rus.ec =

libavtors:
	* FIO не уникальны
	* есть авторы без ФИО
libavtor:
	* левые bid (0)
Проверить:
	* сколько книг у замененных авторов: 130
	* левые записи в кросс-таблицах
	* левые записи в основных таблицах

= Flibusta =

libavtorname:
	* FIO не уникальны
libavtoraliase:
	* BadId не уникальны (26655/26657)
	* Есть несуществующие BadId и GoodId

Т.е. перед загрузкой базы её надо проверить и почистить:
	* книги (не fb2)
	* авторы (пустые и замененные)
	* жанр

* librusec: убрать переводчиков и иллюстраторов
* объединение книг
* локальные патчи:
	* объе

= Итого =
== 1. Либрусек: ==
=== 1. As is ===
1. chk B4:
	* libgenre:
		* левые bid
		* левые gid
	* libseq:
		* левые bid
		* левые sid
	* libmag:
		* левые bid
		* левые mid
	* libavtor:
		* левые bid
		* левые aid
		* role:
			* a - автор (v)
			* c - Редсовет комментатор (x)
			* i - Редсовет иллюстрации (x)
			* o - Редсовет оформление (x)
			* p - person? (x)
			* r - Редсовет редактор (x)
			* s - составитель (x)
			* t - перевод (x)
	* libjoinedbooks:
		* левые BadId
		* левые GoodId
	* libbook:
		* guid
2. del:
	* libbook:
		* не в libjoinedbooks.BadId
3. chk after:
=== 2. FB2 only ===
1. del:
	* libbook:
		* [не fb2]
		* не в libjoinedbooks.BadId
		* единственная книга в сериале
	* libgenre: без книг
	* libseq: без книг
	* libmag: без книг
	* libavtor: без книг; не авторы (\0|'a')
	* libgenres: без книг
	* libseq: без книг
	* libmag: без книг
	* libavtors: без книг; main?
2. проверяем
	* libbook:
		* Deleted
		* guid
=== 3. Load ===
=== 4. chk w/ files ===
* (sql => inpx)

= ToDo =
* Книги:
	* group by
* Авторы:
	* ...
* Жанры:
	* ISO/ГОСТ

= Ideas =
* sql > inpx > web
* 0.0.2: discovery only (web2py/webtopy/flask/bottle)
* 0.0.3: произведение > книга > файл
* совмещать книги по guid
* и авторов - по книгам
* архив документов в виде fb2 < odf2fb2
* [group by series]
* filter: fb2/non-subj
