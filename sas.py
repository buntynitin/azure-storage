import os
import yaml
from datetime import datetime, timedelta
from azure.storage.blob import generate_blob_sas, generate_container_sas, BlobSasPermissions, ContainerSasPermissions


def load_config():
    dir_root = os.path.dirname(os.path.abspath(__file__))
    with open(dir_root + "/config.yaml", "r") as yamlfile:
        return yaml.load(yamlfile, Loader=yaml.FullLoader)


# def sas(connection_string, container_name, blob_name):
#     container_client = ContainerClient.from_connection_string(connection_string, container_name)
#     blob_client = container_client.get_blob_client(blob_name)
#     sas_url = generate_blob_sas(account_name='nitinstorageazure', container_name=container_name, blob_name=blob_name, account_key='zVg54DKtp4iQPdUNXdIJo9uNUrG7KcnCEROZc3mbeeUYPQYZkcG9ey26VTNUEwDiDonXl3Nbpr3meQYhUu+4qQ==')
#     return 'https://' + 'nitinstorageazure' + '.blob.core.windows.net/' + container_name + '/' + blob_name + '?' + sas_url

def generate_sas_blob_token(connection_string, container_name, file_name):
    sas = generate_blob_sas(account_name='nitinstorageazure',
                            account_key='zVg54DKtp4iQPdUNXdIJo9uNUrG7KcnCEROZc3mbeeUYPQYZkcG9ey26VTNUEwDiDonXl3Nbpr3meQYhUu+4qQ==',
                            container_name=container_name,
                            blob_name=file_name,
                            permission=BlobSasPermissions(read=True, write=True, delete=True),
                            expiry=datetime.utcnow() + timedelta(hours=2))

    logging.info(
        'https://' + 'nitinstorageazure' + '.blob.core.windows.net/' + container_name + '/' + file_name + '?' + sas)
    sas_url = 'https://' + 'nitinstorageazure' + '.blob.core.windows.net/' + container_name + '/' + file_name + '?' + sas
    return sas_url


def generate_sas_container_token(connection_string, container_name):
    sas = generate_container_sas(account_name='nitinstorageazure',
                                 account_key='zVg54DKtp4iQPdUNXdIJo9uNUrG7KcnCEROZc3mbeeUYPQYZkcG9ey26VTNUEwDiDonXl3Nbpr3meQYhUu+4qQ==',
                                 container_name=container_name,
                                 permission=ContainerSasPermissions(read=True, list=True, write=True),
                                 expiry=datetime.utcnow() + timedelta(hours=2))

    logging.info('https://' + 'nitinstorageazure' + '.blob.core.windows.net/' + container_name + '?' + sas)
    sas_url = 'https://' + 'nitinstorageazure' + '.blob.core.windows.net/' + container_name + '?' + sas
    return sas_url


if __name__ == '__main__':
    config = load_config()
    # print(generate_sas_blob_token(config["azure_storage_connectionstring"], config["images_container_name"],
    #                               "database.svg"))
    print(generate_sas_container_token(config["azure_storage_connectionstring"], config["images_container_name"]))