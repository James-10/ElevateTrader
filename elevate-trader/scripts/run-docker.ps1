#! bin/bash

echo "Starting docker build"

docker build -t elevate_trader:dev -f Dockerfile  .
docker run --rm --name elevate_trader elevate_trader:dev