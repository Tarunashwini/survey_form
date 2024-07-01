from azure.storage.blob import BlobServiceClient
from datetime import datetime

print("azure")

# Your storage account credentials
storage_account_key = "xX5KlLkFtHNvBcHv8DKSANjt83SUAchjl3DcJu/Xgm1ShOFqXE4PPZ0jjAE1ImdqsEJWI3hSfsFe+AStekyXaA=="
storage_account_name = "storageforstreamlit"
connection_string = "DefaultEndpointsProtocol=https;AccountName=storageforstreamlit;AccountKey=xX5KlLkFtHNvBcHv8DKSANjt83SUAchjl3DcJu/Xgm1ShOFqXE4PPZ0jjAE1ImdqsEJWI3hSfsFe+AStekyXaA==;EndpointSuffix=core.windows.net"
container_name = "streamlitstoragecontainer"

def upload_to_blob_storage(file_path, file_name):
    try:
        # Create a BlobServiceClient using the connection string
        blob_service_client = BlobServiceClient.from_connection_string(connection_string)

        # Get a BlobClient to interact with the specified blob
        # Append a timestamp to the file name to ensure uniqueness
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        unique_file_name = f"{file_name}_{timestamp}"

        blob_client = blob_service_client.get_blob_client(container=container_name, blob=unique_file_name)

        # Open the file and upload its contents to Azure Blob Storage
        with open(file_path, "rb") as data:
            blob_client.upload_blob(data, overwrite=True)
        
        print("Uploaded " + unique_file_name + " file successfully.")
    
    except Exception as e:
        print(f"Failed to upload {file_name} due to {str(e)}")

# Example usage
# upload_to_blob_storage("path/to/your/file.txt", "uploaded_file_name.txt")
