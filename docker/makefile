#!/bin/bash

VERSION:=$(shell cd ../words && python manage.py ver)
LOCALNAME:= words:$(VERSION)
REMOTENAME:= stevenkang/words:$(VERSION)
LATESTNAME:= stevenkang/words:latest
RUNNAME:= words_$(VERSION)

.PHONY: build
build:
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
	docker build -t $(LOCALNAME) .
	rm -r ./app

.PHONY: tag
tag:
	docker tag $(LOCALNAME) $(REMOTENAME)
	docker tag $(LOCALNAME) $(LATESTNAME)

.PHONY: push
push:
	docker push $(REMOTENAME)
	docker push $(LATESTNAME)

LOCAL:= $(abspath $(shell pwd)/../words/local)

.PHONY: runit
runit: $(LOCAL)
	docker run \
		-it \
		-v $(LOCAL):/app/local \
		-p8888:8888 \
		--name $(RUNNAME) \
		$(LOCALNAME)

.PHONY: run
run: $(LOCAL)
	docker run \
		-d \
		-v $(LOCAL):/app/local \
		-p8888:8888 \
		--restart=always \
		--name $(RUNNAME) \
		$(LOCALNAME)

.PHONY: stop
stop:
	-docker stop $(RUNNAME)

.PHONY: clean
clean: stop
	-docker container rm $(RUNNAME)
	-docker image rm -f $(REMOTENAME)
	-docker image rm -f $(LATESTNAME)
