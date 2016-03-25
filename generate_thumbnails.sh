#! /bin/sh

cd static/gallery
mogrify -resize 500x500 -path thumbs *.*
