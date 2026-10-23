#!/bin/bash

cp main.py Package/usr/bin/typewriter.py && chmod +x Package/usr/bin/typewriter.py

dpkg-deb --build Package

mv Package.deb typewriter-$(cat Package/DEBIAN/control | grep Version | cut -d " " -f 2).deb