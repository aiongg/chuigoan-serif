#!/bin/bash

# get absolute path to bash script
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null && pwd )"

# clean existing build artifacts and rebuild output directories
rm -rf $DIR/target/WOFF
rm -rf $DIR/target/WOFF2
ttf_dir="$DIR/target/TTF"
woff_dir="$DIR/target/WOFF"
woff2_dir="$DIR/target/WOFF2"
mkdir -p $woff_dir $woff2_dir

for filename in ${ttf_dir}/*.ttf; do
    sfnt2woff $filename
    mv ${filename/ttf/woff} $woff_dir
    woff2_compress $filename
    mv ${filename/ttf/woff2} $woff2_dir
done
