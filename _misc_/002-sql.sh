#!/bin/sh
# check and prepare flibusta and librusec databases
# modes: quiet, interactive, auto
# TODO: chk_* += show_*

FN=flibusta
LR=librusec

usage() {
        echo $"Usage: $1 <option>
        Options:
	lc	Librusec check
	ld	Librusec clean
"
}

do_mysql() {
	mysql -u$1 -p$1 $1 -sse "$2"
}

cnt() {
	# db, table
	do_mysql $1 "SELECT COUNT(*) FROM $2;"
}

ask_orphan() {
	# db, srctable, srccolumn dsttable, dst_columnt
	#echo "SELECT COUNT(*) FROM $2 LEFT JOIN $4 ON $2.$3 = $4.$5 WHERE $4.$5 IS NULL;"
	do_mysql $1 "SELECT COUNT(*) FROM $2 LEFT JOIN $4 ON $2.$3 = $4.$5 WHERE $4.$5 IS NULL;"
}

del_orphan() {
	# db, srctable, srccolumn dsttable, dst_columnt
	do_mysql $1 "DELETE $2 FROM $2 LEFT JOIN $4 ON $2.$3 = $4.$5 WHERE $4.$5 IS NULL;"
}

chk_librusec() {
	echo "-- chk"
	echo -n "--- libbook:		";	cnt $LR libbook
		echo -n "---- repl..d & Del:	"
			do_mysql $LR "SELECT COUNT(bid) FROM libbook JOIN libjoinedbooks ON libbook.bid = libjoinedbooks.BadId WHERE libbook.Deleted = 1;"
		echo -n "---- repl..d & !Del:	"
			do_mysql $LR "SELECT COUNT(bid) FROM libbook JOIN libjoinedbooks ON libbook.bid = libjoinedbooks.BadId WHERE libbook.Deleted != 1;"
			# 1. Штоле replaced and Deleted - это "заменена на"?
		echo -n "---- !repl..d & Del:	"	# никакого эффекта
			do_mysql $LR "SELECT COUNT(bid) FROM libbook LEFT JOIN libjoinedbooks ON libbook.bid = libjoinedbooks.BadId WHERE libbook.Deleted = 1 AND libjoinedbooks.BadId IS NULL;"
			# 2. Есть каскадные замены
		# echo -n "---- duplicated md5:	";	nothing
		#	do_mysql $LR "SELECT bid, md5, COUNT(md5) AS counter FROM libbook GROUP BY md5 ORDER BY md5;"
	echo -n "--- libjoinedbooks:	";		cnt $LR libjoinedbooks
		echo -n "---- orphan BadId:	";	ask_orphan $LR libjoinedbooks BadId libbook bid
		echo -n "---- orphan GoodId:	";	ask_orphan $LR libjoinedbooks GoodId libbook bid
		#echo -n "---- non-uniq BadId:	";
		#	do_mysql $LR "SELECT BadId, COUNT(BadId) FROM libjoinedbooks GROUP BY BadId;"
	echo -n "--- libavtor:		";		cnt $LR libavtor
		echo -n "---- orphan book:	";	ask_orphan $LR libavtor bid libbook bid
		echo -n "---- orphan author:	";	ask_orphan $LR libavtor aid libavtors aid
	echo -n "--- libavtors:		";		cnt $LR libavtors
		echo -n "---- empty:		";	ask_orphan $LR libavtors aid libavtor aid
		echo -n "---- repl..d:		";
			do_mysql $LR "SELECT COUNT(aid) FROM libavtors WHERE main <> 0;"
		echo -n "---- repl..d &!empty:	";
			do_mysql $LR "SELECT COUNT(DISTINCT libavtor.aid) FROM libavtor LEFT JOIN libavtors ON libavtor.aid = libavtors.aid WHERE libavtors.main <> 0;"
		echo -n "---- orphan main:	";
			do_mysql $LR "SELECT COUNT(a.aid) FROM libavtors a LEFT JOIN libavtors b ON a.main = b.aid WHERE a.main <> 0 AND b.aid IS NULL;"
		# TODO: chk cascade replacements
		echo -n "---- repl..d cascade:	";
			do_mysql $LR "SELECT COUNT(a.aid) FROM libavtors a LEFT JOIN libavtors b ON a.main = b.aid WHERE a.main <> 0 AND b.main IS NOT NULL;"
	echo -n "--- libgenre:		";		cnt $LR libgenre
		echo -n "---- orphan book:	";	ask_orphan $LR libgenre bid libbook bid
		echo -n "---- orphan genre:	";	ask_orphan $LR libgenre gid libgenres gid
	echo -n "--- libgenres:		";		cnt $LR libgenres
		echo -n "---- empty:		";	ask_orphan $LR libgenres gid libgenre gid
	echo -n "--- libseq:		";		cnt $LR libseq
		echo -n "---- orphan book:	";	ask_orphan $LR libseq bid libbook bid
		echo -n "---- orphan seq:	";	ask_orphan $LR libseq sid libseqs sid
	echo -n "--- libseqs:		";		cnt $LR libseqs
		echo -n "---- empty:		";	ask_orphan $LR libseqs sid libseq sid
	echo -n "--- libmag:		";		cnt $LR libmag
		echo -n "---- orphan book:	";	ask_orphan $LR libmag bid libbook bid
		echo -n "---- orphan mag:	";	ask_orphan $LR libmag mid libmags mid
		#echo -n "---- non-uniq bid:mid:	";
	echo -n "--- libmags:		";		cnt $LR libmags
		echo -n "---- empty:		";	ask_orphan $LR libmags mid libmag mid
}

cln_librusec() {
echo "-- del"
# libbook: replaced and deleted; non-fb2
echo "--- libjoinedbooks (BadId, GoodId)";
	del_orphan $LR libjoinedbooks BadId libbook bid
	del_orphan $LR libjoinedbooks GoodId libbook bid
echo "--- libavtor (bid, aid)"
	del_orphan $LR libavtor bid libbook bid
	del_orphan $LR libavtor aid libavtors aid
	do_mysql $LR "DELETE * FROM libavtor WHERE role <> 'a';"
echo "--- libavtors (tune replaced, nobook)"
	# clean orphan main
	do_mysql $LR "UPDATE libavtors a SET a.main=0 LEFT JOIN libavtors b ON a.main = b.aid WHERE a.main <> 0 AND b.aid IS NULL;"
	# TODO: tune replaced (recursing)
	# TODO: resolve cascade replace
	# nobook
	#del_orphan $LR libavtors aid libavtor aid	# nobook
echo "--- libgenre (bid, gid)"
	del_orphan $LR libgenre bid libbook bid
	del_orphan $LR libgenre gid libgenres gid
echo "--- libgenres (nobook)"
	del_orphan $LR libgenres gid libgenre gid
echo "--- libseq (bid, sid)"
	del_orphan $LR libseq bid libbook bid
	del_orphan $LR libseq sid libseqs sid
echo "--- libmag (bid, mid)"
	del_orphan $LR libmag bid libmags mid
	del_orphan $LR libmag mid libmags mid
echo "--- libseqs (nobook)"
	del_orphan $LR libseqs sid libseq sid
echo "--- libmags (nobook)"
	del_orphan $LR libmags mid libmag mid
}

case "$1" in
lc)
	chk_librusec
	;;
ld)
	cln_librusec
	;;
*)
	usage $0
        RETVAL=1
esac
