FROM mcr.microsoft.com/playwright/python:v1.51.0-noble

# Set the working directory inside the container
WORKDIR /app

# Copy the necessary directories and files into the container
COPY locators /app/locators/
COPY pages /app/pages/
COPY reports /app/reports/
COPY tests /app/tests/
COPY utilities /app/utilities/

COPY config.json /app/
COPY pytest.ini /app/
COPY requirements.txt /app/

# Install Python dependencies from requirements.txt
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Install Bash Command Line Tools
RUN apt-get update
RUN apt-get -qy --no-install-recommends install \
    curl \
    sudo \
    unzip \
    vim \
    wget \
    xvfb

# Install Chrome
RUN apt-get update
RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
RUN apt-get install -y ./google-chrome-stable_current_amd64.deb
RUN rm ./google-chrome-stable_current_amd64.deb

# Install Playwright dependencies and Chromium
RUN playwright install --with-deps

# Install additional browser (if needed)
RUN playwright install chromium

## Install Java (required for Allure)
#RUN apt-get update && apt-get install -y openjdk-11-jdk
#
## Set JAVA_HOME environment variable
#ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
#ENV PATH=$JAVA_HOME/bin:$PATH

# Install Java (required for Allure)
RUN apt-get update && apt-get install -y \
    openjdk-11-jre-headless \
    wget && \
    wget https://repo.maven.apache.org/maven2/io/qameta/allure/allure-commandline/2.33.0/allure-commandline-2.33.0.tgz && \
    tar -zxvf allure-commandline-2.33.0.tgz && \
    mv allure-2.33.0 /opt/allure && \
    ln -s /opt/allure/bin/allure /usr/local/bin/allure



RUN chmod +x /app/tests/scripts/run_test_suite.sh

WORKDIR /app/tests/scripts

CMD ["/bin/bash"]