FROM python:3.10

WORKDIR /app

COPY . .

RUN apt-get update && apt-get install -y locales && \
echo "pt_BR.UTF-8 UTF-8" >> /etc/locale.gen && \
locale-gen pt_BR.UTF-8 && \
update-locale LANG=pt_BR.UTF-8

RUN apt-get install -y build-essential curl software-properties-common git 
RUN rm -rf /var/lib/apt/lists/*

ENV LANG=pt_BR.UTF-8
ENV LANGUAGE=pt_BR:pt
ENV LC_ALL=pt_BR.UTF-8

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

CMD [ "streamlit", "run", "home.py" ]