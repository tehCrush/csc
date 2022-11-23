#!/bin/bash
package_file=csc
BASEDIR=$PWD
VENV=$(pipenv --venv)
pipenv requirements > requirements.txt
mkdir $BASEDIR/deploy
cp lambda_function.py deploy/
docker run -v "$PWD":/var/task "lambci/lambda:build-python3.8" /bin/sh -c "pip install -r requirements.txt -t deploy/; exit"
cd $BASEDIR/deploy
docker run --rm -e DOCKER_LAMBDA_STAY_OPEN=1 -e DOCKER_LAMBDA_API_PORT=9001 -p 9001:9001 -v "$PWD":/var/task:ro,delegated lambci/lambda:python3.8 lambda_function.lambda_handler
