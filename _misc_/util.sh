#!/bin/sh
# Utility scripts

usage() {
    echo "Usage: $0 {dl|df|ll|lf|ml|mf|rl|rf}"
}

dl() {
    # Download librusec
    rm sql/l/*.sql.gz
    for t in libavtor libavtors libbook libgenre libgenremeta libgenres libjoinedbooks libmag libmags libseq libseqs;
    do
        n=1000; while ! wget -q -P sql/l -t0 -c http://lib.rus.ec/sql/$t.sql.gz; do if (let "$n<0") then break; fi; sleep 10s; n=$((n-1)); done;
    done
}

df() {
    # Download flibusta
    rm sql/f/*.sql.gz
    for t in libavtor libtranslator libavtoraliase libavtorname libbook libfilename libgenre libgenrelist libjoinedbooks librate libseqname libseq libsrclang
    do
        n=1000; while ! wget -q -P sql/f -t0 -c http://flibusta.is/sql/lib.$t.sql.gz; do if (let "$n<0") then break; fi; sleep 10s; n=$((n-1)); done;
    done
}

ll() {
    # Load librusec original DB into local DB
    for i in `grep -v ^# lre.lst`
    do
        echo $i
        gunzip -c sql/l/$i | mysql -ulibrusec -plibrusec librusec
    done
}

lf() {
    # Load flibusta original DB into local DB
    for i in `grep -v ^# fn.lst`
    do
        echo "$i"
        gunzip -c  sql/f/$i | mysql -uflibusta -pflibusta flibusta
    done
}

ml() {
    # Dump librusec DB (30")
    (echo "BEGIN;"; mysqldump -ulibrusec -plibrusec librusec; echo "COMMIT;") | gzip > librusec.sql.gz
}

mf() {
    # Dump flibusta DB
    mysqldump -uflibusta -pflibusta flibusta | gzip > flibusta.sql.gz
}

rl() {
    # Restore librusec DB (5')
    gunzip -c librusec.sql.gz | mysql -ulibrusec -plibrusec librusec
}

rf() {
    # Restore flibusta DB
    gunzip -c  flibusta.sql.gz | mysql -uflibusta -pflibusta flibusta
}

case "$1" in
dl)
    dl
    ;;
df)
    df
    ;;
ll)
    ll
    ;;
lf)
    lf
    ;;
ml)
    ml
    ;;
mf)
    mf
    ;;
rl)
    rl
    ;;
rf)
    rf
    ;;
*)
    usage
    ;;
esac
