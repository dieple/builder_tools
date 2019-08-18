## Introduction

A python script to create, build and run the docker image. Once the docker image is up and running you'll get a bash shell as a local development environment on your host PC.
Within this repo you can perform Infrastructure as Code (IaC) using 
* [terrascript](https://github.com/mjuenema/python-terrascript)
* Ansible
* Kubernetes
* Helm
* Terraform
* AWS CLI
* aws-vault

## Why would I wanna use this?

* Quick, easy and repeatable method to setup your local development environment.
* Isolated from your host PC. Don't have to worry about software version conflicts with your host environment. 
* Every developer using this tool will have the same version of software

## Software installed
* Python3
* python-terraform --> provides a wrapper of `terraform` command line tool
* python-terrascript --> generates terraform code using python.
* Terraform binary (defaults to v0.11.7 for enactor development but can be overidden)
* Ansible  (defaults to v2.5.0 but can be overidden)
* AWS CLI
* AWS Vault --> Profiles, MFA and roles switching capability
* Kubectl
* Helm

The packages are build using pip install if possible, further addons can be included during docker image build stage.

## Prerequisites

* Install docker on the host machine
* Python3 on host machine
* Create developer AWS IAM account, setup MFA on AWS console and noted down the MFA ARN.
* Create "$HOME/.aws/config" file on host machine with these entries below (edit to match your environment)
* Create "$HOME/.kube" directory for K8s.


```
[default]
region=eu-west-1

[profile dev]
mfa_serial=arn:aws:iam::<mfa-aws-account-id>:mfa/aws_iam_account
role_arn=arn:aws:iam::<switch-role-aws-account-id>:role/developers

[profile staging]
mfa_serial=arn:aws:iam::<mfa-aws-account-id>:mfa/aws_iam_account
role_arn=arn:aws:iam::<switch-role-aws-account-id>:role/developers
```


## Usage

```bash
$ git clone_this_repos_into_a_directory...
$ cd directory   
$ python3 setup.py -h

usage: setup.py [-h] --githubUsername GITHUBUSERNAME --githubEmail GITHUBEMAIL
              --profile PROFILE [--imageName IMAGENAME]
              [--terraformVersion TERRAFORMVERSION]
              [--ansibleVersion ANSIBLEVERSION]
              [--dockerAppUser DOCKERAPPUSER]
              [--installAnsible [INSTALLANSIBLE]]
              [--installTerraform [INSTALLTERRAFORM]]

Required arguments:
  --githubUsername GITHUBUSERNAME
                        Github username
  --githubEmail GITHUBEMAIL
                        Github email
  --profile PROFILE     Profile to use with aws-vault

optional arguments:
  -h, --help            show this help message and exit
  --imageName IMAGENAME
                        Docker image name
  --terraformVersion TERRAFORMVERSION
                        Terraform version
  --ansibleVersion ANSIBLEVERSION
                        Ansible version
  --dockerAppUser DOCKERAPPUSER
                        Docker OS App user
  --installAnsible [INSTALLANSIBLE]
                        Install ansible?
  --installTerraform [INSTALLTERRAFORM]
                        Install Terraform?

$ python3 setup.py  --githubUsername=yourGithubUsername --githubEmail=yourGithubEmail --dockerAppUser=devops --profile=enactor-dev
    
    
... snip
Successfully built 4f84992ea3d1
Successfully tagged cloudops:latest
2019-02-20 16:58:52,107 - root - INFO - run_command: docker run --interactive --tty -u devops --rm --volume "$HOME/.aws:/home/devops/.aws" --volume "$HOME/repos:/repos" cloudops /bin/bash

Enter Access Key ID: YourAccessKeyId
Enter Secret Access Key: YourAcccessKeySecrets
Enter passphrase to unlock /home/devops/.awsvault/keys/:
Added credentials to profile "dev" in vault
Enter passphrase to unlock /home/devops/.awsvault/keys/:
Enter token for arn:aws:iam:::<aws-account-number-mfa>/<github-user-id>: 995559
Enter passphrase to unlock /home/devops/.awsvault/keys/:
devops@67fb998d20da:/repos$

Voila you now have a development environment (built within a few minutes) on your host PC!

Note that $HOME/repos is where I checked out the git repos and can be seen in /repos in the docker image, where you can run terraform plan, etc. 
```    


## Tidy up...
```bash
$ docker images

REPOSITORY          TAG                 IMAGE ID            CREATED             SIZE
cloudops            latest              397f27ce6b84        17 seconds ago      787MB
<none>              <none>              11035dde5ea5        18 hours ago        787MB
ubuntu              16.04               7e87e2b3bf7a        5 weeks ago         117MB

$ docker rmi 397f27ce6b84
Untagged: cloudops:latest
Deleted: sha256:397f27ce6b84e3950f4c88a70993d0e511cd6716baa704e669d56c0e7a0de4fb
Deleted: sha256:abddd2e59479a25ae85aa11fe86774872df23a482bf3600e19a711117dedde60
Deleted: sha256:698fc7e394eda565582d71fe908fee4c7b2429df9cd4bac2fd574ac545b6cce2
```


## WARNING

DO NOT push or save the developer image back to docker registry as it's got the developer sensitive keys.

# Terraform Development using Terrascript

#### To create the initial bucket to hold terraform statefile 
Make sure this line is enable in build.py: "generate_s3(inargs, True, False)"
```bash
$ cd terrascript/vars
Modify <module>.yaml to meet your environment

$ # cd to terrascript folder
$ python build.py
usage: build.py [-h] -a ACCOUNT -e ENVIRONMENT -c CICD -p PROFILE
                  [-v VARFILES] [-t TFAPPLY] [-d TFDESTROY]
build.py: error: the following arguments are required: -a/--account, -e/--environment, -c/--cicd, -p/--profile
$ # python3 build.py -a <aws-account-name> -c <cicd_mode_true_false> -e <environment> -p <aws-vault-profile-name> -t <terraform_apply_true_false> 
$ python build.py -a dataops_staging -c false -e staging - p dataops-staging -t true

```


#### To create a new VPC
```bash
$ # Make sure this line is in build.py: generate_vpc(inargs)
$ python build.py -a dataops_staging -c false -e staging - p dataops-staging -t true

```