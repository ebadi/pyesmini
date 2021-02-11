#!/bin/bash
sudo apt install build-essential git pkg-config libgl1-mesa-dev libpthread-stubs0-dev libjpeg-dev libxml2-dev libpng-dev libtiff5-dev libgdal-dev libpoppler-dev libdcmtk-dev libgstreamer1.0-dev libgtk2.0-dev libcairo2-dev libpoppler-glib-dev libxrandr-dev libxinerama-dev curl cmake

git clone git@github.com:ebadi/esmini.git esmini # dev repo
cd esmini
git checkout dev # dev branch
mkdir build
cd build
cmake ../ -DUSE_OSG=true -DCMAKE_BUILD_TYPE=Release
make -j4 install
cd ../../
cp ./esmini/build/EnvironmentSimulator/Libraries/esminiRMLib/libesminiRMLib.so pyesmini/libesminiRMLib.so
cp ./esmini/build/EnvironmentSimulator/Libraries/esminiLib/libesminiLib.so pyesmini/libesminiLib.so
cp -r esmini/resources/ .

python3 tests/pyesmini_tests.py
python3 tests/pyesminiRM_tests.py
