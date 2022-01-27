FROM opensearchproject/opensearch:1.2.1

ENV GMAIL_USER <secret data>
ENV GMAIL_PASS <secret data>

# keystore
RUN /usr/share/opensearch/bin/opensearch-keystore create
RUN echo $GMAIL_USER | /usr/share/opensearch/bin/opensearch-keystore add --stdin plugins.alerting.destination.email.my_sender.username
RUN echo $GMAIL_PASS | /usr/share/opensearch/bin/opensearch-keystore add --stdin plugins.alerting.destination.email.my_sender.password

# plugin
RUN /usr/share/opensearch/bin/opensearch-plugin install analysis-kuromoji
