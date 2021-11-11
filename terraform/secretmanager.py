from google.cloud import secretmanager

def access_secret_version(project_id, secret_id, version_id):
    client = secretmanager.SecretManagerServiceClient()

    # Build the resource name of the secret version.
    name = f"projects/{project_id}/secrets/{secret_id}/versions/{version_id}"

    # Access the secret version.
    response = client.access_secret_version(request={"name": name})

    payload = response.payload.data.decode("UTF-8")

    return payload


#if __name__=="__main__":
#    projekti = os.getenv('PROJEKTI')
#    secret_id = os.getenv('SECRET_ID')
#    version_id = os.getenv('VERSION_ID')
#    access_secret_version(projekti, secret_id, version_id)