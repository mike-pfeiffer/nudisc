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
