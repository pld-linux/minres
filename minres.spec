#
# Conditional build:
%bcond_with     acml    # With ACML version of BLAS instead of NETLIB implementation
%bcond_with	atlas	# With ATLAS version of BLAS instead of NETLIB implementation
			# (mutually exclusive with acml)
#
Summary:	Iterative linear equations solver
Summary(pl):	Rozwi±zywanie równañ liniowych metod± iteracyjn±
Name:		minres
Version:	20030722
Release:	1%{?with_acml:ACML}%{?with_atlas:ATLAS}
License:	CPL
Group:		Libraries
Source0:	http://www.stanford.edu/group/SOL/software/minres/f77/minres.f
# Source0-md5:	99448f9c2c673ca4e1ea1dd4c9df7ff5
Source1:	http://www.stanford.edu/group/SOL/software/minres/f77/minresblas.f
# Source1-md5:	c510879f60034d2b41b4354f921e039f
Source2:	http://www.stanford.edu/group/SOL/software/minres/f77/minres_f77.README
# Source2-md5:	bf7c71f77416c9a8bbe267dea85134a0
Patch0:		%{name}-automake_support.patch
Patch1:		%{name}-omitblas.patch
URL:		http://www.stanford.edu/group/SOL/software/minres.html
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc-g77
BuildRequires:  libtool >= 2:1.5
%{!?with_acml:%{!?with_atlas:BuildRequires:	blas-devel}}
%{?with_acml:ExclusiveArch:	amd64}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Implementation of a conjugate-gradient type method for solving sparse
linear equations: solve Ax = b or (A - sI)x = b. The matrix A - sI must
be symmetric but it may be definite or indefinite or singular. The
scalar s is a shifting parameter -- it may be any number. The method is
based on Lanczos tridiagonalization. You may provide a preconditioner,
but it must be positive definite.
MINRES is really solving the least-squares problem minimize ||(A - sI)x
- b||. 

%description -l pl
Implementacja gradientowej metody rozwi±zywania rzadkich uk³adów równañ
liniowych, postaci Ax = b albo (A - sI)x = b. Macierz A - sI musi byæ
symetryczna, ale nie mo¿e byæ nieokre¶lona i/lub osobliwa. Skalar s mo¿e
byæ dowoln± liczb±. Metoda jest oparta na trójdiagonalizacji Lanczosa.
Mo¿na jej dostarczyæ dodatnio okre¶lony preconditioner.
W rzeczywisto¶ci, MINRES rozwi±zuje problem metody najmniejszych
kwadratów: minimalizacja normy ||(A - sI)x - b||.

%package devel
Summary:	MINRES development files
Summary(pl):	Pliki programistyczne MINRES
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
MINRES development files.

%description devel -l pl
Pliki programistyczne MINRES.

%package static
Summary:	Static MINRES library
Summary(pl):	Statyczna biblioteka MINRES
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static MINRES library.

%description static -l pl
Statyczna biblioteka MINRES.

%prep
%setup -q -c -T
cp %{SOURCE1} .
%patch0 -p1
%patch1 -p1

cp %{SOURCE0} .
cp %{SOURCE2} README

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	CFLAGS=-O3 \
	LDFLAGS=%{?with_acml:"-lm -lg2c -lacml"}%{?with_atlas:"-lf77blas -latlas"}%{!?with_acml:%{!?with_atlas:-lblas}}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README
%attr(755,root,root) %{_libdir}/libminres.so.*.*.*

%files devel
%defattr(644,root,root,755)
%doc minres.f
%attr(755,root,root) %{_libdir}/libminres.so
%{_libdir}/libminres.la

%files static
%defattr(644,root,root,755)
%{_libdir}/libminres.a
