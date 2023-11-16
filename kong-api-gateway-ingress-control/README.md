### General Idea
In this small demonstration, Kong API Gateway will be deployed as an ingress controller in a Kubernetes (k8s) infrastructure. The purpose of this demonstration is to provide a hands-on experience illustrating how ingress and load balancers in Kubernetes interact with services through the Kong API Gateway.
![image](https://github.com/suppi147/NT114.O11.ATCL-Information-Security-Specialization-Project/assets/97881547/0ab5e010-a2c3-44e4-8815-f7603e6518ff)

### Hands-on
- Create image for flask foo and bar service then upload to dockerhub. At this step we need source code of foo and bar service plus their's dockerfile. Then run the build.sh.
  ![image](https://github.com/suppi147/NT114.O11.ATCL-Information-Security-Specialization-Project/assets/97881547/df56967b-37cb-41cb-a3cf-dc257aa9b907)
- Build foo and bar service with bar-service.yaml, foo-service.yaml for connection and deployment for pod initialization.
  ![image](https://github.com/suppi147/NT114.O11.ATCL-Information-Security-Specialization-Project/assets/97881547/7c417a0b-b24e-4cdb-bd85-9a52c4d1dcee)
- Reconfigure kong-ingress-controller.yaml with `loadBalancerSourceRanges: "0.0.0.0/0"` in order to access from localhost.
  ![image](https://github.com/suppi147/NT114.O11.ATCL-Information-Security-Specialization-Project/assets/97881547/d7d8b63e-9cb7-4db1-acd2-565670ac447b)
- After that run the config file.
  ![image](https://github.com/suppi147/NT114.O11.ATCL-Information-Security-Specialization-Project/assets/97881547/facb9bd4-4479-48eb-96da-eeb418744473)
- Apply ingress route for foo and bar service with ingress.yaml.
  ![image](https://github.com/suppi147/NT114.O11.ATCL-Information-Security-Specialization-Project/assets/97881547/51023868-16ac-4989-a86b-6bb1a259007a)
- Check for load balancer internal port.
  ![image](https://github.com/suppi147/NT114.O11.ATCL-Information-Security-Specialization-Project/assets/97881547/c13737d6-65c3-4e4c-bf0e-5731bdf182ca)
- port forwarding
  ```
  kubectl port-forward -n noteziee service/kong-proxy 8080:80 &
  ```
- check foo and bar by http://localhost:31846
  ![image](https://github.com/suppi147/NT114.O11.ATCL-Information-Security-Specialization-Project/assets/97881547/a0245b6b-0935-4e0a-a55a-c8a1d7609018)
  
### References
![konghp ingress control](https://konghq.com/blog/engineering/kubernetes-ingress-api-gateway)
