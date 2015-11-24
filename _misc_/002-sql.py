#!/bin/env python
# -*- coding: utf-8 -*-
'''
Tool to check/tune librusec/flibusta databases
'''

from __future__ import print_function
import sys
import mysql.connector

REQ = (
	'librusec',
	'flibusta',
)

reload(sys)
sys.setdefaultencoding('utf-8')

# SQLs
CNT		= "SELECT COUNT(*) FROM %s;"
ORPHAN		= "SELECT COUNT(*) FROM %s LEFT JOIN %s ON %s.%s = %s.%s WHERE %s.%s IS NULL;"
A_MV_RM		= "SELECT COUNT(bid) FROM libbook      JOIN libjoinedbooks ON libbook.bid = libjoinedbooks.BadId WHERE libbook.Deleted = 1;"
A_MV_NRM	= "SELECT COUNT(bid) FROM libbook      JOIN libjoinedbooks ON libbook.bid = libjoinedbooks.BadId WHERE libbook.Deleted != 1;"
A_NMV_RM	= "SELECT COUNT(bid) FROM libbook LEFT JOIN libjoinedbooks ON libbook.bid = libjoinedbooks.BadId WHERE libbook.Deleted = 1 AND libjoinedbooks.BadId IS NULL;"
A_ORPH		= "SELECT COUNT(*) FROM %s LEFT JOIN %s ON %s.%s = %s.%s WHERE %s.%s IS NULL;"
A_REPLD		= "SELECT COUNT(aid) FROM libavtors WHERE main <> 0;"
A_REPLD_FULL	= "SELECT COUNT(DISTINCT libavtor.aid) FROM libavtor LEFT JOIN libavtors ON libavtor.aid = libavtors.aid WHERE libavtors.main <> 0;"
A_REPLD_ORPH	= "SELECT COUNT(a.aid) FROM libavtors a LEFT JOIN libavtors b ON a.main = b.aid WHERE a.main <> 0 AND b.aid IS NULL;"
A_REPLD_CASC	= "SELECT COUNT(a.aid) FROM libavtors a LEFT JOIN libavtors b ON a.main = b.aid WHERE a.main <> 0 AND b.main IS NOT NULL;"
D_ORPH		= "DELETE %s FROM %s LEFT JOIN %s ON %s.%s = %s.%s WHERE %s.%s IS NULL;"

def	align():
	'''
	Align str to x tabs (x8 spaces)
	'''

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
	prn_out(3, t, get_one(c, CNT, t))

def	chk_librusec (conn, cur):
	'''
	Check Lib.Rus.ec DB
	@param conn:mysql.connector.connect
	@param cur:mysql.connector.connect,cursor
	'''
	prn_out(1, 'LibRusEc')
	prn_out(2, 'chk')
	prn_tbl(cur, 'libbook')
	prn_out(4, 'mv & Del',		get_one(cur, A_MV_RM))	# Замененные и удаленные
	prn_out(4, 'mv & !Del',		get_one(cur, A_MV_NRM))	# Замененные и НЕ удаленные
	prn_out(4, '!mv & Del',		get_one(cur, A_NMV_RM))	# НЕ замененные и удаленные
	prn_tbl(cur, 'libjoinedbooks')
	prn_out(4, 'orph bad',		get_orph(cur, ('libjoinedbooks', 'BadId',  'libbook', 'bid')))	# У книг левые источники
	prn_out(4, 'orph good',		get_orph(cur, ('libjoinedbooks', 'GoodId', 'libbook', 'bid')))	# У книг левые замены
	prn_tbl(cur, 'libavtor')
	prn_out(4, 'orph book',		get_orph(cur, ('libavtor', 'bid',  'libbook', 'bid')))
	prn_out(4, 'orph auth',		get_orph(cur, ('libavtor', 'aid',  'libavtors', 'aid')))
	prn_tbl(cur, 'libavtors')
	prn_out(4, 'empty',		get_orph(cur, ('libavtors', 'aid',  'libavtor', 'aid')))
	prn_out(4, 'replaced',		get_one(cur, A_REPLD))
	prn_out(4, 'replaced & !empty',	get_one(cur, A_REPLD_FULL))
	prn_out(4, 'replaced w/ bad',	get_one(cur, A_REPLD_ORPH))
	prn_out(4, 'replaced cascade',	get_one(cur, A_REPLD_CASC))
	prn_tbl(cur, 'libgenre')
	prn_out(4, 'orph book',		get_orph(cur, ('libgenre', 'bid',  'libbook', 'bid')))
	prn_out(4, 'orph genre',	get_orph(cur, ('libgenre', 'gid',  'libgenres', 'gid')))
	prn_tbl(cur, 'libgenres')
	prn_out(4, 'empty',		get_orph(cur, ('libgenres', 'gid',  'libgenre', 'gid')))
	prn_tbl(cur, 'libseq')
	prn_out(4, 'orph book',		get_orph(cur, ('libseq', 'bid',  'libbook', 'bid')))
	prn_out(4, 'orph seq',		get_orph(cur, ('libseq', 'sid',  'libseqs', 'sid')))
	prn_tbl(cur, 'libseqs')
	prn_out(4, 'empty',		get_orph(cur, ('libseqs', 'sid',  'libseq', 'sid')))
	prn_tbl(cur, 'libmag')
	prn_out(4, 'orph book',		get_orph(cur, ('libmag', 'bid',  'libbook', 'bid')))
	prn_out(4, 'orph mag',		get_orph(cur, ('libmag', 'mid',  'libmags', 'mid')))
	prn_tbl(cur, 'libmags')
	prn_out(4, 'empty',		get_orph(cur, ('libmags', 'mid',  'libmag', 'mid')))
	#conn.commit()

def	del_orph(c, a):
	'''
	Delete orphan records
	@param c:cursor
	@param a:tuple - arguments
	'''
	return get_one(c, A_ORPH_B, (a[0], a[2], a[0], a[1], a[2], a[3], a[2], a[3]))

def	cln_librusec (conn, cur):
	prn_out(1, 'LibRusEc')
	prn_out(2, 'cln')
	prn_out(3, 'libjoinedbooks')
	del_orph(cur, ('libjoinedbooks', 'BadId', 'libbook', 'bid'))
	#conn.commit()

def main ():
	conn = mysql.connector.connect(host='localhost', user=REQ[0], passwd=REQ[0], db=REQ[0], charset='utf8')
	if not conn.is_connected():
		print('DB oops')
		exit(1)
	cursor = conn.cursor()
	chk_librusec(conn, cursor)
	cursor.close()
	conn.close()

if (__name__ == '__main__'):
	main()
