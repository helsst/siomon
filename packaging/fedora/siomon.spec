%global commit 2f0b399085de511ff14d8a8a2b69c71f7a40558c
%global shortcommit 2f0b399

Name:           siomon
Version:        0.2.3
Release:        1%{?dist}
Summary:        Hardware information and real-time sensor monitoring tool

License:        MIT
URL:            https://github.com/level1techs/siomon
Source0:        %{name}-%{version}.tar.gz
Source1:        %{name}-%{version}-vendor.tar.gz

ExclusiveArch:  %{rust_arches}

BuildRequires:  cargo
BuildRequires:  rust
BuildRequires:  systemd-rpm-macros

Requires:       libcap
Requires(post): libcap
Requires(post): systemd
Requires(posttrans): systemd-udev
Requires(postun): systemd-udev
Recommends:     dmidecode
Recommends:     i2c-tools
Recommends:     msr-tools
Suggests:       hddtemp

%description
siomon is a Linux hardware information and real-time sensor monitoring tool.
It provides a TUI dashboard for live sensor monitoring and one-shot hardware
information subcommands.

%prep
%autosetup -n %{name}-%{version} -a 1
mkdir -p .cargo
cat > .cargo/config.toml <<'EOF'
[source.crates-io]
replace-with = "vendored-sources"

[source.vendored-sources]
directory = "vendor"
EOF

%build
cargo build --frozen --release --all-features
cargo run --frozen --package xtask -- shell-completion bash > sio.bash
cargo run --frozen --package xtask -- shell-completion zsh > _sio
cargo run --frozen --package xtask -- shell-completion fish > sio.fish

%install
install -Dpm0755 target/release/sio %{buildroot}%{_bindir}/sio
install -Dpm0644 sio.bash %{buildroot}%{_datadir}/bash-completion/completions/sio
install -Dpm0644 _sio %{buildroot}%{_datadir}/zsh/site-functions/_sio
install -Dpm0644 sio.fish %{buildroot}%{_datadir}/fish/vendor_completions.d/sio.fish
install -Dpm0644 packaging/udev/50-siomon.rules %{buildroot}%{_udevrulesdir}/50-siomon.rules
install -Dpm0644 packaging/tmpfiles/siomon.conf %{buildroot}%{_tmpfilesdir}/siomon.conf

%check
cargo test --frozen --all-features

%post
%tmpfiles_create siomon.conf
if command -v setcap >/dev/null 2>&1; then
    setcap cap_perfmon,cap_sys_rawio=ep %{_bindir}/sio 2>/dev/null || :
fi

%posttrans
udevadm control --reload-rules >/dev/null 2>&1 || :
udevadm trigger --subsystem-match=powercap >/dev/null 2>&1 || :

%postun
udevadm control --reload-rules >/dev/null 2>&1 || :

%files
%license LICENSE
%doc README.md
%{_bindir}/sio
%{_datadir}/bash-completion/completions/sio
%{_datadir}/zsh/site-functions/_sio
%{_datadir}/fish/vendor_completions.d/sio.fish
%{_udevrulesdir}/50-siomon.rules
%{_tmpfilesdir}/siomon.conf

%changelog
* Mon May 18 2026 Level1Techs Package Team <level1techspackageteam@gmail.com> - 0.2.3-1
- Initial Fedora COPR package
