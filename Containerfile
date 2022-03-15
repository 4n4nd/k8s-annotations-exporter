FROM python:3.10-alpine
RUN apk add --no-cache git

WORKDIR /usr/src/app
COPY . ./
RUN pip install --no-cache-dir .

CMD [ "k8s_annotations_exporter", "-h" ]
