#!/usr/bin/env bash

# Set the timezone.
if [[ "${SET_CONTAINER_TIMEZONE}" = "true" ]]; then
	echo ${CONTAINER_TIMEZONE} | tee /etc/timezone && \
	ln -sf /usr/share/zoneinfo/Europe/London /etc/localtime && \
	dpkg-reconfigure -f noninteractive tzdata
	echo "Container timezone set to: $CONTAINER_TIMEZONE"
else
	echo "Container timezone not modified"
fi

