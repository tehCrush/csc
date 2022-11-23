# Build stage 0 as base
from lambci/lambda:build-python3.8 as build
#RUN mkdir /var/task
WORKDIR /var/task

COPY requirements.txt .
RUN bash -c "pip install -r requirements.txt -t /var/task/; exit"

FROM lambci/lambda:python3.8 as deploy
COPY --from=build /var/task /var/task

ENV DOCKER_LAMBDA_STAY_OPEN=1 \
    DOCKER_LAMBDA_API_PORT=9001 \
    AWS_LAMBDA_FUNCTION_NAME=lambda_function \
    AWS_LAMBDA_FUNCTION_HANDLER=lambda_handler
COPY lambda_function.py /var/task/
VOLUME /var/task
EXPOSE 9001
