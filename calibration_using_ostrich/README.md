# Calibration of JULES models using Ostrich 

# Key links 

1. JULES User Guide ([https://jules-lsm.github.io/latest/index.html](https://jules-lsm.github.io/latest/index.html))
2. Portable Jules ([https://github.com/NERC-CEH/portable-jules](https://github.com/NERC-CEH/portable-jules))


# Instalation


## Python 

>> Instructions tailored for JASMIN 

### 1. Get miniconda

```
wget https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-Linux-x86_64.sh
```
### 2. Deactivate Jaspy 

```
module unload jaspy
```

### 3. Creating base environment 

```
bash Miniforge3-Linux-x86_64.sh
```

Following [JASMIN documentation](https://help.jasmin.ac.uk/docs/software-on-jasmin/conda-environments-and-python-virtual-environments/), do the following 


Accept the default location (~/miniforge3). If you need to change this, see the section “Varying the installation location” near the end of this page for more info.


Say no to the question about conda init, because saying yes will cause it to add lines to your ~/.bashrc file causing your base environment to be activated every time you log in, which may interfere with the use of Jaspy.

If you say no, you can still follow the instructions below when you wish to activate your base environment.


### 4. Activate base environment 

```
source ~/miniforge3/bin/activate
```

### 5. Create the new environment 

```
conda create --name newenv --file python/packages.txt
```
>> Note: The file is provided on documentation/installs/python 

It is important to choose an easy and straightforward location, for instance, like:

```
/home/users/$USER/python-envs/conda/jules_calib
```

For instance, to have in this way, I did:

```
mkdir -p /home/users/$USER/python-envs/conda/

conda create --prefix /home/users/$USER/python-envs/conda/jules_calib --file python/packages.txt
```

## Ostrich 

### 1. Get Ostrich 

To ensure that future installations have the same options, I upload the version that I using to GitHub. Thus, do

1a. Create a folder 
```
mkdir -p ~/software/Ostrich_v17.12.19
cd ~/software/Ostrich_v17.12.19
```

1b. Get the code 

```
git clone git@github.com:ijaguirre/opt_ostrich.git
```

### 2. Load the libraries in JASMIN

```
module load oneapi/compilers/24.2.0
module load oneapi/mpi/24.2.0
module load netcdf/intel2024.2.0/4.9.2
module load netcdf/intel2024.2.0/fortran/4.6.1
export HDF5_LIBDIR=/apps/jasmin/supported/libs/hdf5/intel2024.2.0/1.14.4-2/lib
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$HDF5_LIBDIR
export NETCDF_FORTRAN_ROOT=/apps/jasmin/supported/libs/netcdf/intel2024.2.0/fortran/4.6.1
module unload jaspy
source ~/miniforge3/bin/activate
eval "$(mamba shell hook --shell bash)"
mamba activate /home/users/$USER/python-envs/conda/jules_calib
```

### 3. Compile the code 

```
make MPI
```

### 4. Save the path of the the file OstrichMPI

```
realpath OstrichMPI
```

```
%% for instance, /home/users/iaguirre/soft/Ostrich_v17.12.19/OstrichMPI
```

## (Portable) Jules 

### 1. Clone the code and navigate to the repository root directory

```
mkdir -p ~/software 
cd ~/software
git clone https://github.com/NERC-CEH/portable-jules.git
cd portable-jules
```

### 2. Store MOSRS credentials. 

Next, create a file called .env in the root of the repository containing the following lines:
```
!!!--->file .env
MOSRS_USERNAME="<your MOSRS username>"
MOSRS_PASSWORD="<your MOSRS password>"
```

### 3. Install cargo

```
curl https://sh.rustup.rs -sSf | sh
```

It will download a script, and start the installation. If everything goes well, you’ll see this appear:

```
Rust is installed now. Great!
```

### 4. Installing nix 

```
unshare --user --pid --mount echo "YES"
cargo install nix-user-chroot
```

Then, 

Install Nix:
```
sh <(curl -L https://nixos.org/nix/install) --no-daemon
```
Reload the environment:
```
source "$HOME/.nix-profile/etc/profile.d/nix.sh" 2>/dev/null || true
```

Verify:
```
nix --version
```
Expected location:
```
~/.nix-profile/bin/nix
```

### 5. Install devbox

5.1 Getting the proper file. 

This can be installed on two ways:

5a. From the source 

First, download the devbox install script using

```
curl --silent --show-error --fail --location --output ./devbox_install "https://get.jetify.com/devbox"
```

Next edit it to do the following:

Change /usr/local/bin to a location in user space, e.g. /$HOME/.local/bin
Remove the (command -v sudo || true) part from the beginning of the relevant line.
Finally, run the script

5b. Using the modified file

>> Note: The file is provided on documentation/installs/devbox/

5.2 Installing 

Once having the file:

```
chmod u+x ./devbox_install
./devbox_install
```

5.3 Continuing the installation 


```
# Download and build JULES
# NOTE: this step requires MOSRS credentials
devbox run --env-file .env setup

# Confirm that jules.exe exists in $PATH
# (should return /path/to/portable-jules/_build/build/bin/jules.exe)
devbox run which jules.exe

# Run the Loobos example
devbox run loobos
```
In this case, loobos will likely run because the all the libraries are already loaded. 

6. Clean test. 

Test that portable jules works using the example data Loobos. 

Open a new terminal, and run run each line (not all lines at once):

```
cd /home/users/$USER/soft/portable-jules
nix-user-chroot ~/.nix bash -l
source ~/.nix-profile/etc/profile.d/nix.sh
devbox run loobos
```

The expected outcome should be:
```
[user@jasmin portable-jules]$ devbox run loobos
Info: Running script "loobos" on /home/users/$USER$/soft/portable-jules
whoami: cannot find name for user ID 7056384
/etc/profile.d/zz-modules.sh: line 1: [: !=: unary operator expected
Changing directory to /home/users/$USER$/soft/portable-jules/examples/loobos
Running /home/users/$USER$/software/portable-jules/_build/build/bin/jules.exe /home/users/$USER/software/portable-jules/examples/loobos/namelists
No errors raised!
```

These instructions works using the latest JULES. 

To install another version, see below

By default, ./setup.sh or devbox run setup will download the most recent revision of JULES (i.e. HEAD). However, one can specify a revision by passing an optional argument with the -r flag, as in ./setup.sh -r <rev> or devbox run setup -r <rev>, or by setting the environment variables JULES_REVISION.

The following (copied from here) maps named versions of JULES to revision identifiers. To download version 7.8, for example, one would do ./setup.sh -r 29791 or devbox run setup -r 29791.

```
vn3.1 = 11
vn3.2 = 27
vn3.3 = 52
vn3.4 = 65
vn3.4.1 = 67
vn4.0 = 101
vn4.1 = 131
vn4.2 = 793
vn4.3 = 1511
vn4.3.1 = 1709
vn4.3.2 = 1978
vn4.4 = 2461
vn4.5 = 3197
vn4.6 = 4285
vn4.7 = 5320
vn4.8 = 6925
vn4.9 = 8484
vn5.0 = 9522
vn5.1 = 10836
vn5.2 = 12251
vn5.3 = 13249
vn5.4 = 14197
vn5.5 = 15100
vn5.6 = 15927
vn5.7 = 16960
vn5.8 = 17881
vn5.9 = 18812
vn6.0 = 19395
vn6.1 = 20512
vn6.2 = 21512
vn6.3 = 22411
vn7.0 = 23518
vn7.1 = 24383
vn7.2 = 25256
vn7.3 = 25896
vn7.4 = 26897
vn7.5 = 28091
vn7.6 = 28692
vn7.7 = 29181
vn7.8 = 29791
vn7.8.1 = 29986
vn7.9 = 30414
```

Key sources:
1. Portable JULES: https://github.com/NERC-CEH/portable-jules
2. Ostrich: https://www.civil.uwaterloo.ca/envmodelling/Ostrich.html
3. Cargo: https://doc.rust-lang.org/cargo/getting-started/installation.html
4. Nix https://github.com/nix-community/nix-user-chroot
5. 
