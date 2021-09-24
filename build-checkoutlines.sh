#!/usr/bin/env sh

set -e

family=SourceSerif4
optical_sizes=(Caption SmText Text Subhead Display)
roman_weights=(ExtraLight Light Regular Semibold Bold Black)
italic_weights=(ExtraLightIt LightIt It SemiboldIt BoldIt BlackIt)

# get absolute path to bash script
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null && pwd )"

function checkout_lines {
	local slope=${1}
	local opsz=${2}
	local weight=${3}
	font_dir=$DIR/$slope/Instances/$opsz/$weight
	font_ufo=$font_dir/font.ufo
	if [[ $opsz == 'Text' ]]
		# the 'Text' styles do not include their opsz name
		then ps_name=$family-$weight
	fi
	echo "Running checkoutlinesufo ..."
    checkoutlinesufo -e \
        -g verticallinecmb,verticallinecmb.cap,dotabovertcmb,dotabovertcmb.cap,overticalline,Overticalline,Overticalline.sc,odotabovert,Odotabovert,Odotabovert.sc,Odotabovertacute,odotabovertacute,Odotabovertacute.sc,Odotabovertgrave,odotabovertgrave,Odotabovertgrave.sc,Odotabovertcircumflex,odotabovertcircumflex,Odotabovertcircumflex.sc,Odotabovertmacron,odotabovertmacron,Odotabovertmacron.sc,Odotabovertbreve,odotabovertbreve,Odotabovertbreve.sc,Odotabovertverticalline,odotabovertverticalline,Odotabovertverticalline.sc,Odotabovertcaron,odotabovertcaron,Odotabovertcaron.sc,N.sups.sc \
        $font_ufo
    echo "Running psautohint ..."
    psautohint $font_ufo
	echo "Done with $ps_name"
	echo ""
	echo ""
}

for s in ${optical_sizes[@]}
do
	for w in ${roman_weights[@]}
	do
		checkout_lines Roman $s $w
	done
done

for s in ${optical_sizes[@]}
do
	for w in ${italic_weights[@]}
	do
		checkout_lines Italic $s $w
	done
done
