# Container Image Creation

In this directory you'll find supporting scripts and files for building a QPID
dispatch router container image using [Buildah](https://github.com/projectatomic/buildah).

## Install Buildah

You can find more information about using **Buildah** and installing it from
the [introduction documentation](https://github.com/projectatomic/buildah/blob/master/docs/tutorials/01-intro.md)
but the _tl;dr_ is basically the following. We assume everything is being
built on Fedora 27 or 28.

    sudo dnf install buildah -y
