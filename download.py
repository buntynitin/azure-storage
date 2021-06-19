from azure.storage.blob import ContainerClient


def download(connection_string, container_name, blob_name):
    # noinspection PyBroadException
    try:
        container_client = ContainerClient.from_connection_string(connection_string, container_name)
        blob_client = container_client.get_blob_client(blob_name)
        bytes_content = blob_client.download_blob().readall()
        with open("files/" + blob_name, "wb") as file:
            file.write(bytes_content)
            return True
    except Exception:
        return False
