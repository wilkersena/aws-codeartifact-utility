# aws-codeartifact-utility
This utility will download all artifacts and its versions from your AWS CodeArtifact repository tha use Maven as package manager, store then in a folder and will create a txt file with the maven deploy commands to all artifacts in a destination repository, if you want to deploy it in a diferent repository.

## Requirements
* Python 3+
* AWS CLI v2
* Apache Maven
* Java

## AWS CodeArtifact with Maven
* https://docs.aws.amazon.com/pt_br/codeartifact/latest/ug/maven-mvn.html
  
## How to use

``` python
git clone https://github.com/wilkersena/aws-codeartifact-utility.git
```

## Create the artifact folder

Create a folder in the same aws-codeartifact-utility.py file level:

`yourdir/aws-codeartifact-utility/aws-codeartifact-utility.py`

`yourdir/aws-codeartifact-utility/myartifacts`

## Edit the aws-codeartifact-utility.py file

Fill with your AWS information

``` python
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
```

## Run the python file

``` 
python aws-codeartifact-utility.py
```

The artifacts will be stored in the artifact folder and the file with the deploy commands in the same level at the script.

## Next features
* Deploy the artifacts automatically

