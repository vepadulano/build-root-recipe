# Building ROOT for ROOT developers, step by step

## 1. Forking the `root` and `roottest` repositories

You need to have your own forks of the repositories in order to propose
modifications in the form of GitHub PRs. In some cases the modifications will
need to go in `roottest`, so it's better to clone both. Go on the respective
websites:

* https://github.com/root-project/root
* https://github.com/root-project/roottest

And click on the `Fork` button in the top right of the web UI.

## 2. Clone the repositories and track the upstream git remote

You can now clone both repositories on your machine, e.g. via

```
$: git clone https://github.com/YOURUSERNAME/root
$: git clone https://github.com/YOURUSERNAME/roottest
```

## 3. Create a build and install directories

To keep things clean, it is suggested to create a separate directory for the
build and for the installation.

```
$: mkdir mybuild myinstall
```

## 4. Configure the CMake build

There are many [configuration options](https://root.cern/install/build_from_source/#all-build-options).
For the purposes of development and testing, the following configuration is
suggested:

```
$: cmake -DCMAKE_BUILD_TYPE=RelWithDebInfo -Dtesting=ON -Droottest=ON -DCMAKE_INSTALL_PREFIX=myinstall -B mybuild -S root
```
The process of launching the Cmake build may be sped up by using the ccache package, if it is installed in the system. To activate it, add `-Dccache=ON` to variables.

## 5. Build and install

Finally, you can launch the CMake build via:

```
$: cmake --build mybuild --target install -jNPROC
```

Where `NPROC` is the number of available cores you want to send in parallel for the build.
