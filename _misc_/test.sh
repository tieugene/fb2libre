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
# replaces
#CMD="(SELECT BadId, GoodId FROM libjoinedbooks WHERE GoodId = realId OR realId IS NULL) UNION (SELECT BadId, realId FROM libjoinedbooks WHERE GoodId <> realId AND realId IS NOT NULL) ORDER BY BadId LIMIT 100;"
# Autthors self aliase:
#CMD="SELECT * FROM libavtoraliase WHERE GoodId = BadId"
# f.Authors repl cascade:
#CMD="SELECT * FROM libavtoraliase a JOIN libavtoraliase b ON a.GoodId = b.BadId WHERE a.GoodId <> a.BadId AND b.GoodId <> b.BadId ORDER BY a.BadId LIMIT 50;"
# l.Books repl cascade
#CMD="SELECT * FROM libjoinedbooks a JOIN libjoinedbooks b ON a.GoodId = b.BadId WHERE a.GoodId <> a.BadId AND b.GoodId <> b.BadId ORDER BY a.BadId LIMIT 50;"
# l.Authors repl cascade
#CMD="SELECT a.aid, a.main, b.main FROM libavtors a JOIN libavtors b ON a.main = b.aid WHERE b.main <> 0 ORDER BY a.aid LIMIT 50;"
# f.libjoinedbooks repl w/ self
#CMD="SELECT * FROM libjoinedbooks WHERE BadId = GoodId OR BadId = realId ORDER BY BadID;"
#CMD="SELECT *  FROM libjoinedbooks WHERE BadId = 321262;"
# f.libjoinedbooks repl cascade
# - realId
CMD="SELECT a.BadId, a.GoodId, a.realId, b.GoodId, b.realId FROM libjoinedbooks a JOIN libjoinedbooks b ON a.realId = b.BadId WHERE a.BadId <> a.realId ORDER BY a.BadId LIMIT 50;"
# - GoodId
# CMD="SELECT a.BadId, a.GoodId, a.realId, b.GoodId, b.realId FROM libjoinedbooks a JOIN libjoinedbooks b ON a.GoodId = b.BadId WHERE (a.GoodId = a.realId OR a.realId IS NULL) AND a.BadId <> a.GoodId AND a.BadId <> a.realId ORDER BY a.BadId LIMIT 50;"
# - Together
#CMD="(SELECT a.BadId, a.GoodId, a.realId, b.GoodId, b.realId FROM libjoinedbooks a JOIN libjoinedbooks b ON a.realId = b.BadId WHERE a.BadId <> a.realId) UNION (SELECT a.BadId, a.GoodId, a.realId, b.GoodId, b.realId FROM libjoinedbooks a JOIN libjoinedbooks b ON a.GoodId = b.BadId WHERE (a.GoodId = a.realId OR a.realId IS NULL) AND a.BadId <> a.GoodId AND a.BadId <> a.realId) LIMIT 50;"
# - Result
CMD="SELECT COUNT(*) FROM ((SELECT a.BadId, a.GoodId, a.realId, b.GoodId, b.realId FROM libjoinedbooks a JOIN libjoinedbooks b ON a.realId = b.BadId WHERE a.BadId <> a.realId) UNION (SELECT a.BadId, a.GoodId, a.realId, b.GoodId, b.realId FROM libjoinedbooks a JOIN libjoinedbooks b ON a.GoodId = b.BadId WHERE (a.GoodId = a.realId OR a.realId IS NULL) AND a.BadId <> a.GoodId AND a.BadId <> a.realId));"
$FN "$CMD"
