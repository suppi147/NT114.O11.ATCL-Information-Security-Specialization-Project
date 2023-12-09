docker build -t session-management:latest .
docker tag session-management:latest suppi147/session-management:latest
docker push suppi147/session-management:latest

kubectl delete -f /root/shared/Demonstration/session-management-module/dev-environment/k8s-env-creator/master-node/session-management-service.yaml
kubectl apply -f /root/shared/Demonstration/session-management-module/dev-environment/k8s-env-creator/master-node/session-management-service.yaml
