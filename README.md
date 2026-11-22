# harbour-chocolate-doom

Chocolate Doom 3.1.1 for Sailfish OS, built on build.sailfishos.org.
Touch overlay: floating stick (left), look swipe (right), F fire, U use,
< > weapons, M menu, E enter, Y confirm.
In menus: swipe moves the cursor (repeats while held), tap selects.

## Repo setup

    git init -b main
    git submodule add https://github.com/chocolate-doom/chocolate-doom chocolate-doom
    git -C chocolate-doom checkout chocolate-doom-3.1.1
    git submodule add https://github.com/libsdl-org/SDL_mixer SDL_mixer
    git -C SDL_mixer checkout release-2.8.2
    git add -A && git commit -m "Initial package"
    git tag 3.1.1-1

Push, then create the OBS package with `_service` (tar_git, revision is the tag).

## Notes

- SDL_mixer is built static and minimal inside the spec (no Jolla package found).
- IWAD goes in ~/.local/share/games/doom/ (no game data shipped).
- Options: `-notouch` disables the overlay, `-touch` forces it, `-touchdebug` prints touch and key events.
- The patch also applies to upstream HEAD a2dfd51.
