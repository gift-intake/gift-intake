# Gift Intake

## Overview

A Named Entity Recognition (NER) solution to extract and structure key information from unstructured donation email content.

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

## Frontend (Outlook add-in)

The Yeoman generator to scaffold the adding using [Reat.js](https://react.dev/) with [Tailwind](https://tailwindcss.com/) and [Shadcn](https://ui.shadcn.com/) to handle the styling and premade components.

## Backend

The backend for the application was written using the FastAPI framework that is used to handle all networking requestions from the client and the server. While also exposing the documentation using `http:[ip]:[port]/docs` that provides and OpenAPI schema for working with the backend.
