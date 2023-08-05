#!/bin/bash

#kernel functions
for f in Correlate Convolve Dilate Erode Close Open DilateIntensity ErodeIntensity CloseIntensity OpenIntensity DilateI ErodeI CloseI OpenI Smooth EdgeOut EdgeIn Edge TopHat BottomHat Hmt HitNMiss HitAndMiss Thinning Thicken Distance IterativeDistance; do
  for i in Unity Gaussian DoG LoG Blur Comet Binomial Laplacian Sobel FreiChen Roberts Prewitt Compass Kirsch Diamond Square Rectangle Disk Octagon Plus Cross Ring Peaks Edges Corners Diagonals LineEnds LineJunctions Ridges ConvexHull ThinSe Skeleton Chebyshev Manhattan Octagonal Euclidean; do
  convert sample2_crop_border.jpg -colorspace Gray -morphology $f $i sample_$f+$i.jpg
  done
done
