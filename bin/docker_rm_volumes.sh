#!/bin/bash

docker volume ls | awk '{ print $NF }' | tail -n +2 | while read line; do
  docker volume rm "${line}"
done