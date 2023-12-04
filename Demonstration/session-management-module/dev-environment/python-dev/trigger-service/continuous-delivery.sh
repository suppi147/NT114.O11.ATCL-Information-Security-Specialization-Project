docker build -t session-trigger:latest .
docker tag session-trigger:latest suppi147/session-trigger:latest
docker push suppi147/session-trigger:latest

kubectl delete -f trigger-service.yaml
kubectl apply -f trigger-service.yaml
