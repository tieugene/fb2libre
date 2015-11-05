#!/bin/env python
# -*- coding: utf-8 -*-
'''
Tool to parse inpx' and create sqls
Result: sql
Usage (1'40" + 5'50"):
./<thisscript> | gzip > result.sql.gz && gunzip -c ./result.sql.gz | ./manage.py dbshell 2> err.txt
Or:
./<thisscript> | ./manage.py dbshell

Then:
gawk '{print $4}' err.txt | sed -e 's/://g' > err.lst
gunzip -c result.sql.gz | head -n 1477253 | tail > 1477253.txt
'''

import sys, os, zipfile

reload(sys)
sys.setdefaultencoding('utf-8')

# const
libase = '/mnt/shares/ftp/pub/Lib'
libs = ( # abbr, name, path_to_inpx, path_to_archives, URL
    (
	'fn',
	'Flibusta.net',
	os.path.join(libase, 'fb2.Flibusta.Net/flibusta_fb2_local.inpx'),
	os.path.join(libase, 'fb2.Flibusta.Net'),
	'https://flibusta.me/b/%d'
    ),
    (
	'lre',
	'Lib.rus.ec',
	os.path.join(libase, '_Lib.rus.ec - Официальная/librusec_local_fb2.inpx'),
	os.path.join(libase, '_Lib.rus.ec - Официальная/lib.rus.ec'),
	'http://lib.rus.ec/b/%d'
    ),
)
sql_lib    = "INSERT INTO core_lib    (id, abbr, name, inpx, arch, bookurl) VALUES (%d, '%s', '%s', '%s', '%s', '%s');"
sql_arch   = "INSERT INTO core_arch   (id, lib_id, fname) VALUES (%d, %d, '%s');"
#sql_author = "INSERT INTO core_author (id, lname, fname, mname) VALUES (%d, '%s', '%s', '%s');"
sql_author = "INSERT INTO core_author (id, name) VALUES (%d, '%s');"
sql_genre  = "INSERT INTO core_genre  (id, abbr) VALUES (%d, '%s');"
sql_lang   = "INSERT INTO core_lang   (id, abbr) VALUES (%d, '%s');"
sql_series = "INSERT INTO core_series (id, name) VALUES (%d, '%s');"
sql_book   = "INSERT INTO core_book\
 (id, arch_id, title, series_id, serno, fname, size, deleted, pubed, lang_id, rate)\
 VALUES (%d, %d, '%s', %s, %s, %d, %d, %d, '%s', %d, %s);"
sql_book_authors = "INSERT INTO core_book_authors (book_id, author_id) VALUES (%d, %d);"
sql_book_genres  = "INSERT INTO core_book_genres  (book_id, genre_id)  VALUES (%d, %d);"

# var
author  = dict()
genre   = dict()
series  = dict()
lang    = dict()
arch_id = 1
book_id = 1

def out_sql (sql, data):
    print sql % data

def split_by_colon (s):
    return s.split(':')

def screen_quote(s):
    return s.replace("'", "''")

def try_add (d, i, sql):
    '''
    @param d:dict
    @param i:str
    @param sql:str
    @return id:int
    '''
    i = i.strip(' ')
    if (i):
        if (i in d):
            id = d[i]
        else:
            id = len(d) + 1
            d[i] = id
            out_sql(sql, (id, screen_quote(i)))
    else:
        id = 0
    return id

def try_add_author (i):
    '''
    s:set
    i:str
    '''
    i = i.strip(' ')
    if i:
        fio = i.split(',')
        if len(fio) == 1:
            fio.extend(['', ''])
        elif len(fio) == 2:
            fio.append('')
        i = ','.join(fio)
        if (i not in author):
            author.add(i)
            out_sql(sql_author, (len(author), screen_quote(fio[0]), screen_quote(fio[1]), screen_quote(fio[2])))

def parse_line (lib_id, arch_id, l):
    '''
    @param lib_id:int - subj (0-based)
    @param arch_id:int - arch id (0-based)
    @param l:int - line to parse
    @return None
    AUTHOR*.GENRE*.TITLE.[SERIES].[SERNO].FILE.SIZE.LIBID.[DEL].EXT.DATE.[LANG].[RATE].[KEYWORDS]
    '''
    #print l
    global book_id
    fb2 = l.split("\004")
    # 1. lang
    lang_id = try_add(lang, fb2[11].upper(), sql_lang)
    # 2. series
    series_id = try_add(series, fb2[3], sql_series)
    # 3. book
    out_sql(sql_book, (
        book_id,
        arch_id,
        screen_quote(fb2[2]),
        str(series_id) if series_id else 'NULL',
        fb2[4] if fb2[4] else 'NULL',
        int(fb2[5]),
        int(fb2[6]),
        1 if fb2[8] == '1' else 0,
        fb2[10],
        lang_id,
        fb2[12] if fb2[12] else 'NULL'
    ))
    # 4. authors 
    for i in split_by_colon(fb2[0]):
        id = try_add(author, i, sql_author)
        if id:
            out_sql(sql_book_authors, (book_id, id))
    # 4.1. authors
    # 5. genres
    for i in split_by_colon(fb2[1]):
        id = try_add(genre, i, sql_genre)
        if id:
            out_sql(sql_book_genres, (book_id, id))
    book_id += 1

def parse_inp (lib_id, z, fn):
    '''
    TODO: patches (replaces)
    @param lib_id:int - subj (0-based)
    @param id:int - arch id (0-based)
    @param z:zipfile - archive
    @param fn:str - filename (something.inp)
    @return None
    '''
    global arch_id
    out_sql(sql_arch, (arch_id, lib_id, fn.rstrip('.inp')))
    inp = z.open(fn)
    #print "== %s ==" % fn
    for line in inp.readlines():
        parse_line(lib_id, arch_id, line.rstrip("\n"))
        #break

def parse_inpx (lib_id, lib):
    '''
    Parse an *.inxp file
    @param lib_id:int - lib id (0-based)
    @param lib:tuple - lib info
    @return None
    '''
    #print "= %s =" % lib[0]
    global arch_id
    out_sql(sql_lib, (lib_id, lib[0], lib[1], lib[2], lib[3], lib[4]))
    z = zipfile.ZipFile(lib[2], 'r')
    filelist = z.namelist()
    filelist.sort()
    for fn in filelist:
        if fn.endswith('.inp'): # filter non-imp
            parse_inp(lib_id, z, fn)
            arch_id += 1

def main ():
    out_sql('BEGIN;%s', '')
    for lib_id, lib in enumerate(libs):
        parse_inpx(lib_id+1, lib)
    out_sql('COMMIT;%s', '')

if (__name__ == '__main__'):
    main()
