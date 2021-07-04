# Install GADGET-4 on Bridges-2

# Useful Resources

## GADGET-4

GADGET-4 page: https://wwwmpa.mpa-garching.mpg.de/gadget4/

GADGET-4 source code: http://gitlab.mpcdf.mpg.de/vrs/gadget4

GADGET-4 manual: https://wwwmpa.mpa-garching.mpg.de/gadget4/gadget4_manual.pdf



## Bridges-2 User Guide

https://www.psc.edu/resources/bridges-2/user-guide-2/



## `module` command

``` bash
module list					         # show all loaded modules
module load <module_name>		   # load module <module_name>
module spider <module_name>		# list all possible version of <module_name>
module show <module_name>		   # show the path of <module_name>
```







# Install GADGET-4 on Bridges-2

## 1. Download GADGET-4 code 

According to [GADGET-4 page]( https://wwwmpa.mpa-garching.mpg.de/gadget4/):

> ## Obtaining the code
>
> The code can be obtained through a public git-repository, hosted by a gitlab server at the Max-Planck Computing and Data Facility (MPCDF). The repository's page is
>
> http://gitlab.mpcdf.mpg.de/vrs/gadget4
>
> To get a cloned repository of the code, you can issue the command:
>
> ```
> git clone http://gitlab.mpcdf.mpg.de/vrs/gadget4
> ```
>
> Note that the gitlab repository site offers to submit questions, or to propose patches to the code via pull requests.

Put the directory `gadget4` to some place on the bridges2, we only build the executable (something like `a.out`) in `/gadget4` directory, we will not put our model (simulation run) in this folder.

## 2. Install Compilation requirements

### 2.1 some non-standard libraries

In the [GADGET-4 manual](https://wwwmpa.mpa-garching.mpg.de/gadget4/gadget4_manual.pdf), we need 6 libraries for compilation: 

1. `mpi`: for parallel programs
2. `gsl`: The GNU scientific library
3. `fftw3`: Fastest Fourier Transform in the West
4. `hdf5`: GADGET-4 read/write the output snapshots files in `hdf5` format
5. `hwloc`: not sure what exact this for,  but `mpi` needs it.
6. `vectorclass`: GADGET-4 needs this one for hydrodynamics

Fortunately, the last one is included in GADGET-4 directory inside `/gadget4/src/vectorclass/`, and all the other except `gsl` have been install on bridges2. So we only need to install `gsl`.



### 2.2 Install gsl

1. **Download gsl** from: https://www.gnu.org/software/gsl/#downloading, under [nearest GNU mirror](https://ftpmirror.gnu.org/gsl/), choose `gsl-2.7.tar.gz` near the bottom (we **don't** need `gsl-2.7.tar.gz.sig` file). 

   Copy the download link of file `gsl-2.7.tar.gz`:  https://mirrors.tripadvisor.com/gnu/gsl/gsl-2.7.tar.gz.

   In bridges2, type: `wget https://mirrors.tripadvisor.com/gnu/gsl/gsl-2.7.tar.gz` to **download** gsl-2.7

   **Extract files** from the tar-ball, type: `tar -xvzf gsl-2.7.tar.gz`

   

2. Build gsl library:

   inside directory `/gsl-2.7`:

   ``` bash
   ./configure --prefix=/jet/home/xli233/usr	# gsl-2.7 will be installed in /jet/home/xli233/usr, choose your own direcotry for this
   
   #... some ouputs
   
   make
   
   #.... some outputs
   
   make install
   
   #..... some outputs and DONE!
   ```

   We will need the contents inside the directory behind `--prefix=`, later.



###  2.3 Load other dependencies 

For they other required modules, we just load the modules in bridges2:

``` bash
# module
module load intelmpi/20.4-intel20.4		# mpi
module load fftw/3.3.8				      # fftw3
module load hdf5/1.12.0-intel20.4		# hdf5 
module load anaconda3/2020.11		      # anaconda3 for python3, this is optional
```

You should put above lines into the `~/.bashrc` file, and do `source ~/.bashrc`. After that, these modules will be automatically loaded each time you log in bridges2.



Now all we get all dependencies for compiling GADGET-4



## 3. Configure GADGET-4 `Makefile`

This part basically followed the section of **Building the code** in [GADGET-4 manual](https://wwwmpa.mpa-garching.mpg.de/gadget4/gadget4_manual.pdf). We need to modify the `Makefile` in `/gadget4` to tell GADGET-4 where the path of those libraries we have in step2. 

**Everything did here is inside the gadget4 directory.**

### 3.1 Configure Makefile.systype`

1. make a copy from `Template-Makefile.systype`:

   ``` bash
   cp Template-Makefile.systype Makefile.systype
   ```

2. Inside `Makefile.systype`, create a system type for bridges2.

   ```bash
   # Select Target Computer
   #
   # Please copy this file to Makefile.systype and uncomment your
   # system. Don't commit changes to this file unless you add support for
   # a new system.
   
   SYSTYPE="Bridges2"
   
   #SYSTYPE="Generic-gcc"
   #SYSTYPE="Generic-intel"
   #SYSTYPE="Generic-gcc-single"
   #SYSTYPE="Generic-intel-single"
   #SYSTYPE="Darwin"
   #SYSTYPE="Magny"
   #SYSTYPE="gcc-paranoia"
   #SYSTYPE="libs"
   #SYSTYPE="hydra"
   #SYSTYPE="bwforcluster"
   ```



### 3.2 Configure `Makefile`

Inside `Makefile`

1. Change Python path (in line 97):

   Since there are both `python2` and `python3` installed on bridges2, we need to specify which we use in GADGET-4 (here I use `python3`)

   Change (line 97) **from**:

   ``` bash
   PYTHON   = /usr/bin/python
   ```

   **to**

   ``` bash
   PYTHON   = /usr/bin/python3
   ```

   or

   ``` bash
   PYTHON   = /opt/packages/anaconda3/bin/python		# if you loaded anaconda3 module
   ```

2. Add system type `Bridges2`

   below `#define available Systems#`, add:

   ```makefile
   ifeq ($(SYSTYPE),"Bridges2")
   # compliers
   CC       =  mpicc   -std=c11      # sets the C-compiler
   CPP      =  mpicxx  -std=c++11    # sets the C++-compiler
   OPTIMIZE =  -ggdb -O3 -march=native  -Wall -Wno-format-security
   
   # the paths of libraries from step2
   GSL_INCL   = -I/jet/home/xli233/usr/gsl-2.7/include		# change this to your direcotries
   GSL_LIBS   = -L/jet/home/xli233/usr/gsl-2.7/lib		      # change this to your direcotries
   
   FFTW_INCL  = -I/jet/packages/spack/opt/spack/linux-centos8-zen/gcc-8.3.1/fftw-3.3.8-bx5uvjft5olrdheauq2yqu3z5yhkmlj2/include
   FFTW_LIBS  = -L/jet/packages/spack/opt/spack/linux-centos8-zen/gcc-8.3.1/fftw-3.3.8-bx5uvjft5olrdheauq2yqu3z5yhkmlj2/lib
   HDF5_INCL  = -I/opt/packages/hdf5/hdf5-1.12.0/INTEL/include
   HDF5_LIBS  = -L/opt/packages/hdf5/hdf5-1.12.0/INTEL/lib
   HWLOC_INCL = -I/jet/packages/spack/opt/spack/linux-centos8-zen/gcc-8.3.1/hwloc-1.11.11-cwrbfukoux5el2tykg525q7gidypgunz/include
   HWLOC_LIBS = -L/jet/packages/spack/opt/spack/linux-centos8-zen/gcc-8.3.1/hwloc-1.11.11-cwrbfukoux5el2tykg525q7gidypgunz/lib
   
   endif
   ```

   **Note:**

   In the first line `ifeq ($(SYSTYPE),"Bridges2")`, name `Bridges2` must be **IDENTICAL** to what we added in `Makefile.systype` in step 3.1.2.

   `GSL_INCL` and `GSL_LIBS` are `include` and `lib` directories inside where you installed gsl (the path after `--prefix=` in step 2.2). You should change this to your own path.

   All other libraries path I found in bridges2 should be valid for you too, just copy and past to your `Makefile`





# Test GADGET-4

Inside `/gadget4/examples/CollidingGalaxiesSFR`, copy `Config.sh` to `/gadget4`, and type

``` bash
make
```

if there was no error and an executable file `Gadget4` appeared in `/gadget4` after `make` then ***you are ready to rock***! 🤘



# Run GADGET-4 on bridges2

Seems all compute partition is not available now, I need to check this later.

