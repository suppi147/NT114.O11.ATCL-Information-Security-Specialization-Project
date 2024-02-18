docker build -t authen-service:latest .
docker tag authen-service:latest suppi147/authen-service:latest
docker push suppi147/authen-service:latest

kubectl delete -f /root/shared/Demonstration/authentication-module/k8s-env-creator/controller-node/authen-service.yaml
kubectl apply -f /root/shared/Demonstration/authentication-module/k8s-env-creator/controller-node/authen-service.yaml
