sudo rm -rf ui/node_modules
docker-compose -f docker-compose.yml -f docker-compose.dev.yml build && docker-compose -f docker-compose.yml -f docker-compose.dev.yml up -d
echo y | docker system prune
