docker build -t epoch-service:latest .
docker tag epoch-service:latest suppi147/epoch-service:latest
docker push suppi147/epoch-service:latest

kubectl delete -f /root/shared/Demonstration/Example-Services/EpochService/k8s-env-creator/controller-node/epoch-service.yaml
kubectl apply -f /root/shared/Demonstration/Example-Services/EpochService/k8s-env-creator/controller-node/epoch-service.yaml
