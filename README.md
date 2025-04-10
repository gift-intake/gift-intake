# Gift Intake 
## Overview
  The University of Manitoba’s Donor Relations Department is responsible for maintaining relationships with donors. In addition, it manages significant correspondence as part of the 5-15 fundraisers it hosts throughout the year. Most of the work is completed within the Outlook inboxes, which serve as the primary storage for donor communications. To improve efficiency, the department aims to use ‘modern machine learning techniques’ to automatically extract key information from email bodies and attachments. This includes gift type, payment method, monetary value, constraints, and distribution methods by reducing the amount of manual labor required when reading emails for key information while improving the accuracy and consistency of data being extracted.

## Installation & Setup
1. Clone the repository  
```git clone https://github.com/gift-intake/gift-intake.git```
2. First, go to the directory of the "GiftIntake-add-in "  
   ```cd GiftIntake-add-in```
    - Install dependencies  
   ```npm i```    
    - Run the frount-end(Outlook add-in)   
   ```npm start```
 3. Second, go to the directory of the "machine_learning"  
    ```cd machine-learning/machine_learning```  
     - Install the dependencies  
     ```poetry install```  
     - Run the back-end  
     ```poetry run uvicorn machine_learning.main:app --reload```  
4. Open your Outlook inbox in your browser and open the donation email. In the App, you will see our add-in.

## Models
  We ran the test on selected LLama3.2, Deepseek-R1, Gemma2, Qwen, and GLiNER as they are all modern small models that are easily hostable CPU-based machines without a graphics card. After the experiment with different modern models, the resulting model with the best model for our sample size of 100 was GLiNER with a hamming score of 81.92%.
  
  The model we used to help generate the datasets for the experiment and fine-tune our language model is Mistral. 

## Front-end(Outlook add-ins)
  We use the Yeoman generator to build the base frame of the add-ins with Reat.js.  
  
## Back-end
  
