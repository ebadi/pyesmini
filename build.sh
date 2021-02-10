#!/bin/bash
sudo apt install build-essential git pkg-config libgl1-mesa-dev libpthread-stubs0-dev libjpeg-dev libxml2-dev libpng-dev libtiff5-dev libgdal-dev libpoppler-dev libdcmtk-dev libgstreamer1.0-dev libgtk2.0-dev libcairo2-dev libpoppler-glib-dev libxrandr-dev libxinerama-dev curl cmake

git clone https://github.com/esmini/esmini.git esmini
cd esmini
git checkout b772909dae9205aaacccd2692dc42599888afa57 # 1st Feb 2021 = esmini 2.1.5 (build 1108)
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
