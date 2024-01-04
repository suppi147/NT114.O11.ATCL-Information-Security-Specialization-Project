docker build -t quote-service:latest .
docker tag quote-service:latest suppi147/quote-service:latest
docker push suppi147/quote-service:latest

kubectl delete -f /root/shared/Demonstration/Example-Services/QuoteService/k8s-env-creator/controller-node/quote-service.yaml
kubectl apply -f /root/shared/Demonstration/Example-Services/QuoteService/k8s-env-creator/controller-node/quote-service.yaml
