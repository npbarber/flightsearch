#!/usr/bin/env make

NOSETESTS ?= $(shell sh -c 'which nosetests 2>/dev/null || echo nosetests')

test:
	$(NOSETESTS) tests/unittests
