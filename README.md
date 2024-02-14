# HexUtils

HexUtils is a coherent framework assembled by the Higgs group at Johns Hopkins University, comprised of mostly Python-based tools which are actively maintained for use in our research and designed to be compatible with the CJLST framework for H → ZZ → 4l. 

The wiki pages in this repository are meant to orient new users as well as provide detailed instructions for use of these tools in physics analyses. 

Keep in mind that this framework can be modified to run over any kind of ROOT TTrees, but is intended for OOTB use on trees produced by the CJLST framework. (Please contact one of the members of our group for more information about modification.) Also note that while HexUtils is maintained by the Higgs group at JHU, it is entirely independent from JHUGen which is our model-independent generator of new resonances that produces LHE files of simulated events.

## Installing the framework

Follow these instructions if you are installing these tools on **LXPLUS** or a similar service which has CMSSW releases available. Otherwise, read on. 

1. Copy the install.sh locally.
2. Specify the ```CMSSW_release``` you want to use at the top of install.sh. Currently, **CMSSW_12_2_0** is recommended.
3. Execute ```source install.sh``` to automatically check out the CMSSW release and HexUtils repository, and build everything.

## Use on a machine without CMSSW or CernVM-FS

If you wish, it is possible to use a Docker or Singluarity image file to load a compatible CMSSW container on your local system. We have available for use standalone and cc7-cvmfs-based images, with the latter being compatible with Parrot to bypass the privilege issues associated with accessing /cvmfs through a FUSE module.

If you already have the following dependencies installed, loading a container is not necessary. Simply clone this repository into your working area, compile, and refer to the wiki pages detailing the usage of these utilities.

## Dependencies

All of the tools in this framework can, in principle, be run outside of a CMSSW environment on any machine. To make sure you are using compatible versions of the required dependencies, please refer to the guidelines below. Note that these version numbers are consistent with the CMSSW release which is used for development of this framework, but are not explicitly required. 

- Python 3.9.6
- ROOT 6.22 (with pyROOT compiled for Python3)
- numpy 1.17.5
- root-numpy 4.8.0
- tqdm 4.62.2 (optional but highly recommended)

## Installing on a local machine

The easiest way to install HexUtils on a local machine is to use <a href="https://www.anaconda.com/products/distribution">Anaconda</a>. Personally we recommend the lightweight <a href="https://docs.conda.io/en/latest/miniconda.html">Miniconda</a>, as it isn't as bulky as the full Anaconda system.

Initialize a new Conda environment on your computer (or, if you'd like, you can simply use your current one). Make sure that this environment has an instance of Python with a version $\geq$ 3.9. Then do the following commands:

Install the dependencies listed <a href="https://root.cern/install/dependencies/">here</a> for ROOT for your given operating system. Afterwards, do the following on conda.

```console
conda install numpy
conda install -c conda-forge root=6.22 root_numpy=4.8.0 tqdm
```

**DON'T BE WORRIED IF THIS TAKES SOME TIME!** Conda can be slow at times, but it should all work out in the end.

To check your installation, run the following in your terminal:
```console
conda list
```

This command should list all the installed packages and dependencies that you have installed in your current environment. If you see all the packages you need, the installation was successful!


 After installing these dependencies, *wget* the <a href="https://raw.githubusercontent.com/hexutils/HexUtils/main/install.sh">install.sh</a> file to the directory you would like to place HexUtils (make sure to give it permissions with *chmod*!), and run the installer. The following commands should work here:
 ```console
 wget https://raw.githubusercontent.com/hexutils/HexUtils/main/install.sh
 chmod 777 install.sh
 ./install.sh
 ```

 Follow any additional directions the installer gives you and it should all work out for you!
 
 After installing, make sure to run
 ```console
 source install.sh
 ```
in the directory where you initially called it to install the file - this will make sure all the necessary paths are configured!
