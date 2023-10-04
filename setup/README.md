## Requirement
- 2 Ubuntu server virtual machines version 22.04 LTS
## Virtualbox network structure
![image](https://github.com/suppi147/NT114.O11.ATCL-Information-Security-Specialization-Project/assets/97881547/01f8d54e-7703-4aac-9496-fb21895b0446)
## Controller node and worker node installation
- update and upgrade
  ```
  apt update
  apt -y upgrade
  ```
- add IPs to local domain name service /etc/host.
  ```
  printf "\n10.0.2.7 k8s-controller\n10.0.2.15 k8s-worker\n\n" >> /etc/hosts
  ```
- choose module for kernel containerd.
```
  printf "overlay\nbr_netfilter\n" >> /etc/modules-load.d/containerd.conf
```
- Load 2 modules
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
- apply configuration in `/etc/sysctl.d/`.
  ```
  sysctl --system
  ```
- install, extract and move containerd to bin.
  ```
  wget https://github.com/containerd/containerd/releases/download/v1.6.16/containerd-1.6.16-linux-amd64.tar.gz -P /tmp/
  tar Cxzvf /usr/local /tmp/containerd-1.6.16-linux-amd64.tar.gz
  wget https://raw.githubusercontent.com/containerd/containerd/main/containerd.service -P /etc/systemd/system/
  ```
- enable containerd.
  ```
  systemctl daemon-reload
  systemctl enable --now containerd
  ```
- install runc.
  ```
  wget https://github.com/opencontainers/runc/releases/download/v1.1.4/runc.amd64 -P /tmp/
  install -m 755 /tmp/runc.amd64 /usr/local/sbin/runc
  ```
- install cni-plugin for containerd.
  ```
  wget https://github.com/containernetworking/plugins/releases/download/v1.2.0/cni-plugins-linux-amd64-v1.2.0.tgz -P /tmp/
  mkdir -p /opt/cni/bin
  tar Cxzvf /opt/cni/bin /tmp/cni-plugins-linux-amd64-v1.2.0.tgz
  ```
- reboot.
  ```
  reboot
  ```
- turn off swap.
  ```
  swapoff -a
  ```
- install packages apt support packages.
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
    ```
- Init a kubernetes cluster.
  ```
  kubeadm init --pod-network-cidr 10.10.0.0/16 --kubernetes-version 1.26.1 --node-name k8s-controller
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
  ```
- Configure calico cidr network.
  ```
  nano custom-resources.yaml
  ```
  ![image](https://github.com/suppi147/NT114.O11.ATCL-Information-Security-Specialization-Project/assets/97881547/92b46b21-6332-4e74-bc1b-3c4ec43c2e48)
- Apply changes.
  ```
  kubectl apply -f custom-resources.yaml
  ```
- Create token to connect worker node.
  ```
  kubeadm token create --print-join-command
  ```
### Configuration on Worker node
- turn off swap
  ```
  swapoff -a
  ```
- add token from worker node
  ```
  kubeadm join 10.0.2.7:6443 --token b79ii9.grhfc84n91hya0ha --discovery-token-ca-cert-hash sha256:57435c7db6df95bbea34d9c2a3e7233f4441042384239787a9828375b8cdd00f
  ```
