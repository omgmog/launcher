# GameShell launcher for PocketCHIP

This is the Launcher from the Gameshell, ported over to the PocketCHIP.

![](https://media.discordapp.net/attachments/422472890441793539/585821529913425923/2019-06-05-132318_480x272_scrot.png)

### Note

This is has been tested on my own PocketCHIP to ensure repeatability a couple of times, but you might encounter your own probems if you don't have a working `apt` for example.

## Installation

```
cd ~
git clone https://github.com/omgmog/launcher.git
cd launcher
chmod +x install.sh
bash ./install.sh
```

## Uninstallation

Uninstallation is quite lazy, it just restores the awesomewm config, and re-installs `pocket-home`.

```
bash ./install.sh -u
```

## Button configuration

The button layout is as follows:

- A/OK - `8`
- B/Back - `0`
- X - `7`
- Y - `9`
- D-pad - d-pad

- Volume control: `Ctrl` + `-` or `+`, Then `0` (back) to close/confirm

This should be the most consistent with what you're used to on PocketCHIP, while also providing the additional buttons that the launcher uses.

You can also use `enter` to select things, and `escape` to go back.

The usual `ctrl`+`tab` and `ctrl`+`q` shortcuts from `pocket-home` will work everywhere too.

## Adding new shortcuts

To add a new shortcut, create a `.sh` file in the `~/launcher/Menu/GameShell` directory (you can copy one of the others) or `~/apps/Menu` directory.

The filename indicates the order, and must start with a number and underscore:

```
NN_Name Of Shortcut.sh
```

To set an icon for the shortcut, you need to add an 80x80 png in `~/launcher/skin/pocket/Menu/GameShell` with a filename that matches the app shortcut, but without the number and underscore prefix:

```
Name Of Shortcut.png
```

If you don't have an icon, the launcher will use the first letters of the shortcut and the blank icon found at `~/launcher/skin/pocket/sys.py/gameshell/blank.png`

If you have problems with applications not using the whole screen, or failing to start, you can try specifying the display at the start of your command, e.g.:

```
DISPLAY=:0 leafpad
```

Other than that, you can follow the instructions from the Gameshell wiki for launching games in emulators directly, if you have `retroarch` installed on your PocketCHIP: https://github.com/clockworkpi/GameShellDocs/wiki/New-ICONS-that-start-games-in-one-click-from-the-MENU

Or you can grab any of the game launchers that have bene collected here: https://github.com/omgmog/launcher-community-apps

## Known problems and missing features

I've raised [issues](https://github.com/omgmog/launcher/issues) for everything I'm aware of. If you notice something else, please raise an issue!

## Help!

Having problems with anything? Check these common problems below, or raise an [issue](https://github.com/omgmog/launcher/issues/new)
