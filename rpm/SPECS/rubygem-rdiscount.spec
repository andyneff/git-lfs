%global gemdir %(ruby -rubygems -e 'puts Gem::dir' 2>/dev/null)
%define gem_name rdiscount
Name:           rubygem-%{gem_name}
Version:        2.1.8
Release:	1%{?dist}
Summary:        Fast Implementation of Gruber's Markdown in C

Group:          Applications/Programming
License:        BSD
URL:		https://rubygems.org/gems/%{gem_name}
Source0:	https://rubygems.org/downloads/%{gem_name}-%{version}.gem
BuildRoot:      %(echo %{_topdir}/BUILDROOT/%{gem_name}-%{version})
BuildRequires:	gem > 1.9.2
Requires:       ruby > 1.9.2
BuildArch:      noarch

%description
Fast Implementation of Gruber's Markdown in C

%prep

%build

%install
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT
gem install -V --local --force --install-dir ${RPM_BUILD_DIR}/%{gemdir} %{SOURCE0}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
/

%changelog
* Wed May 20 2015 Andrew Neff <andyneff@users.noreply.github.com> - 2.1.8
- Initial Spec
