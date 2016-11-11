#!/bin/bash

# run curl within a k8s cluster via kubectl

export KURL_DEPLOYMENT=curl-$(hostname)
kubectl run --rm ${KURL_DEPLOYMENT} --image=radial/busyboxplus:curl -i --tty


