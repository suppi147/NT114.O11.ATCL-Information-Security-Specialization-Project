docker build -t authorization:latest .
docker tag authorization:latest suppi147/authorization:latest
docker push suppi147/authorization:latest

kubectl delete -f /root/shared/Demonstration/authorization-module/dev-environment/k8s-env-creator/master-node/authorization-service.yaml
kubectl apply -f /root/shared/Demonstration/authorization-module/dev-environment/k8s-env-creator/master-node/authorization-service.yaml
