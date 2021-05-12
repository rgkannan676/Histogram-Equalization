# Histogram Equalization
Histogram equalization is a method used in image processing to improve the contrast of the image. The basic principle of Histogram equalization is to spread out the high frequency pixels so that areas with lower contrast can obtain higher contrast. This method will increase the global contrasts of the image without loss of any information. 

![image](https://user-images.githubusercontent.com/29349268/118016699-4afdc000-b388-11eb-93ea-298370e153f9.png)

**Fig:** Histogram of pixel intensity before and after Histogram equalization. The frequency of the pixel intensity is more spread out after the equalization.

# Steps of Histogram Equalization.
1.	Fix the number of buckets L to which values can be transformed. In an image, pixel values can vary from 0 to 255, therefore L=256.
2.	Calculate the total number of pixels (MN) in the image. This will be equal to M (length) * N (width) of image. 
For example, M = 100 N = 250, M*N = 25000
3.	Find the frequency of a pixel intensity in the image. 
For example, if a pixel intensity of value 150 is present in 4000 times in the image, then the frequency of the pixel intensity value 150 is 4000. Similarly find frequency for each pixel intensity. 
4.	Find the probability of each pixel intensity in the image. This can be calculated by Frequency of a Value / total number of pixels (MN). 
For example, Frequency of pixel intensity 150 =4000 and MN= 25000, then probability = 4000/25000 = 0.16
5.	Transform the old pixel intensities into new Histogram equalized intensities.
New value = (L-1) *∑ Pj, where ∑ Pj is the cumulative probability of all pixel intensity values till the value whose transform is being calculated.
6.	Replace the old pixel intensities with new one in the image. 

# Samples images before and after applying histogram equalization

![image](https://user-images.githubusercontent.com/29349268/118016963-9d3ee100-b388-11eb-858f-7aca1357b0a0.png)
![image](https://user-images.githubusercontent.com/29349268/118018924-f90a6980-b38a-11eb-81c9-39dd2046e174.png)

# Advantages of Histogram Equalization
1.	This is a simple and straight forward method to improve the contrast of image.
2.	This is a very good and effective technique to improve the contrast of the images which were took in low light. For example, see the below sampled image.  

![image](https://user-images.githubusercontent.com/29349268/118017347-14747500-b389-11eb-938c-a5d423aa8872.png)

**Fig:** The above figures are before and after histogram equalization, respectively. Here we can see that many features in the low light area are clearly visible after then equalization. 

# Disadvantages of Histogram Equalization
1.	The histogram equalization can map pixel values which were close to values which are far apart. This can cause the image to loss its smoothness. Can cause the image to be bumpy in some areas. See the below example:
 
![image](https://user-images.githubusercontent.com/29349268/118017613-69b08680-b389-11eb-9236-29a28d225afb.png)

**Fig:** In the above histogram plots, before and after histogram equalization, we can see the pixel intensities in the circled portion, which were close to each other are mapped to pixel values with a visible difference. 
 
![image](https://user-images.githubusercontent.com/29349268/118017702-81880a80-b389-11eb-8b40-8faaf0a39203.png)

**Fig:** In the above figure before and after histogram equalization, we can see that the circled portion has loss the smoothness after histogram equalization.

2.	Histogram equalization can amplify the noises in an image.  The noises and nearby pixels can be mapped to pixel intensities that can be far apart. This will make the noises in the picture more noticeable and can reduce the quality of the image. For example, see the below figure

![image](https://user-images.githubusercontent.com/29349268/118017803-9b295200-b389-11eb-9126-3e4928a1fb1e.png)

**Fig:** In the above figure before and after histogram equalization respectively, we can see that the circled portion which has a noise caused by the folding of image has been amplified after the histogram equalization.

3.	If large number of pixels have a particular pixel intensity, this may cause large band of pixel intensities to be mapped one intensity. If a large number of pixels are mapped to a particular pixel intensity value, this will cause the probability of that pixel intensity to be large. In Histogram equalization New pixel intensity value = (L-1) *∑ Pj, where ∑ Pj is the cumulative probability of all pixel intensity. So, when the probability is high, the pixels will be mapped to new pixel intensity which will be far away from the previous newly mapped pixel intensity. This will reduce the smoothness of the image. Please see the below example

![image](https://user-images.githubusercontent.com/29349268/118017891-b5fbc680-b389-11eb-9355-af23b0cd5c48.png)

**Fig:** The first image is the histogram of image before equalization. Here we can see that the number of pixels which has pixel intensity 255 is very large compared to other pixels. Due to this while doing histogram equalization, intensities less than 255 is mapped to pixel values with low intensities due to low probability values. This causes a large gap in the histogram of pixel intensities causing the loss of smoothness. 

![image](https://user-images.githubusercontent.com/29349268/118017958-c7dd6980-b389-11eb-8b48-a6a8f8e90f9b.png)

**Fig:** Above are the images of the histograms mentioned in previous figure. In the equalized image, we can note that the pixel intensity 255 (high brightness) is predominant and the transformation is not smooth with the neighbouring pixels. This is because of the large gap in pixel intensity histogram values.

# Improvements in Histogram Equalization
**1**.	To reduce the loss of smoothness, a smoothening filter can be applied. After the histogram equalization, a smoothening filter like bilateral filtering can be used.
This will make the image smooth and will reduce the noise created by equalization. The bilateral filter in the library OpenCV2 was used for smoothening the image. Below is the code used.

```
  import cv2 as cv
  tranformedImage = cv.imread("./Transformed/Transformed_"+image)
  #Filtering the transformed image after Histogram Equalization
  filteredImage=cv.bilateralFilter(tranformedImage, 20, 90, 90)
  cv.imwrite("./Smoothen/Smoothen_"+image, filteredImage)
```

![image](https://user-images.githubusercontent.com/29349268/118018197-12f77c80-b38a-11eb-9864-6f181236c8e0.png)

**Fig**: The above images are before and after smoothening filter applied in a histogram equalized image. We can see that the image where bilateral filter applied is smoother and have less noise.

**2**.	One of the issues of Global Histogram equalization is that the contrast of regions with significant brighter or darker will not be sufficiently enhanced. Instead of applying global histogram, we can apply localized histogram equalization by dividing the image into multiple boxes and applying the histogram equalization on each of them independently.

![image](https://user-images.githubusercontent.com/29349268/118018340-3b7f7680-b38a-11eb-82fd-51d28a8b655e.png)

**Fig**: First is the original image. Second is image where Histogram equalization was done globally. In the third image Histogram equalization was done locally after splitting the image into four windows. From above images we can see that the contrast of the circled(dark) region was better in the local window-based histogram equalization. 

In local window HE technique each window will be independent to each other. This will improve the contrast of areas which are significantly brighter or darker. But the issue with this technique is that there is a clear separation in the intensity values in the border region of the windows.

**3**.  But with the above process, we can see that there is intensity discontinuity in the chosen window borders. To avoid this Adaptative Histogram Equalization (AHE) can be used. This will smoothen the window border using interpolation of the pixels at border. 

**4**. Contrasted Limited AHE (CLAHE) is another variation of AHE where contrast is limited by a threshold. This will reduce the amplification of noise by limiting the contrast amplification in AHE.

![image](https://user-images.githubusercontent.com/29349268/118018533-7da8b800-b38a-11eb-9249-ab97c19cd7b3.png)

**Fig**: First is the original image. In second image Histogram equalization was done globally. In third image Histogram equalization was done locally after splitting the image into four windows. In fourth image CLAHE was performed. From this image we can understand that CLAHE enhances contrast of regions which has extensive bright or dark regions and provides a smoother image by avoiding noises using threshold limiting
