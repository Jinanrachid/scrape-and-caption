import streamlit as st
import requests
import boto3
import io
from botocore.exceptions import ClientError

# --- AWS S3 Configuration ---
BUCKET_NAME = "captiongenerationbucketjr2025"

def get_s3_client():
    """Create and return an S3 client."""
    return boto3.client("s3")

def bucket_exists(s3, bucket_name: str) -> bool:
    """Check if S3 bucket exists."""
    try:
        s3.head_bucket(Bucket=bucket_name)
        return True
    except ClientError as e:
        error_code = e.response["Error"]["Code"]
        if error_code in ("404", "NoSuchBucket"):
            return False
        st.error(f"Error checking bucket: {e}")
        return False

def upload_to_s3(s3, file, bucket_name):
    """Upload file to S3."""
    try:
        image_for_s3 = io.BytesIO(file.getvalue())
        s3.upload_fileobj(image_for_s3, bucket_name, file.name)
        st.info(f" Uploaded {file.name} to {bucket_name}")
    except Exception as e:
        st.error(f"Error uploading image to S3: {e}")

def request_caption(file):
    """Send image to backend for caption generation."""
    try:
        # Prepare the file for the request
        files = {"image": (file.name, file, file.type)}
        # Send POST request to the backend
        response = requests.post("http://localhost:5000/caption", files=files)

        # Check if the response is successful
        if response.ok:
            # Safe JSON parsing with fallback to plain text
            try:
                caption = response.json().get("caption", response.text)
            except ValueError:
                caption = response.text
            st.markdown(caption)
        else:
            # Handle error message properly
            try:
                error_msg = response.json().get("error", response.text)
            #if JSON parsing fails, fallback to plain text
            except ValueError:
                error_msg = response.text
            #print error message in Streamlit
            st.error(f"Backend Error [{response.status_code}]: {error_msg}")

    #handle request exception
    except requests.exceptions.RequestException as e:
        st.error(f"Request failed: {e}")

# --- Streamlit App ---
st.title("📸 Image Caption Generator")

s3 = get_s3_client()

if not bucket_exists(s3, BUCKET_NAME):
    st.error(f" Bucket {BUCKET_NAME} does not exist. Please create it in AWS S3.")
else:
    uploaded_image = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

    if uploaded_image:
        # Display uploaded image
        st.image(uploaded_image, caption="Uploaded Image", use_container_width=True)

        # Upload to S3
        upload_to_s3(s3, uploaded_image, BUCKET_NAME)

        # Caption generation
        if st.button("Generate Caption"):
            with st.spinner("Generating caption..."):
                request_caption(uploaded_image)
