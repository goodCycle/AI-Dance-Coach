# AI Dance Coach
CS470 (Introduction to Artificial Intelligence) term project

This is a prototype for the AI Dance Coach.




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

## Dependencies (Flask Application)

## Server Setup:


### what to do

    # update and install dependencies
    sudo apt-get update
    sudo apt install python3-pip
    sudo apt-get install nginx
    sudo apt-get install gunicorn3
    pip3 install flask
    
    # clode git repository into  /home/pose
    git clone https://github.com/goodCycle/AI-Dance-Coach.git
    
    # configuring the nginx 
    cd /etc/nginx/sites-enabled/
    sudo nano app
    
    # make sure the server allows http requests on port 80
    
    # setup gunicorn3
    cd /etc/systemd/system/
    sudo vim gunicorn3.service
    
    # restart everything
    sudo systemctl daemon-reload
    sudo service gunicorn3 restart
    sudo service nginx restart

## app

    server{
            listen 80;
            server_name 208.43.39.216;
    
            location / {
                    proxy_pass http://unix:/home/pose/AI-Dance-Coach/Backend/app.sock;
            } 
    }

### gunicorn3.service

    [Unit]
    Description=Gunicorn instance to serve myproject
    After=network.target
    # We will give our regular user account ownership of the process since it owns all of the relevant files
    [Service]
    # Service specify the user and group under which our process will run.
    User=pose
    # give group ownership to the www-data goup so that Nginx can communicate easily with the Gunicorn processes.
    Group=www-data
    # We'll then map out the working directory and set the PATH environmental variable so that the init system knows where our the executables for the process are located (within our virtual environment).
    WorkingDirectory=/home/pose/AI-Dance-Coach/Backend
    # We'll then specify the commanded to start the service
    ExecStart = /usr/bin/gunicorn3 --workers 3 --bind unix:app.sock -m 007 app:app


BACKEND TESTING INSTRUCTIONS + EXPECTED OUTPUT

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
* **Doheon Hwang** - []()





