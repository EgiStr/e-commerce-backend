## Getting Started

First, clone project:

```bash
git clone https://github.com/EgiStr/e-commerce-backend.git

```

second, Create environment python:

```bash
py -m venv Env
# or
# with other environment 
```

Third, activate environment & install requirements:


```bash
# in cmd 
Env\Scripts\activate #in powershell Activate.ps1
pip install -r  requirements.txt

```

create projects in firebase for activate push notification :
download admin sdk in dashboard with format .json
place sdk in `root/utils/firebase`
and rename with firebaseSdk.json

migrate database :
```bash
python manage.py migrate
```

last,run the development server:

```bash
python manage.py runserver
``` 

Open [http://localhost:8000](http://localhost:8000) with your browser to see the result.

you can see endpoint with [http://localhost:8000/api/](http://localhost:8000/api/) to see endpoint endpoint 