docker buildx build --platform=linux/amd64 -t jxch/capital-server:amd64-$(Get-Date -Format 'yyyyMMdd') -t jxch/capital-server:amd64-latest . --push
