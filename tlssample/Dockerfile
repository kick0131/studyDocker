# centos + Japanese language and timezone
FROM centos:8
RUN rpm --import /etc/pki/rpm-gpg/RPM-GPG-KEY-centosofficial && \
    dnf -y install glibc-locale-source && \
    dnf clean all && \
    localedef -f UTF-8 -i ja_JP ja_JP.UTF-8 && \
    ln -sf /usr/share/zoneinfo/Asia/Tokyo /etc/localtime
ENV LANG="ja_JP UTF-8" \
    LANGUAGE="ja_JP:ja" \
    LC_ALL="ja_JP.UTF-8" \
    TZ="Asia/Tokyo"

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
