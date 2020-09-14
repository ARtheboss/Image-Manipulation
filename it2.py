import numpy as np
from PIL import Image, ImageDraw
from math import sqrt

loc = input("\nImage name: ")
im1 = Image.open(loc)
pix1 = im1.load()

N = int(input("\nN x N transformation matrix (enter N): "))

width = im1.size[0]
height = im1.size[1]

print("\nTransformation matrix")

fill_in = False

transformation = np.zeros((N, N))
for i in range(N):
	for j in range(N):
		transformation[i, j] = float(input("Value in transformation matrix at position ("+str(i+1)+", "+str(j+1)+"): "))
		if transformation[i, j] >= 2:
			fill_in = True

print(transformation)


cords = np.ones((N, width*height))

edges = np.zeros((N, 4))
edges[0, 1] = width-1
edges[0, 3] = width-1
edges[1, 2] = height-1
edges[1, 3] = height-1

edges = np.dot(transformation, edges)

minx = min(edges[0,0],edges[0,1],edges[0,2],edges[0,3])+width*10
maxx = max(edges[0,0],edges[0,1],edges[0,2],edges[0,3])+width*10
miny = min(edges[1,0],edges[1,1],edges[1,2],edges[1,3])+height*10
maxy = max(edges[1,0],edges[1,1],edges[1,2],edges[1,3])+height*10

print("Image size: " + str(maxx-minx) + " X " + str(maxy-miny))

finalim = Image.new('RGB', (width*20, height*20))
pix3 = finalim.load()

for x in range(width):
	for y in range(height):
		cords[0, y*width+x] = x
		cords[1, y*width+x] = y

final = np.dot(transformation, cords)

for i in range(width*height):
	if(i % height == 0):
		print("   "+str(round(i/(width*height)*100)) + "%", end='\r')
	pix3[final[0, i]+width*10,final[1, i]+height*10] = pix1[i % width, i // width]

crop = input("\nCrop image (y/n): ")

if crop != "n":
	finalim = finalim.crop((minx,miny,maxx,maxy))

if fill_in:
	print("Stretching image...")
	pixels = finalim.load()
	for i in reversed(range(1,finalim.size[0]-1)):
		for j in reversed(range(1,finalim.size[1]-1)):
			if pixels[i,j] == (0, 0, 0):
				if pixels[i-1,j] != (0,0,0):
					pixels[i,j] = pixels[i-1,j]
				elif pixels[i,j-1] != (0,0,0):
					pixels[i,j] = pixels[i,j-1]
				elif pixels[i-1,j-1] != (0,0,0):
					pixels[i,j] = pixels[i-1,j-1]
name = "t-"+loc
print("\nSaved as "+name)
finalim.save(name)



