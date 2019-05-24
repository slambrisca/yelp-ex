#!/usr/bin/env bash

dir=`dirname "$1"`
workdir=`basename "$dir"`
filename=`basename "$1"`

docker run -v $dir:/$workdir yelpex python app.py /$workdir/$filename
