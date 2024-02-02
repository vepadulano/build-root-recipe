# General guidelines and recipes to create a development environment with ROOT

Developing ROOT requires being able to build the project from source and knowing
which components to configure depending on one's needs. See the following
sections to set up your coding environment with ROOT.

## Prerequisites

ROOT depends on other libraries, some of them are necessary also in the build
process. You can find a list dependencies [on our website](https://root.cern/install/dependencies/).
Follow the instructions to install the dependencies on your system.

## Building ROOT

The ROOT source code is built via [CMake](https://cmake.org/). Usually in a
development environment one would need a build of ROOT with debug symbols, i.e.
`-DCMAKE_BUILD_TYPE=RelWithDebInfo` or `-DCMAKE_BUILD_TYPE=Debug`. Detailed
instructions on how to build ROOT from source are available [on our website](https://root.cern/install/build_from_source/),
but it is also suggested to use the Python script `launch_build.py` available in
this repository.

### The build script

The `launch_build.py` script can help you streamline the building process:

```python
$: python launch_build.py -h
usage: launch_build.py [-h] [--njobs NJOBS] [--name NAME] [--mode {default,debug,relwithdebinfo}] [--opts [OPTS ...]]

options:
  -h, --help            show this help message and exit
  --njobs NJOBS         As in 'cmake -jNJOBS'
  --name NAME           The name of this build. If specified, it takes precedence over the automatic choice for a name
  --mode {default,debug,relwithdebinfo}
                        Build process mode
  --opts [OPTS ...]     List of cmake options. This is exclusive with the choices from the 'mode' option. It is crucial to specify this option with an equal
                        sign and quoted , as in: 'python launch_build.py --opts="-DOpt1=ON -DOpt2=OFF"'
```

It creates the following directories in the curreng working directory:

```
- rootsrc/
- roottest/
- rootbuild/
- rootinstall/
```

* `rootsrc` is the directory where the ROOT source resides. If not already
  present, it will be downloaded.
* `roottest` is the directory where the seoarate testing repository roottest
  source resides. If not already present, it will be downloaded.
* `rootbuild` and `rootinstall` store respectively build and install directories
  produced by CMake. Every time the `launch_build.py` script is launched, it
  creates two separate sub-directories for the current build and installation,
  for example:
  ```
  - rootbuild/
    --> build1/
    --> build2/
  - rootinstall/
    --> install1/
    --> install2/
  ```

The script launches a CMake build with the appropriate flags, depending on
either one of the already available modes (see the `mode` option) or the flags
passed by the `--opts` option. For example:

```
$: python launch_build.py --mode relwithdebinfo
$: python launch_build.py --name mybuild --opts="-Dminimal=ON -DCMAKE_BUILD_TYPE=RelWithDebInfo"
```
