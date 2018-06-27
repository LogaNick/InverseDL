#!/bin/bash

while read url ; do
    echo "fetching $url"
    curl "$url"
done < url.txt

mkdir smallNORB

echo "Done fetching archive files. Extracting..."

for archive in ./*.gz ; do
    gzip -d "$archive"
done

for archive in smallnorb*; do
    mv "$archive" ./smallNORB/
done

echo "Done!"
