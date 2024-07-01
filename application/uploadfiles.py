from azure.storage.blob import BlobServiceClient
import os

print("azure")

# Your storage account credentials
storage_account_key = "xX5KlLkFtHNvBcHv8DKSANjt83SUAchjl3DcJu/Xgm1ShOFqXE4PPZ0jjAE1ImdqsEJWI3hSfsFe+AStekyXaA=="
storage_account_name = "storageforstreamlit"
connection_string = "DefaultEndpointsProtocol=https;AccountName=storageforstreamlit;AccountKey=xX5KlLkFtHNvBcHv8DKSANjt83SUAchjl3DcJu/Xgm1ShOFqXE4PPZ0jjAE1ImdqsEJWI3hSfsFe+AStekyXaA==;EndpointSuffix=core.windows.net"
container_name = "streamlitstoragecontainer"

def append_to_blob_storage(file_path, file_name):
    try:
        # Create a BlobServiceClient using the connection string
        blob_service_client = BlobServiceClient.from_connection_string(connection_string)

        # Get a BlobClient to interact with the specified blob
        blob_client = blob_service_client.get_blob_client(container=container_name, blob=file_name)

        # Download the existing file if it exists
        existing_data = b""
        if blob_client.exists():
            download_stream = blob_client.download_blob()
            existing_data = download_stream.readall()
        
        # Read the new data
        with open(file_path, "rb") as data:
            new_data = data.read()
        
        # Combine the existing data and new data
        combined_data = existing_data + new_data

        # Upload the combined data back to Azure Blob Storage
        blob_client.upload_blob(combined_data, overwrite=True)
        
        print(f"Uploaded {file_name} file successfully.")
    
    except Exception as e:
        print(f"Failed to upload {file_name} due to {str(e)}")

# Example usage
# append_to_blob_storage("path/to/your/file.txt", "uploaded_file_name.txt")
