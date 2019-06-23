# Copyright (C) Quartet Health, Inc - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential

SHELL := /bin/bash

REMOTE_DIR ?= ~

IMG=product_clustering

export

.PHONY: build
build:
	docker build -t ${IMG} .

