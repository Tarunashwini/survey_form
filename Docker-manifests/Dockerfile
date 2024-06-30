# Use an official Python runtime as a parent image
FROM python:3.11.9

# Install git
RUN apt-get update && \
    apt-get install -y git

# Clone the repository
RUN git clone https://github.com/Tarunashwini/survey_form.git

# Set the working directory
WORKDIR /survey_form

# Install dependencies
RUN pip install --no-cache-dir streamlit==1.25.0

RUN pip install azure-storage-blob

# Expose the port streamlit runs on
EXPOSE 8501

# Command to run streamlit app
CMD ["streamlit", "run", "application/app.py"]
