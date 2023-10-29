#!/bin/bash

if [ "$(docker ps -q -f name=postgres_14)" ]; then
    echo "Postgres container is already running"
else
    if [ "$(docker ps -aq -f status=exited -f name=postgres_14)" ]; then
        echo "Removing stopped Postgres container"
        docker rm postgres_14
    fi
    echo "Starting Postgres container"
    docker run -p 5432:5432 -e POSTGRES_PASSWORD=password -e POSTGRES_USER=postgres -e POSTGRES_DB=db --name postgres_14 -d postgres:14
fi
