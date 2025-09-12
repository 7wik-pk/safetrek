sudo apt update
sudo apt install -y ca-certificates curl software-properties-common

sudo iptables -A INPUT -p tcp --dport 80 -j ACCEPT
sudo iptables -A INPUT -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT

# Add Docker's official GPG key
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

# Add Docker repo
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu jammy stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io

# Start Docker and enable on boot
sudo systemctl start docker
sudo systemctl enable docker

# Add your user to docker group so you can run docker without sudo
sudo usermod -aG docker $USER
newgrp docker

chmod 777 ./cloud_deploy.sh

rm docker-compose.yml
mv docker-compose-cloud.yml docker-compose.yml