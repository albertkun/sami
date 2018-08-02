
## install virtual env
sudo pip install virtualenv

##set up virtual env
virtualenv my_app

##activate virtual env
source my_app/bin/activate

## install stuff without activating venv
my_app/bin/pip install requests

## leave venv
deactivate
