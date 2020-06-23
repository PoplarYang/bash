#OS_VERSION = 7.0.1406
#OS_VERSION = 7.1.1503
#OS_VERSION = 7.2.1511
#OS_VERSION = 7.3.1611
#OS_VERSION = 7.4.1708
#OS_VERSION = 7.5.1804
#OS_VERSION = 7.6.1810
#OS_VERSION = 7.7.1908
OS_VERSION = 7.8.2003

.PHONY: run
run:
	docker run -itd -v $(PWD)/data:/mnt \
	--name centos_$(OS_VERSION) centos:$(OS_VERSION)

.PHONY: rund
rund:
	docker run -it -v $(PWD)/data:/mnt \
	--name centos_$(OS_VERSION) centos:$(OS_VERSION) /bin/bash

.PHONY: build
build:
	docker build -t centos:$(OS_VERSION) .

.PHONY: exec
exec:
	docker exec -it centos_$(OS_VERSION) /bin/bash

.PHONY: clean_docker
clean_docker:
	-docker stop centos_$(OS_VERSION)
	-docker rm centos_$(OS_VERSION)

.PHONY: base
base:
	docker exec -it centos_$(OS_VERSION) /bin/bash /mnt/centos7_base_repo_download.sh
	docker exec -it centos_$(OS_VERSION) /bin/bash /mnt/upload_base_repo.sh

.PHONY: clean
clean:
	-rm -rf data/*.tar.gz data/centos_ext_repo data/centos_repo
