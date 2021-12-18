FROM python:3.8

# - INSTALL GUNICORN
RUN python3 -m pip install pip --upgrade
RUN pip install gunicorn

# - COPY SRC FILES
COPY . /app

# - INSTALL PYTHON REQUIREMENTS
WORKDIR /app
RUN pip install --no-cache-dir -r doc/requirements.txt

WORKDIR /app/src
EXPOSE 721

# - START
CMD gunicorn -c /app/gunicorn.conf main:app -t 999999
