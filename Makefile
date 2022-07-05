# You can set these variables from the command line, and also
# from the environment for the first two.
SHELL               =/bin/bash
SOURCEDIR           = .
BUILDDIR            = build

DOCKER_BUILD       ?= docker build -f

SPHINXOPTS         ?=
SPHINXBUILD        ?= sphinx-build

NODE_VERSION        ?=1.34.1
LIBSODIUM_VERSION   ?=66f017f1
ADDRESS_VERSION     ?=3.9.0
BECH_VERSION        ?=1.1.2
CNCLI_VERSION       ?=4.0.4
POOL_VERSION        ?=1.34.1-2

SUBDIRS              = cetd
# TODO add following:
# address bech32 cncli pool voting
DOCS_TARGETS         = html
help:
	@$(DOCKER) --help

.PHONY: help Makefile clean

all: $(SUBDIRS)
clean: $(SUBDIRS)
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) clean
publish: $(SUBDIRS)
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) publish
force:

$(SUBDIRS):force
	$(MAKE) -C $@ $(MAKECMDGOALS)


# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
$(DOCS_TARGETS): force
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)



