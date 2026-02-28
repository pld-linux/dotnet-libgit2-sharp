Summary:	C# git library
Summary(pl.UTF-8):	Biblioteka git dla C#
Name:		dotnet-libgit2-sharp
Version:	0.21.1
Release:	2
License:	MIT
Group:		Libraries
#Source0Download: https://github.com/libgit2/libgit2sharp/releases
Source0:	https://github.com/libgit2/libgit2sharp/archive/v%{version}/libgit2sharp-%{version}.tar.gz
# Source0-md5:	7824fa9213c72e303b43bc5c02ddd37f
Patch0:		%{name}-framework.patch
URL:		http://libgit2.github.com/
BuildRequires:	libgit2-devel >= 0.23
BuildRequires:	mono-devel >= 3.6
BuildRequires:	pkgconfig
Requires:	libgit2-devel >= 0.23
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
LibGit2Sharp brings all the might and speed of libgit2, a native Git
implementation, to the managed world of .NET and Mono.

%description -l pl.UTF-8
LibGit2Sharp dostarcza całość możliwości oraz szybkość libgit2 -
natywnej implementacji Gita - do zarządzanego świata .NET i Mono.

%package devel
Summary:	Development files for git2 C# library
Summary(pl.UTF-8):	Pliki programistyczne biblioteki C# libgit2
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Development files for git2 C# library.

%description devel -l pl.UTF-8
Pliki programistyczne biblioteki C# libgit2.

%prep
%setup -q -n libgit2sharp-%{version}
%patch -P0 -p1

%{__rm} Lib/CustomBuildTasks/CustomBuildTasks.dll
%{__rm} -r Lib/NativeBinaries

%build
cd Lib/CustomBuildTasks
xbuild CustomBuildTasks.csproj /property:Configuration=Release
ln -snf bin/Release/CustomBuildTasks.dll .
cd ../..

xbuild LibGit2Sharp/LibGit2Sharp.csproj /property:Configuration=Release

cat >LibGit2Sharp/bin/Release/LibGit2Sharp.dll.config <<EOF
<configuration>
  <dllmap dll="git2-e0902fb" target="libgit2.so.23"/>
</configuration>
EOF

%install
rm -rf $RPM_BUILD_ROOT

# libgit2sharp is not strong name signed, cannot do that
#gacutil -i LibGit2Sharp/bin/Release/LibGit2Sharp.dll -root $RPM_BUILD_ROOT%{_prefix}/lib

install -d $RPM_BUILD_ROOT{%{_prefix}/lib/mono/git2,%{_pkgconfigdir}}
cp -p LibGit2Sharp/bin/Release/LibGit2Sharp.dll* $RPM_BUILD_ROOT%{_prefix}/lib/mono/git2
cat >$RPM_BUILD_ROOT%{_pkgconfigdir}/libgit2sharp.pc <<'EOF'
prefix=%{_prefix}
exec_prefix=${prefix}
libdir=${prefix}/lib
Libraries=${prefix}/lib/mono/git2/LibGit2Sharp.dll

Name: libgit2sharp
Description libgit2sharp - .NET binding for libgit2 library
Version: %{version}
Libs: -r:${prefix}/lib/mono/git2/LibGit2Sharp.dll
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CHANGES.md LICENSE.md README.md acknowledgments.md
%dir %{_prefix}/lib/mono/git2
%{_prefix}/lib/mono/git2/LibGit2Sharp.dll
%{_prefix}/lib/mono/git2/LibGit2Sharp.dll.config
%{_prefix}/lib/mono/git2/LibGit2Sharp.dll.mdb

%files devel
%defattr(644,root,root,755)
%{_pkgconfigdir}/libgit2sharp.pc
