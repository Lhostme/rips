# Remote Image Processing Service?

## Build
docker build -t my-python-app .

## Run linux
docker run -it --rm -v $(pwd)/vidData:/vidData my-python-app

## Run Windows
docker run -it --rm -v ${pwd}\vidData:\vidData my-python-app
