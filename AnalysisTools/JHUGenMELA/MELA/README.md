# Instruction for using JHUGenMELA/MELA

1. Define the environment variable 

```
SCRAM_ARCH
```

to one of the slc folders in MELA/data.

* If you are using CMS software, this step can be skipped.

2. Compile using

```
./setup.sh -j N # (N being the number of cores to compile, or blank for max. allowed)
```

* The script decides whether to use standalone computation or integration to experimental software.
* Either the one in this folder, or that in the main JHUGenMELA folder works; they do the same thing.
* Feedback on how this script works in different environments is appreciated.
