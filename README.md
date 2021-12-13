# Potree for WebGL based point cloud viewer

- [Potree](https://github.com/potree/potree) is a free open-source WebGL based point cloud renderer for large point clouds.  
- For own data, we should first convert it to potree-supported format, and then use Potree for rendering on WebGL.
- This repo introduces how to convert common point cloud data and render it on WebGL.

Environments: 
- Ubuntu 18.04/20.04.
- Nodejs
- Potree viewer
- Potreeconvert


## Potree Installation


### Install [node.js](http://nodejs.org/)

Download `tar.xz` on official website (e.g. nodejs-16.x), and unzip

```
$ tar xf  node-vxx.xx.xx-linux-x64.tar.xz       
$ cd node-vxx.xx.xx-linux-x64/                  
$ ./bin/node -v                              
vxx.xx.xx     
```

If you want to use `node` in terminal, 2 methods as follows:

a) Set soft links 

```
ln -s /opt/nodejs/bin/npm   /usr/local/bin/ 
ln -s /opt/nodejs/bin/node   /usr/local/bin/

# If not, alternative:
ln -s /opt/nodejs/bin/npm   /usr/bin/ 
ln -s /opt/nodejs/bin/node   /usr/bin/
```

```
# check if work
$ node --version
$ npm --version
```

```
# If remove soft links
rm /usr/local/bin/node
rm /usr/local/bin/npm
# or
rm /usr/bin/node
rm /usr/bin/npm
```

These method: Sometimes software updates may cause soft links to fail.

b) Set environment variables 

```
# vim/vi to open
vim /etc/profile

# add at the end and save
export NODE_HOME=/opt/nodeJs  # use your path
export PATH=$PATH:$NODE_HOME/bin 
export NODE_PATH=$NODE_HOME/lib/node_modules

# make it effect and verify
source /etc/profile
node -v 
```


c) Using apt manner

If the above two methods fail, such as donot found command for `sudo npm XXX`, you can use apt manner.  
Ubuntu default installation sources, i.e., `sudo apt install nodejs`，often only install the old version, with just nodejs and no npm.

Install the latest or specific version (with npm), as follows:

```
# First, download package ([obtain latest version link](https://github.com/nodesource/distributions/blob/master/README.md))
# Node.js v16.x:
curl -fsSL https://deb.nodesource.com/setup_16.x | sudo -E bash -
# Node.js v14.x:
curl -fsSL https://deb.nodesource.com/setup_14.x | sudo -E bash -

# Second, installation
sudo apt-get install -y nodejs

# Using `node -v` and `npm -v` to check whether the installation is successful.
```

Here we adopt the `apt` manner. Otehr details please refer to [[1]](https://www.runoob.com/nodejs/nodejs-install-setup.html), [[2]](https://www.jianshu.com/p/50fb7228238b).


### Install Potree

```
git clone https://github.com/potree/potree.git  
# or download stable released version: potree-1.8-release from github
cd potree-1.8
npm install  # Install dependencies, as specified in package.json, and create a build in ./build/potree.
```

Run Potree

```
cd potree
npm start
```

Go to http://localhost:1234/ to test the examples.

Each time we should go into `potree` folder and executive "npm start" to start the potree services.

Thus we can set `npm start` as a self-starting service. First, create a file: npmstart.sh,   

```
cd ***/path/potree
npm start &
```

Then save it to the folder: /etc/profile.d/，then reboot. 
Factly the viewer link is like `http://localhost:1234/examples/choosed_file_name.html`.

Other self-starting setting methods can be seen [here](https://blog.51cto.com/u_14442495/2905438).
```
Put self-starting script in /etc/rc.d/rc.local. (/etc/rc.local is the same as /etc/rc.d/rc.local),   
e.g. `/mnt/npmstart.sh` at the end of the rc.local file.
Reboot after adding the permission:
chmod +x ***.sh
chmod +x /etc/rc.d/rc.local
```



## Potreeconvert

For you own point cloud (e.g. .las, .laz, .zst, .bin, etc.), you should convert to potree format by [PotreeConverter](https://github.com/potree/PotreeConverter).

Noted, PotreeConverter only support Ubuntu 20.04.

```
sudo apt-get update && apt-get install -y gcc g++ gdb cmake python 
sudo apt update && apt install -y git

# Lastool
sudo git clone https://github.com/m-schuetz/LAStools.git 
    && cd LAStools/LASzip 
    && mkdir build && cd build 
    && cmake -DCMAKE_BUILD_TYPE=Release .. 
    && make

sudo apt-get install libtbb2 libtbb-dev 

sudo git clone https://github.com/potree/PotreeConverter.git 
    && cd PotreeConverter 
    && mkdir build && cd build 
    && cmake -DCMAKE_BUILD_TYPE=Release -DLASZIP_INCLUDE_DIRS=/LAStools/LASzip/build/src/liblaszip.so .. 
    && make 
```

For Ubuntu 18.04, we use docker to pack the PotreeConverter and call this docker for conversion. This repo gives the `Dockerfile` of PotreeConverter.


Refere [here](https://github.com/potree/PotreeConverter/issues/180).




## Potreeconvert Plus

By PotreeConverter, we will obtain the converted potree-format data, i.e., octree.bin, metadata.json and hierarchy.bin. Then, modify one of the examples (html files in Potree/examples/) with the your own path of metadata.json file, see [Potreeconverter](https://github.com/potree/PotreeConverter). Open this html by potree viewer to visulize the point cloud, such as `http://localhost:1234/examples/test.html`.

To generate it automatically, we build a python file (`genhtml.py`) to automaticly generate the html files, and a shell script (`run.sh`) to run the `PotreeConverter` and `genhtml` to produce the converted files and html files in docker.

Files:

```
run.sh: input point cloud data path, output results in potree-1.8/pointclouds
./potreeconvert/Potreeconverter input -o output
genhtml.py: generate html into potree/dataview
```

Usage:
For example, the .las for view is at: /home/pcloud/potree-1.8/data/test.las
1) Build the docker: `sudo docker build -t potreetransform .`;
2) Run the docker:
```
sudo docker run -it -v /home/pcloud/potree-1.8/data/:/usr/src/app/data/ -v /home/pcloud/potree-1.8/dataview/:/usr/src/app/dataview/ potreetransform /usr/src/app/run.sh test.las
```



file organization:

```
Potree:
---- potree-1.8
    ---- data
    ---- dataview
---- potreetransform
    ---- PotreeConverter
    ---- genhtml.py
    ---- run.sh
---- Nodejs
```




## Others

In Windows, after install PotreeDesktop, potreeconvert may does not work, probably because of the lack of some dlls. Just download thses dlls.




