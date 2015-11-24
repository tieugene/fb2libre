#!/bin/sh
for i in `grep -v ^# fn.lst`
do
    echo "$i"
    gunzip -c  sql/fn/$i | mysql -uflibusta -pflibusta flibusta
done
