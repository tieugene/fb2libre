#!/bin/env python
# -*- coding: utf-8 -*-
'''
Tool to parse inpx'
Result:
* a.txt - authors
* g.txt - genres
* l.txt - lang
* s.txt - series
'''

import sys, os, zipfile

reload(sys)
sys.setdefaultencoding('utf-8')

# const
libase = '~/ftp/pub/Lib'
libs = ( # abbr, name, path_to_inpx, path_to_archives
    ('Flibusta.net', os.path.join(libase, 'fb2.Flibusta.Net/flibusta_fb2_local.inpx')),
    ('Lib.rus.ec',   os.path.join(libase, '_Lib.rus.ec - Официальная/librusec_local_fb2.inpx'),
)

# var
author  = set()
genre   = set()
series  = set()
lang    = set()

def split_by_colon (s):
    return s.split(':')

def try_to_add (s, i):
    '''
    s:set
    i:str
    '''
    i = i.strip(' ')
    if ((i) and (i not in s)):
        s.add(i)

def parse_line (l):
    # AUTHOR*.GENRE*.TITLE.[SERIES].[SERNO].FILE.SIZE.LIBID.[DEL].EXT.DATE.[LANG].[RATE].[KEYWORDS]
    #print l
    fb2 = l.split("\004")
    for i in split_by_colon(fb2[0]):    # authors
        try_to_add(author, i)
    for i in split_by_colon(fb2[1]):    # genre
        try_to_add(genre, i)
    try_to_add(series, fb2[3])          # series
    try_to_add(lang, fb2[11].upper())   # lang

def parse_inp (z, fn):
    inp = z.open(fn)
    #print "== %s ==" % fn
    for line in inp.readlines():
        parse_line(line.rstrip("\n"))
        #break

def parse_inpx (path):
    '''
    '''
    z = zipfile.ZipFile(path, 'r')
    filelist = z.namelist()
    filelist.sort()
    for fn in filelist:
        if fn.endswith('.inp'): # filter non-imp
            parse_inp(z, fn)

def out_data (s, fn):
    with open(fn,"w") as f:
        l = list(s)
        l.sort()
        f.write("\n".join(l))

def main ():
    toout = (
        (author, 'a.txt'),
        (genre,  'g.txt'),
        (series, 's.txt'),
        (lang,   'l.txt'),
    )
    for lib in libs:
        print "= %s =" % lib[0]
        parse_inpx(lib[1])
    for s, fn in toout:
        out_data(s, fn)

if (__name__ == '__main__'):
    main()
