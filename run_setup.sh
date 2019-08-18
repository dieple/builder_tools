# Modify to meet your env and run below to have a development env on your box.

#	--shareHostVolume=$HOME/repos Directory on your host which contains your git repos

python ./setup.py --githubUsername=dieple \
	--githubEmail=dieple1@gmail.com \
	--terraformVersion=0.11.13 \
	--installTerraform=true \
	--dockerAppUser=dataops \
	--profile=dataops-dev \
	--shareHostVolume=$HOME/repos \
	--imageName=dataops


