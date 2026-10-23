#!/bin/bash

version=$(awk '/^Version:/ { print $2; exit }' Package/DEBIAN/control)
package_file="typewriter-${version}.deb"

    if [[ -f "$package_file" ]]; then
        echo "Version ${version} in Package/DEBIAN/control matches existing package ${package_file}."
        echo ""
        echo "Update version in control! (Or manually delete ${package_file} to rebuild.)"
        exit 1
    fi

cp main.py Package/usr/bin/typewriter.py && chmod +x Package/usr/bin/typewriter.py

dpkg-deb --build Package

mv Package.deb "$package_file"