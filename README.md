# PDF Converter
**A real-time OCR model tailored for printed texts(those in PDF files) based on CRNN, acc% = 98%**  
Text extraction from PDFs has distinct characteristics compared to general OCR tasks:  
1. Compared to real-world images, the pixel complexity is not high when recognizing text in PDFs.  
2. The content to be recognized consists entirely of printed fonts, making it easier to build targeted training samples.  
3. To enhance text information accuracy, not all text contents need to be detected.  
  
Therefore, by analyzing the above characteristics, my goal is to establish an OCR-based converter that is more focused on the distinctive features of PDF recognition and possesses higher accuracy.  
After a study of relevant theoretical methods, the task of the PDF converter is divided into four mini tasks, as:   
1. Targeted training samples generation.  
2. Implementation of a filtering and recognition mechanism for PDFs.   
3. Image grayscale processing.  
4. Recognition model. 
Here is the whole picture of the design of PDF Converter:    
<p align="center">
    <img src="https://github.com/Venyus/OCR/assets/118938648/d759b065-0e3d-4ef0-a4c2-c49f36529cc2">
</p>
  
**Specified Raw Data Generation**  
The target of the PDF converter is printed text. In order to obtain a model that aligns more closely with the task objectives and achieves better performance, I exclusively generate training data instead of opting for publicly available data sources.
To maximize my training data and the model's generalization ability in PDF context conversion, I have considered various potential variable factors when detecting the text, including:  
<p align="center">
    <img src="https://github.com/Venyus/OCR/assets/118938648/5f51e89c-26fa-481f-9183-002bbead4c28">
</p>

1. Text Content: In fact, the object I aim to detect is the English text of annual reports. The units composing the data should include various possible punctuation marks and English letters. However, after multiple attempts, generating raw data by randomly organizing the units might lead to an excessively large training loss, consequently causing gradient vanishing when training the model. Therefore, for the text content, I ultimately adopted text from Reuters' publicly available news database.  
2. Font size and Font Style: To further ensure the model's generalization ability and enhance sample diversity, font size and font format are also variable. The font size varies from 14 to 24 randomly within raw data samples, which aligns with the font sizes commonly found in the body text of PDF reports. Moreover, I collect 42 different font style and their transformers, such as Arial, Arial Bold, Arial Italic, Arial Light, Times New Roman, Times New Roman Bold, and so on.   
3. Background color: The background color of the text area is also present in PDF reports, which is a necessary consideration for text detection. To further enhance the final performance of the model, I randomly selected background color of the texts for nine chosen light colors, as ‘White’, ‘Light Blue’, ‘Light Pink’, ‘Light Yellow’, ‘Light Green’, ‘Light Orange’, ‘Light Purple’, ‘Light Gray’ and ‘Light Brown’.  
4. Num of Char: By examining the texts in each line of the PDF reports, the character count for each line in the generated raw data ranges from 10 to 100.  
5. Other Notes: The position of the text within the image also significantly impacts the model's performance, but the solution to this issue will be reflected in image processing.

**Implementation of Recognizer**  
Locating the texts to be recognized in PDF reports is a crucial but challenging task. Firstly, PDF report styles vary significantly, and constructing a labeled, trainable PDF set is difficult. Additionally, not every section of text in a PDF report contains relevant and useful information, such as sidebar directories. These factors can potentially result in misalignment of text, sentences interleaving, and a reduction in the information quality of paragraphs during recognition.  
Faced with the issues mentioned above, I decided to build up a visual user interface (UI) to facilitate manual recognition as much as possible, ensuring the quality of detecting results.  
<p align="center">
    <img src="https://github.com/Venyus/OCR/assets/118938648/051ce0b6-e12b-4148-b28c-14fa322282d9">
</p>  

To seamlessly integrate with the subsequent recognition model, this is a Python-based UI interface. It also supports real-time recognizing using the recognition model.  
**Image Processing**  
Firstly, this is a highly effective component in improving model performance. Before adding the image processing module, the model's average accuracy was around 20%. After incorporating image processing, the accuracy of the model started to increase to over 80%. Image Processing includes three functions: 1) image grayscale, 2) splitting an image with multi-text-line into multiple images with single-text-line, 3) and text centering.  
1. Image Grayscale: To enhance the feature extraction during network training and for subsequent steps, splitting an image with multi-text-line into multiple images with single-text-line, I have applied grayscale to both the train data for training model and the data to be recognized to trained model. The following images are the examples of grayscale.
<p align="center">
    <img src="https://github.com/Venyus/OCR/assets/118938648/c7bcb691-2063-439b-ba64-680794643982">
</p>  

To obtain a clear and information-preserved grayscale image, I first deactivate the three channels of the image's RGB, preserving a single channel. Then I construct an ‘Gray Pixel Values and Image Rendering Mapping’, visualized as below.
<p align="center">
    <img src="https://github.com/Venyus/OCR/assets/118938648/6776d9c9-61e3-4af7-858f-2628c92d2220">
</p> 

After multiple testing, the pixel around 130 was found to be the most suitable as the grayscale threshold. This means that pixel value below the threshold is to be converted to 0, and value above the threshold is to be converted to 255 during the grayscale conversion.  
3. Splitting the multi-text-line image and text centering: No matter during the model training process or recognizing texts from images, the presence of multiline texts of input images tends to increase the complexity of the recognition task, leading to a significant decrease in accuracy. To address this, both during model training and subsequent image recognition, preprocessing steps are implemented to split images in advance. This is done to ensure an enhanced performance of the model.  
Following the previous step, the image underwent grayscale processing, resulting in pixel values representing with only two distinct: 0 and 255. Here, 0 indicates the area containing texts, while 255 represents the background region. Based on the pixel values, I can perform splitting the multi-text-line image and text centering as illustrated in the following.  
<p align="center">
    <img src="https://github.com/Venyus/OCR/assets/118938648/2d472110-b9fb-4f6a-9f74-91ce88b712b5">
</p>  

In simple terms, I identify entire rows or columns with pixel values of 255 as split boundaries. Consequently, multiple lines of content are transformed into individual lines.  
After splitting the multi-text-line image and text centering the input image, I retain only the regions containing texts. This results in a highly standardized set of objects for recognition.  

**Recognition Model**  
The combination of CRNN with CTC provides a powerful solution for text detection. Firstly, through end-to-end learning, the model can directly learn from images to character sequences without the need for manual feature design. Secondly, the bidirectional LSTM layers effectively capture the sequential information of characters, crucial for the accuracy of text detection. Simultaneously, the convolutional layers offer sensitivity to spatial features, while the LSTM layers model temporal dependencies, enabling the model to comprehend both local details and global context. The introduction of CTC loss enhances the flexibility of the network in handling text sequences of varying lengths, adapting to diverse text lengths. This combination also enables the network to effectively handle variable-length texts, showcasing excellence across various real-world scenarios.  
Building on the considerations mentioned above, I have decided to construct a CRNN+CTC architecture for text detection of PDF. The following is the architecture diagram of our network.  
<p align="center">
    <img src="https://github.com/Venyus/OCR/assets/118938648/514976bb-ced5-4db7-9f24-c341fb9c0969">
</p>  

In summary, the CRNN model consists of a CNN for feature extraction and a BiLSTM for sequence modeling. The final output is a sequence of characters, with each character being associated with a specific time step.  


**Selected Model and Its Performance**  
Based on the mentioned framework for text detection, I fine-tuned a total of 11 models by adjusting training samples, text lengths, model hyperparameters, and other parameters. In the end, the selected model is as follows:  
<p align="center">
    <img src="https://github.com/Venyus/OCR/assets/118938648/d232a3e7-1383-4db3-bd12-d53806ee965b">
</p>  

And here is the summary of the CRNN network:  
<p align="center">
    <img src="https://github.com/Venyus/OCR/assets/118938648/9d5c0e78-10f0-44ce-8988-dbf3530a8e7a">
</p>  
  
**Results**  
<p align="center">
    <img src="https://github.com/Venyus/OCR/assets/118938648/985bbca5-b2fb-4a64-a836-e48d74b2414b">
</p> 

<p align="center">
    <img src="https://github.com/Venyus/OCR/assets/118938648/d684b0fe-c607-4fec-b5a3-057971bfe0d1">
</p> 

<p align="center">
    <img src="https://github.com/Venyus/OCR/assets/118938648/e8f33ee8-fe81-4904-8ae3-c34104bf1fb5">
</p> 
  
**Code Files Association Guide**  
<p align="center">
    <img width="601" alt="image" src="https://github.com/Venyus/OCR/assets/118938648/64479532-59c2-4f75-add6-50c2af53995b">
</p> 

