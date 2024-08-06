FROM debian:latest

# Include dist 
COPY dist/ /root/dist/

# Install dependencies
RUN apt-get update && \
    apt-get install -y \
    git \
    build-essential \
    libsqlite3-dev \
    wget

# Set the Current Working Directory inside the container
WORKDIR /galah

# Clone the galah repository from GitHub
RUN git clone https://github.com/0x4D31/galah.git .

# Copy the service account key file into the container
COPY dist/honeypot.json /galah/honeypot.json

#Copy custom config file 
COPY dist/config/ /galah/config/

#Copy custom default.json
COPY dist/default.json /galah/templates

# Copy the TLS certificate and key files into the container
COPY dist/cert/key.pem /galah/cert/key.pem
COPY dist/cert/cert.pem /galah/cert/cert.pem

# Create the logs directory
RUN mkdir /galah/logs

# Install the required Go version
RUN wget https://golang.org/dl/go1.22.0.linux-amd64.tar.gz && \
    tar -C /usr/local -xzf go1.22.0.linux-amd64.tar.gz && \
    rm go1.22.0.linux-amd64.tar.gz && \
    ln -s /usr/local/go/bin/go /usr/bin/go

# Use a shell script for multiple commands
RUN CGO_ENABLED=1 go mod download && \
    CGO_ENABLED=1 go build -o galah ./cmd/galah

# Run the executable
ENTRYPOINT ["./galah"]
