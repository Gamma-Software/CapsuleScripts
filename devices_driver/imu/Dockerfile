FROM python:3

WORKDIR /usr/src/app

COPY . .
RUN pip install vn100lib/
RUN pip install --no-cache-dir -r requirements.txt
RUN python install_on_docker.py

CMD [ "python", "./imu_measure.py" ]
EXPOSE 1884/tcp
