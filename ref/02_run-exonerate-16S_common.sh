#!/bin/bash
# Install exonerate first with conda.
# $ conda -c bioconda exonerate

COMMON_FA=$(dirname $0)"/16S_common.oligos.fa"

REF_FA=$1

OUT="16S_common."${REF_FA/.fa/}".vulgar"
echo "$COMMON_FA -> $REF_FA -> $OUT"

exonerate $COMMON_FA $REF_FA | grep ^vulgar > $OUT
