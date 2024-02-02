import argparse
import os
import re
import shlex
import subprocess
from typing import Iterable


def create_directories_if_necessary() -> Iterable[str]:
    cwd = os.getcwd()
    root_home = os.path.join(cwd, "rootsrc")
    if not os.path.exists(root_home):
        subprocess.run(shlex.split(
            "git clone https://github.com/root-project/root.git rootsrc"), check=True)
    if not os.path.exists(os.path.join(cwd, "roottest")):
        subprocess.run(shlex.split(
            "git clone https://github.com/root-project/roottest.git"), check=True)
    root_build = os.path.join(cwd, "rootbuild")
    if not os.path.exists(root_build):
        os.mkdir(root_build)
    root_install = os.path.join(cwd, "rootinstall")
    if not os.path.exists(root_install):
        os.mkdir(root_install)

    return root_home, root_build, root_install


build_opts = {
    "default": "-DCMAKE_BUILD_TYPE=RelWithDebInfo",
    "debug": (
        "-DCMAKE_BUILD_TYPE=Debug -Dtesting=ON -Droottest=ON "
        "-Dtest_distrdf_pyspark=ON -Dtest_distrdf_dask=ON"
    ),
    "relwithdebinfo": (
        "-DCMAKE_BUILD_TYPE=RelWithDebInfo -Dtesting=ON -Droottest=ON "
        "-Dtest_distrdf_pyspark=ON -Dtest_distrdf_dask=ON"
    ),
}

parser = argparse.ArgumentParser()
parser.add_argument("--njobs", help="As in 'cmake -jNJOBS'",
                    default=os.cpu_count(), type=int)
parser.add_argument(
    "--name", help=("The name of this build. If specified, it takes "
                    "precedence over the automatic choice for a name"))
parser.add_argument("--mode", help="Build process mode",
                    choices=list(build_opts.keys()), default="default")
parser.add_argument("--opts", help=(
    "List of cmake options. This is exclusive with the choices from the 'mode' "
    "option. It is crucial to specify this option with an equal sign and quoted "
    ", as in: 'python launch_build.py --opts=\"-DOpt1=ON -DOpt2=OFF\"'"
),
    nargs="*")
args = parser.parse_args()
print(args.opts)


def launch_build():

    root_home, root_build, root_install = create_directories_if_necessary()

    if args.name is None:
        # Figure out a sensible name to give to the build/install directories
        p = subprocess.run(["git", "status"], cwd=root_home,
                           check=True, capture_output=True)
        gitstatus = p.stdout.decode()
        pattern = re.compile("^On branch (?P<branch>.*)")
        branch = pattern.match(gitstatus).groupdict()["branch"]

        if branch == "master":
            # Further specify builds on the master branch with the commit SHA
            p = subprocess.run(["git", "rev-parse", "--short", "HEAD"],
                               cwd=root_home, check=True, capture_output=True)
            sha = p.stdout.decode().rstrip()
            branch += "-" + sha

        dirname = branch + "-" + args.mode if args.mode else branch + "-custom"
    else:
        dirname = args.name

    # Check if we are using a conda environment
    dirname = dirname + \
        (f"-conda-{os.environ['CONDA_DEFAULT_ENV']}" if os.environ.get(
            'CONDA_DEFAULT_ENV', "") else "")

    build_dir = os.path.join(root_build, dirname)
    if not os.path.exists(build_dir):
        os.mkdir(build_dir)
    install_dir = os.path.join(root_install, dirname)
    if not os.path.exists(install_dir):
        os.mkdir(install_dir)

    if not os.path.exists(os.path.join(build_dir, "CMakeCache.txt")):
        base_opts = shlex.split("cmake -GNinja -Dccache=ON")
        mode_opts = args.opts[0] if args.opts else build_opts[args.mode]
        mode_opts = shlex.split(mode_opts)
        dirs_opts = shlex.split(
            f"-DCMAKE_INSTALL_PREFIX={install_dir} -B {build_dir} -S {root_home}")
        configure_command = base_opts + mode_opts + dirs_opts
        subprocess.run(configure_command, check=True)

    njobs = args.njobs
    build_command = f"cmake --build {build_dir} --target install -j{njobs}"
    subprocess.run(shlex.split(build_command), check=True)


if __name__ == "__main__":
    launch_build()
