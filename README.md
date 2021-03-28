# nudisc

Network Utilities - Discovery Tool

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

5. To change IP range or Protocols you will need to modify the **nudisc.py**
file with **vim**.

```shell
root@57576b930eba:/app# vim nudisc.py
```

*Alternatively, you can install any other applications you wish in this
container.*

6. The targets output files are formatted for use as input files with other
nmap commands and scripts.
