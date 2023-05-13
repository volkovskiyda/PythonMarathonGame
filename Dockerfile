FROM python:3.9
WORKDIR /home
COPY assets/ assets/
ADD main.py .
ADD requirements.txt .
RUN pip install -r requirements.txt
RUN pyinstaller main.py --add-data 'assets:assets' --onefile --windowed
ENTRYPOINT dist/main
