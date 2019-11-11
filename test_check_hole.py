import cv2
import numpy as np
from argparse import ArgumentParser
import os,time

def remove(img):
	A = []

	gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
	blur = cv2.blur(gray, (3,3))
	_,binary = cv2.threshold(blur, 15, 255, cv2.THRESH_BINARY_INV)

	kernel = np.ones((3,3),np.uint8)
	dialte = cv2.dilate(binary,kernel,iterations=3)

	_,cnts,_ = cv2.findContours(dialte, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

	for cnt in cnts:
		x,y,w,h = cv2.boundingRect(cnt)
		if w < 300 or h < 300:
			continue
		A.append([[x,y,w,h],cnt])

	return A,dialte

def transform(img,trans):
	rows,cols,_ = img.shape
	if isinstance(trans,float):
		M = cv2.getRotationMatrix2D((cols/2,rows/2),trans,1)
		dst = cv2.warpAffine(img,M,(cols,rows))
	elif isinstance(trans,tuple):
		x,y = trans
		M = np.float32([[1,0,x],[0,1,y]])
		dst = cv2.warpAffine(img,M,(cols,rows))
	return dst

def rotated(img):
	# cnt = [box,cnt] 
	cnt,binary = remove(img)

	if len(cnt) == 0:
		print("")
		return img,binary
	else:
		I,_,angle = cv2.minAreaRect(cnt[0][1])

		if angle < -45:
			angle = 90+angle

		# x,y,w,h = cnt[0][0]

		cv2.drawContours(img, [cnt[0][1]], 0, (0,255,0))

		rows,cols,_ = img.shape
		x0,y0 = int(I[0]),int(I[1])
		v = (cols//2 - x0,rows//2 - y0)

		# dst = transform(img,angle)
		# dst = transform(img,v)
		dst = img

		cv2.circle(dst,(x0,y0),5,(0,255,0),2)

		return dst,binary


def main():
	parse = ArgumentParser(description="Auto align")
	parse.add_argument("-f","--folder",type=str,help="folder path",default="")
	args = parse.parse_args()

	folder = args.folder
	window = cv2.namedWindow("",cv2.WINDOW_FREERATIO)

	if os.path.isdir(folder):
		list_images = os.listdir(folder)
		for f in list_images:
			filename = os.path.join(folder,f)
			img = cv2.imread(filename)
			if isinstance(img,np.ndarray):
				t0 = time.time()
				dst,dilate = rotated(img)
				print(time.time()-t0)
				cv2.imshow(window, dst)
				cv2.waitKey(0)
				# cv2.imshow(window,dilate)
				# cv2.waitKey(0)

		cv2.destroyAllWindows()

if __name__ == "__main__":
	main()




