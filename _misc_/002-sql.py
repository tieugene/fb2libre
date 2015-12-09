#!/bin/env python
# -*- coding: utf-8 -*-
'''
Tool to check/tune librusec/flibusta databases

Workflow:
* check
* repair (orphaned, self)
* tune (cascade replace)
* patch (loops, patches)
* delete unwanted (no-fb2, empty)
* export

Lib:
* Lib.rus.ec
* Flibusta
Actions:
* Check
* Repair (w/ patch?)
* Clean (delete !fb2)
* Export

= Notes =
Flibusta libjoinedbooks (BadId, GoodId, relaId):
* BadId, GoodId WHERE GoodId = realId OR realId IS NULL
* BadId, realId WHERE GoodId <> realId AND realId IS NOT NULL

Возможно в loop надо учитывать Deleted
'''

from __future__ import print_function
import sys, argparse, pprint
import mysql.connector

# ?
REQ = (
	'librusec',
	'flibusta',
)

reload(sys)
sys.setdefaultencoding('utf-8')

# SQLs
# common
CNT		= "SELECT COUNT(*) FROM %s;"
ORPHAN		= "SELECT COUNT(*) FROM %s LEFT JOIN %s ON %s.%s = %s.%s WHERE %s.%s IS NULL;"
A_ORPH		= "SELECT COUNT(*) FROM %s LEFT JOIN %s ON %s.%s = %s.%s WHERE %s.%s IS NULL;"
D_ORPH		= "DELETE %s FROM %s LEFT JOIN %s ON %s.%s = %s.%s WHERE %s.%s IS NULL;"
# L only
LA_MV_RM	= "SELECT COUNT(bid) FROM libbook      JOIN libjoinedbooks ON libbook.bid = libjoinedbooks.BadId WHERE libbook.Deleted = 1;"
LA_MV_NRM	= "SELECT COUNT(bid) FROM libbook      JOIN libjoinedbooks ON libbook.bid = libjoinedbooks.BadId WHERE libbook.Deleted != 1;"
LA_NMV_RM	= "SELECT COUNT(bid) FROM libbook LEFT JOIN libjoinedbooks ON libbook.bid = libjoinedbooks.BadId WHERE libbook.Deleted = 1 AND libjoinedbooks.BadId IS NULL;"
LA_REPLD	= "SELECT COUNT(aid) FROM libavtors WHERE main <> 0;"
LA_REPLD_FULL	= "SELECT COUNT(DISTINCT libavtor.aid) FROM libavtor LEFT JOIN libavtors ON libavtor.aid = libavtors.aid WHERE libavtor.role = 'a' AND libavtors.main <> 0;"
LA_REPLD_ORPH	= "SELECT COUNT(a.aid) FROM libavtors a LEFT JOIN libavtors b ON a.main = b.aid WHERE a.main <> 0 AND b.aid IS NULL;"
#LA_REPLD_CASC	= "SELECT COUNT(a.aid) FROM libavtors a LEFT JOIN libavtors b ON a.main = b.aid WHERE a.main <> 0 AND b.main IS NOT NULL;"
LD_NOTAUTH	= "DELETE libavtor FROM libavtor WHERE role <> 'a';"
# F only
A_LJB_ORPH_REAL	= "SELECT COUNT(*) FROM libjoinedbooks LEFT JOIN libbook ON libjoinedbooks.realId = libbook.BookId WHERE libjoinedbooks.realId IS NOT NULL AND libbook.BookId IS NULL;"
F_BOOK_REPL	= "(SELECT BadId, GoodId FROM libjoinedbooks WHERE (GoodId = realId OR realId IS NULL) AND BadId <> GoodId) UNION (SELECT BadId, realId FROM libjoinedbooks WHERE (GoodId <> realId AND realId IS NOT NULL) AND BadId <> realId) ORDER BY BadId;"
F_BOOK_CASC1	= "SELECT COUNT(*) FROM libjoinedbooks a JOIN libjoinedbooks b ON a.realId = b.BadId WHERE a.BadId <> a.realId;"
F_BOOK_CASC2	= "SELECT COUNT(*) FROM libjoinedbooks a JOIN libjoinedbooks b ON a.GoodId = b.BadId WHERE (a.GoodId = a.realId OR a.realId IS NULL) AND a.BadId <> a.GoodId AND a.BadId <> a.realId;"

def	prn_out(l, k, v = None):
	'''
	Prints operation result
	@param l:int - level
	@param k:str - title
	@param v:str - value
	'''
	title = ("%s %s:" % ('-' * l, k)).ljust(16, ' ')
	if v != None:
		print("%s\t%s" % (title, v))
	else:
		print(title)

def	get_one(c, q, a = None):
	'''
	Counts records
	@param c:cursor
	@param q:str
	@param a:* - argument[s]
	@return int record count
	'''
	#print(q % a if a else q)
	c.execute(q % a if a else q)
	return c.fetchone()[0]

def	get_orph(c, a):
	'''
	@param c:cursor
	@param a:tuple - arguments
	'''
	return get_one(c, A_ORPH, (a[0], a[2], a[0], a[1], a[2], a[3], a[2], a[3]))

def	prn_tbl(c, t):
	'''
	Prints table records count
	@param c:cursor
	@param t:str - table name
	'''
	prn_out(1, t, get_one(c, CNT, t))

def	__exec(c, q, a = None):
	'''
	Execute query
	@param c:cursor
	@param q:str
	@param a:* - argument[s]
	'''
	#print(q % a if a else q)
	c.execute(q % a if a else q)

def	__del_orph(c, a):
	'''
	Delete orphan records
	@param c:cursor
	@param a:tuple - arguments
	'''
	return __exec(c, D_ORPH, (a[0], a[0], a[2], a[0], a[1], a[2], a[3], a[2], a[3]))

stack_l = []
stack_s = set()
loops = set()

def	__chk_loop(c, q):
	'''
	TODO:
	* no dubt
	* resolve trivail loop (id<>id)
	* sort by 1st loop
	Split:
	* trivial loop (id-id)
	* extract loops
	* split combo (path+loop) into path+loop
	* solve loop:
	** not deleted
	** if not (or > 1): id/date
	'''
	def	__find_dest(d, k, v):
		'''
		Try to find endpoint
		@param k:int - main key
		@param v:int - current replacement
		'''
		global stack_l, stack_s, loops
		if v in stack_s:	# loop detected
			stack_l = stack_l[stack_l.index(v):]	# cut off head items
			if len(stack_l) == 2:
				stack_l.sort()	# resolve trivial loops
			hash = tuple(stack_l)
			if not hash in loops:
				loops.add(hash)
				if len(hash) == 2:
					sep = ' <> '
				else:
					sep = ' > '
				print(sep.join(map(str, stack_l)))
				return 1
			else:
				return 0
		stack_l.append(v)
		stack_s.add(v)
		dest = d.get(v, None)
		if dest:
			return __find_dest(d, k, dest)
		return 0
	global stack_l, stack_s, loops
	count = 0
	loops.clear()
	__exec(c, q)
	repl_d = dict(c.fetchall())
	for k, v in repl_d.iteritems():
		del stack_l[:]
		stack_s.clear()
		count += __find_dest(repl_d, k, v)
	return count

def	chk_librusec (conn, cur):
	'''
	Check Lib.Rus.ec DB
	@param conn:mysql.connector.connect
	@param cur:mysql.connector.connect,cursor
	'''
	#prn_tbl(cur, 'libbook')
	#prn_out(2, 'mv & Del',		get_one(cur, LA_MV_RM))		# Замененные и удаленные
	#prn_out(2, 'mv & !Del',	get_one(cur, LA_MV_NRM))	# Замененные и НЕ удаленные
	#prn_out(2, '!mv & Del',	get_one(cur, LA_NMV_RM))	# НЕ замененные и удаленные
	prn_tbl(cur, 'libjoinedbooks')
	prn_out(2, 'orph bad',		get_orph(cur, ('libjoinedbooks', 'BadId', 'libbook', 'bid')))	# У книг левые источники
	prn_out(2, 'orph good',		get_orph(cur, ('libjoinedbooks', 'GoodId', 'libbook', 'bid')))	# У книг левые замены
	prn_out(2, 'repl w/ self',	get_one(cur, 'SELECT COUNT(*) FROM libjoinedbooks WHERE BadId = GoodId;'))
	prn_out(2, 'repl w/ loop',	__chk_loop(cur, "SELECT DISTINCT BadId, GoodId FROM libjoinedbooks WHERE BadId <> GoodId ORDER BY BadId;"))
	prn_out(2, 'repl cascade',	get_one(cur, "SELECT COUNT(*) FROM libjoinedbooks a JOIN libjoinedbooks b ON a.GoodId = b.BadId WHERE a.GoodId <> a.BadId AND b.GoodId <> b.BadId;"))
	prn_tbl(cur, 'libavtor')
	prn_out(2, 'orph book',		get_orph(cur, ('libavtor', 'bid', 'libbook', 'bid')))
	prn_out(2, 'orph auth',		get_orph(cur, ('libavtor', 'aid', 'libavtors', 'aid')))
	prn_tbl(cur, 'libavtors')
	prn_out(2, 'empty',		get_orph(cur, ('libavtors', 'aid', 'libavtor', 'aid')))
	prn_out(2, 'repl w/ bad',	get_one(cur, LA_REPLD_ORPH))
	prn_out(2, 'repl w/ self',	get_one(cur, 'SELECT COUNT(*) FROM libavtors WHERE aid = main;'))
	prn_out(2, 'repl w/ loop',	__chk_loop(cur, 'SELECT a.aid, b.aid FROM libavtors a LEFT JOIN libavtors b ON a.main = b.aid WHERE b.aid <> 0 ORDER BY a.aid;'))
	prn_out(2, 'repl cascade',	get_one(cur, "SELECT COUNT(*) FROM libavtors a JOIN libavtors b ON a.main = b.aid WHERE b.main <> 0"))
	#prn_out(2, 'repl',		get_one(cur, LA_REPLD))
	#prn_out(2, 'repl & !empty',	get_one(cur, LA_REPLD_FULL))
	prn_tbl(cur, 'libgenre')
	prn_out(2, 'orph book',		get_orph(cur, ('libgenre', 'bid', 'libbook', 'bid')))
	prn_out(2, 'orph genre',	get_orph(cur, ('libgenre', 'gid', 'libgenres', 'gid')))
	prn_tbl(cur, 'libgenres')
	prn_out(2, 'empty',		get_orph(cur, ('libgenres', 'gid', 'libgenre', 'gid')))
	prn_tbl(cur, 'libseq')
	prn_out(2, 'orph book',		get_orph(cur, ('libseq', 'bid', 'libbook', 'bid')))
	prn_out(2, 'orph seq',		get_orph(cur, ('libseq', 'sid', 'libseqs', 'sid')))
	prn_tbl(cur, 'libseqs')
	prn_out(2, 'empty',		get_orph(cur, ('libseqs', 'sid', 'libseq', 'sid')))
	prn_tbl(cur, 'libmag')
	prn_out(2, 'orph book',		get_orph(cur, ('libmag', 'bid', 'libbook', 'bid')))
	prn_out(2, 'orph mag',		get_orph(cur, ('libmag', 'mid', 'libmags', 'mid')))
	prn_tbl(cur, 'libmags')
	prn_out(2, 'empty',		get_orph(cur, ('libmags', 'mid', 'libmag', 'mid')))

def	__mv_auths(c):
	'''
	Replace authors
	'''
	def	__mv_auth(c, s, d):
		'''
		Find repl recursively (!).
		@param c:cursor
		@param s:int - source author's id
		@param d:int - dest author's id
		@retrun int - new dest|0 (loop/notexists)
		'''
		print("> %d" % d, end='')
		if (s == d):				# loop
			print(": Loop detected", end="")
			retvalue = 0
			# TODO: split loop
		else:
			__exec(c, "SELECT DISTINCT main FROM libavtors WHERE aid = %d;", d)
			rec = c.fetchone()
			if rec:				# dest exists
				if rec[0]:		# we have chain
					retvalue = __mv_auth(c, s, rec[0])
					# TODO: replace main back in chain
				else:			# endpoint
					retvalue = d	# do nothing
			else:				# dest not exists
				print(": Not exists", end="")
				retvalue = 0
		return retvalue
	__exec(c, "SELECT DISTINCT libavtor.aid, libavtors.main FROM libavtor LEFT JOIN libavtors ON libavtor.aid = libavtors.aid WHERE libavtors.main <> 0 ORDER BY libavtor.aid;")
	repl = c.fetchall()	# list of tuples
	for rec in repl:	# old_aid:int, new_aid:int
		print("%d\t" % rec[0], end='')
		d = __mv_auth(c, rec[0], rec[1])
		if d:	# real end replacer
			# del exists: 
			__exec(c, "DELETE a FROM libavtor a JOIN libavtor b ON a.bid = b.bid WHERE a.aid = %d AND b.aid = %d;", (rec[0], rec[1]))
			# update other
			__exec(c, "UPDATE libavtor SET aid=%d WHERE aid=%d;", (rec[1], rec[0]))
			pass
		else:	# reset main
			__exec(c, "UPDATE libavtors SET main=0 WHERE aid=%d;", rec[0])
		print()

def	cln_librusec (conn, cur):
	'''
	Clean librusec DB (30")
	'''
	conn.start_transaction()
	prn_out(2, 'libjoinedbooks')
	__del_orph(cur, ('libjoinedbooks', 'BadId', 'libbook', 'bid'))
	__del_orph(cur, ('libjoinedbooks', 'GoodId', 'libbook', 'bid'))
	# FIXME: recuring (w/ loop detection)
	prn_out(2, 'libavtor')
	__del_orph(cur, ('libavtor', 'bid', 'libbook', 'bid'))
	__del_orph(cur, ('libavtor', 'aid', 'libavtors', 'aid'))
	__exec(cur, LD_NOTAUTH)
	conn.commit()
	conn.start_transaction()
	prn_out(2, 'libavtors')
	# clean bad replaces - bad SQL
	#__exec(cur, "UPDATE libavtors AS a LEFT JOIN libavtors AS b ON a.main = b.aid SET a.main=0 WHERE a.main <> 0 AND b.aid IS NULL;")
	# tune replaced & !empty
	__mv_auths(cur)
	__del_orph(cur, ('libavtors', 'aid', 'libavtor', 'aid'))
	prn_out(2, 'libgenre')
	__del_orph(cur, ('libgenre', 'bid', 'libbook', 'bid'))
	__del_orph(cur, ('libgenre', 'gid', 'libgenres', 'gid'))
	prn_out(2, 'libgenres')
	__del_orph(cur, ('libgenres', 'gid', 'libgenre', 'gid'))
	prn_out(2, 'libseq')
	__del_orph(cur, ('libseq', 'bid', 'libbook', 'bid'))
	__del_orph(cur, ('libseq', 'sid', 'libseqs', 'sid'))
	prn_out(2, 'libseqs')
	__del_orph(cur, ('libseqs', 'sid', 'libseq', 'sid'))
	prn_out(2, 'libmag')
	__del_orph(cur, ('libmag', 'bid', 'libbook', 'bid'))
	__del_orph(cur, ('libmag', 'mid', 'libmags', 'mid'))
	prn_out(2, 'libmag')
	__del_orph(cur, ('libmags', 'mid', 'libmag', 'mid'))
	conn.commit()

def	chk_flibusta (conn, cur):
	prn_tbl(cur, 'libjoinedbooks')
	prn_out(2, 'orph bad',		get_orph(cur, ('libjoinedbooks', 'BadId', 'libbook', 'BookId')))	# У книг левые источники
	prn_out(2, 'orph good',		get_orph(cur, ('libjoinedbooks', 'GoodId', 'libbook', 'BookId')))	# У книг левые замены
	prn_out(2, 'orph real',		get_one(cur, A_LJB_ORPH_REAL))
	prn_out(2, 'repl w/ self',	get_one(cur, "SELECT COUNT(*) FROM libjoinedbooks WHERE BadId = GoodId OR BadId = realId;"))
	prn_out(2, 'repl w/ loop',	__chk_loop(cur, F_BOOK_REPL))
	prn_out(2, 'repl cascade',	get_one(cur, F_BOOK_CASC1) + get_one(cur, F_BOOK_CASC2))
	prn_tbl(cur, 'libavtor')
	prn_out(2, 'orph book',		get_orph(cur, ('libavtor', 'BookId', 'libbook', 'BookId')))
	prn_out(2, 'orph auth',		get_orph(cur, ('libavtor', 'AvtorId', 'libavtorname', 'AvtorId')))
	prn_tbl(cur, 'libavtorname')
	prn_out(2, 'empty',		get_orph(cur, ('libavtorname', 'AvtorId', 'libavtor', 'AvtorId')))
	prn_tbl(cur, 'libavtoraliase')
	prn_out(2, 'orph bad',		get_orph(cur, ('libavtoraliase', 'BadId', 'libavtorname', 'AvtorId')))
	prn_out(2, 'orph good',		get_orph(cur, ('libavtoraliase', 'GoodId', 'libavtorname', 'AvtorId')))
	prn_out(2, 'repl w/ self',	get_one(cur, 'SELECT COUNT(*) FROM libavtoraliase WHERE BadId = GoodId;'))
	prn_out(2, 'repl w/ loop',	__chk_loop(cur, "SELECT DISTINCT BadId, GoodId FROM libavtoraliase WHERE BadId <> GoodId ORDER BY BadId;"))
	prn_out(2, 'repl cascade',	get_one(cur, "SELECT COUNT(*) FROM libavtoraliase a JOIN libavtoraliase b ON a.GoodId = b.BadId WHERE a.GoodId <> a.BadId AND b.GoodId <> b.BadId;"))
	prn_tbl(cur, 'libgenre')
	prn_out(2, 'orph book',		get_orph(cur, ('libgenre', 'BookId', 'libbook', 'BookId')))
	prn_out(2, 'orph genre',	get_orph(cur, ('libgenre', 'GenreId', 'libgenrelist', 'GenreId')))
	prn_tbl(cur, 'libgenrelist')
	prn_out(2, 'empty',		get_orph(cur, ('libgenrelist', 'GenreId', 'libgenre', 'GenreId')))
	prn_tbl(cur, 'libseq')
	prn_out(2, 'orph book',		get_orph(cur, ('libseq', 'BookId', 'libbook', 'BookId')))
	prn_out(2, 'orph seq',		get_orph(cur, ('libseq', 'SeqId', 'libseqname', 'SeqId')))
	prn_tbl(cur, 'libseqname')
	prn_out(2, 'empty',		get_orph(cur, ('libseqname', 'SeqId', 'libseq', 'SeqId')))
	prn_tbl(cur, 'libfilename')
	prn_out(2, 'orph book',		get_orph(cur, ('libfilename', 'BookId', 'libbook', 'BookId')))

def	cln_flibusta (conn, cur):
	conn.start_transaction()
	conn.commit()
	# [libbook: remove non-fb2]
	prn_out(2, 'libjoinedbooks')
	__del_orph(cur, ('libjoinedbooks', 'BadId', 'libbook', 'BookId'))
	__del_orph(cur, ('libjoinedbooks', 'GoodId', 'libbook', 'BookId'))
	# FIXME: realId
	# FIXME: recurring loop
	prn_out(2, 'libavtor')
	__del_orph(cur, ('libavtor', 'BookId', 'libbook', 'BookId'))
	__del_orph(cur, ('libavtor', 'AvtorId', 'libavtorname', 'AvtorId'))
	prn_out(2, 'libavtoraliase')
	__del_orph(cur, ('libavtoraliase', 'BadId', 'libavtorname', 'AvtorId'))
	__del_orph(cur, ('libavtoraliase', 'GoodId', 'libavtorname', 'AvtorId'))
	# FIXME: recurring loop
	prn_out(2, 'libavtorname')
	__del_orph(cur, ('libavtorname', 'AvtorId', 'libavtor', 'AvtorId'))
	prn_out(2, 'libgenre')
	__del_orph(cur, ('libgenre', 'GenreId', 'libgenrelist', 'GenreId'))
	prn_out(2, 'libgenrelist')
	__del_orph(cur, ('libgenrelist', 'GenreId', 'libgenre', 'GenreId'))
	prn_out(2, 'libseq')
	__del_orph(cur, ('libseq', 'BookId', 'libbook', 'BookId'))
	__del_orph(cur, ('libseq', 'SeqId', 'libseqname', 'SeqId'))
	prn_out(2, 'libseqname')
	__del_orph(cur, ('libseqname', 'SeqId', 'libseq', 'SeqId'))
	prn_out(2, 'libfilename')
	__del_orph(cur, ('libfilename', 'BookId', 'libbook', 'BookId'))

what2do = {
	('l', 't'): (chk_librusec, REQ[0], 'Librusec test'),
	('l', 'u'): (cln_librusec, REQ[0], 'Librusec update'),
	#('l', 'e'): (exp_librusec, REQ[0], 'Librusec export'),
	('f', 't'): (chk_flibusta, REQ[1], 'Flibusta test'),
	('f', 'u'): (cln_flibusta, REQ[1], 'Flibusta update'),
	#('f', 'e'): (exp_flibusta, REQ[1], 'Flibusta export'),
}

def main (f, b, t):
	'''
	@param f:function
	@param b:str - DB/login/pass name
	@param t:str - title
	'''
	conn = mysql.connector.connect(host='localhost', user=b, passwd=b, db=b, charset='utf8')
	if not conn.is_connected():
		print('DB oops')
		return 1
	cursor = conn.cursor()
	print('= %s =' % t)
	f(conn, cursor)
	cursor.close()
	conn.close()

if (__name__ == '__main__'):
	# TODO: add SQL loading
	parser = argparse.ArgumentParser(description='Check/clean libraries DBs.')
	parser.add_argument('lib', help='Library (l - lib.rus.ec, f - Flibusta)', choices=('l', 'f'))
	parser.add_argument('act', help='Action (t - test, u - clean, e - export)',  choices=('t', 'u', 'e'))
	#parser.add_argument('v', help='Verbose',  choices=('t', 'u', 'e'))
	args = parser.parse_args()
	largs = (args.lib, args.act)
	#print(largs)
	main(*what2do[largs])
