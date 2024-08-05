# ���������� ������� ����� Ubuntu 20.04
FROM ubuntu:20.04

# ������������� ����������� ������
RUN apt-get update && apt-get install -y \
    openssh-server \
    sudo \
    vim \
    iptables \
    && rm -rf /var/lib/apt/lists/*

# ������� ������� ��� SSH-�������
RUN mkdir /var/run/sshd

# ��������� ������������ ��� �����������
RUN useradd -rm -d /home/ansible -s /bin/bash -g root -G sudo -u 1000 ansible
RUN echo 'ansible:<�� �������� ������� ������>' | chpasswd

# ��������� ���� �� ������
RUN sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config
RUN sed -i 's/#PasswordAuthentication yes/PasswordAuthentication yes/' /etc/ssh/sshd_config

# ��������� �����
EXPOSE 22
EXPOSE 443

# ����������� ������ ��� ��������� iptables
COPY script.sh /usr/local/bin/script.sh

# ������� ������ �����������
RUN chmod +x /usr/local/bin/script.sh

# � ��������� SSH-�������
CMD ["/usr/sbin/sshd", "-D"]

#������ ������!