# scrape-and-caption

A project for **data scraping, caption generation, and web application development** using Python, Amazon Bedrock, Flask, and Streamlit.  

This project has **two main parts**:  

1. **Data Scraping & Caption Generation**  
2. **Web Application for Image Upload and Captioning**  

---

## Project Overview

### 1. Data Scraping & Model Invocation
- Scraped product images from **Mytheresa**.  
- Invoked the **Claude Sonnet 3.5 v2 model** via Amazon Bedrock to generate professional captions for a subset of images in `Task1/under_1000`.  

**Scraped Data Details:**
- 1000 images of women’s clothes → `Task1/women_clothing`  
- 100 images of shoes → `Task1/shoes`  
- 50 images from designer “Saint Laurent” → `Task1/saint_laurent`  
- 20 clothes under 1000 euros → `Task1/under_1000`  

---

### 2. Web Application Development

**Frontend (Streamlit):**
- Allows users to upload an image.  
- Stores the uploaded image in an **Amazon S3 bucket**.  
- Displays the generated caption returned by the backend.  

**Backend (Flask):**
- Receives requests from the frontend.  
- Invokes the **Claude Sonnet model**.  
- Sends the generated caption back to the frontend.  

---

### Languages and Tools Used

- **Programming Language:** Python  
- **Frameworks & Libraries:**  
  - Flask – Backend API  
  - Streamlit – Frontend application  
  - boto3 – AWS S3 interaction  
  - requests, urllib.parse, io, csv, json, base64, os, botocore.exceptions – Utility and data handling  

---

## Amazon Bedrock Setup

1. Download your **AWS Access Keys**:  
   - Open the AWS Console → IAM → Users → [Your User] → Security Credentials → Access Keys  
   - Download the keys and save them securely (do **not** upload to GitHub)  

2. Configure AWS CLI:

```
aws configure
# Enter AWS Access Key ID
# Enter AWS Secret Access Key
# Set Default Region (e.g., us-west-2)
# Set Default Output Format (json)
```
## Folder Structure
```
scrape-and-caption/
│
├─ application/
│   ├─ backend/
│   │   ├─ app.py           # Flask backend for handling image uploads and caption generation
│   │   └─ model_claude.py  # Code to interact with Claude model
│   │
│   ├─ frontend/
│   │   ├─ index.py         # Streamlit frontend
│   │   └─ requirements.txt # Dependencies for frontend
│
├─ model_inference.py       # Generates captions for images in Task1/under_1000
├─ scrape_data.py           # Scrapes images from Mytheresa
└─ README.md

```
## Installation and Setup
### 1. Clone the repository

```
git clone https://github.com/Jinanrachid/scrape-and-caption.git
cd scrape-and-caption
```

 ### 2. Create a virtual environment

```
python -m venv .venv
```
### 3. Activate the virtual environment

```
.venv\Scripts\activate  # Windows
```
### 4. Install dependencies

```
pip install -r application/frontend/requirements.
```
## Usage Instructions
### Part 1: Scraping Data
```
python scrape_data.py
```
### Part 2: Generate Captions for Task1/under_1000
```
python model_inference.py
```
- Uses model_claude.py to generate captions for every image in Task1/under_1000.
- Saves results as a CSV file named captions.csv in the same folder.
### Part 3: Run Web Application
```
cd application/backend
python app.py
```
Frontend (Streamlit): (in a separate terminal)
```
cd application/frontend
streamlit run index.py
```


