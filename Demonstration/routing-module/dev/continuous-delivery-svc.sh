docker build -t routing-service:latest .
docker tag routing-service:latest suppi147/routing-service:latest
docker push suppi147/routing-service:latest

kubectl delete -f /root/shared/Demonstration/routing-module/k8s-env-creator/controller-node/routing-service.yaml
kubectl apply -f /root/shared/Demonstration/routing-module/k8s-env-creator/controller-node/routing-service.yaml
