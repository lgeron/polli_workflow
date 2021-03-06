#!/bin/bash

WD=$PWD
MOSES=$WD/mosesdecoder
GIZA=$WD/giza-pp

mkdir output_source
mkdir output_tgt

# CSV needs to be in the format L1-L2.csv for the pipeline to work! e.g. en-es.csv
CSV=$1
python process_csv.py $CSV > langs.txt
FILE1=$WD/L1.txt
FILE2=$WD/L2.txt
l1=sed '1q;d' $WD/langs.txt
l2=sed '2q;d' $WD/langs.txt
rm $WD/langs.txt

# TOKENIZE

$MOSES/scripts/tokenizer/tokenizer.perl -l $l1 \
    < $FILE1 \
    > tok.$FILE1

$MOSES/scripts/tokenizer/tokenizer.perl -l $l2 \
    < $FILE2 \
    > tok.$FILE2

TFILE1=tok.$FILE1
TFILE2=tok.$FILE2

# ALIGN

cd $GIZA/GIZA++-v2/
./plain2snt.out $WD/$TFILE1 $WD/$TFILE2

sntfile1=${TFILE1}_${TFILE2}.snt
sntfile2=${TFILE2}_${TFILE1}.snt
./snt2cooc.out $WD/$TFILE1.vcb $WD/$TFILE2.vcb $WD/$sntfile1 > corp_st.cooc
./snt2cooc.out $WD/$TFILE2.vcb $WD/$TFILE1.vcb $WD/sntfile2 > corp_ts.cooc

./GIZA++ -S $WD/$TFILE1.vcb -T $WD/$TFILE2.vcb -C $WD/$sntfile1 -CoocurrenceFile $WD/corp_st.cooc -outputpath $WD/output_source

./GIZA++ -S $WD/$TFILE2.vcb -T $WD/$TFILE1.vcb -C $WD/$sntfile2 -CoocurrenceFile $WD/corp_ts.cooc -outputpath $WD/output_tgt

cd $WD
mv output_source/*.VA3.final source_tgt.VA3
mv output_tgt/*.VA3.final tgt_source.VA3
rm -rf output_source
rm -rf output_tgt
rm tok.*

# PYTHON FILES
mv stanford* stanford-postagger

num_lines=$3
python3 va32pos.py source_tgt.VA3 tgt_source.VA3 $num_lines
