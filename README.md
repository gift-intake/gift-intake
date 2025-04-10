# gift-intake

A Named Entity Recognition (NER) solution to extract and structure key information from unstructured donation email content.

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
