# Simple ETCD cluster

[![Etcd cluster CI](https://github.com/garutilorenzo/docker-etcd-cluster/actions/workflows/ci.yml/badge.svg)](https://github.com/garutilorenzo/docker-etcd-cluster/actions/workflows/ci.yml)
[![GitHub issues](https://img.shields.io/github/issues/garutilorenzo/docker-etcd-cluster)](https://github.com/garutilorenzo/docker-etcd-cluster/issues)
![GitHub](https://img.shields.io/github/license/garutilorenzo/docker-etcd-cluster)
[![GitHub forks](https://img.shields.io/github/forks/garutilorenzo/docker-etcd-cluster)](https://github.com/garutilorenzo/docker-etcd-cluster/network)
[![GitHub stars](https://img.shields.io/github/stars/garutilorenzo/docker-etcd-cluster)](https://github.com/garutilorenzo/docker-etcd-cluster/stargazers)

![etcd](https://garutilorenzo.github.io/images/etcd.png)

### Requirements

* docker
* docker-compose
* docker swarm cluster (optional)

Additional requirements for testing purposes:

* python3
* pipenv
* pip3

#### Deploy etcd cluster with docker compose

```
docker-compose up -d
```

check the status of the environment:

```
docker-compose ps


     Name                   Command               State                        Ports                      
----------------------------------------------------------------------------------------------------------
etcd_etcd-00_1   etcd --name=etcd-00 --data ...   Up      2379/tcp, 2380/tcp                              
etcd_etcd-01_1   etcd --name=etcd-01 --data ...   Up      2379/tcp, 2380/tcp                              
etcd_etcd-02_1   etcd --name=etcd-02 --data ...   Up      2379/tcp, 2380/tcp                              
etcd_nginx_1     /docker-entrypoint.sh ngin ...   Up      0.0.0.0:2379->2379/tcp,:::2379->2379/tcp, 80/tcp
```

#### Test the environment

```
pipenv shell
pip install -r requirements.txt
python test/etcd-test.py 
hey key1
hey key2
```

Check the log of the nginx service to see the traffic redirected to the etcd hosts:

```
docker-compose logs -f nginx

Attaching to etcd_nginx_1
nginx_1    | /docker-entrypoint.sh: /docker-entrypoint.d/ is not empty, will attempt to perform configuration
nginx_1    | /docker-entrypoint.sh: Looking for shell scripts in /docker-entrypoint.d/
nginx_1    | /docker-entrypoint.sh: Launching /docker-entrypoint.d/10-listen-on-ipv6-by-default.sh
nginx_1    | 10-listen-on-ipv6-by-default.sh: info: Getting the checksum of /etc/nginx/conf.d/default.conf
nginx_1    | 10-listen-on-ipv6-by-default.sh: info: Enabled listen on IPv6 in /etc/nginx/conf.d/default.conf
nginx_1    | /docker-entrypoint.sh: Launching /docker-entrypoint.d/20-envsubst-on-templates.sh
nginx_1    | /docker-entrypoint.sh: Launching /docker-entrypoint.d/30-tune-worker-processes.sh
nginx_1    | /docker-entrypoint.sh: Configuration complete; ready for start up
nginx_1    | 2021-10-08T09:41:23+00:00 172.28.0.1 TCP 200 422 665 0.052 172.28.0.3:2379 "665" "422" "0.000"
nginx_1    | 2021-10-08T09:41:24+00:00 172.28.0.1 TCP 200 422 665 0.046 172.28.0.2:2379 "665" "422" "0.000"
nginx_1    | 2021-10-08T09:50:56+00:00 172.28.0.1 TCP 200 422 665 0.029 172.28.0.4:2379 "665" "422" "0.000"
```

#### Docker swarm stack

To deploy the etcd cluster on a docker swarm cluster:

```
docker stack deploy -c etcd-stack.yml etcd
```

Check the status of the deployment:

```
docker stack ps etcd

mx6fvfwye547   etcd_etcd-00.1       quay.io/coreos/etcd:v3.5.0   node-2    Running         Running 3 hours ago                                        
wybd7n4oitae   etcd_etcd-01.1       quay.io/coreos/etcd:v3.5.0   node-4    Running         Running 3 hours ago                                        
rmlycc3uvc8t   etcd_etcd-02.1       quay.io/coreos/etcd:v3.5.0   node-2    Running         Running 3 hours ago                                        
rexh1smoalpo   etcd_nginx.1         nginx:alpine                 node-2    Running         Running 21 hours ago    

docker service ls
ID             NAME                  MODE         REPLICAS   IMAGE                          PORTS
1u709kzgmo2b   etcd_etcd-00          replicated   1/1        quay.io/coreos/etcd:v3.5.0     
m7ze76xi58ww   etcd_etcd-01          replicated   1/1        quay.io/coreos/etcd:v3.5.0     
1535r562g3az   etcd_etcd-02          replicated   1/1        quay.io/coreos/etcd:v3.5.0     
v8n8qlo3dm30   etcd_nginx            replicated   1/1        nginx:alpine                   *:2379->2379/tcp
```




