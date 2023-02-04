docker buildx build --platform=linux/arm64,linux/amd64 -t jxch/capital-server:$(Get-Date -Format 'yyyyMMdd') -t jxch/capital-server:latest . --push
