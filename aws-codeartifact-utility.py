import boto3
import re

"""
Author: Wilker Guedes
Email: wilker.senag@gmail.com
Description: Download in a local folder all maven artifacts and its versions from AWS CodeArtifact and generate Maven deploy command to all artifacts.

"""

# Initial Setup
region = 'us-east-2' # The region where artifacts are.
artifact_folder = 'myartifacts' # The local folder where you'd like to store the artifacts, it must be created in the same level of this script.
default_domain = 'your_artifact_domain' # The domain name associated with your artifacts repositories.
default_repository = 'your_artifact_repository' # The name of your specific repository.
default_domain_owner = 'your_aws_account_id' # The account ID number

# The domain, repository and account ID destination to be used in the deploy command.
destination_domain = 'your_destination_artifact_domain' # The domain name associated with your artifacts repositories.
destination_repository = 'your_destination_artifact_repository' # The name of your specific repository.
destination_domain_owner = 'your_destination_aws_account_id' # The account ID number
destination_region = 'us-east-2' # The region where artifacts will be stored.

client = boto3.client('codeartifact',
    aws_access_key_id ='AAAAAAAAAAAAAAAAAA', # Your Access key ID.
    aws_secret_access_key ='9999999999999999999999999999', # Your Secret access key.
    region_name=region
    )


package_list = []  # Store the list of packages identifyed in the repository
deploy_command = [] # The list of commands to deploy the package, it wil be stored in a txt file in the end of script execution.


package_list_temp = client.list_packages(
    domain = default_domain,
    domainOwner = default_domain_owner,
    repository = default_repository,
    format = 'maven'
)


package_list = package_list_temp['packages']


def get_package_version(package,namespace):
    """_summary_

    Args:
        package (String): The name of the requested package.
        namespace (String): The namespace of the package. The package component that specifies its namespace depends on its type.
        For example: The namespace of a Maven package is its groupId.

    Returns:
        List : A list of versions of the requested package.
    """

    response = client.list_package_versions(
        domain = default_domain,
        domainOwner = default_domain_owner,
        repository = default_repository,
        format = 'maven',
        namespace = namespace,
        package = package,
        status = 'Published',
        maxResults=10,
    )
    
    
    return response['versions']


for package in package_list:
    """_summary_
    For each package listed in the repository, this loop will get its version
    and for each versions it will download the artifacts ".pom" and ".jar" files.
    """
    versions = get_package_version(package['package'],package['namespace'])
    package['version'] = versions
    
    for version in versions:
        
        assets = client.list_package_version_assets(
            domain = default_domain,
            domainOwner = default_domain_owner,
            repository = default_repository,
            format = 'maven',
            namespace = package['namespace'],
            package = package['package'],
            packageVersion = version['version'],
            maxResults=10
        )
    
        for asset in assets['assets']:
    
            file = client.get_package_version_asset(
                domain = default_domain,
                domainOwner = default_domain_owner,
                repository = default_repository,
                format = 'maven',
                namespace = package['namespace'],
                package = package['package'],
                packageVersion = version['version'],
                asset = asset['name'],
                packageVersionRevision = version['revision']
            )
            
            extension = file['assetName'].split('.')[-1]
            
            if extension == 'jar':
            
                artifact = file['asset'].read()
                with open('./'+artifact_folder+'/'+file['assetName'], "wb") as f:
                    f.write(artifact)
                command = f'mvn deploy:deploy-file -Dpackaging="{extension}" -DrepositoryId="{destination_domain +"-"+ destination_repository}"\
                -Durl="https://{destination_domain}-{destination_domain_owner}.d.codeartifact.{destination_region}.amazonaws.com/maven/{destination_repository}/"\
            -DgroupId="{package["namespace"]}" -DartifactId="{package["package"]}" -Dversion="{version["version"]}" -Dfile="{file["assetName"]}"'
                deploy_command.append(re.sub(' +', ' ', command))

# Create the txt file with the deploy commands.
with open('deploy_'+destination_region+'.txt', 'w') as f:
    f.write('\n'.join(deploy_command))

