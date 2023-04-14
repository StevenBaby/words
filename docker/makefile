#!/bin/bash

.PHONY: words
words:
	mkdir -p ./app
	cp -r ../words/locale ./app/locale
	cp -r ../words/resources ./app/resources
	cp -r ../words/settings ./app/settings
	cp -r ../words/utils ./app/utils
	cp -r ../words/viewer ./app/viewer
	cp -r ../words/words ./app/words
	cp -r ../words/manage.py ./app/manage.py
	cp -r ../words/requirements.txt ./app/requirements.txt
	cp -r ./entrypoint.sh ./app/entrypoint.sh
	docker build -t words .
	rm -r ./app


LOCAL:= $(abspath $(shell pwd)/../words/local)

.PHONY: runit
runit: $(LOCAL)
	docker run \
		-it \
		-v $(LOCAL):/app/local \
		-p8888:8888 \
		words

.PHONY: run
run: $(LOCAL)
	docker run \
		-d \
		-v $(LOCAL):/app/local \
		-p8888:8888 \
		--restart=always \
		words
