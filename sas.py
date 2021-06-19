from datetime import datetime, timedelta
from azure.storage.blob import generate_blob_sas, generate_container_sas, BlobSasPermissions, ContainerSasPermissions


def download_blob_sas(account_name, account_key, container_name, blob_name, expiration_time):
    sas = generate_blob_sas(account_name=account_name,
                            account_key=account_key,
                            container_name=container_name,
                            blob_name=blob_name,
                            permission=BlobSasPermissions(read=True),
                            expiry=datetime.utcnow() + timedelta(minutes=expiration_time))

    sas_url = 'https://' + account_name + '.blob.core.windows.net/' + container_name + '/' + blob_name + '?' + sas
    return sas_url


def upload_blob_sas(account_name, account_key, container_name, blob_name, expiration_time):
    sas = generate_container_sas(account_name=account_name,
                                 account_key=account_key,
                                 container_name=container_name,
                                 permission=ContainerSasPermissions(write=True),
                                 expiry=datetime.utcnow() + timedelta(minutes=expiration_time))

    sas_url = 'https://' + account_name + '.blob.core.windows.net/' + container_name + '/' + blob_name + '?' + sas
    return sas_url

# if __name__ == '__main__':
#     config = load_config()
#     # print(generate_sas_blob_token(config["azure_storage_connectionstring"], config["images_container_name"],
#     #                               "database.svg"))
#     print(generate_sas_container_token(config["azure_storage_connectionstring"], config["images_container_name"]))
