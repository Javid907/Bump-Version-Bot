FROM python:3.8-slim

ENV APP_HOME /app
ENV LANG=en_US.UTF-8 LANGUAGE=en_US:en LC_ALL=en_US.UTF-8 PATH="/root/.local/bin:${PATH}"
EXPOSE 5000

RUN apt-get update \
	&& apt-get install -y --no-install-recommends locales curl sudo git jq procps ssh-client\
	&& sed -i -e 's/# en_US.UTF-8 UTF-8/en_US.UTF-8 UTF-8/' /etc/locale.gen \
	&& locale-gen

RUN mkdir $APP_HOME
COPY . $APP_HOME
WORKDIR $APP_HOME

RUN pip3 install -r ./requirements.txt
RUN pip3 install --user -U ./

CMD ["python3.8","-u","./bin/app.py"]
