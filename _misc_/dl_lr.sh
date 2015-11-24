#!/bin/sh
#
# Script to download and restore original lib.rus.ec MySQL database files
# Part of MHL

rm sql/lre/*.sql.gz
for t in libavtor libavtors libbook libgenre libgenremeta libgenres libjoinedbooks libmag libmags libseq libseqs;
do
    n=1000; while ! wget -q -P sql/lre -t0 -c http://lib.rus.ec/sql/$t.sql.gz; do if (let "$n<0") then break; fi; sleep 10s; n=$((n-1)); done;
done
