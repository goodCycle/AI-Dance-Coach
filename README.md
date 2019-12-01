# AI Dance Coach
CS470 (Introduction to Artificial Intelligence) Term Project

This is a prototype for the AI Dance Coach, an application that compares your movements to those of a professional performer and highlights mistakes.

 The pipeline consists of recording a video and sending it to our server for processing where it is broken down into separate frames and fed them into OpenPose, an open-source pose detection model.

  It then uses a custom pose difference calculation to compare the submitted video frames to a sample video and respond with a visualization of the first part where the pose of the user strongly deviates from the sample pose. 
  
   The app runs on smartphones running iOS.

   A short demo video can be found [here](https://drive.google.com/file/d/1stwlxUdNVAYhl817kuzX1GkZBdsm_Hw0/view).
   
   Video samples for testing the app can be found [here](https://drive.google.com/drive/u/0/folders/1daD3I4Pri5CF8vuz1-AeLGCcGby_wDyf).
   
   For testing the app with fidelity-lowered compressed videos, sample images for evaluating the app can be found [here](http://cocodataset.org/#explore).




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

To install all packages needed for this project:

    cd Backend
    pip3 install -r requirements.txt

Configure nginx

make sure that server allows incomming http requests on port 80

in  /etc/nginx/sites-enabled/ create file called "app" with the following content

    server{
            listen 80;
            server_name <YOUR SERVER IP>;
    
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

## Frontend

### iOS

* After cloning the Project,
```
   cd AIDanceCoach
   yarn
   cd ios && pod install
   cd ..
   react-native run-ios
```

* You can change the server address in `AIDanceCoach/.env`.
```
   SERVER_ENDPOINT=http://208.43.39.216:5000 #Change this address
```

## Backend

To run the deployment server after setup, run:

    sudo systemctl daemon-reload
    sudo service gunicorn3 start
    sudo service nginx start

For testing purposes, you can start the flask development server by running

    sudo python3 app.py

in the Backend directory. This will open the app on port 5000 as opposed to 80.

### Testing the server (replace the IP with your own)

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

2 video files, a json with the raw data, and a json with a short configuration.

First send sample a sample video.

Second send trial videos and get the respose.

So an example for two sending up a sample and comparing it could be:

    curl -X POST -F file=@"/mnt/c/Users/nomis/Desktop/three.mp4" -F file=@"/mnt/c/Users/nomis/Desktop/test0.json" http://208.43.39.216
    
    curl -X POST -F file=@"/mnt/c/Users/nomis/Desktop/four.mp4" -F file=@"/mnt/c/Users/nomis/Desktop/test1.json" http://208.43.39.216 --output response.zip

With test0.json being

    {
      "is_sample": true,
      "compare_to": "three.mp4"
    }

and test1.json being

    {
      "is_sample": false,
      "compare_to": "three.mp4"
    }


## Evaluation
In the `Backend` folder, run
```
 python3 evaluate.py
```

With input images compressed with parameter `QF`(in `Backend/evaluate.py`), this evaluates accuracy of pose detection in compressed images.

Directory of input images can be customized in `Backend/evaluate_compression/Evaluator.py`.

The accuracy is measured by 2D Euclidean distance between keypoints of uncompressed image and keypoints of compressed image.

Accuracy measurement can be improved by implementing [Object Keypoint Similarity(OKS)](http://cocodataset.org/#keypoints-eval), but need additional adjustments to match the input format of the OKS API.



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





