# bugs

| bugs | solutions |
| --- | --- |
| The connection to the server 10.0.2.7:6443 was refused - did you specify the right host or port?
→ swap is not off
→ have not create network yet | swapoff -a
https://stackoverflow.com/questions/56737867/the-connection-to-the-server-x-x-x-6443-was-refused-did-you-specify-the-right
kubeadm init --pod-network-cidr 10.10.0.0/16 --kubernetes-version 1.26.1 --node-name k8s-controller |
| kubectl get nodes
E1016 06:16:47.767861 1105 memcache.go:238] couldn't get current server API group list: Get "http://localhost:8080/api?timeout=32s": dial tcp 127.0.0.1:8080: connect: connection refused
→ authentication problems | 
sudo mkdir -p $HOME/.kube
sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
sudo chown $(id -u):$(id -g) $HOME/.kube/config
https://stackoverflow.com/questions/76841889/kubectl-error-memcache-go265-couldn-t-get-current-server-api-group-list-get |
| Unable to connect to the server: x509: certificate signed by unknown authority (possibly because of "crypto/rsa: verification error" while trying to verify candidate authority certificate "kubernetes")
→ certificate exist from previous config | sudo kubeadm reset 
sudo rm -r $HOME/.kube
kubeadm init --pod-network-cidr 10.10.0.0/16 --kubernetes-version 1.26.1 --node-name k8s-controller
sudo mkdir -p $HOME/.kube
sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
sudo chown $(id -u):$(id -g) $HOME/.kube/config
https://stackoverflow.com/questions/36939381/x509-certificate-signed-by-unknown-authority-kubernetes |
| [ERROR CRI]: container runtime is not running: output: E1016 07:30:32.776096 23753 remote_runtime.go:616] "Status from runtime service failed" err="rpc error: code = Unavailable desc = connection error: desc = \"transport: Error while dialing dial unix /var/run/cri-dockerd.sock: connect: no such file or directory\"”
→ missing cri-dockerd adapter (an open source adapter that provides fully CRI-conformant compatibility between Docker Engine and the Kubernetes system) | https://github.com/Mirantis/cri-dockerd
- the second option
https://github.com/Mirantis/cri-dockerd
kubeadm join 10.0.2.7:6443 --token gfn320.s3i6ermjxotghyt5 --discovery-token-ca-cert-hash sha256:8a7442f13a775b179d0e1cd8f6ab713655e1cb81b69b3ff4f041ef7f22b358b3 --cri-socket=unix:///var/run/cri-dockerd.sock |