= Lib.rus.ec =

libavtor:	book/author
	* bid:int(10) - book id ?
	* aid:int(10) - author id ?
	* role:int(1) - author/translator/illustrator
libavtors:	authors
	* aid:int(10) - author id (pk)
libbook:
	* bid:int(10) - book id (pk)
libgenremeta:	???
	* gid - genre id
	* gidm
libgenre:	book/genre
	* bid
	* gid
libgenres:	genres
	* gid - pk
	* code:char - abbr
	* gdesk:char - description (ru)
	* edesk:char - description (en)
libjoinedbooks:	book replacements
	* Timelll:timestamp - replacement Time
	* BadId:int(11) - book that replaced
	* GoodId:int(11) - book replaced to
libmag:	book/magazine
	* bid - book id
	* mid - magazine id
	* y:int - year (?)
	* m:int - month (?)
libmags:	magazines
	* mid:int - pk
	* class:char - magazine/newspaper
	* title:char - subj
	* firstyear:int - 
	* lastyear:int - 
	* peryear:int - periodicity
libquality:	raitings ?
	* bid - book id
	* uid:int - user id ?
	* q:char(1) - rate ?
librate:	rate history (?)
	* bid
	* uid
	* Rate:char(1)
	* Time:timestamp
libseq:	book/sequence
	* bid - book id
	* sid - sequence id
	* sn:int - sequence order
	* sort:decimal(28) - ???
libseqs:	sequences
	* sid - pk
	* seqname:char - title
	* parent:int - parent sequence id
	* nn:int - order in parent sequence
	* good:int ?
	* lang:char(2) - language
	* type:char(1) - ? (default 'a')
libsrclang:	book/lang (source)
	* bid - book id
	* SrcLang:char(2)

= Flibusta.net =

lib.a.annotations_pics
lib.a.annotations
lib.b.annotations_pics
lib.b.annotations
lib.libavtoraliase - author aliaces
lib.libavtorname - like libavtors
lib.libavtor - like libavtor
lib.libbook - like libbook
lib.libfilename:	book filenames
lib.libgenrelist - like libgenres
lib.libgenre - like libgenre
lib.libjoinedbooks - like libjoinedbooks
lib.librate - like libquolity ?
lib.libseqname - 
lib.libseq
lib.libsrclang
lib.libtranslator
lib.reviews                                                                                                                                                      