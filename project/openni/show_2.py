#!/usr/bin/python
import cv2
import numpy as np
#from primesense import openni2
#from primesense import _openni2 as c_api
from openni import openni2
from openni import _openni2 as c_api
X=320
Y=240
scale=2.5
openni2.initialize()
dev = openni2.Device.open_any()
depth_stream = dev.create_depth_stream()
color_stream = dev.create_color_stream()
depth_stream.start()
depth_stream.set_video_mode(c_api.OniVideoMode(pixelFormat = c_api.OniPixelFormat.ONI_PIXEL_FORMAT_DEPTH_100_UM, resolutionX = X, resolutionY = Y, fps = 60))
color_stream.start()
while True:
	frame = depth_stream.read_frame()
	frame_data = frame.get_buffer_as_uint16()
	dimg = np.frombuffer(frame_data, dtype=np.uint16)
	dimg.shape = (1, Y, X)
	dimg = np.concatenate((dimg, dimg, dimg), axis=0)
	dimg = np.swapaxes(dimg, 0, 2)
	dimg = np.swapaxes(dimg, 0, 1)
	dimg = cv2.resize(dimg, dsize=(int(X*scale),int(Y*scale)))

	frame = color_stream.read_frame()
	frame_data = np.array(frame.get_buffer_as_triplet()).reshape([Y,X,3])
	R = frame_data[:,:,0]
	G = frame_data[:,:,1]
	B = frame_data[:,:,2]
	frame_data = np.transpose(np.array([B,G,R]),[1,2,0])
	img = cv2.resize(frame_data, dsize=(int(X*scale),int(Y*scale)))
	cv2.imshow("image", img)
	cv2.imshow("depthimage", dimg)
	key = cv2.waitKey(10)
	if int(key) ==  113:
		break
openni2.unload()