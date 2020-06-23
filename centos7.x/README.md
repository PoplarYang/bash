获取依赖的基础安装包

## build 镜像
1. 修改Dockerfile，确认操作系统版本版本，默认是最新版
2. build 镜像
```bash
docker build -t centos:7.8.2003 .
```

### Makefile Usage
```bash
# 1. 获取 base repo 并上传
make run base

# 2. 清理镜像
make clean_docker

# 3. 清理目录
make clean
```
