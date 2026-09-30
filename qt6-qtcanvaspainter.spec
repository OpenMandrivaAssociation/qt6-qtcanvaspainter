#define beta rc
#define snapshot 20200627
%define major 6

%define _qtdir %{_libdir}/qt%{major}

Name:		qt6-qtcanvaspainter
Version:	6.12.0
Release:	%{?beta:0.%{beta}.}%{?snapshot:0.%{snapshot}.}1
%if 0%{?snapshot:1}
# "git archive"-d from "dev" branch of git://code.qt.io/qt/qtcanvaspainter.git
Source:		qtcanvaspainter-%{?snapshot:%{snapshot}}%{!?snapshot:%{version}}.tar.zst
%else
Source:		https://download.qt.io/%{?beta:development}%{!?beta:official}_releases/qt/%(echo %{version}|cut -d. -f1-2)/%{version}%{?beta:-%{beta}}/submodules/qtcanvaspainter-everywhere-src-%{version}%{?beta:-%{beta}}.tar.xz
%endif
Group:		System/Libraries
Summary:	Qt %{major} Canvas Painter - accelerated 2D painting for Qt Quick and QRhi
BuildRequires:	cmake
BuildRequires:	ninja
BuildRequires:	cmake(Qt%{major}Core)
BuildRequires:	cmake(Qt%{major}CorePrivate)
BuildRequires:	cmake(Qt%{major}Gui)
BuildRequires:	cmake(Qt%{major}GuiPrivate)
BuildRequires:	cmake(Qt%{major}Widgets)
BuildRequires:	cmake(Qt%{major}WidgetsPrivate)
BuildRequires:	cmake(Qt%{major}Quick)
BuildRequires:	cmake(Qt%{major}QuickPrivate)
BuildRequires:	cmake(Qt%{major}ShaderTools)
BuildRequires:	cmake(Qt%{major}ShaderToolsTools)
BuildRequires:	qt%{major}-cmake
BuildRequires:	pkgconfig(gl)
BuildRequires:	pkgconfig(xkbcommon)
BuildRequires:	pkgconfig(vulkan)
License:	GPLv3
# Supported as of 6.12. Library is GPL-3.0-only (no LGPL edition).

%description
Accelerated 2D painting API for Qt Quick and QRhi-based render targets.
HTML Canvas 2D-style painting with adjustable antialiasing, custom
brushes, and QRhi backends. Supported as of Qt 6.12. The library is
GPL-3.0-only (there is no LGPL edition).

%define extra_devel_files_CanvasPainter \
%{_qtdir}/bin/qcshadergen \
%{_qtdir}/sbom/*

%define extra_files_Canvas2D \
%{_qtdir}/qml/QtCanvas2D

%define extra_devel_files_Canvas2D \
%{_qtdir}/lib/cmake/Qt6Qml/QmlPlugins/Qt6canvas2dplugin*.cmake

%qt6libs CanvasPainter Canvas2D

%package examples
Summary:	Examples for the Qt %{major} Canvas Painter module
Group:		Development/KDE and Qt

%description examples
Examples for the Qt %{major} Canvas Painter module

%files examples
%{_qtdir}/examples/canvaspainter

%prep
%autosetup -p1 -n qtcanvaspainter%{!?snapshot:-everywhere-src-%{version}%{?beta:-%{beta}}}
%cmake -G Ninja \
	-DCMAKE_INSTALL_PREFIX=%{_qtdir} \
	-DQT_BUILD_EXAMPLES:BOOL=ON \
	-DQT_WILL_INSTALL:BOOL=ON

%build
export LD_LIBRARY_PATH="$(pwd)/build/lib:${LD_LIBRARY_PATH}"
%ninja_build -C build

%install
%ninja_install -C build
%qt6_postinstall
