#!/bin/bash
docker-compose --verbose -f docker-compose.yml down 
docker-compose --verbose -f docker-compose.yml build
docker-compose --verbose -f docker-compose.yml up -d 

