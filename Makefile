run:    build
	@docker run \
	    --rm \
		-ti \
	    databaker

build:
	@docker build -t databaker .

.PHONY: run build
