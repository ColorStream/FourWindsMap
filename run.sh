#!/bin/bash
set -e
gunicorn FourWindsMap.wsgi --log-file -