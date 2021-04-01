# nudisc

Network Utilities - Discovery Tool

[![nudisc workflow](https://github.com/pfeiffermj/nudisc/actions/workflows/nudisc_actions.yml/badge.svg?branch=main)](https://github.com/pfeiffermj/nudisc/actions/workflows/nudisc_actions.yml)

## Setup

1. Clone the repository.

```shell
git clone https://github.com/pfeiffermj/nudisc.git
```

2. Change directory to the cloned repository.

```shell
cd nudisc
```

3. Build the docker image for the nudisc container.

```shell
sudo docker image build --tag local:nudisc .
```

4. Run interactive session with the nudisc container.

```shell
sudo docker container run -it --name nudisc local:nudisc
```

5. Restart interactive session with the nudisc container. 

```shell
sudo docker container start nudisc -ai
```

6. Reattach to the running container.

```shell
sudo docker container attach nudisc
```

## Basic Usage

1. When you are in an interactive session with the container a similar prompt will appear:

```shell
root@57576b930eba:/app#
```

2. To execute the **nudisc** Python app run the following command:

```shell
root@57576b930eba:/app# ./nudisc.py
```

3. When the protocol scans are complete output will placed in the **targets**
folder.

```shell
root@57576b930eba:/app# ls targets/
icmp_targets.txt  tcp_targets.txt  udp_targets.txt
```

4. You can view the contents of each file using **cat**.

```shell
root@57576b930eba:/app# cat targets/tcp_targets.txt 
192.168.2.1
192.168.3.1
192.168.4.1
192.168.5.1
192.168.5.9
192.168.10.1
192.168.11.1
```

5. The targets output files are formatted for use as input files with other
nmap commands and scripts.

## scan.json

To modify what will be scanned modify the **scan.json** file either before or
after the container build.

The container includes vim but you are free to download any text editor you
wish to use.

```json
{
    "ipv4_range" : "192.168.0.0/20",
    "ip_protocols" : "1,6,17",
    "tcp_ports" : "22,23,25,53,80,443,445,1433,3306,3389,5800,5900,8080,8443",
    "udp_ports" : "53,67,68,69,123,161,162,514,636,2055"
}
```
