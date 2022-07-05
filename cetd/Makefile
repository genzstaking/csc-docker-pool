# You can set these variables from the command line, and also
# from the environment for the first two.
SHELL               =/bin/bash
DOCKER_BUILD       ?= docker build -f
SOURCEDIR           = .
BUILDDIR            = build

VERSIONS           ?=1.0.1
# Put it first so that "make" without argument is like "make help".
help:
	@$(DOCKER) --help

.PHONY: help Makefile clean


all: $(VERSIONS)
clean:
cli: all
force:
publish: $(VERSIONS)
	docker push ghcr.io/genz-bank/cetd:latest 
	docker push ghcr.io/genz-bank/cetd:$(VERSIONS)
	

$(SUBDIRS):force
	$(MAKE) -C $@ $(MAKECMDGOALS)


$(VERSIONS): force
	@$(DOCKER_BUILD) Dockerfile \
		--build-arg VERSION=$@ \
		--tag ghcr.io/genz-bank/cetd:$@ \
		--tag ghcr.io/genz-bank/cetd:latest .



