# PDF Converter
**A real-time OCR model tailored for printed texts(those in PDF files) based on CRNN**
Text extraction from PDFs has distinct characteristics compared to general OCR tasks:
1.Compared to real-world images, the pixel complexity is not high when recognizing text in PDFs.
2.The content to be recognized consists entirely of printed fonts, making it easier to build targeted training samples.
3.To enhance text information accuracy, not all text contents need to be detected.

Therefore, by analyzing the above characteristics, my goal is to establish an OCR-based converter that is more focused on the distinctive features of PDF recognition and possesses higher accuracy.
After a study of relevant theoretical methods, the task of the PDF converter is divided into four mini tasks, as: 
1.Targeted training samples generation. 
2.Implementation of a filtering and recognition mechanism for PDFs. 
3.Image grayscale processing
4.Recognition model. 
Here is the whole picture of the design of PDF Converter: 

![image](https://github.com/Venyus/OCR/assets/118938648/d759b065-0e3d-4ef0-a4c2-c49f36529cc2)

**Specified Raw Data Generation**  
The target of the PDF converter is printed text. In order to obtain a model that aligns more closely with the task objectives and achieves better performance, we exclusively generate training data instead of opting for publicly available data sources.
To maximize our training data and the model's generalization ability in PDF context conversion, we have considered various potential variable factors when detecting the text, including:
