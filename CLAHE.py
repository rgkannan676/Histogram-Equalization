#Following code can be used for performing Contrasted Limited Adaptive Histogram Equalisation (CLAHE) using the CV2 library.
#This Assignment is done using Google Collab
import sys, os
import cv2

##Sample image files are stored inside my Google Drive.
##Below code snippet is to traverse to the right path were the images are store.
def traverseToGoogleDriveFolder():
  if 'google.colab' in sys.modules:
    from google.colab import drive
    drive.mount('/content/gdrive',force_remount=True)
    os.chdir('/content/gdrive')
    folder_name = 'workFolder'
    import subprocess
    path_to_folder = subprocess.check_output('find . -type d -name ' + str(folder_name), shell=True).decode("utf-8")
    path_to_folder = path_to_folder.replace('\n',"")
    os.chdir(path_to_folder)
      ##Traversal to the folder were images are kept completed.

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
  rgb_image = cv2.imread(image)
  #Converting Image CIELAB to differentiate colour components from brightness component.
  lab_image = cv2.cvtColor(rgb_image, cv2.COLOR_BGR2LAB)
  #Extracting L component corresponding to brightness of image
  Lab_components = cv2.split(lab_image)
  #Defining CLAHE. Mention the threshold value and grid size of the local histogram window.
  CLAHE = cv2.createCLAHE(clipLimit=40.0,tileGridSize=(8,8))
  #Perform CLAHE in the image brightness component
  Lab_components[0] = CLAHE.apply(Lab_components[0])
  #Merging the newly calculated Brightness to orginal image.
  lab_image = cv2.merge(Lab_components)
  #convert back to RGB format
  rgb_image = cv2.cvtColor(lab_image, cv2.COLOR_LAB2BGR)
  #save image
  cv2.imwrite("./Transformed/Transformed_"+image, rgb_image)
