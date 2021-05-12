%matplotlib inline
#This Assignment is done using Google Collab
import sys, os
from PIL import Image
from PIL import ImageFilter
import numpy as np
import matplotlib.pyplot as plt
import cv2 as cv
import math

##Function to plot histogram of an image
def plotHistogram(imageHistogram):
   plt.ylabel('Frequency')
   plt.xlabel('Pixel Value');
   color_array=np.array(['r','g','b'])
   plt.hist(imageHistogram.reshape(imageHistogram.shape[0]*imageHistogram.shape[1],-1), density=False, bins=256, range=(0,255), histtype='bar',color='b')
   plt.show()


##Sample image files are stored inside my Google Drive.
##Below code snippet is to traverse to the right path were the images are store.
def traverseToGoogleDriveFolder():
  if 'google.colab' in sys.modules:
    from google.colab import drive
    drive.mount('/content/gdrive',force_remount=True)
    os.chdir('/content/gdrive')
    folder_name = 'ComputerVision_Assg1'
    import subprocess
    path_to_folder = subprocess.check_output('find . -type d -name ' + str(folder_name), shell=True).decode("utf-8")
    path_to_folder = path_to_folder.replace('\n',"")
    os.chdir(path_to_folder)
      ##Traversal to the folder were images are kept completed.

#Convert a given rgb image into YCrCb array
def convertRGBtoYCrCbImageArray(rgbImage):
  convertedImage= rgbImage.convert('YCbCr')
  #Transform YCrCb image into a matrix
  return np.array(convertedImage)

#Extracts the Y component of an RGB matrix.
def getYComponentOfRGBImage(rgbImage):
  #Transform YCrCb image into a matrix
  hsvImageArray=convertRGBtoYCrCbImageArray(rgbImage)
  #Y component is the first channel in the matrix. Return the first channel
  yArray=np.array(hsvImageArray[:,:,0],dtype=int)
  return yArray

#Replaces the Y component of an RGB image with new value.
def replaceYComponentInRGBImage(rgbImage,newYValue):
  #Transform YCrCb image into a matrix
  hsvImageArray=convertRGBtoYCrCbImageArray(rgbImage)
  hsvImageArray[:,:,0]=newValueArray 
  tranformedImage=Image.fromarray(hsvImageArray.astype(np.uint8),mode='YCbCr')
  tranformedImage=tranformedImage.convert('RGB')
  return tranformedImage

#Calculate the probability of each Y component (i.e. 0-255) present in the array. 
#returns the L(buckets),h(height of image),w(width of image) and Probability matrix of Y component.
def calculateProbabilityOfAllValuesInYMatrix(YArray):
   #getting image size and dept
  (h,w)=YArray.shape
  #calculate M*N
  MN=h*w
  
  #L is set to 256 (0-255)
  L=256
  
  #Getting the frequency of each values in Y component
  imageHistogramCalculation=np.histogram(YArray.reshape(MN,-1),bins=[i for i in range(0,257)],range=(0,255))
  imageHistogram=imageHistogramCalculation[0]
  imageHistogram=np.array(imageHistogram.reshape(imageHistogram.shape[0],-1))

  #Calculating probability =(frequency of a pixel value present) / (total number of pixels in the image)
  probabilityMatrixofY = imageHistogram/MN
  return h,w,L,probabilityMatrixofY


#Traversing to google drive folder.
try:
  traverseToGoogleDriveFolder()
except subprocess.CalledProcessError as cmderr:
  print ('Error occured while traversing to google drive.')
  print (cmderr.output)
  exit(0) #exiting further execution as folder traverse failed.

#Iterate all the images in the folder and applying Histogram Equalization.
for image in os.listdir('.'):
  #Reading each image
  initialImage=None
  try:
    initialImage=Image.open(image)
  except IsADirectoryError:
    continue
  
  valueArray=getYComponentOfRGBImage(initialImage)
  
  #Plot the histogram of Y component before Histogram Equalization
  plotHistogram(valueArray)
  
  imageHieght,imageWidth=valueArray.shape
  
  #Decides the number of windows in the image.
  verticalSplit,horizontalSplit=2,2
  
  initialRowindex=0
  #Calculates the number of pixels of the window.
  rowindexChange=math.ceil(imageHieght/verticalSplit)
  columnindeChange=math.ceil(imageWidth/horizontalSplit)
  endRowindex=initialRowindex+rowindexChange
  
  newValueArray = np.zeros_like(valueArray,dtype=int)

  #Loop to split the image into multiple windows and calculate the histogram of each window independently.
  for r in range(0,verticalSplit):    
    initialColumnindex=0
    endColumnindex=initialColumnindex+columnindeChange
    if r==verticalSplit-1:
      endRowindex=imageHieght
    
    for c in range(0,horizontalSplit):

      if c==horizontalSplit-1:
         endColumnindex=imageWidth

      #Get the probability matrix of a particular window. Contains the probability = (Frequency of a Y value) / (Total number of Y components) of the window matrix.
      #Get the L (number of buckets), h(height of image),w(width of image)
      newBoxArray=valueArray[initialRowindex:endRowindex, initialColumnindex:endColumnindex]
      
      h,w,L,probabilityMatrix = calculateProbabilityOfAllValuesInYMatrix(newBoxArray)
      
      #Variable to store cumulative probability of Y value of a window  
      cumulativeProbability=0

      #Array to store the new transform of Y values in a window.
      pixelMappingArray=np.zeros((probabilityMatrix.shape[0], probabilityMatrix.shape[1]),dtype=int)

      
      for pixelPosition in range(0,probabilityMatrix.shape[0]):

          #Adding the probality of a Y value Pij to cumulative frequency.
          cumulativeProbability = cumulativeProbability+ probabilityMatrix[pixelPosition,0]
          #Calculating the transformed value of a Y component and assigning the new value in mapping array.
          pixelMappingArray[pixelPosition,0] = round((L-1) *cumulativeProbability)


      #Changing the old Y values to new transformed value using the mapping array of a window.

      for height in range(0,endRowindex-initialRowindex):
        for width in range(0,endColumnindex-initialColumnindex):        
          newValueArray[height+initialRowindex,width+initialColumnindex]= pixelMappingArray[newBoxArray[height,width]]

      initialColumnindex=endColumnindex
      endColumnindex=initialColumnindex+columnindeChange

    initialRowindex=endRowindex
    endRowindex=initialRowindex+rowindexChange

  #Plot the histogram of Y component after Histogram Equalization
  plotHistogram(newValueArray)

  #Replace the Y component in the RGB image with the new transformed value.
  tranformedImage=replaceYComponentInRGBImage(initialImage,newValueArray)
  #Save the tranformed image.
  tranformedImage.save("./Transformed/Transformed_"+image)