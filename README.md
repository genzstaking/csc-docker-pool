# CSC Docker tools

CSC Docker is a simple CLI tool to manage relay and staking node in
CSC network. 
There are many common scenarios in CSC node management and this tool
makes them easy.

## Requirenment

- Docker
- Python

## Getting start

	pip install csc-docker-tool
	genz-docker-cetd relay init --name main
	genz-docker-cetd relay run --name main
	
	genz-docker-cetd staking init --name main-staking
	genz-docker-cetd staking run --name main-staking


