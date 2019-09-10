# Bridge\_A2C

## Requirements
- Python 3.7.3
- Cuda 10.0
- Pytorch 1.2.0

```
# Requirements including pytorch packages

$ pip install -r requirements.txt
```

### Double dummy solver
Use [dds](https://github.com/dds-bridge/dds) and [python-dds](https://github.com/Afwas/python-dds).

#### Procedure
Clone [dds](https://github.com/dds-bridge/dds) and make 'libdds.so'.
```
$ mkdir bridge_env/dds_files
$ cd bridge_env/dds_files
$ git clone https://github.com/dds-bridge/dds

# Then make 'libdds.so'.
# Details are written in dds/INSTALL.
```

Clone [python-dds](https://github.com/Afwas/python-dds). 
```
$ cd bridge_env/dds_files
$ git clone https://github.com/Afwas/python-dds

# Change the directory name for importing python_dds/dds.py in python codes.
$ mv python-dds/ python_dds/
```
Chage the path to the file 'libdds.so' in the file [dds.py](./bridge_env/dds_files/python_dds/examples/dds.py).

```
# bridge_env/dds_files/python_dds/examples/dds.py

from ctypes import *
import os       # addition

base_path = os.path.dirname(os.path.abspath(__file__))      # addition

dds = cdll.LoadLibrary(base_path+"/../../dds/src/libdds.so")    # change
print('Loaded lib {0}'.format(dds))
```
