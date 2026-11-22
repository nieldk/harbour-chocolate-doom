Name:       harbour-chocolate-doom
Summary:    Chocolate Doom with touch controls
Version:    3.1.1
Release:    1
License:    GPLv2+ and zlib
URL:        https://github.com/chocolate-doom/chocolate-doom
Source0:    %{name}-%{version}.tar.bz2
Patch0:     0001-touch-controls.patch
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  pkgconfig(sdl2) >= 2.0.14

%description
Chocolate Doom, a Doom source port that stays true to the vanilla
behaviour, with an on-screen touch overlay: floating stick, look swipe
and fire, use, weapon and menu buttons.

Doom data is not included. Put an IWAD (for example doom.wad,
doom2.wad or a Freedoom IWAD) in ~/.local/share/games/doom/

%prep
%setup -q -n %{name}-%{version}
patch -p1 -d chocolate-doom < %{PATCH0}

%build
# Minimal static SDL2_mixer: Doom needs sample mixing and the music hook only.
mkdir mixer-build
cd mixer-build
cmake ../SDL_mixer \
    -DCMAKE_BUILD_TYPE=Release \
    -DCMAKE_INSTALL_PREFIX=$PWD/../mixer-prefix \
    -DCMAKE_POSITION_INDEPENDENT_CODE=ON \
    -DBUILD_SHARED_LIBS=OFF \
    -DSDL2MIXER_VENDORED=OFF \
    -DSDL2MIXER_DEPS_SHARED=OFF \
    -DSDL2MIXER_SAMPLES=OFF \
    -DSDL2MIXER_INSTALL=ON \
    -DSDL2MIXER_CMD=OFF \
    -DSDL2MIXER_FLAC=OFF \
    -DSDL2MIXER_GME=OFF \
    -DSDL2MIXER_MOD=OFF \
    -DSDL2MIXER_MP3=OFF \
    -DSDL2MIXER_MIDI=OFF \
    -DSDL2MIXER_OPUS=OFF \
    -DSDL2MIXER_WAVPACK=OFF \
    -DSDL2MIXER_VORBIS=STB
make %{?_smp_mflags}
make install
cd ..

mkdir build
cd build
cmake ../chocolate-doom \
    -DCMAKE_BUILD_TYPE=Release \
    -DCMAKE_C_FLAGS="%{optflags} -DHARBOUR_SAILFISH" \
    -DCMAKE_PREFIX_PATH=$PWD/../mixer-prefix \
    -DCMAKE_FIND_PACKAGE_PREFER_CONFIG=Off \
    -DENABLE_SDL2_NET=Off \
    -DCMAKE_DISABLE_FIND_PACKAGE_PNG=TRUE \
    -DCMAKE_DISABLE_FIND_PACKAGE_SampleRate=TRUE \
    -DCMAKE_DISABLE_FIND_PACKAGE_FluidSynth=TRUE
make %{?_smp_mflags} chocolate-doom

%install
install -D -m 0755 build/src/chocolate-doom %{buildroot}%{_bindir}/%{name}
install -D -m 0644 data/%{name}.desktop \
    %{buildroot}%{_datadir}/applications/%{name}.desktop
for s in 86 108 128 172; do
    install -D -m 0644 data/icons/${s}x${s}/%{name}.png \
        %{buildroot}%{_datadir}/icons/hicolor/${s}x${s}/apps/%{name}.png
done

%files
%defattr(-,root,root,-)
%license chocolate-doom/COPYING.md
%{_bindir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/apps/%{name}.png

%changelog
* Sun Nov 22 2026 Niel - 3.1.1-1
- Initial package: Chocolate Doom 3.1.1 with touch controls
