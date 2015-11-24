#!/bin/sh
for i in `grep -v ^# lre.lst`
do
    echo $i
    gunzip -c sql/lre/$i | mysql -ulibrusec -plibrusec librusec
done
