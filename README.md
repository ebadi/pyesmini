## PyEsmini
Python wrapper for [Environment Simulator Minimalistic (esmini)](https://github.com/esmini/esmini).

To build on Ubuntu, simply run the following command that downloads the codes and resources and builds the esmini's shared objects:
```
./build.sh
```

A sample Python code:
```
XOSCFILE = "resources/xosc/pedestrian.xosc"
pyesmini = PyEsmini(XOSCFILE)
print(">>> First object name: ", pyesmini.getObjectName(0))

for i in range(500):
    pyesmini.step()
```

Please check [examples](examples/) directory for example codes and [documentations](/docs).

#### Credits

This work is done by [Infotiv AB](https://www.infotiv.se) under [VALU3S](https://valu3s.eu/) project. This project has received funding from the [ECSEL](https://www.ecsel.eu) Joint Undertaking (JU) under grant agreement No 876852. The JU receives support from the European Union’s Horizon 2020 research and innovation programme and Austria, Czech Republic, Germany, Ireland, Italy, Portugal, Spain, Sweden, Turkey.

[PyEsmini](https://github.com/ebadi/pyesmini) project is started and currently maintained by Hamid Ebadi.