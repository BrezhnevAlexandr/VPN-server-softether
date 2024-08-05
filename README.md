# Softether VPN server as a microservice.


This tutorial presents Softether VPN server as a microservice based on docker container and ansible playbook.

The following steps are required for installation and configuration:
## 1. Clone the repository
```bash
git clone https://github.com/BrezhnevAlexandr/VPN-server-softether.git
```
## 2. Build the container
Before building, you need to set a password for the ansible user in the docker file.
build the image:
```bash
docker build -t VPN_server .
```
## 4. Run the container
```bash
docker run --privileged -d -p 2222:22 -p 443:443 --name VPN_server VPN_server
```
If we re-create the containerp on the machine, we need to delete the old entry:
```bash
ssh-keygen -f "/home/<username>/.ssh/known_hosts" -R "[localhost]:2222"
```
## 5. Go to the container, check availability

check ssh availability:
```bash
ssh ansible@localhost -p 2222
```
## 6. Replace the default passwords in the secrets file
ansible-vault encrypt secrets.yml
## 7. Set the connection parameters in the inventory file. In particular, replace with the new password ansible
## 8. Encrypt secrets.yml
ansible-vault encrypt secrets.yml
## 9. launch playbook
```bash
cd vpn_setup/
ansible-playbook -i inventory.ini site.yml --ask-vault-pass
```
## 10. For additional configuration, you can use the server console:
vpn console:
```bash
/opt/vpnserver/vpncmd
``` 
