{
  imports = [
    ./alertmanager.nix
    ./exporters/blackbox.nix
    ./exporters/channel.nix
    ./exporters/domain.nix
    ./exporters/fastly.nix
    ./exporters/github.nix
    ./exporters/hydra.nix
    ./exporters/nixos.nix
    ./exporters/node.nix
    ./exporters/packet-sd.nix
    ./exporters/packet-spot-market.nix
    ./exporters/postgresql.nix
    ./exporters/r13y.nix
    ./exporters/rfc39.nix
  ];

  networking.extraHosts = ''
    10.254.1.1 bastion
    10.254.1.5 rhea
    10.254.1.6 pluto

    10.254.1.9 haumea

    10.254.3.1 webserver
  '';

  networking.firewall.allowedTCPPorts = [
    9090
  ];

  services.prometheus = {
    enable = true;
    extraFlags = [
      "--storage.tsdb.retention=${toString (150 * 24)}h"
      "--web.external-url=https://monitoring.nixos.org/prometheus/"
    ];
    globalConfig.scrape_interval = "15s";
  };
}
