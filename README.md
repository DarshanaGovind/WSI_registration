# WSI_registration

This code for whole slide-based image registration has been developed by Darshana Govind (d8@buffalo.edu).

The codes register two whole slide images (WSIs), PAS and IF, where PAS is the fixed image and IF is the image to be registered. The code also extracts the registered glomeruli (annotations must be given as input to the pipeline as an xml file) in high resultion, ffrom both whole slides.

The code 'Precise_registration.py' can be given the exact x and y translation values for precise registration.

The code 'landmark_based_registration.py' can be used to select landmark points on two WSIs to register them.




