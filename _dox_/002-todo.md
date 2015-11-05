Цель: перегнать мета книг из sql в свой sql

* заливаем sql
* выливаем в sql
* отдельные адаптеры для либрусека и флибусты

Tables:
	* lib - тут понятно
		* arch - тут тоже понятно
	* genre - глобально
	* lang - глобально
	* series - глобально
	* author
	* book <> произведение+файл

Бонусы:
	* объединение:
		* авторов (в пределах либы и между либами)
		* книг (...)
		* жанров (...)
		* 

to teach:
	* author uid
	* book guid <> md5
	* book guid+size
	* 

CREATE DATABASE librusec CHARACTER SET utf8 COLLATE utf8_general_ci;
GRANT ALL PRIVILEGES ON librusec.* TO librusec@localhost IDENTIFIED BY 'librusec' WITH GRANT OPTION;