#!/bin/sh
curl --location 'localhost:9515/session' \
--header 'Content-Type: application/json; charset=utf-8' \
--data '{
  "capabilities": {
    "firstMatch": [
      {
        "browserName": "chrome"
      }
    ]
  }
}'

