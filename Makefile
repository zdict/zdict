docker-zdict:
	# Let users can use `make docker-zdict apple bird`
	# https://stackoverflow.com/questions/6273608
	@docker run -it --rm zdict/zdict $(filter-out $@,$(MAKECMDGOALS))

docker-run:
	@docker run -it --entrypoint=/bin/bash --rm zdict/zdict

docker-pull:
	@docker pull zdict/zdict

docker-push:
	@docker push zdict/zdict

docker-build:
	@docker build -t "zdict/zdict:latest" .

# Make docker-zdict don't complain about no make rules for apple, bird, ...
%:
	@:
