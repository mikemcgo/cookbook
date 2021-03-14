#!/usr/bin/env sh

docker ps -a -q --filter name="pytest*" --format="{{.ID}}" | xargs -I {} docker stop {} | xargs -I {} docker rm {}