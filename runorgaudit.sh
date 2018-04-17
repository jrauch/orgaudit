#!/bin/sh

DATEDIR=$(date +%Y%m%d%H%M)
OUTDIR="results/$DATEDIR.html"

if [ ! -e orgaudit.env ]
then
	virtualenv orgaudit.env
	. orgaudit.env/bin/activate
	pip install -r requirements.txt
fi

if [ ! -e results ]
then
	mkdir results
fi

. orgaudit.env/bin/activate
python ./orgaudit.py $1 > $OUTDIR
