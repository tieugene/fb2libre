#!/bin/sh
# test
FN="mysql -uflibusta -pflibusta flibusta -se"
LR="mysql -ulibrusec -plibrusec librusec -se"
#CMD="SELECT DISTINCT Ver FROM libbook ORDER BY Lang;"
#CMD="SELECT DISTINCT LastName, FirstName, MiddleName FROM libavtorname;"
#CMD="SELECT COUNT(*) FROM libavtorname;"
#CMD="SELECT COUNT(*) FROM libavtor WHERE aid=11;"
#CMD="SELECT DISTINCT BadId FROM libavtoraliase;"
# сколько книг у замененных авторов
#CMD="SELECT libavtors.aid, libavtor.bid FROM libavtors LEFT JOIN libavtor ON libavtors.aid = libavtor.aid WHERE libavtors.main <> 0;"
#CMD="SELECT libmags.* FROM libmags LEFT JOIN libmag ON libmags.mid = libmag.mid WHERE libmag.mid IS NULL;"
#CMD="SELECT libgenres.* FROM libgenres LEFT JOIN libgenre ON libgenres.gid = libgenre.gid WHERE libgenre.gid IS NULL;"
#CMD="SELECT DISTINCT role FROM libavtor;"
#CMD="SELECT a.aid, a.main FROM libavtors a LEFT JOIN libavtors b ON a.main = b.aid WHERE a.main <> 0 AND b.main IS NOT NULL ORDER BY a.aid;"
#CMD="SELECT DISTINCT main FROM libavtors WHERE aid = 283;"
#CMD="SELECT a.aid, b.aid FROM libavtors a LEFT JOIN libavtors b ON a.main = b.aid WHERE b.aid <> 0 ORDER BY a.aid LIMIT 50;"
#CMD="(SELECT BadId, GoodId FROM libjoinedbooks WHERE GoodId = realId OR realId IS NULL) UNION (SELECT BadId, realId FROM libjoinedbooks WHERE GoodId <> realId AND realId IS NOT NULL) ORDER BY BadId LIMIT 100;"
# Auto aliase:
CMD="SELECT * FROM libavtoraliase WHERE GoodId = BadId"
$FN "$CMD"
