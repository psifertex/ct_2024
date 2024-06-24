#!/bin/bash

if [ "$1" == "build" ]
then
  BUILD="--static slides"
else
  BUILD="--watch"
fi

SCRIPT=$(realpath "$0")
SP=$(dirname "$SCRIPT")

docker run --rm -p 1948:1948 -p 35729:35729 \
	-v "$SP":/slides \
	-v "$SP"/images:/images \
	webpronl/reveal-md:latest /slides $BUILD \
	--glob './*.md';


if [ "$1" == "build" ]
then
  rm -f firmware_hacking_2.zip
  zip -r firmware_hacking_2.zip samples slides
fi
