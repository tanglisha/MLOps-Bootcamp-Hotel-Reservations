FROM jenkins/jenkins:lts

# Default jenkins user is jenkins
# We need to be root to install docker (dind)
USER root

# prep apt registry to set up new keys
RUN apt-get update && \
    apt install -y \
    python3 \
    python3-pip \
    python3-venv \
    ca-certificates \
    curl \
    && \
    install -m 0755 -d /etc/apt/keyrings 


# add gcp to apt registry
RUN curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | gpg --dearmor -o /usr/share/keyrings/cloud.google.gpg \
    && \
    echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] https://packages.cloud.google.com/apt cloud-sdk main" | tee -a /etc/apt/sources.list.d/google-cloud-sdk.list 

# add docker to apt registry
RUN curl -fsSL https://download.docker.com/linux/debian/gpg -o /etc/apt/keyrings/docker.asc \
    && \ 
    chmod a+r /etc/apt/keyrings/docker.asc \
    && \
    echo \
    "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/debian \
    $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
    tee /etc/apt/sources.list.d/docker.list > /dev/null 


# Install docker & gcp 
RUN apt-get update \
    && \
    apt-get install -y \
    docker-ce \
    docker-ce-cli \
    containerd.io \
    docker-buildx-plugin \
    docker-compose-plugin \
    apt-transport-https \
    gnupg \
    google-cloud-cli 


# add the jenkins user to the docker group
RUN usermod -aG docker jenkins && \
    mkdir -p {/var/lib/docker,/var/jenkins_home}

# create a host volume
# the z option allows the volume to be shared
VOLUME /var/lib/docker:/var/jenkins_home:z

# Run as the jenkins user
USER jenkins