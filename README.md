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
3.Image grayscale processing.  
4.Recognition model. 
Here is the whole picture of the design of PDF Converter: 

![image](https://github.com/Venyus/OCR/assets/118938648/d759b065-0e3d-4ef0-a4c2-c49f36529cc2)  

**Specified Raw Data Generation**  
The target of the PDF converter is printed text. In order to obtain a model that aligns more closely with the task objectives and achieves better performance, we exclusively generate training data instead of opting for publicly available data sources.
To maximize our training data and the model's generalization ability in PDF context conversion, we have considered various potential variable factors when detecting the text, including:  
![image](https://github.com/Venyus/OCR/assets/118938648/5f51e89c-26fa-481f-9183-002bbead4c28)  
1.Text Content: In fact, the object we aim to detect is the English text of annual reports. The units composing the data should include various possible punctuation marks and English letters. However, after multiple attempts, generating raw data by randomly organizing the units might lead to an excessively large training loss, consequently causing gradient vanishing when training the model. Therefore, for the text content, we ultimately adopted text from Reuters' publicly available news database.  
2.Font size and Font Style: To further ensure the model's generalization ability and enhance sample diversity, font size and font format are also variable. The font size varies from 14 to 24 randomly within raw data samples, which aligns with the font sizes commonly found in the body text of PDF reports. Moreover, we collect 42 different font style and their transformers, such as Arial, Arial Bold, Arial Italic, Arial Light, Times New Roman, Times New Roman Bold, and so on.  
3.Background color: The background color of the text area is also present in PDF reports, which is a necessary consideration for text detection. To further enhance the final performance of the model, we randomly selected background color of the texts for nine chosen light colors, as ‘White’, ‘Light Blue’, ‘Light Pink’, ‘Light Yellow’, ‘Light Green’, ‘Light Orange’, ‘Light Purple’, ‘Light Gray’ and ‘Light Brown’.  
4.Num of Char: By examining the texts in each line of the PDF reports, the character count for each line in the generated raw data ranges from 10 to 100.  
5.Other Notes: The position of the text within the image also significantly impacts the model's performance, but the solution to this issue will be reflected in image processing.  

