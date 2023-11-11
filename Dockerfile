FROM sathishsk/music

RUN apt-get -y update 
RUN apt-get install -y ffmpeg 

WORKDIR /app

copy requirements.txt req.txt
RUN pip install --upgrade pip
RUN pip3 install --no-cache-dir -r req.txt 

COPY . .

CMD ["python3", "bot.py"]
