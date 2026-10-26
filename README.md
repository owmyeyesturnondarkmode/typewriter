# Typewriter

Typewriter is a minimalist text editor based on GTK 4 and libadwaita.

## Build and install the Flatpak

The Flatpak manifest uses the GNOME 49 runtime, which provides GTK 4,
libadwaita, and PyGObject. On a system with Flatpak and `flatpak-builder`
installed, first add Flathub if it is not already configured:

```sh
flatpak remote-add --user --if-not-exists flathub https://flathub.org/repo/flathub.flatpakrepo
```

From the project root, build and install the app for the current user:

```sh
flatpak-builder --user --install --install-deps-from=flathub --force-clean build-dir com.typewriter.Typewriter.yml
```

Run it with:

```sh
flatpak run com.typewriter.Typewriter
```

To create a distributable bundle instead, build the repository and export a
single-architecture bundle:

```sh
flatpak-builder --user --repo=repo --force-clean build-dir com.typewriter.Typewriter.yml
flatpak build-bundle repo typewriter.flatpak com.typewriter.Typewriter
```

The manifest grants display access and portal access for file open/save
dialogs; it does not grant general access to the host filesystem.