.PHONY: build build_t build_m up_t up_m up prune down_t down_m down down_all

build_m:
	@echo "Building both LND and Bitcoind for mainnet"
	docker-compose \
		--file docker-compose.mainnet.yml \
		build


build_t:
	@echo "Building both LND and Bitcoind for testnet"
	docker-compose \
		--file docker-compose.testnet.yml \
		build

build: build_t

up_t:
	@echo "Spinning up Docker for LND and Bitcoind for testnet"
	docker-compose \
		--file docker-compose.testnet.yml \
		up
up_m: 
	@echo "Spinning up Docker for LND and Bitcoind for mainnet"
	docker-compose \
		--file docker-compose.mainnet.yml \
		up

up: up_t

up_d: 
	@echo "Spinning up Docker for LND and Bitcoind for testnet"
	docker-compose \
		--file docker-compose.testnet.yml \
		up -d

prune:
	docker system prune

down_t:
	docker-compose \
		--file docker-compose.testnet.yml \
		down

down_m:
	docker-compose \
		--file docker-compose.mainnet.yml \
		down

down: down_t

down_all: down_t \
		down_m