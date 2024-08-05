# Используем базовый образ Ubuntu 20.04
FROM ubuntu:20.04

# Установливаем необходимые пакеты
RUN apt-get update && apt-get install -y \
    openssh-server \
    sudo \
    vim \
    iptables \
    && rm -rf /var/lib/apt/lists/*

# Создаем каталог для SSH-сервера
RUN mkdir /var/run/sshd

# Добавляем пользователя для подключения
RUN useradd -rm -d /home/ansible -s /bin/bash -g root -G sudo -u 1000 ansible
RUN echo 'ansible:<не забываем указать пароль>' | chpasswd

# Разрешаем вход по паролю
RUN sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config
RUN sed -i 's/#PasswordAuthentication yes/PasswordAuthentication yes/' /etc/ssh/sshd_config

# Открываем порты
EXPOSE 22
EXPOSE 443

# Накручиваем скрипт для настройки iptables
COPY script.sh /usr/local/bin/script.sh

# Сделаем скрипт исполняемым
RUN chmod +x /usr/local/bin/script.sh

# И запускаем SSH-сервера
CMD ["/usr/sbin/sshd", "-D"]

#Сборка готова!