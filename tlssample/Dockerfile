FROM centos:latest

# workfile set
COPY . /code/
WORKDIR /code

# first setup
RUN echo "alias ll='ls -la'" >> ~/.bashrc
RUN yum -y install python39
RUN python3 -m venv venv

# application execute
RUN chmod 777 app.sh
CMD ["./app.sh"]
