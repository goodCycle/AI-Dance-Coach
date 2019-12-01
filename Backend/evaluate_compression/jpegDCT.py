# Reference: 
# https://www.hdm-stuttgart.de/~maucher/Python/MMCodecs/html/jpegUpToQuant.html

import cv2
import numpy as np
import math
import random
# from matplotlib import pyplot as plt
# import matplotlib.cm as cm

class ApplyDCTcomp:
        def __init__(self, qf, in_path, out_path):
                ###################################################
                # Step 1: Read image
                B=8 # blocksize (In Jpeg the
                print("output path:", out_path)
                img1 = cv2.imread(in_path, cv2.IMREAD_UNCHANGED)
                # print("read")
                h, w = img1.shape[:2]
                point = (random.randrange(0,math.floor(h)), random.randrange(0,math.floor(w)))
                # print(point)

                # h,w=np.array(img1.shape[:2])/40 * 40
                h = math.ceil((h//80)*80)
                w = math.ceil((w//80)*80)
                img1=img1[:h,:w]

                #Convert BGR to RGB
                img2=np.zeros(img1.shape,np.uint8)
                img2[:,:,0]=img1[:,:,2]
                img2[:,:,1]=img1[:,:,1]
                img2[:,:,2]=img1[:,:,0]

                block=np.floor(np.array(point)/B) #first component is col, second component is row
                scol=math.floor(block[0])
                srow=math.floor(block[1])

                ###################################################
                # Step 2: Transform BGR to YCrCb and Subsample Chrominance Channels
                transcol=cv2.cvtColor(img1, cv2.COLOR_BGR2YCrCb)
                SSV=2
                SSH=2
                crf=cv2.boxFilter(transcol[:,:,1],ddepth=-1,ksize=(2,2))
                cbf=cv2.boxFilter(transcol[:,:,2],ddepth=-1,ksize=(2,2))
                crsub=crf[::SSV,::SSH]
                cbsub=cbf[::SSV,::SSH]
                imSub=[transcol[:,:,0],crsub,cbsub]

                ###################################################
                # Step 3 and 4: Discrete Cosinus Transform and Quantisation
                ### Luminace
                QY=np.array([   [16,11,10,16,24,40,51,61],
                                [12,12,14,19,26,48,60,55],
                                [14,13,16,24,40,57,69,56],
                                [14,17,22,29,51,87,80,62],
                                [18,22,37,56,68,109,103,77],
                                [24,35,55,64,81,104,113,92],
                                [49,64,78,87,103,121,120,101],
                                [72,92,95,98,112,100,103,99]])
                ### Chrominance
                QC=np.array([   [17,18,24,47,99,99,99,99],
                                [18,21,26,66,99,99,99,99],
                                [24,26,56,99,99,99,99,99],
                                [47,66,99,99,99,99,99,99],
                                [99,99,99,99,99,99,99,99],
                                [99,99,99,99,99,99,99,99],
                                [99,99,99,99,99,99,99,99],
                                [99,99,99,99,99,99,99,99]])

                # TODO: scale quality factor
                # QF=35
                QF=qf
                if QF < 50 and QF > 1:
                        scale = np.floor(5000/QF)
                elif QF < 100:
                        scale = 200-2*QF
                else:
                        print("Quality Factor must be in the range [1..99]")
                        scale = np.floor(1/QF)
                scale=scale/100.0
                ### Quantization based on YCrCb 
                Q=[QY*scale,QC*scale,QC*scale]

                TransAll=[]
                TransAllQuant=[]
                ch=['Y','Cr','Cb']
                for idx,channel in enumerate(imSub):
                        channelrows=channel.shape[0]
                        channelcols=channel.shape[1]
                        Trans = np.zeros((channelrows,channelcols), np.float32)
                        TransQuant = np.zeros((channelrows,channelcols), np.float32)
                        blocksV=math.ceil(channelrows/B)
                        blocksH=math.ceil(channelcols/B)
                        vis0 = np.zeros((channelrows,channelcols), np.float32)
                        vis0[:channelrows, :channelcols] = channel
                        vis0=vis0-128
                        for row in range(blocksV):
                                for col in range(blocksH):
                                        currentblock = cv2.dct(vis0[row*B:(row+1)*B,col*B:(col+1)*B])
                                        Trans[row*B:(row+1)*B,col*B:(col+1)*B]=currentblock
                                        TransQuant[row*B:(row+1)*B,col*B:(col+1)*B]=np.round(currentblock/Q[idx])
                        TransAll.append(Trans)
                        TransAllQuant.append(TransQuant)
                        if idx==0:
                                selectedTrans=Trans[srow*B:(srow+1)*B,scol*B:(scol+1)*B]
                        else:
                                sr=math.floor(srow/SSV)
                                sc=math.floor(scol/SSV)
                                selectedTrans=Trans[sr*B:(sr+1)*B,sc*B:(sc+1)*B]

                # print("encoded")

                ###################################################
                # Decoding
                DecAll=np.zeros((h,w,3), np.uint8)
                for idx,channel in enumerate(TransAllQuant):
                        channelrows=channel.shape[0]
                        channelcols=channel.shape[1]
                        blocksV=math.ceil(channelrows/B)
                        blocksH=math.ceil(channelcols/B)
                        back0 = np.zeros((channelrows,channelcols), np.uint8)
                        for row in range(blocksV):
                                for col in range(blocksH):
                                        dequantblock=channel[row*B:(row+1)*B,col*B:(col+1)*B]*Q[idx]
                                        currentblock = np.round(cv2.idct(dequantblock))+128
                                        currentblock[currentblock>255]=255
                                        currentblock[currentblock<0]=0
                                        back0[row*B:(row+1)*B,col*B:(col+1)*B]=currentblock
                        back1=cv2.resize(back0,(w,h))
                        DecAll[:,:,idx]=np.round(back1)
                # print("decoded")
                reImg=cv2.cvtColor(DecAll, cv2.COLOR_YCrCb2BGR)
                cv2.imwrite(out_path, reImg)
                # print("saved")
                img3=np.zeros(img1.shape,np.uint8)
                img3[:,:,0]=reImg[:,:,2]
                img3[:,:,1]=reImg[:,:,1]
                img3[:,:,2]=reImg[:,:,0]
                SSE=np.sqrt(np.sum((img2-img3)**2))
                # print("Sum of squared error: ",SSE)
                # return SSE
