# SRIP-Portal
A django-based web application developed for the Student Remote Internship Program

## Prerequisites & Requirements
* Python 3.6 or higher
* MongoDB 3.6 or higher
* Other pip packages are listed in 'requirements.txt'

## Usage
We use gunicorn to deploy the application on an apache server.
The script 'prod_gunicorn.bash' holds the commands for deployment. For a quick reset or refresh of the server, 'reset.sh' has been written.
Note: When deploying on a new container, make sure that daemon mongod is running before deployment

```
sudo systemctl start mongod.service
cd srip-portal
./reset.sh
```


