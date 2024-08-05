Softether VPN server as a microservice.


This tutorial presents Softether VPN server as a microservice based on docker container and ansible playbook.

The following steps are required for installation and configuration:
1. Clone the repository
git clone https://github.com/BrezhnevAlexandr/VPN-server-softether.git

2. Build the container
Before building, you need to set a password for the ansible user in the docker file.
build the image:
docker build -t task_test:0.0.1 .
3. Run the container
docker run --privileged -d -p 2222:22 -p 443:443 --name test_task task_test:0.0.1
If we re-create the containerp on the machine, we need to delete the old entry:
ssh-keygen -f "/home/student/.ssh/known_hosts" -R "[localhost]:2222"
4. Go to the container, check availability
# check ssh availability
ssh ansible@localhost -p 2222
5. Replace the default passwords in the secrets file
ansible-vault encrypt secrets.yml
6. Set the connection parameters in the inventory file. In particular, replace with the new password ansible
7. Encrypt secrets.yml
ansible-vault encrypt secrets.yml
8. launch playbook
cd vpn_setup/
ansible-playbook -i inventory.ini site.yml --ask-vault-pass
9. For additional configuration, you can use the server console:
# vpn console
/opt/vpnserver/vpncmd 



#############################################################################################################



Softether VPN серевер как микросервис.


В данном мануале представлен Softether VPN серевер как микросервис на основе docker-контейнера и плейбука ansible.

Для устнаовки и настройки требуется выполнить следующие шаги:
1. Клонирование репозитория
git clone https://github.com/BrezhnevAlexandr/VPN-server-softether.git

2. Сборка контейнера
Перед сборкой необходимо задать пароль пользователю ansible в docker-файле.
собрать образ:
docker build -t task_test:0.0.1 .
3. Запуск контейнера
docker run --privileged -d -p 2222:22 -p 443:443 --name test_task task_test:0.0.1
Если повторно создаем контейнеп на машине, то необходимо удалить старую запись:
ssh-keygen -f "/home/student/.ssh/known_hosts" -R "[localhost]:2222"
4. Зайти в контейнер, проверить доступность
# проверка доступности по ssh
ssh ansible@localhost -p 2222
5. Заменить пароли по умолчанию в файле secrets
ansible-vault encrypt secrets.yml
6. Задать в файле inventory параметры подключения. В частности заменить на новый пароль ansible
7. Зашифровать secrets.yml
ansible-vault encrypt secrets.yml
8. апуск playbook
cd vpn_setup/
ansible-playbook -i inventory.ini site.yml --ask-vault-pass
9. Для дополнительной настройки можно воспользоваться консолью сервера:
#  консоль vpn
/opt/vpnserver/vpncmd 