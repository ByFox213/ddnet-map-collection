# k8s

secret.yaml
```
apiVersion: v1
kind: Secret
metadata:
  name: map-collection
type: Opaque
stringData:
  .env: |
    host = 127.0.0.1
    port = 5432
    user = ddstats
    passwd = password
    db = ddstats
```

deployment.yaml
```
apiVersion: batch/v1
kind: CronJob
metadata:
  name: map-collection
spec:
  schedule: "0 6 * * *"
  jobTemplate:
    spec:
      template:
        metadata:
          labels:
            app: ddstats
        spec:
          containers:
          - name: mapcollection
            image: image:latest
            imagePullPolicy: IfNotPresent
            volumeMounts:
            - name: config
              mountPath: /tw/.env
              subPath: .env
          imagePullSecrets:
          - name: venom-bf
          volumes:
          - name: config
            secret:
              secretName: map-collection
          restartPolicy: OnFailure
```
