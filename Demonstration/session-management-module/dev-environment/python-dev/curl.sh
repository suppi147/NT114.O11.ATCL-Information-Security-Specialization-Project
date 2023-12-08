kubectl exec -it curl-service-c7b8bc7db-ccgfh -n dev -- curl -X POST -d "userID=1" http://session-management-service/test
