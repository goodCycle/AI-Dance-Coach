# AI Dance Coach
CS470 (Introduction to Artificial Intelligence) term project

This is a prototype for the AI Dance Coach. The backend of the application takes in a video of a move being performed




---
# Prerequisites
The prerequisites are split up into three parts:
* Backend - OpenPose
* Backend - Flask Server
* Frontend - React Native App

---

# Backend

**Disclaimer**: Due to a variety of systems involved, the setup process includes a lot of steps and can vary depending on your environment. To limit possible sources of error, using a fresh install of Ubuntu 18.04 when setting up this system is recommended.

Below are the specifications of the server that this setup was tested on. These should only serve as a reference point.
However, we recommend using a machine with a powerfull (Nvidia) GPU, as CPU inference for OpenPose requires some additional setup and is too slow for large scale video analysis.

#### Hardware

RAM: 2x 16GB Hynix 16GB 2400 DDR4

CPU: 2x 2.2GHz Intel Xeon-Skylake (5120-GOLD)

GPU: NVIDIA TESLA K80

#### Software

OS : Ubuntu 18.04

Accelerator: Cuda 9.1 with cuDNN 7.6.5

Deep learning framework: Caffe OpenPose Branch


## Dependencies (Pose Estimation)

**General dependencies:**

    sudo apt-get install python3 python3-opencv freeglut3 freeglut3-dev libxi-dev libxmu-dev dkms build-essential gcc-6 g++-6 linux-headers-$(uname -r) nvidia-cuda-toolkit cmake libhdf5-serial-dev libopencv-dev libatlas-base-dev liblapacke-dev libblkid-dev e2fslibs-dev libboost-all-dev libaudit-dev python-numpy doxygen libgflags-dev gflags libgoogle-glog-dev autoconf automake libtool curl make unzip
    

After installing the above dependencies, restart to load in the correct nvidia drivers

    sudo reboot

Test the CUDA installation with 

    nvcc --version


**cuDNN**

For performance reasons, installing cuDNN is highly recommended

- [Download](https://developer.nvidia.com/cudnn)
- [Installation](https://docs.nvidia.com/deeplearning/sdk/cudnn-install/index.html)

When following the testing instructions, be sure to change the Cuda directory in the Makefile 

( /usr if your nvcc is in /usr/bin )

**Installing protoc:**

Follow the installation instructions [here](https://askubuntu.com/questions/1072683/how-can-i-install-protoc-on-ubuntu-16-04) (Important: Skip the Prerequesites part)

**Currently optional**:

Installing caffe:

    sudo apt-get install caffe-cuda

Test the caffe installation with

    caffe --version

## OpenPose

[Installing OpenPose](https://github.com/CMU-Perceptual-Computing-Lab/openpose/blob/master/doc/installation.md) (only for reference, follow the steps below)

From the root directory, create the build folder:

    mkdir build
    cd build

Set the correct environment variables:

    export CC=gcc-6
    export CXX=g++-6

Generate the makefile:

    cmake -DBUILD_PYTHON=ON ..

Build openpose:

    make -j`nproc`


To install OpenPose in your environment after building, run :

    sudo make install

in the build directory.

### Optional:

[Adding the experimental models](https://github.com/CMU-Perceptual-Computing-Lab/openpose_train/blob/master/experimental_models/README.md) 


- 25B Option 2

(Getting these to run requires additional workarounds)

## Flask Application

### Web server setup

Using [Flask](https://palletsprojects.com/p/flask/)  as framework, [nginx](http://nginx.org/) as  web server, and [gunicorn](https://gunicorn.org/) as server gateway interface.

    sudo apt-get install nginx
    sudo apt-get install gunicorn3
    pip3 install flask

Configure nginx

make sure that server allows incomming http requests on port 80

in  /etc/nginx/sites-enabled/ create file called "app" with the following content

    server{
            listen 80;
            server_name 208.43.39.216;
    
            location / {
                    proxy_pass http://unix:/home/pose/AI-Dance-Coach/Backend/app.sock;
            } 
    }

Configure gunicorn

in /path/to/file create a file called "gunicorn3.service" with the following content

    [Unit]
    Description=Gunicorn instance to serve myproject
    After=network.target
    [Service]
    User=pose
    Group=www-data
    WorkingDirectory=/home/pose/AI-Dance-Coach/Backend
    ExecStart = /usr/bin/gunicorn3 --workers 3 --bind unix:app.sock -m 007 app:app

Setup App

Clone git repository into /home/pose

    git clone https://github.com/goodCycle/AI-Dance-Coach.git
    git pull

Start everything

    sudo systemctl daemon-reload
    sudo service gunicorn3 start
    sudo service nginx start

### Testing the server

send an http request

    curl -X POST -F file=@"/path/to/file.mp4" -F file=@"/path/to/file.json" http://208.43.39.216 --output response.zip

with file.mp4 beeing an video of a human performing a coreography 
(note: behaviour is only defined for exactly one human beeing in the video)

and file.json beeing a json, config file with the following format

    {
      "is_sample": <bool>,
      "compare_to": <name_of_file.mp4>
    }

The server will return a zip filder, with returning the result of the analysis.

2 video files, a json with the raw data, and a json with a short configuration

First send sample a sample video

Second send trial videos and get the respose

So an example for two sending up a sample and comparing it could be:

    curl -X POST -F file=@"/mnt/c/Users/nomis/Desktop/one.mp4" -F file=@"/mnt/c/Users/nomis/Desktop/test0.json" http://208.43.39.216
    
    curl -X POST -F file=@"/mnt/c/Users/nomis/Desktop/two.mp4" -F file=@"/mnt/c/Users/nomis/Desktop/test1.json" http://208.43.39.216 --output response.zip

With test0.json beeing

    {
      "is_sample": true,
      "compare_to": "one.mp4"
    }

and test1.json beeing

    {
      "is_sample": false,
      "compare_to": "one.mp4"
    }


---
## Frontend

### iOS
* For building the iOS App,  **Xcode** is required.
* Install the following dependencies:
```
   brew install yarn
   sudo gem install cocoapods
```


---
# Running the App


## Backend

WITH WSGI AND WITH DEBUG SERVER

BACKEND TESTING INSTRUCTIONS + EXPECTED OUTPUT

## Frontend

## iOS

* After cloning the Project,
```
   cd AIDanceCoach
   yarn
   cd ios && pod install
   cd ..
   react-native run-ios
```

WHERE TO ENTER SERVER IP

## Built With

* [React-Native](https://facebook.github.io/react-native/) - Front end framework
* [Flask](https://www.palletsprojects.com/p/flask/) - Backend framework for processing requests
* [OpenPose](https://github.com/CMU-Perceptual-Computing-Lab/openpose) - Pose estimation model
* [OpenCV](https://opencv.org/) - Video processing


## Authors

* **Jaeyi Hong** - [goodCycle](https://github.com/goodCycle)
* **Adrian Steffan** - [adriansteffan](https://github.com/adriansteffan)
* **Simon Zocholl** - [SimonZocholl](https://github.com/SimonZocholl)
* **Doheon Hwang** - [hdh112](https://github.com/hdh112)





