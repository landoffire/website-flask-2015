#! /bin/sh

cd static/gallery
mogrify -resize 400x400 -path thumbs *.*
