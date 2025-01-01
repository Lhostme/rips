# Remote Image Processing Service?

## Build
docker build -t my-python-app .

## Run linux
docker run -it --rm -v $(pwd)/vidData:/vidData my-python-app

## Run Windows
docker run -p 5000:5000 -it --rm -v ${pwd}\vidData:\vidData my-python-app
