#!/bin/bash
# Written by gao on 20180416

set -e
BUILDDIR=build
rm -rf $BUILDDIR
if [ ! -f $BUILDDIR ]; then
    mkdir -p $BUILDDIR
fi
pushd $BUILDDIR
cmake ..
make VERBOSE=1 -j 1
ln -fs `pwd`/lib/AQctpmd.so ../AQctpmd/test/AQctpmd.so
ln -fs `pwd`/lib/AQctptd.so ../AQctptd/test/AQctptd.so
cp ../AQctpmd/test/AQctpmd.* ../
cp ../AQctptd/test/AQctptd.* ../
popd
