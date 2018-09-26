#!/usr/bin/env bash

# create scratch container
newcontainer=$(buildah from scratch)

# mount scratch container
scratchmnt=$(buildah mount $newcontainer)

# install bash and coreutils
dnf install --assumeyes --installroot $scratchmnt --releasever=28 \
	bash coreutils \
	--setopt install_weak_deps=false \
	--setopt tsflags=nodocs

# install QPID dispatch router and dependencies
cd /home/mockbuild/rpmbuild/RPMS/
dnf install --assumeyes --installroot $scratchmnt \
	--setopt install_weak_deps=false \
	--setopt tsflags=nodocs \
	qpid-dispatch-router-1.2.0-1.el7.x86_64.rpm \
	qpid-dispatch-tools-1.2.0-1.el7.x86_64.rpm \
	qpid-proton-c-0.24.0-1.el7.x86_64.rpm \
	qpid-proton-cpp-0.24.0-1.el7.x86_64.rpm \
	python2-qpid-proton-0.24.0-1.el7.x86_64.rpm

# clean up our cache to keep the image small
dnf clean all --assumeyes --installroot $scratchmnt --releasever=28

# set the default start up command
buildah config --cmd /usr/sbin/qdrouterd $newcontainer

# set metadata
buildah config --created-by "NFVPE @ Red Hat" $newcontainer
buildah config --author "admin at nfvpe.site" --label name=qpid-dispatch-router $newcontainer

# unmount and commit changes
buildah unmount $newcontainer
buildah commit $newcontainer qpid-dispatch-router

# push into docker for upload to docker hub
# buildah push qpid-dispatch-router docker-daemon:nfvpe/qpid-dispatch-router:1.2.0-1

# test run
# docker run -it -v $HOME/qdr.conf.d/:/etc/qdr.conf.d/:Z \
#     -P \
#     --net=host \
#     nfvpe/qpid-dispatch-router:1.2.0-1 /usr/sbin/qdrouterd --config=/etc/qdr.conf.d/qdrouterd.conf
