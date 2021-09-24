#!/bin/bash

# get absolute path to bash script
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null && pwd )"

# clean existing build artifacts and rebuild output directories
otf_dir="$DIR/target/OTF"
ttf_dir="$DIR/target/TTF"
var_dir="$DIR/target/VAR"

woff_dir="$DIR/target/WOFF"
woff_otf_dir="$woff_dir/OTF"
woff_ttf_dir="$woff_dir/TTF"
woff_var_dir="$woff_dir/VAR"
rm -rf $woff_dir

woff2_dir="$DIR/target/WOFF2"
woff2_otf_dir="$woff2_dir/OTF"
woff2_ttf_dir="$woff2_dir/TTF"
woff2_var_dir="$woff2_dir/VAR"
rm -rf $woff2_dir

rm -rf $var_dir/*.woff
rm -rf $var_dir/*.woff2
mkdir -p $woff_otf_dir $woff_ttf_dir $woff_var_dir $woff2_otf_dir $woff2_ttf_dir $woff2_var_dir

for filename in ${otf_dir}/*.otf; do
    [ -e "$filename" ] || continue
    sfnt2woff $filename
    woff2_compress $filename
    f="$(basename -- $filename)"
    mv ${filename/otf/woff} $woff_otf_dir/$f.woff
    mv ${filename/otf/woff2} $woff2_otf_dir/$f.woff2
done

for filename in ${ttf_dir}/*.ttf; do
    [ -e "$filename" ] || continue
    sfnt2woff $filename
    woff2_compress $filename
    f="$(basename -- $filename)"
    mv ${filename/ttf/woff} $woff_ttf_dir/$f.woff
    mv ${filename/ttf/woff2} $woff2_ttf_dir/$f.woff2
done

for filename in ${var_dir}/*.otf; do
    [ -e "$filename" ] || continue
    sfnt2woff $filename
    woff2_compress $filename
    f="$(basename -- $filename)"
    mv ${filename/otf/woff} $woff_var_dir/$f.woff
    mv ${filename/otf/woff2} $woff2_var_dir/$f.woff2
done

for filename in ${var_dir}/*.ttf; do
    [ -e "$filename" ] || continue
    sfnt2woff $filename
    woff2_compress $filename
    f="$(basename -- $filename)"
    mv ${filename/ttf/woff} $woff_var_dir/$f.woff
    mv ${filename/ttf/woff2} $woff2_var_dir/$f.woff2
done
