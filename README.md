# Gift Intake

## Overview

The University of Manitoba’s Donor Relations Department is responsible for maintaining relationships with donors. In addition, it manages significant correspondence as part of the 5-15 fundraisers it hosts throughout the year. Most of the work is completed within the Outlook inboxes, which serve as the primary storage for donor communications. To improve efficiency, the department aims to use ‘modern machine learning techniques’ to automatically extract key information from email bodies and attachments. This includes gift type, payment method, monetary value, constraints, and distribution methods by reducing the amount of manual labor required when reading emails for key information while improving the accuracy and consistency of data being extracted.

## Installation & Setup

This assume that you have [Node.js](https://nodejs.org/en), [Python](https://www.python.org/), [TesseractOCR](https://github.com/tesseract-ocr/tesseract), and [Poetry](https://python-poetry.org/) installed on the local machine.

1. Clone the repository  
   `git clone https://github.com/gift-intake/gift-intake.git`
2. First, go to the directory of the "outlook-add-in":
   - `cd outlook-add-in`
   - Install dependencies:
     `npm install`
   - Run the front-end using:
     `npm start`
3. Second, go to the directory "machine-learning":
   - `cd machine-learning`
   - Install the dependencies using:
     `poetry install`
   - Run starting the backend server using:
     `poetry run uvicorn machine_learning.main:app --reload`
4. Open your Outlook inbox in your browser and open the donation email. In the App, you will see our add-in.

## Docker

The backend can be bundled using [Docker](https://www.docker.com/) while the Docker Image file can be found in [`machine-learning/Dockerfile`](./machine-learning/Dockerfile).

## Models

We ran the test on selected LLama3.2, Deepseek-R1, Gemma2, Qwen, and GLiNER as they are all modern small models that are easily hostable CPU-based machines without a graphics card. After the experiment with different modern models, the resulting model with the best model for our sample size of 100 was GLiNER with a hamming score of 81.92%.

The model we used to help generate the datasets for the experiment and fine-tune our language model is Mistral.

## Frontend (Outlook add-in)

The Yeoman generator to scaffold the adding using [Reat.js](https://react.dev/) with [Tailwind](https://tailwindcss.com/) and [Shadcn](https://ui.shadcn.com/) to handle the styling and premade components.

## Backend

The backend for the application was written using the FastAPI framework that is used to handle all networking requestions from the client and the server. While also exposing the documentation using `http:[ip]:[port]/docs` that provides and OpenAPI schema for working with the backend.
