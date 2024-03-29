#################################################################
# CloudOps IaC Local Development Environment
#
# Please do not modify the Dockerfile manually as it generate
# by builder.py. All modifications should be done in
# templates/Dockerfile.template
#################################################################
FROM ubuntu:18.04

# Set this environment variable to true to set timezone on container start.
ENV SET_CONTAINER_TIMEZONE false
# Default container timezone as found under the directory /usr/share/zoneinfo/.
ENV CONTAINER_TIMEZONE Europe/London

# Setup TERM and PS1
ENV TERM=xterm-color

RUN set -ex && \
  apt-get update && \
  DEBIAN_FRONTEND=noninteractive apt-get install -y python3-pip \
                        python3-dev \
                        python-dbus \
                        ntp \
                        libglib2.0-dev \
                        libgtk2.0-dev \
                        pkg-config \
                        python-gobject \
                        libgirepository1.0-dev \
                        vim \
                        git \
                        curl \
                        gcc \
                        g++ \
                        libffi-dev \
                        libssl-dev \
                        zip \
                        unzip \
                        tar \
                        postgresql-client \
                        dnsutils \
                        sudo \
                        tree \
                        gettext \
                        apt-utils \
                        groff \
                        ca-certificates \
                        bash \
                        openssh-client \
                        openssh-server \
                        rsync \
                        grsync \
                        bash-completion && \
            apt-get autoremove -yqq --purge && \
            rm -rf /tmp/*.rpm && \
            apt-get clean && \
            rm -rf \
                /var/lib/apt/lists/* \
                /tmp/* \
                /var/tmp/* \
                /usr/share/man \
                /usr/share/doc \
                /usr/share/doc-base && \
            cd /usr/local/bin && \
            ln -s /usr/bin/python3 python && \
            pip3 install --upgrade pip

# install kubectl
RUN apt-get update && \
	DEBIAN_FRONTEND=noninteractive apt-get install -y apt-transport-https

RUN curl -s https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key add -
RUN echo "deb https://apt.kubernetes.io/ kubernetes-xenial main" | tee -a /etc/apt/sources.list.d/kubernetes.list

RUN curl -sL -o /usr/local/bin/aws-vault https://github.com/99designs/aws-vault/releases/download/v4.5.1/aws-vault-linux-amd64 && chmod +x /usr/local/bin/aws-vault

RUN curl -SsL https://github.com/kvz/json2hcl/releases/download/v0.0.6/json2hcl_v0.0.6_linux_amd64 | tee /usr/local/bin/json2hcl > /dev/null && chmod 755 /usr/local/bin/json2hcl

RUN  curl -sL -o /usr/local/bin/yaml2json https://github.com/wakeful/yaml2json/releases/download/0.3.1/yaml2json-linux-amd64 && chmod +x /usr/local/bin/yaml2json

RUN curl -sL -o /usr/local/bin/jq  https://github.com/stedolan/jq/releases/download/jq-1.6/jq-linux64 && chmod +x /usr/local/bin/jq

RUN curl --silent --location "https://github.com/weaveworks/eksctl/releases/download/latest_release/eksctl_$(uname -s)_amd64.tar.gz" | tar xz -C /tmp && mv /tmp/eksctl /usr/local/bin/ && chmod +x /usr/local/bin/eksctl

RUN curl -sL -o /usr/local/bin/aws-iam-authenticator https://amazon-eks.s3-us-west-2.amazonaws.com/1.12.7/2019-03-27/bin/linux/amd64/aws-iam-authenticator && chmod +x /usr/local/bin/aws-iam-authenticator

RUN wget -q https://storage.googleapis.com/kubernetes-helm/helm-v2.13.1-linux-amd64.tar.gz -O - | tar -xzO linux-amd64/helm > /usr/local/bin/helm  && chmod +x /usr/local/bin/helm

RUN wget -q https://github.com/derailed/k9s/releases/download/0.7.13/k9s_0.7.13_Linux_x86_64.tar.gz -O - | tar -xzO k9s > /usr/local/bin/k9s  && chmod +x /usr/local/bin/k9s

RUN curl -sL -o /usr/local/bin/kubectl https://storage.googleapis.com/kubernetes-release/release/v1.12.6/bin/linux/amd64/kubectl && chmod +x /usr/local/bin/kubectl



RUN rm -rf /root/.cache
RUN rm -rf /tmp/*

# Note that entry.sh is generated by setup.py script
#ADD entry.sh /scripts/
#ENTRYPOINT ["/scripts/entry.sh"]
