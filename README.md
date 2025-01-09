# gift-intake

A Named Entity Recognition (NER) solution to extract and structure key information from unstructured donation email content.

## Docker

To set up the environment for testing and running the application, we use Docker to containerize the environment and deploy the application. It is assumed that Docker and Docker Compose are installed and functioning properly.

First, create a .env file in the root directory to store the credential information:

```env
POSTGRES_USER=giftintake_dev
POSTGRES_PASSWORD=giftintake_dev
```

To run the application, simply execute the following command:

```bash
docker-compose up
```
