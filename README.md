## Cloning the aerospike-tools-backup
```shell
git clone https://github.com/aerospike/aerospike-tools-backup.
```


## Building

### Build Prerequisites.
```shell
1$ sudo yum install openssl-devel glibc-devel autoconf automake libtool

[Optional:]
$ sudo yum install lua-devel
$ sudo yum install gcc-c++ graphviz rpm-build

```
### Build Aerospike C client
```shell
git clone https://github.com/aerospike/aerospike-client-c.git
git checkout tags/<version>

export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/lib
git submodule update --init
make EVENT_LIB=libuv
make install

Note: after building copy the content of aerospke c client and paste to aserospke-tool-backup inside module directory.
```

### Build the utility tool.
```shell
yum update

# Install C client dependencies...

# asbackup dependencies
yum groupinstall 'Development Tools'
yum install openssl-devel libcurl-devel libzstd-devel

# build libuv from source since the headers
# aren't in the libuv yum package
git clone https://github.com/libuv/libuv
cd libuv
sh autogen.sh
./configure
make
make install
cd ..

# for aws-sdk-cpp build
yum install cmake

# download aws sdk
git clone https://github.com/aws/aws-sdk-cpp.git
cd aws-sdk-cpp
git checkout $AWS_SDK_VERSION
git submodule update --init --recursive

# build aws sdk dynamic
mkdir build
cmake3 -S . -B build -DCMAKE_BUILD_TYPE=Release -DBUILD_ONLY="s3" -DBUILD_SHARED_LIBS=ON -DENABLE_TESTING=OFF -DCMAKE_INSTALL_PREFIX=/usr/local -DCMAKE_INSTALL_LIBDIR=lib
make -C build

# install aws static sdk
cd build
make install
cd ../..
# Compiling the aerospike-tool (run this in aerospike-tool directory.)
export PATH=/opt/rh/devtoolset-7/root/usr/bin/:$PATH
make EVENT_LIB=libuv
```

## Creating patch file and Applying patch file

### Create patch file
```shell
git diff > <file-name>.patch
```

### Applying patch file
```shell
git apply <file-name>.patch
```


## Checking memory leaks.

### Install valgrind
```shell
yum install valgrind
```

### Running valgrind
```shell
valgrind <your_binary_executable>
```
## Building RPM package.
### Installing the required packages.
```shell
sudo yum install rpm-build rpmdevtools
```

### Create a working directory.
```shell
rpmdev-setuptree  
(Note: This will create a directory name as rpmbuild in /root directory)
```
### Create a spec file.
```shell
rpmdev-newspec <my_package_name>
```


### Structure of rpmbuild.
```
rpmbuild/ (Root directory for RPM package building)

├── BUILD (Temporary build directory)

├── RPMS (your_package.rpm {Binary RPM package})

├── SOURCES (your_source_code.tar.gz)

├── SPECS  your_package.spec (RPM spec file for your package)

├── SRPMS  your_package.src.rpm (Source RPM package)

└── BUILDROOT (Temporary build root during package build)

```
### Build the RPM package:
```shell
rpmbuild -bb rpmbuild/SPECS/my_package_name.spec
```


