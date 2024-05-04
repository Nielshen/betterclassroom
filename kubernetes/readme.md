####Local development:

- start wsl 2
- Install and run Docker
![Alt-Text](docs/dockerhub.png)
- Install K3D
```brew install k3d```
or
```curl -s https://raw.githubusercontent.com/k3d-io/k3d/main/install.sh | bash```
- Run K3D
```k3d cluster create mycluster -p "8088:80@loadbalancer"```

    
```kubectl config current-context```
![Alt-Text](docs/context.png)

- Install flux cli
```brew install fluxcd/tap/flux```
- Create namespace
```kubectl create namespace flux-system```
![Alt-Text](docs/flux.png)

- Create secret

``` sh
kubectl create secret generic gitlab-token \
  --from-literal=username=<Gitlab Username> \
  --from-literal=password=<Gitlab Token> \
  -n flux-system
```
  
- Connect flux to the Git Repo

TODO TEST THIS
```flux install```

```flux install --components=image-reflector-controller,image-automation-controller```
```
flux create source git gitlab-repo \
  --url=https://gitlab.in.htwg-konstanz.de/lehre/meiglspe/sose24/betterclassroom.git \
  --branch=main \
  --interval=1m
flux create kustomization betterclassroom \
  --source=GitRepository/gitlab-repo \
  --path="./kubernetes" \
  --prune=true \
  --interval=1m
```

- Add registry secrets

```sh 
kubectl create secret docker-registry my-registry-secret \
  --docker-server=registry.gitlab.in.htwg-konstanz.de \
  --docker-username=<Gitlab Username> \
  --docker-password=<Gitlab Token> \
  --docker-email=<Gitlab Mail> \
 --namespace=betterclassroom
```
```sh 
kubectl create secret docker-registry my-registry-secret \
  --docker-server=registry.gitlab.in.htwg-konstanz.de \
  --docker-username=<Gitlab Username> \
  --docker-password=<Gitlab Token> \
  --docker-email=<Gitlab Mail> \
 --namespace=flux-system
```

- Edit Hosts

Open the editor with administrative privileges and navigate to  C:\Windows\System32\drivers\etc\hosts and add the Line: 
```127.0.0.1 better-classroom.com```

- Better Classrooms should be accessible under

Frontend: http://better-classroom.com:8088/


![Alt-Text](docs/frontend.png)

Backend: http://better-classroom.com:8088/api/students


![Alt-Text](docs/backend.png)

###Manually Delete and apply new versions
go to 
betterclassroom/kubernetes

```kubectl delete -f backendDeployment.yaml```

```kubectl apply -f backendDeployment.yaml```


###Access Database
port forward

```kubectl port-forward svc/mongodb -n betterclassroom 27017:27017```

``mongo --host 127.0.0.1 --port 27017``