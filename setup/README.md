### Requirement
- 2 Ubuntu server virtual machines version 22.04 LTS
### Virtualbox network structure
![image](https://github.com/suppi147/NT114.O11.ATCL-Information-Security-Specialization-Project/assets/97881547/01f8d54e-7703-4aac-9496-fb21895b0446)
### Controller node installation
- add IPs to local domain name service /etc/host.
- `printf "\n10.0.2.7 k8s-controller\n10.0.2.15 k8s-worker\n\n" >> /etc/hosts`
- choose module for kernel containerd.
- `printf "overlay\nbr_netfilter\n" >> /etc/modules-load.d/containerd.conf`
- Load 2 modules
- 1. `modprobe overlay`: This command loads the "overlay" kernel module into the Linux kernel. The "overlay" filesystem is commonly used in containerization technologies like Docker and containerd to provide a **layered file system for containers.**
- 2. `modprobe br_netfilter`: This command loads the "br_netfilter" kernel module, which is related to **bridged networking** and is often used in **container setups** to enable n**etwork filtering and firewall rules for containers.**
- `modprobe overlay
   modprobe br_netfilter`
