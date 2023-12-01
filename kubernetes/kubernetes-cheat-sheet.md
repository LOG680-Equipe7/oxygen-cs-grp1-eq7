# Kubernetes First Deployment Commands

To deploy the necessary components for the first time in Kubernetes, run the following commands in order:

1. Deploy the PostgreSQL database:
```
kubectl apply -f kubernetes/postgres-deployment.yaml
kubectl apply -f kubernetes/postgres-secret.yaml
kubectl apply -f kubernetes/postgres-service.yaml
kubectl apply -f kubernetes/postgres-persistent-volume.yaml
kubectl apply -f kubernetes/postgres-volume-claim.yaml
```

2. Deploy the application:
```
kubectl apply -f kubernetes/app-config.yaml
kubectl apply -f kubernetes/app-deployment.yaml
kubectl apply -f kubernetes/app-service.yaml
```

3. Deploy the cronjob:
```
kubectl apply -f kubernetes/cluster-service.yaml
```