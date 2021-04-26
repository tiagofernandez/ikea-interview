#!/bin/sh

export $(grep -v '^#' .env | xargs)
gunicorn -b 0.0.0.0:5000 warehouse:app
