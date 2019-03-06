# Crisis Management System 

## Pipfile 
We are using pipenv to create a virtual environment for our projects, to manage our python packages easily. 

To use pipenv, 

```bash
pip3 install pipenv
```
or 
```bash
pip install pipenv
```
 
## Clone the repository

```bash
git clone git@github.com:jwngo/CMS3003.git
```

Once it has been cloned, 
```bash 
cd CMS3003
```
Install all dependencies from Pipfile
```bash
pipenv install 
``` 
or 
```bash
pipenv sync
``` 
You will require a python of version >3.7

## Localhost

To run django on localhost, 

```bash
pipenv shell
cd cms
python manage.py runserver
``` 

After commiting, please make a **pull request** instead of 
```bash 
git push origin master
``` 
to prevent merge conflicts! 
