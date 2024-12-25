VERSION=0
DATE=`date +'%y-%m-%d.%H:%M:%S'`

all: clean environment

clean:
	@echo "Removing Python virtual environment"
	@rm -rf venv
	@rm -rf dist
	@rm -rf src/sourcevault_test.egg-info/
	@find ./ -name "*pycache*" -type d -exec rm -rf {} \; -print

environment:
	@echo "Building Python virtual environment"
	@python3 -m venv venv
	@venv/bin/pip install --upgrade pip
	@venv/bin/pip install -r requirements.txt

build:
	@echo "Build"
ifeq ($(VERSION), 0)
	@venv/bin/python version.py
else
	@venv/bin/python version.py -v $(VERSION)
endif
	@rm -rf dist
	@venv/bin/python -m build

#upload:
#	@echo "Uploading repo to https://files.sourcevault.dev"
#	@git archive -o /mnt/nginx-static/v01/lite/salvation-lite/master-${DATE}.tar.gz --prefix=master/ HEAD

#publish:
#	@echo "Publishing build"
#	@twine upload -r salvation dist/*
