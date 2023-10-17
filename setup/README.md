## Requirement
- 2 Ubuntu server virtual machines version 22.04 LTS
## Virtualbox network structure
![image](https://github.com/suppi147/NT114.O11.ATCL-Information-Security-Specialization-Project/assets/97881547/5a5ebac8-4382-4765-a6c1-004ef862f4d0)
## Controller node and worker node installation
- Update and upgrade.
  ```
  apt update
  apt -y upgrade
  ```
- Add IPs to local domain name service /etc/host.
  ```
  printf "\n10.0.2.7 k8s-controller\n10.0.2.15 k8s-worker\n\n" >> /etc/hosts
  ```
- Choose module for kernel containerd.
```
  printf "overlay\nbr_netfilter\n" >> /etc/modules-load.d/containerd.conf
```
- Load 2 modules.
  1. `modprobe overlay`: This command loads the "overlay" kernel module into the Linux kernel. The "overlay" filesystem is commonly used in containerization technologies like Docker and containerd to provide a **layered file system for containers.**
  2. `modprobe br_netfilter`: This command loads the "br_netfilter" kernel module, which is related to **bridged networking** and is often used in **container setups** to enable **network filtering and firewall rules for containers.**
  ```
  modprobe overlay
  modprobe br_netfilter
  ```
- These parameters determine whether packets crossing a bridge are sent to iptables for processing. Most Kubernetes CNIs(Kubernetes 1.28 supports Container Network Interface) rely on iptables, so this is usually necessary for Kubernetes.
  ``` 
  printf "net.bridge.bridge-nf-call-iptables = 1\nnet.ipv4.ip_forward = 1\nnet.bridge.bridge-nf-call-ip6tables = 1\n" >>     /etc/sysctl.d/99-kubernetes-cri.conf
  ```
- Apply configuration in `/etc/sysctl.d/`.
  ```
  sysctl --system
  ```
- install docker.io
  ```
  apt install docker.io
  ```
- install cri-dockerd
  ```
  git clone https://github.com/Mirantis/cri-dockerd.git
  cd cri-dockerd
  mkdir -p /usr/local/bin
  install -o root -g root -m 0755 cri-dockerd /usr/local/bin/cri-dockerd
  install packaging/systemd/* /etc/systemd/system
  sed -i -e 's,/usr/bin/cri-dockerd,/usr/local/bin/cri-dockerd,' /etc/systemd/system/cri-docker.service
  systemctl daemon-reload
  systemctl enable --now cri-docker.socket
  ```
- Reboot.
  ```
  reboot
  ```
- Turn off swap.
  ```
  swapoff -a
  ```
- Install packages apt support packages.
  ```
  apt-get update
  apt-get install -y apt-transport-https ca-certificates curl
  ```
- Install public key from apt for kubernetes packages.
  ```
  curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key --keyring /usr/share/keyrings/cloud.google.gpg add -
  ```
- Use public key to verify installing packages for kubernetes.
  ```
  echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] https://apt.kubernetes.io/ kubernetes-xenial main" | tee /etc/apt/sources.list.d/kubernetes.list
  ```
- Update again to apply changes.
  ```
  apt-get update
  ```
- Install kubernetes.
  ```
  apt-get install -y kubelet=1.26.1-00 kubeadm=1.26.1-00 kubectl=1.26.1-00
  ```
### Configuration on Controller node
- Reminder:
  - *always turn off swap after boot up.*
  - *delete cluster if needed.*
    ```
    kubeadm reset --force
    rm -r $HOME/.kube
    ```
- Init a kubernetes cluster.
  ```
  kubeadm init --pod-network-cidr 10.10.0.0/16 --kubernetes-version 1.26.1 --node-name k8s-controller --cri-socket=unix:///var/run/cri-dockerd.sock
  ```
- Basic setup to use.
  ```
  mkdir -p $HOME/.kube
  sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
  sudo chown $(id -u):$(id -g) $HOME/.kube/config
  ```
- Install calico.
  ```
  kubectl create -f https://raw.githubusercontent.com/projectcalico/calico/v3.25.0/manifests/tigera-operator.yaml
  kubectl apply -f custom-resources.yaml
  ```
- Configure calico cidr network.
  ```
  nano custom-resources.yaml
  ```
  ![image](https://github.com/suppi147/NT114.O11.ATCL-Information-Security-Specialization-Project/assets/97881547/92b46b21-6332-4e74-bc1b-3c4ec43c2e48)
- Setup crontab.
  ```
  root@k8s-controller:~# cat setup.sh
  sudo swapoff -a
  sudo mkdir -p $HOME/.kube
  sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
  sudo chown $(id -u):$(id -g) $HOME/.kube/config
  root@k8s-controller:~#sudo crontab -e
  #add
  @reboot . /home/su/setup.sh
  ```
- Apply changes.
  ```
  kubectl apply -f custom-resources.yaml
  ```
- Create token to connect worker node.
  ```
  kubeadm token create --print-join-command
  ```
### Configuration on Worker node
- Turn off swap.
  ```
  swapoff -a
  ```
- Setup crontab.
  ```
  su@k8s-worker:~$ sudo chmod +X setup.sh
  su@k8s-worker:~$ cat setup.sh
  sudo swapoff -a
  su@k8s-worker:~$ sudo crontab -e
  #add
  @reboot . /home/su/setup.sh
  ```
- Create token.
  ```
  kubeadm token create --print-join-command
  ```
- Add token from worker node.
  ```
  kubeadm join 10.0.2.7:6443 --token b79ii9.grhfc84n91hya0ha --discovery-token-ca-cert-hash sha256:57435c7db6df95bbea34d9c2a3e7233f4441042384239787a9828375b8cdd00f --cri-socket=unix:///var/run/cri-dockerd.sock
  ```
### Result
![image](https://github.com/suppi147/NT114.O11.ATCL-Information-Security-Specialization-Project/assets/97881547/4b5d336d-b532-4635-b1a0-8387f6dc3e63)
