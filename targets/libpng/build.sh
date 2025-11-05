#!/bin/bash
set -e
set -x
##
# Pre-requirements:
# - env TARGET: path to target work dir
# - env OUT: path to directory where artifacts are stored
# - env CC, CXX, FLAGS, LIBS, etc...
##

if [ ! -d "$TARGET/repo" ]; then
    echo "fetch.sh must be executed first."
    exit 1
fi


if [[ $FUZZER = *lyso* ]] || [[ $FUZZER = *fishfuzz* ]] || [[ $FUZZER = *fuzzchella* ]] ; then
    export LIBS="-l:magma.o -lrt -l:afl_driver.o -lstdc++ -l:afl-llvm-rt.o"
    echo "LIBS variable set to $LIBS"
fi

if [[ $FUZZER = *reach* ]] ; then
    export LIBS="-l:magma.o -lrt -l:afl_driver.o -lstdc++"
    echo "LIBS variable set to $LIBS"
fi


# build the libpng library
cd "$TARGET/repo"
autoreconf -f -i
./configure --disable-shared
make -j$(nproc) clean

if [[ $FUZZER = *dafl* ]]; then
   yes | $FUZZER/smake/smake --init
   $FUZZER/smake/smake -j$(nproc) libpng16.la
   if [ -d "sparrow" ]; then
      $CXX -E -I. contrib/oss-fuzz/libpng_read_fuzzer.cc -o sparrow/libpng_read_fuzzer.i
      cp -r sparrow $OUT/sparrow
   fi
fi

 
make -j$(nproc) libpng16.la

cp .libs/libpng16.a "$OUT/"


# build libpng_read_fuzzer.
$CXX $CXXFLAGS -std=c++11 -I. \
     contrib/oss-fuzz/libpng_read_fuzzer.cc \
     -o $OUT/libpng_read_fuzzer \
     $LDFLAGS .libs/libpng16.a $LIBS -lz
