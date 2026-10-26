#!/bin/bash

version=$(awk '/^Version:/ { print $2; exit }' deb-package/DEBIAN/control)
package_file="typewriter-${version}.deb"

    if [[ -f "$package_file" ]]; then
        echo "Version ${version} in deb-package/DEBIAN/control matches existing package ${package_file}."
        echo ""
        echo "Update version in control! (Or manually delete ${package_file} to rebuild.)"
        exit 1
    fi

cp main.py deb-package/usr/bin/typewriter.py && chmod +x deb-package/usr/bin/typewriter.py

dpkg-deb --build deb-package

mv deb-package.deb "$package_file"