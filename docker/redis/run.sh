docker run --name redis --restart unless-stopped -v redis_db:/data -d -p 6379:6379 redis redis-server --appendonly yes
