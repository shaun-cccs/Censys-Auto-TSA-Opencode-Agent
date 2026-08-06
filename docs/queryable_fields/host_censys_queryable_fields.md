# Censys Platform Queryable Fields

Parsed from `Host Censys Data Definitions.html` (in-app data definitions, <https://platform.censys.io/home/definitions>).

**Total fields: 3539**

| Dataset | Field count |
| --- | --- |
| `host` | 3539 |

## host (3539 fields)

| Field | Type | Description |
| --- | --- | --- |
| `host` | object |  |
| `host.service_count` | integer |  |
| `host.reputation` | object |  |
| `host.reputation.evidence` | nested |  |
| `host.reputation.evidence.additional_fields` | nested |  |
| `host.reputation.evidence.additional_fields.field` | text |  |
| `host.reputation.evidence.additional_fields.value` | text |  |
| `host.reputation.evidence.category` | text |  |
| `host.reputation.evidence.evidence_score` | float |  |
| `host.reputation.evidence.external_signals` | nested |  |
| `host.reputation.evidence.external_signals.description` | text |  |
| `host.reputation.evidence.external_signals.source` | text |  |
| `host.reputation.evidence.external_signals.tlp` | keyword |  |
| `host.reputation.evidence.threats` | nested |  |
| `host.reputation.evidence.threats.threat_types` | text |  |
| `host.reputation.evidence.threats.last_observed_time` | date |  |
| `host.reputation.evidence.threats.threat_id` | text |  |
| `host.reputation.model_version` | text |  |
| `host.reputation.score` | float |  |
| `host.reputation.score_level` | keyword |  |
| `host.greynoise` | object |  |
| `host.greynoise.tags` | nested | The tags associated with the IP address. |
| `host.greynoise.tags.name` | text | The name of the tag. |
| `host.greynoise.actor` | text | The actor that was observed. |
| `host.greynoise.classification` | text | The classification of the IP address. |
| `host.greynoise.last_observed_time` | date | The last time the IP address was observed. |
| `host.ip` | ip |  |
| `host.network` | nested | Information about what type of network the host belongs to. |
| `host.network.satellite` | boolean | Whether the host belongs to a statellite network. |
| `host.network.source` | text | The source of the data. |
| `host.network.hosting` | boolean | Whether the host belongs to an Internet hosting service provider. |
| `host.network.mobile` | boolean | Whether the host belongs to a mobile network. |
| `host.network.mobile_info` | object | Information about the mobile network the host belongs to, if any. |
| `host.network.mobile_info.carrier_name` | text | The name of the mobile carrier. |
| `host.network.mobile_info.mcc` | text | The Mobile Country Code, identifying the country of the mobile network. |
| `host.network.mobile_info.mnc` | text | The Mobile Network Code, identifying the specific carrier network. |
| `host.privacy` | nested | Information about privacy services used by the IP, such as VPNs, Proxies, or Tor. |
| `host.privacy.tor_info` | object | Information about the Tor exit node, if the host is one. |
| `host.privacy.tor_info.relays` | nested |  |
| `host.privacy.tor_info.relays.fingerprint` | text | Relay fingerprint consisting of 40 upper-case hexadecimal characters. |
| `host.privacy.tor_info.relays.bandwidth_rate` | long | Average bandwidth in bytes per second that this relay is willing to sustain over long periods. |
| `host.privacy.tor_info.relays.exit_probability` | double | Probability of this relay to be selected for the exit position, calculated based on consensus weights, relay flags, and bandwidth weights. |
| `host.privacy.tor_info.relays.consensus_weight_fraction` | double | Fraction of this relay's consensus weight compared to the sum of all consensus weights in the network. A rough approximation of the probability of this relay to be selected by clients. |
| `host.privacy.tor_info.relays.platform` | text | Platform string containing operating system and Tor version details. |
| `host.privacy.tor_info.relays.indirect_family` | text | Fingerprints of relays reachable by following effective, mutual family relationships starting at this relay, but not directly in a mutual family relationship. |
| `host.privacy.tor_info.relays.middle_probability` | double | Probability of this relay to be selected for the middle position, calculated based on consensus weights, relay flags, and bandwidth weights. |
| `host.privacy.tor_info.relays.bridge` | boolean | Whether this entry represents a bridge rather than a relay. |
| `host.privacy.tor_info.relays.contact` | text | Contact address of the relay operator. |
| `host.privacy.tor_info.relays.exit_policy` | text | Array of exit-policy lines from the relay's router descriptor. |
| `host.privacy.tor_info.relays.version` | text | Tor software version without leading 'Tor' as reported by the directory authorities. |
| `host.privacy.tor_info.relays.overload_general_timestamp` | long | Timestamp indicating when the relay reached an overloaded state (e.g., OOM invocation, ntor onionskins dropped, or TCP port exhaustion). |
| `host.privacy.tor_info.relays.nickname` | text | Relay nickname consisting of 1-19 alphanumerical characters. |
| `host.privacy.tor_info.relays.transports` | text | Pluggable transport names supported by this bridge. |
| `host.privacy.tor_info.relays.measured` | boolean | Whether the consensus weight of this relay is based on a threshold of 3 or more measurements by Tor bandwidth authorities. |
| `host.privacy.tor_info.relays.or_addresses` | text | IPv4 or IPv6 addresses and TCP ports where the relay accepts onion-routing connections. The first address is the primary onion-routing address. |
| `host.privacy.tor_info.relays.bandwidth_burst` | long | Bandwidth in bytes per second that this relay is willing to sustain in very short intervals. |
| `host.privacy.tor_info.relays.exit_policy_v6_summary` | object | Summary of the relay's IPv6 exit policy containing accepted or rejected TCP ports/port ranges for most IP addresses. |
| `host.privacy.tor_info.relays.exit_policy_v6_summary.accept` | text | TCP ports or port ranges that the relay accepts for most IP addresses. |
| `host.privacy.tor_info.relays.exit_policy_v6_summary.reject` | text | TCP ports or port ranges that the relay rejects for most IP addresses. |
| `host.privacy.tor_info.relays.blocklist` | text | Country codes where this bridge is not served because it is believed to be blocked. |
| `host.privacy.tor_info.relays.recommended_version` | boolean | Whether the Tor software version of this relay is recommended by the directory authorities. |
| `host.privacy.tor_info.relays.observed_bandwidth` | long | Bandwidth estimate in bytes per second of the capacity this relay can handle. The lesser of the maximum sustained output and input over any ten second period in the past day. |
| `host.privacy.tor_info.relays.advertised_bandwidth` | long | Bandwidth in bytes per second that this relay is willing and capable to provide. The minimum of bandwidth_rate, bandwidth_burst, and observed_bandwidth. |
| `host.privacy.tor_info.relays.exit_policy_summary` | object | Summary of the relay's exit policy containing accepted or rejected TCP ports/port ranges for most IP addresses. |
| `host.privacy.tor_info.relays.exit_policy_summary.accept` | text | TCP ports or port ranges that the relay accepts for most IP addresses. |
| `host.privacy.tor_info.relays.exit_policy_summary.reject` | text | TCP ports or port ranges that the relay rejects for most IP addresses. |
| `host.privacy.tor_info.relays.hashed_fingerprint` | text | SHA-1 hash of the bridge fingerprint consisting of 40 upper-case hexadecimal characters. |
| `host.privacy.tor_info.relays.version_status` | text | Status of the Tor software version: recommended, experimental, obsolete, new in series, or unrecommended. |
| `host.privacy.tor_info.relays.guard_probability` | double | Probability of this relay to be selected for the guard position, calculated based on consensus weights, relay flags, and bandwidth weights. |
| `host.privacy.tor_info.relays.dir_address` | text | IPv4 address and TCP port where the relay accepts directory connections. |
| `host.privacy.tor_info.relays.bridgedb_distributor` | text | BridgeDB distributor that this bridge is currently assigned to. |
| `host.privacy.tor_info.relays.consensus_weight` | long | Weight assigned to this relay by the directory authorities that clients use in their path selection algorithm. |
| `host.privacy.tor_info.relays.unreachable_or_addresses` | text | IPv4 or IPv6 addresses and TCP ports where the relay claims to accept onion-routing connections but that the directory authorities failed to confirm as reachable. |
| `host.privacy.tor_info.relays.flags` | text | Relay flags assigned by the directory authorities. |
| `host.privacy.tor_info.relays.alleged_family` | text | Fingerprints of relays that are part of this relay's family but do not consider this relay to be part of their family. |
| `host.privacy.tor_info.relays.exit_addresses` | text | IPv4 addresses that the relay used to exit to the Internet in the past 24 hours. |
| `host.privacy.tor_info.relays.effective_family` | text | Fingerprints of relays in an effective, mutual family relationship with this relay. Always contains the relay's own fingerprint. |
| `host.privacy.vpn` | boolean | Whether the host is a VPN service exit node IP address. |
| `host.privacy.anonymous` | boolean | Whether the host uses any kind of privacy service. |
| `host.privacy.proxy` | boolean | Whether the host is an open web proxy. |
| `host.privacy.relay` | boolean | Whether the host is a location-preserving anonymous relay service, like iCloud Private Relay.. |
| `host.privacy.service_provider` | text | The name of the privacy service providers detected. |
| `host.privacy.source` | text | The source of the data. |
| `host.privacy.tor` | boolean | Whether the host is a Tor exit node. |
| `host.whois` | object |  |
| `host.whois.organization` | object |  |
| `host.whois.organization.abuse_contacts` | object |  |
| `host.whois.organization.abuse_contacts.handle` | text |  |
| `host.whois.organization.abuse_contacts.name` | text |  |
| `host.whois.organization.abuse_contacts.email` | text |  |
| `host.whois.organization.handle` | text |  |
| `host.whois.organization.city` | text |  |
| `host.whois.organization.country` | text |  |
| `host.whois.organization.address` | text |  |
| `host.whois.organization.tech_contacts` | object |  |
| `host.whois.organization.tech_contacts.email` | text |  |
| `host.whois.organization.tech_contacts.handle` | text |  |
| `host.whois.organization.tech_contacts.name` | text |  |
| `host.whois.organization.name` | text |  |
| `host.whois.organization.state` | text |  |
| `host.whois.organization.street` | text |  |
| `host.whois.organization.postal_code` | text |  |
| `host.whois.organization.admin_contacts` | object |  |
| `host.whois.organization.admin_contacts.name` | text |  |
| `host.whois.organization.admin_contacts.email` | text |  |
| `host.whois.organization.admin_contacts.handle` | text |  |
| `host.whois.network` | object |  |
| `host.whois.network.allocation_type` | text |  |
| `host.whois.network.cidrs` | ip_range | A set of CIDRs describing the range. |
| `host.whois.network.created` | date |  |
| `host.whois.network.handle` | text |  |
| `host.whois.network.name` | text |  |
| `host.whois.network.updated` | date |  |
| `host.services.hardware` | nested |  |
| `host.services.hardware.cpe` | text |  |
| `host.services.hardware.edition` | text |  |
| `host.services.hardware.evidence` | nested |  |
| `host.services.hardware.evidence.found_value` | text |  |
| `host.services.hardware.evidence.literal_match` | text |  |
| `host.services.hardware.evidence.negative` | boolean |  |
| `host.services.hardware.evidence.proprietary` | boolean |  |
| `host.services.hardware.evidence.regex` | text |  |
| `host.services.hardware.evidence.semver_expression` | text |  |
| `host.services.hardware.evidence.data_path` | text |  |
| `host.services.hardware.evidence.exists` | boolean |  |
| `host.services.hardware.version` | text |  |
| `host.services.hardware.life_cycle` | object |  |
| `host.services.hardware.life_cycle.end_of_life` | boolean |  |
| `host.services.hardware.life_cycle.end_of_life_date` | date |  |
| `host.services.hardware.life_cycle.release_date` | date |  |
| `host.services.hardware.product` | text |  |
| `host.services.hardware.components` | object |  |
| `host.services.hardware.components.part` | text |  |
| `host.services.hardware.components.product` | text |  |
| `host.services.hardware.components.update` | text |  |
| `host.services.hardware.components.vendor` | text |  |
| `host.services.hardware.components.version` | text |  |
| `host.services.hardware.components.cpe` | text |  |
| `host.services.hardware.components.edition` | text |  |
| `host.services.hardware.components.life_cycle` | object |  |
| `host.services.hardware.components.life_cycle.end_of_life` | boolean |  |
| `host.services.hardware.components.life_cycle.end_of_life_date` | date |  |
| `host.services.hardware.components.life_cycle.release_date` | date |  |
| `host.services.hardware.part` | text |  |
| `host.services.hardware.source` | keyword |  |
| `host.services.hardware.type` | text |  |
| `host.services.hardware.update` | text |  |
| `host.services.hardware.confidence` | double |  |
| `host.services.hardware.vendor` | text |  |
| `host.hardware` | object |  |
| `host.hardware.components` | object |  |
| `host.hardware.components.product` | text |  |
| `host.hardware.components.update` | text |  |
| `host.hardware.components.vendor` | text |  |
| `host.hardware.components.version` | text |  |
| `host.hardware.components.cpe` | text |  |
| `host.hardware.components.edition` | text |  |
| `host.hardware.components.life_cycle` | object |  |
| `host.hardware.components.life_cycle.release_date` | date |  |
| `host.hardware.components.life_cycle.end_of_life` | boolean |  |
| `host.hardware.components.life_cycle.end_of_life_date` | date |  |
| `host.hardware.components.part` | text |  |
| `host.hardware.cpe` | text |  |
| `host.hardware.evidence` | nested |  |
| `host.hardware.evidence.regex` | text |  |
| `host.hardware.evidence.semver_expression` | text |  |
| `host.hardware.evidence.data_path` | text |  |
| `host.hardware.evidence.exists` | boolean |  |
| `host.hardware.evidence.found_value` | text |  |
| `host.hardware.evidence.literal_match` | text |  |
| `host.hardware.evidence.negative` | boolean |  |
| `host.hardware.evidence.proprietary` | boolean |  |
| `host.hardware.vendor` | text |  |
| `host.hardware.edition` | text |  |
| `host.hardware.part` | text |  |
| `host.hardware.type` | text |  |
| `host.hardware.update` | text |  |
| `host.hardware.version` | text |  |
| `host.hardware.confidence` | double |  |
| `host.hardware.product` | text |  |
| `host.hardware.source` | keyword |  |
| `host.hardware.life_cycle` | object |  |
| `host.hardware.life_cycle.end_of_life_date` | date |  |
| `host.hardware.life_cycle.release_date` | date |  |
| `host.hardware.life_cycle.end_of_life` | boolean |  |
| `host.services.software` | nested |  |
| `host.services.software.edition` | text |  |
| `host.services.software.source` | keyword |  |
| `host.services.software.update` | text |  |
| `host.services.software.cpe` | text |  |
| `host.services.software.type` | text |  |
| `host.services.software.evidence` | nested |  |
| `host.services.software.evidence.semver_expression` | text |  |
| `host.services.software.evidence.data_path` | text |  |
| `host.services.software.evidence.exists` | boolean |  |
| `host.services.software.evidence.found_value` | text |  |
| `host.services.software.evidence.literal_match` | text |  |
| `host.services.software.evidence.negative` | boolean |  |
| `host.services.software.evidence.proprietary` | boolean |  |
| `host.services.software.evidence.regex` | text |  |
| `host.services.software.version` | text |  |
| `host.services.software.components` | object |  |
| `host.services.software.components.product` | text |  |
| `host.services.software.components.update` | text |  |
| `host.services.software.components.vendor` | text |  |
| `host.services.software.components.version` | text |  |
| `host.services.software.components.cpe` | text |  |
| `host.services.software.components.edition` | text |  |
| `host.services.software.components.life_cycle` | object |  |
| `host.services.software.components.life_cycle.release_date` | date |  |
| `host.services.software.components.life_cycle.end_of_life` | boolean |  |
| `host.services.software.components.life_cycle.end_of_life_date` | date |  |
| `host.services.software.components.part` | text |  |
| `host.services.software.vendor` | text |  |
| `host.services.software.confidence` | double |  |
| `host.services.software.product` | text |  |
| `host.services.software.life_cycle` | object |  |
| `host.services.software.life_cycle.end_of_life` | boolean |  |
| `host.services.software.life_cycle.end_of_life_date` | date |  |
| `host.services.software.life_cycle.release_date` | date |  |
| `host.services.software.part` | text |  |
| `host.operating_system` | object |  |
| `host.operating_system.version` | text |  |
| `host.operating_system.vendor` | text |  |
| `host.operating_system.components` | object |  |
| `host.operating_system.components.version` | text |  |
| `host.operating_system.components.cpe` | text |  |
| `host.operating_system.components.edition` | text |  |
| `host.operating_system.components.life_cycle` | object |  |
| `host.operating_system.components.life_cycle.end_of_life_date` | date |  |
| `host.operating_system.components.life_cycle.release_date` | date |  |
| `host.operating_system.components.life_cycle.end_of_life` | boolean |  |
| `host.operating_system.components.part` | text |  |
| `host.operating_system.components.product` | text |  |
| `host.operating_system.components.update` | text |  |
| `host.operating_system.components.vendor` | text |  |
| `host.operating_system.evidence` | nested |  |
| `host.operating_system.evidence.data_path` | text |  |
| `host.operating_system.evidence.exists` | boolean |  |
| `host.operating_system.evidence.found_value` | text |  |
| `host.operating_system.evidence.literal_match` | text |  |
| `host.operating_system.evidence.negative` | boolean |  |
| `host.operating_system.evidence.proprietary` | boolean |  |
| `host.operating_system.evidence.regex` | text |  |
| `host.operating_system.evidence.semver_expression` | text |  |
| `host.operating_system.part` | text |  |
| `host.operating_system.confidence` | double |  |
| `host.operating_system.cpe` | text |  |
| `host.operating_system.edition` | text |  |
| `host.operating_system.life_cycle` | object |  |
| `host.operating_system.life_cycle.end_of_life` | boolean |  |
| `host.operating_system.life_cycle.end_of_life_date` | date |  |
| `host.operating_system.life_cycle.release_date` | date |  |
| `host.operating_system.product` | text |  |
| `host.operating_system.source` | keyword |  |
| `host.operating_system.type` | text |  |
| `host.operating_system.update` | text |  |
| `host.labels` | object |  |
| `host.labels.value` | text |  |
| `host.labels.confidence` | double |  |
| `host.labels.evidence` | nested |  |
| `host.labels.evidence.found_value` | text |  |
| `host.labels.evidence.literal_match` | text |  |
| `host.labels.evidence.negative` | boolean |  |
| `host.labels.evidence.proprietary` | boolean |  |
| `host.labels.evidence.regex` | text |  |
| `host.labels.evidence.semver_expression` | text |  |
| `host.labels.evidence.data_path` | text |  |
| `host.labels.evidence.exists` | boolean |  |
| `host.labels.source` | keyword |  |
| `host.dns` | object |  |
| `host.dns.forward_dns` | object |  |
| `host.dns.forward_dns.key` | text |  |
| `host.dns.forward_dns.value` | object |  |
| `host.dns.forward_dns.value.name` | text |  |
| `host.dns.forward_dns.value.record_type` | keyword |  |
| `host.dns.forward_dns.value.resolve_time` | date |  |
| `host.dns.forward_dns.value.server` | text |  |
| `host.dns.names` | text |  |
| `host.dns.reverse_dns` | object |  |
| `host.dns.reverse_dns.server` | text |  |
| `host.dns.reverse_dns.names` | text |  |
| `host.dns.reverse_dns.resolve_time` | date |  |
| `host.services` | nested |  |
| `host.services.cisco_ipsla` | object |  |
| `host.services.cisco_ipsla.handshake` | object |  |
| `host.services.cisco_ipsla.handshake.message` | object |  |
| `host.services.cisco_ipsla.handshake.message.type` | unsigned_long |  |
| `host.services.cisco_ipsla.handshake.message.ip` | text |  |
| `host.services.cisco_ipsla.handshake.message.length` | unsigned_long |  |
| `host.services.cisco_ipsla.handshake.message.port` | unsigned_long |  |
| `host.services.cisco_ipsla.handshake.header` | object |  |
| `host.services.cisco_ipsla.handshake.header.length` | unsigned_long |  |
| `host.services.cisco_ipsla.handshake.header.seq` | unsigned_long |  |
| `host.services.cisco_ipsla.handshake.header.unknown` | unsigned_long |  |
| `host.services.cisco_ipsla.handshake.header.version` | unsigned_long |  |
| `host.services.cisco_ipsla.measure_response` | object |  |
| `host.services.cisco_ipsla.measure_response.send_seq` | unsigned_long |  |
| `host.services.cisco_ipsla.measure_response.send_time` | unsigned_long |  |
| `host.services.cisco_ipsla.measure_response.type` | unsigned_long |  |
| `host.services.cisco_ipsla.measure_response.flags` | unsigned_long |  |
| `host.services.cisco_ipsla.measure_response.payload` | text |  |
| `host.services.cisco_ipsla.measure_response.receive_seq` | unsigned_long |  |
| `host.services.cisco_ipsla.measure_response.receive_time` | unsigned_long |  |
| `host.services.syncthing_bep` | object |  |
| `host.services.syncthing_bep.device_name` | text |  |
| `host.services.syncthing_bep.num_connections` | integer |  |
| `host.services.syncthing_bep.server_name` | text |  |
| `host.services.syncthing_bep.timestamp` | long |  |
| `host.services.syncthing_bep.version` | text |  |
| `host.services.pgbouncer` | object |  |
| `host.services.pgbouncer.startup_capabilities` | object |  |
| `host.services.pgbouncer.startup_capabilities.v4` | boolean |  |
| `host.services.pgbouncer.startup_capabilities.v2` | boolean |  |
| `host.services.pgbouncer.startup_capabilities.v3` | boolean |  |
| `host.services.krpc` | object |  |
| `host.services.krpc.ping_response_id` | text |  |
| `host.services.melsec` | object |  |
| `host.services.melsec.cpu_info` | text |  |
| `host.services.iscsi` | object |  |
| `host.services.iscsi.connection` | object |  |
| `host.services.iscsi.connection.cmd_seq` | unsigned_long |  |
| `host.services.iscsi.connection.status_seq` | unsigned_long |  |
| `host.services.iscsi.connection.version_active` | unsigned_long |  |
| `host.services.iscsi.connection.version_max` | unsigned_long |  |
| `host.services.iscsi.connection.isid` | unsigned_long |  |
| `host.services.iscsi.connection.ahs_length` | unsigned_long |  |
| `host.services.iscsi.connection.keyval_pairs` | text |  |
| `host.services.iscsi.connection.max_new_cmds` | unsigned_long |  |
| `host.services.iscsi.connection.tsih` | unsigned_long |  |
| `host.services.iscsi.errors` | text |  |
| `host.services.iscsi.targets` | object |  |
| `host.services.iscsi.targets.errors` | text |  |
| `host.services.iscsi.targets.name` | text |  |
| `host.services.iscsi.targets.private_portals` | text |  |
| `host.services.iscsi.targets.public_portals` | text |  |
| `host.services.iscsi.targets.alias` | text |  |
| `host.services.iscsi.targets.auths` | text |  |
| `host.services.iscsi.targets.dns_portals` | text |  |
| `host.services.kcodes_netusb` | object |  |
| `host.services.kcodes_netusb.device_id` | text |  |
| `host.services.kcodes_netusb.session_id` | text |  |
| `host.services.kcodes_netusb.version` | text |  |
| `host.services.kcodes_netusb.capabilities` | text |  |
| `host.services.denon_heos` | object |  |
| `host.services.denon_heos.mac_address` | text |  |
| `host.services.etcd` | object |  |
| `host.services.etcd.version` | object |  |
| `host.services.etcd.version.cluster` | text |  |
| `host.services.etcd.version.server` | text |  |
| `host.services.etcd.v2` | object |  |
| `host.services.etcd.v2.total_keys` | unsigned_long |  |
| `host.services.etcd.v2.auth` | object |  |
| `host.services.etcd.v2.auth.enabled` | boolean |  |
| `host.services.etcd.v2.members` | object |  |
| `host.services.etcd.v2.members.peer_urls` | text |  |
| `host.services.etcd.v2.members.client_urls` | text |  |
| `host.services.etcd.v2.members.id` | text |  |
| `host.services.etcd.v2.members.name` | text |  |
| `host.services.etcd.v3` | object |  |
| `host.services.etcd.v3.auth` | object |  |
| `host.services.etcd.v3.auth.enabled` | boolean |  |
| `host.services.etcd.v3.members` | object |  |
| `host.services.etcd.v3.members.client_urls` | text |  |
| `host.services.etcd.v3.members.id` | text |  |
| `host.services.etcd.v3.members.name` | text |  |
| `host.services.etcd.v3.members.peer_urls` | text |  |
| `host.services.etcd.v3.total_keys` | unsigned_long |  |
| `host.services.tibia` | object |  |
| `host.services.tibia.location` | text |  |
| `host.services.tibia.login_ip` | text |  |
| `host.services.tibia.login_port` | text |  |
| `host.services.tibia.name` | text |  |
| `host.services.tibia.server` | text |  |
| `host.services.tibia.url` | text |  |
| `host.services.tibia.version` | text |  |
| `host.services.tibia.client_version` | text |  |
| `host.services.scan_time` | date |  |
| `host.services.qdrant_grpc` | object |  |
| `host.services.qdrant_grpc.version` | text |  |
| `host.services.qdrant_grpc.commit` | text |  |
| `host.services.labels` | nested |  |
| `host.services.labels.confidence` | double |  |
| `host.services.labels.evidence` | nested |  |
| `host.services.labels.evidence.semver_expression` | text |  |
| `host.services.labels.evidence.data_path` | text |  |
| `host.services.labels.evidence.exists` | boolean |  |
| `host.services.labels.evidence.found_value` | text |  |
| `host.services.labels.evidence.literal_match` | text |  |
| `host.services.labels.evidence.negative` | boolean |  |
| `host.services.labels.evidence.proprietary` | boolean |  |
| `host.services.labels.evidence.regex` | text |  |
| `host.services.labels.source` | keyword |  |
| `host.services.labels.value` | text |  |
| `host.services.nfs_mountd` | object |  |
| `host.services.nfs_mountd.export_lists` | object |  |
| `host.services.nfs_mountd.export_lists.groups` | text |  |
| `host.services.nfs_mountd.export_lists.directory` | text |  |
| `host.services.protocol` | text |  |
| `host.services.anerma_cf_forth` | object |  |
| `host.services.anerma_cf_forth.serial_number` | text |  |
| `host.services.anerma_cf_forth.unit_name` | text |  |
| `host.services.anerma_cf_forth.version` | text |  |
| `host.services.anerma_cf_forth.ip` | ip |  |
| `host.services.anerma_cf_forth.product` | text |  |
| `host.services.mavlink` | object |  |
| `host.services.mavlink.frames` | nested |  |
| `host.services.mavlink.frames.message_type` | text |  |
| `host.services.mavlink.frames.payload` | text |  |
| `host.services.mavlink.frames.system_id` | unsigned_long |  |
| `host.services.mavlink.frames.version` | unsigned_long |  |
| `host.services.mavlink.frames.component_id` | unsigned_long |  |
| `host.services.mavlink.frames.message_id` | unsigned_long |  |
| `host.services.mavlink.saw_pong` | boolean |  |
| `host.services.ripple` | object |  |
| `host.services.ripple.ripple_clio` | object |  |
| `host.services.ripple.ripple_clio.clio_version` | text |  |
| `host.services.ripple.ripple_clio.rippled_version` | text |  |
| `host.services.ripple.ripple_clio.validated` | boolean |  |
| `host.services.ripple.ripple_clio.validation_quorum` | long |  |
| `host.services.ripple.rippled_peer` | object |  |
| `host.services.ripple.rippled_peer.peer_crawler_response_version` | long |  |
| `host.services.ripple.rippled_peer.peers` | object |  |
| `host.services.ripple.rippled_peer.peers.public_key` | text |  |
| `host.services.ripple.rippled_peer.peers.type` | text |  |
| `host.services.ripple.rippled_peer.peers.version` | text |  |
| `host.services.ripple.rippled_peer.peers.ip` | text |  |
| `host.services.ripple.rippled_peer.peers.port` | long |  |
| `host.services.ripple.rippled_peer.pubkey_node` | text |  |
| `host.services.ripple.rippled_peer.publisher_list` | text |  |
| `host.services.ripple.rippled_peer.server_state` | text |  |
| `host.services.ripple.rippled_peer.validator_sites` | text |  |
| `host.services.ripple.rippled_peer.build_version` | text |  |
| `host.services.ripple.rippled_public` | object |  |
| `host.services.ripple.rippled_public.validation_quorum` | long |  |
| `host.services.ripple.rippled_public.build_version` | text |  |
| `host.services.ripple.rippled_public.hostid` | text |  |
| `host.services.ripple.rippled_public.network_id` | long |  |
| `host.services.ripple.rippled_public.peers` | long |  |
| `host.services.ripple.rippled_public.ports` | object |  |
| `host.services.ripple.rippled_public.ports.protocol` | text |  |
| `host.services.ripple.rippled_public.ports.port` | text |  |
| `host.services.ripple.rippled_public.pubkey_node` | text |  |
| `host.services.ripple.rippled_public.server_state` | text |  |
| `host.services.memberlist` | object |  |
| `host.services.memberlist.node` | object |  |
| `host.services.memberlist.node.port` | unsigned_long |  |
| `host.services.memberlist.node.protocol_version` | unsigned_long |  |
| `host.services.memberlist.node.delegate_versions` | unsigned_long |  |
| `host.services.memberlist.node.incarnation` | unsigned_long |  |
| `host.services.memberlist.node.ip` | ip |  |
| `host.services.memberlist.node.meta` | text |  |
| `host.services.memberlist.node.name` | text |  |
| `host.services.memberlist.encrypted` | boolean |  |
| `host.services.memberlist.encrypted_len` | unsigned_long |  |
| `host.services.memberlist.encryption_version` | unsigned_long |  |
| `host.services.memberlist.error_message` | text |  |
| `host.services.endpoints` | nested |  |
| `host.services.endpoints.path` | text |  |
| `host.services.endpoints.prometheus_target` | object |  |
| `host.services.endpoints.prometheus_target.metric_families` | object |  |
| `host.services.endpoints.prometheus_target.metric_families.help` | text |  |
| `host.services.endpoints.prometheus_target.metric_families.name` | text |  |
| `host.services.endpoints.jenkins` | object |  |
| `host.services.endpoints.jenkins.mode` | text |  |
| `host.services.endpoints.jenkins.node_description` | text |  |
| `host.services.endpoints.jenkins.node_name` | text |  |
| `host.services.endpoints.jenkins.slave_agent_port` | integer |  |
| `host.services.endpoints.jenkins.use_security` | boolean |  |
| `host.services.endpoints.jenkins.assigned_labels` | nested |  |
| `host.services.endpoints.jenkins.assigned_labels.name` | text |  |
| `host.services.endpoints.jenkins.assigned_labels.value` | text |  |
| `host.services.endpoints.jenkins.jobs` | nested |  |
| `host.services.endpoints.jenkins.jobs.description` | text |  |
| `host.services.endpoints.jenkins.jobs.last_build` | object |  |
| `host.services.endpoints.jenkins.jobs.last_build.duration_seconds` | long |  |
| `host.services.endpoints.jenkins.jobs.last_build.number` | long |  |
| `host.services.endpoints.jenkins.jobs.last_build.result` | text |  |
| `host.services.endpoints.jenkins.jobs.last_build.timestamp` | long |  |
| `host.services.endpoints.jenkins.jobs.last_build.url` | text |  |
| `host.services.endpoints.jenkins.jobs.name` | text |  |
| `host.services.endpoints.jenkins.jobs.url` | text |  |
| `host.services.endpoints.transport_protocol` | keyword |  |
| `host.services.endpoints.redlion_web` | object |  |
| `host.services.endpoints.redlion_web.log_names` | text |  |
| `host.services.endpoints.redlion_web.title` | text |  |
| `host.services.endpoints.redlion_web.enhanced_web_server` | boolean |  |
| `host.services.endpoints.graphql` | object |  |
| `host.services.endpoints.graphql.response` | text |  |
| `host.services.endpoints.graphql.supports_introspection` | boolean |  |
| `host.services.endpoints.scan_time` | date |  |
| `host.services.endpoints.ollama` | object |  |
| `host.services.endpoints.ollama.version` | text |  |
| `host.services.endpoints.ollama.models` | nested |  |
| `host.services.endpoints.ollama.models.size_vram` | unsigned_long |  |
| `host.services.endpoints.ollama.models.digest` | text |  |
| `host.services.endpoints.ollama.models.expires_at` | text |  |
| `host.services.endpoints.ollama.models.family` | text |  |
| `host.services.endpoints.ollama.models.model` | text |  |
| `host.services.endpoints.ollama.models.name` | text |  |
| `host.services.endpoints.ollama.models.parent_model` | text |  |
| `host.services.endpoints.ollama.models.size` | unsigned_long |  |
| `host.services.endpoints.ollama.running_models` | nested |  |
| `host.services.endpoints.ollama.running_models.size` | unsigned_long |  |
| `host.services.endpoints.ollama.running_models.size_vram` | unsigned_long |  |
| `host.services.endpoints.ollama.running_models.digest` | text |  |
| `host.services.endpoints.ollama.running_models.expires_at` | text |  |
| `host.services.endpoints.ollama.running_models.family` | text |  |
| `host.services.endpoints.ollama.running_models.model` | text |  |
| `host.services.endpoints.ollama.running_models.name` | text |  |
| `host.services.endpoints.ollama.running_models.parent_model` | text |  |
| `host.services.endpoints.open_directory` | object |  |
| `host.services.endpoints.open_directory.recursive` | boolean |  |
| `host.services.endpoints.open_directory.files` | nested |  |
| `host.services.endpoints.open_directory.files.extension` | text |  |
| `host.services.endpoints.open_directory.files.last_modified` | date |  |
| `host.services.endpoints.open_directory.files.name` | text |  |
| `host.services.endpoints.open_directory.files.path` | text |  |
| `host.services.endpoints.open_directory.files.size` | long |  |
| `host.services.endpoints.open_directory.files.suspicious_score` | double |  |
| `host.services.endpoints.open_directory.files.type` | text |  |
| `host.services.endpoints.banner_hash_sha256` | text |  |
| `host.services.endpoints.influxdb` | object |  |
| `host.services.endpoints.influxdb.build` | text |  |
| `host.services.endpoints.influxdb.setup_allowed` | boolean |  |
| `host.services.endpoints.influxdb.version` | text |  |
| `host.services.endpoints.endpoint_type` | text |  |
| `host.services.endpoints.mcp` | object |  |
| `host.services.endpoints.mcp.server_name` | text |  |
| `host.services.endpoints.mcp.server_version` | text |  |
| `host.services.endpoints.mcp.tools` | nested |  |
| `host.services.endpoints.mcp.tools.name` | text |  |
| `host.services.endpoints.mcp.tools.description` | text |  |
| `host.services.endpoints.mcp.prompts` | nested |  |
| `host.services.endpoints.mcp.prompts.name` | text |  |
| `host.services.endpoints.mcp.protocol_version` | text |  |
| `host.services.endpoints.mcp.resources` | nested |  |
| `host.services.endpoints.mcp.resources.mime_type` | text |  |
| `host.services.endpoints.mcp.resources.name` | text |  |
| `host.services.endpoints.mcp.resources.uri` | text |  |
| `host.services.endpoints.mcp.resources.content` | text |  |
| `host.services.endpoints.mcp.resources.description` | text |  |
| `host.services.endpoints.proxmox_ve` | object |  |
| `host.services.endpoints.proxmox_ve.api_daemon_version` | text |  |
| `host.services.endpoints.proxmox_ve.realms` | nested |  |
| `host.services.endpoints.proxmox_ve.realms.tfa` | text |  |
| `host.services.endpoints.proxmox_ve.realms.type` | text |  |
| `host.services.endpoints.proxmox_ve.realms.comment` | text |  |
| `host.services.endpoints.proxmox_ve.realms.realm` | text |  |
| `host.services.endpoints.keycloak` | object |  |
| `host.services.endpoints.keycloak.token_service` | text |  |
| `host.services.endpoints.keycloak.grant_types_supported` | text |  |
| `host.services.endpoints.keycloak.id_token_signing_alg_values_supported` | text |  |
| `host.services.endpoints.keycloak.public_key` | text |  |
| `host.services.endpoints.keycloak.realm_base_path` | text |  |
| `host.services.endpoints.synology_dsm` | object |  |
| `host.services.endpoints.synology_dsm.apis` | text |  |
| `host.services.endpoints.extracted` | object |  |
| `host.services.endpoints.extracted.copyrights` | nested |  |
| `host.services.endpoints.extracted.copyrights.start_year` | integer |  |
| `host.services.endpoints.extracted.copyrights.text` | text |  |
| `host.services.endpoints.extracted.copyrights.end_year` | integer |  |
| `host.services.endpoints.extracted.copyrights.holder` | text |  |
| `host.services.endpoints.extracted.ip_addresses` | ip |  |
| `host.services.endpoints.extracted.languages` | text |  |
| `host.services.endpoints.extracted.links` | text |  |
| `host.services.endpoints.extracted.mac_addresses` | text |  |
| `host.services.endpoints.extracted.analytics_services` | nested |  |
| `host.services.endpoints.extracted.analytics_services.ids` | text |  |
| `host.services.endpoints.extracted.analytics_services.provider` | text |  |
| `host.services.endpoints.chrome_devtools` | object |  |
| `host.services.endpoints.chrome_devtools.browser` | text |  |
| `host.services.endpoints.chrome_devtools.protocol_version` | text |  |
| `host.services.endpoints.chrome_devtools.targets` | nested |  |
| `host.services.endpoints.chrome_devtools.targets.title` | text |  |
| `host.services.endpoints.chrome_devtools.targets.type` | text |  |
| `host.services.endpoints.chrome_devtools.targets.url` | text |  |
| `host.services.endpoints.chrome_devtools.user_agent` | text |  |
| `host.services.endpoints.chrome_devtools.v8_version` | text |  |
| `host.services.endpoints.chrome_devtools.webkit_version` | text |  |
| `host.services.endpoints.clickhouse_http` | object |  |
| `host.services.endpoints.clickhouse_http.version` | text |  |
| `host.services.endpoints.clickhouse_http.databases` | text |  |
| `host.services.endpoints.clickhouse_http.databases_exposed` | boolean |  |
| `host.services.endpoints.clickhouse_http.display_name` | text |  |
| `host.services.endpoints.clickhouse_http.error` | object |  |
| `host.services.endpoints.clickhouse_http.error.code` | text |  |
| `host.services.endpoints.clickhouse_http.error.message` | text |  |
| `host.services.endpoints.clickhouse_http.timezone` | text |  |
| `host.services.endpoints.wordpress` | object |  |
| `host.services.endpoints.wordpress.home` | text |  |
| `host.services.endpoints.wordpress.name` | text |  |
| `host.services.endpoints.wordpress.namespaces` | text |  |
| `host.services.endpoints.wordpress.timezone_string` | text |  |
| `host.services.endpoints.wordpress.description` | text |  |
| `host.services.endpoints.wordpress.gmt_offset` | text |  |
| `host.services.endpoints.vault` | object |  |
| `host.services.endpoints.vault.initialized` | boolean |  |
| `host.services.endpoints.vault.license_state` | text |  |
| `host.services.endpoints.vault.sealed` | boolean |  |
| `host.services.endpoints.vault.version` | text |  |
| `host.services.endpoints.vault.cluster_name` | text |  |
| `host.services.endpoints.vault.enterprise` | boolean |  |
| `host.services.endpoints.jupyter` | object |  |
| `host.services.endpoints.jupyter.version` | text |  |
| `host.services.endpoints.prometheus` | object |  |
| `host.services.endpoints.prometheus.response` | object | Information Prometheus captured as well as build information. |
| `host.services.endpoints.prometheus.response.all_versions` | text | List of the versions of everything that Prometheus finds i.e., version of Prometheus, Go, Node, cAdvisor, etc. |
| `host.services.endpoints.prometheus.response.config_exposed` | boolean | True when the config endpoint is exposed. |
| `host.services.endpoints.prometheus.response.dropped_targets` | object | List of dropped targets. |
| `host.services.endpoints.prometheus.response.dropped_targets.metrics_path` | text | Path to metrics of target. |
| `host.services.endpoints.prometheus.response.dropped_targets.scheme` | text | URL scheme. |
| `host.services.endpoints.prometheus.response.dropped_targets.address` | text | Address of target. |
| `host.services.endpoints.prometheus.response.dropped_targets.job` | text | Job of target. |
| `host.services.endpoints.prometheus.response.go_versions` | text | List of the versions of Go. |
| `host.services.endpoints.prometheus.response.prometheus_versions` | object |  |
| `host.services.endpoints.prometheus.response.prometheus_versions.go_version` | text | Version of Go used to build Prometheus. |
| `host.services.endpoints.prometheus.response.prometheus_versions.revision` | text | Revision of Prometheus. |
| `host.services.endpoints.prometheus.response.prometheus_versions.version` | text | Version of Prometheus. |
| `host.services.endpoints.prometheus.response.active_targets` | object | List of active targets. |
| `host.services.endpoints.prometheus.response.active_targets.last_scrape` | text | Last time Prometheus scraped target. |
| `host.services.endpoints.prometheus.response.active_targets.scrape_url` | text | URL that Prometheus scraped. |
| `host.services.endpoints.prometheus.response.active_targets.discovered_labels` | object |  |
| `host.services.endpoints.prometheus.response.active_targets.discovered_labels.address` | text | Address of target. |
| `host.services.endpoints.prometheus.response.active_targets.discovered_labels.job` | text | Job of target. |
| `host.services.endpoints.prometheus.response.active_targets.discovered_labels.metrics_path` | text | Path to metrics of target. |
| `host.services.endpoints.prometheus.response.active_targets.discovered_labels.scheme` | text | URL scheme. |
| `host.services.endpoints.prometheus.response.active_targets.health` | text | Whether target is up or down. |
| `host.services.endpoints.prometheus.response.active_targets.labels` | object |  |
| `host.services.endpoints.prometheus.response.active_targets.labels.instance` | text | Instance after relabelling has occurred. |
| `host.services.endpoints.prometheus.response.active_targets.labels.job` | text | Job of target after relabelling has occurred. |
| `host.services.endpoints.prometheus.response.active_targets.last_error` | text | Last error that occurred within target. |
| `host.services.endpoints.banner` | text |  |
| `host.services.endpoints.plex_media_server` | object |  |
| `host.services.endpoints.plex_media_server.version` | text |  |
| `host.services.endpoints.argocd` | object |  |
| `host.services.endpoints.argocd.version` | text |  |
| `host.services.endpoints.argocd.anonymous_exposure` | object |  |
| `host.services.endpoints.argocd.anonymous_exposure.clusters_anonymously_readable` | boolean |  |
| `host.services.endpoints.argocd.anonymous_exposure.application_count` | integer |  |
| `host.services.endpoints.argocd.anonymous_exposure.applications_anonymously_readable` | boolean |  |
| `host.services.endpoints.argocd.anonymous_exposure.cluster_count` | integer |  |
| `host.services.endpoints.argocd.settings` | object |  |
| `host.services.endpoints.argocd.settings.impersonation_enabled` | boolean |  |
| `host.services.endpoints.argocd.settings.installation_id` | text |  |
| `host.services.endpoints.argocd.settings.oidc_config` | object |  |
| `host.services.endpoints.argocd.settings.oidc_config.client_id` | text |  |
| `host.services.endpoints.argocd.settings.oidc_config.issuer` | text |  |
| `host.services.endpoints.argocd.settings.sync_with_replace_allowed` | boolean |  |
| `host.services.endpoints.argocd.settings.url` | text |  |
| `host.services.endpoints.argocd.settings.user_logins_disabled` | boolean |  |
| `host.services.endpoints.argocd.settings.apps_in_any_namespace_enabled` | boolean |  |
| `host.services.endpoints.argocd.settings.exec_enabled` | boolean |  |
| `host.services.endpoints.screenshots` | nested |  |
| `host.services.endpoints.screenshots.handle` | text |  |
| `host.services.endpoints.screenshots.palsimhash` | text |  |
| `host.services.endpoints.screenshots.phash` | text |  |
| `host.services.endpoints.screenshots.extracted_text` | text |  |
| `host.services.endpoints.port` | unsigned_long |  |
| `host.services.endpoints.scada_view` | object |  |
| `host.services.endpoints.scada_view.description` | text |  |
| `host.services.endpoints.scada_view.title` | text |  |
| `host.services.endpoints.hostname` | text |  |
| `host.services.endpoints.nginx_proxy_manager` | object |  |
| `host.services.endpoints.nginx_proxy_manager.setup` | boolean |  |
| `host.services.endpoints.nginx_proxy_manager.version` | text |  |
| `host.services.endpoints.ivanti_avalanche` | object |  |
| `host.services.endpoints.ivanti_avalanche.body` | text |  |
| `host.services.endpoints.ivanti_avalanche.status_code` | integer |  |
| `host.services.endpoints.ivanti_avalanche.version` | text |  |
| `host.services.endpoints.ip` | ip |  |
| `host.services.ws_discovery` | object |  |
| `host.services.ws_discovery.types` | text |  |
| `host.services.ws_discovery.addresses` | text |  |
| `host.services.ws_discovery.metadata_version` | unsigned_long |  |
| `host.services.ws_discovery.scopes` | text |  |
| `host.services.rustdesk_rendezvous` | object |  |
| `host.services.rustdesk_rendezvous.key_exchange` | object |  |
| `host.services.rustdesk_rendezvous.key_exchange.keys` | text |  |
| `host.services.rustdesk_rendezvous.message_type` | text |  |
| `host.services.rustdesk_rendezvous.test_nat_response` | object |  |
| `host.services.rustdesk_rendezvous.test_nat_response.port` | integer |  |
| `host.services.rustdesk_rendezvous.test_nat_response.config_update` | object |  |
| `host.services.rustdesk_rendezvous.test_nat_response.config_update.rendezvous_servers` | text |  |
| `host.services.rustdesk_rendezvous.test_nat_response.config_update.serial` | integer |  |
| `host.services.giop` | object |  |
| `host.services.giop.version` | text |  |
| `host.services.giop.byte_order` | text |  |
| `host.services.giop.implementation_hints` | text |  |
| `host.services.giop.ior` | object |  |
| `host.services.giop.ior.iiop_profile` | object |  |
| `host.services.giop.ior.iiop_profile.host` | text |  |
| `host.services.giop.ior.iiop_profile.object_key_hex` | text |  |
| `host.services.giop.ior.iiop_profile.port` | unsigned_long |  |
| `host.services.giop.ior.iiop_profile.tagged_components` | nested |  |
| `host.services.giop.ior.iiop_profile.tagged_components.ssl_requires` | text |  |
| `host.services.giop.ior.iiop_profile.tagged_components.ssl_supports` | text |  |
| `host.services.giop.ior.iiop_profile.tagged_components.tag` | unsigned_long |  |
| `host.services.giop.ior.iiop_profile.tagged_components.tag_name` | text |  |
| `host.services.giop.ior.iiop_profile.tagged_components.ssl_port` | unsigned_long |  |
| `host.services.giop.ior.iiop_profile.version` | text |  |
| `host.services.giop.ior.type_id` | text |  |
| `host.services.giop.locate_status` | text |  |
| `host.services.giop.message_type` | text |  |
| `host.services.realport` | object |  |
| `host.services.realport.software_version` | unsigned_long |  |
| `host.services.realport.unpatched_etherlite` | boolean |  |
| `host.services.realport.vpd` | object |  |
| `host.services.realport.vpd.key` | text |  |
| `host.services.realport.vpd.value` | text |  |
| `host.services.realport.hardware_id` | unsigned_long |  |
| `host.services.realport.hardware_version` | unsigned_long |  |
| `host.services.realport.num_ports` | unsigned_long |  |
| `host.services.realport.product_name` | text |  |
| `host.services.compromises` | nested |  |
| `host.services.compromises.evidence` | nested |  |
| `host.services.compromises.evidence.data_path` | text |  |
| `host.services.compromises.evidence.exists` | boolean |  |
| `host.services.compromises.evidence.found_value` | text |  |
| `host.services.compromises.evidence.literal_match` | text |  |
| `host.services.compromises.evidence.negative` | boolean |  |
| `host.services.compromises.evidence.proprietary` | boolean |  |
| `host.services.compromises.evidence.regex` | text |  |
| `host.services.compromises.evidence.semver_expression` | text |  |
| `host.services.compromises.confidence` | double |  |
| `host.services.compromises.severity` | keyword |  |
| `host.services.compromises.id` | text |  |
| `host.services.compromises.year` | unsigned_long |  |
| `host.services.compromises.risk_source` | keyword |  |
| `host.services.compromises.source` | keyword |  |
| `host.services.compromises.metrics` | object |  |
| `host.services.compromises.metrics.cvss_v40` | object |  |
| `host.services.compromises.metrics.cvss_v40.components` | object | These metrics contribute to how a CVE is scored. |
| `host.services.compromises.metrics.cvss_v40.components.safety` | keyword |  |
| `host.services.compromises.metrics.cvss_v40.components.privileges_required` | keyword | Describes the level of privileges or access an attacker must have before successful exploitation. There are three possible values: None (N) – There is no privilege or special access required to conduct the attack, Low (L) – The attacker requires basic, “user” level privileges to leverage the exploit, High (H) – Administrative or similar access privileges are required for successful attack. |
| `host.services.compromises.metrics.cvss_v40.components.provider_urgency` | keyword |  |
| `host.services.compromises.metrics.cvss_v40.components.attack_complexity` | keyword | Indicates conditions beyond the attacker’s control that must exist in order to exploit the vulnerability. The Attack Complexity metric is scored as either Low or High. There are two possible values: Low (L) – There are no specific pre-conditions required for exploitation, High (H) – The attacker must complete some number of preparatory steps in order to get access. |
| `host.services.compromises.metrics.cvss_v40.components.integrity` | keyword | Refers to whether the protected information has been tampered with or changed in any way. If there is no way for an attacker to alter the accuracy or completeness of the information, integrity has been maintained. Integrity has three values: None (N) – There is no loss of the integrity of any information, Low (L) – A limited amount of information might be tampered with or modified, but there is no serious impact on the protected system, High (H) – The attacker can modify any/all information on the target system, resulting in a complete loss of integrity. |
| `host.services.compromises.metrics.cvss_v40.components.user_interaction` | keyword | Describes whether a user, other than the attacker, is required to do anything or participate in exploitation of the vulnerability. User interaction has two possible values: None (N) – No user interaction is required, Required (R) – A user must complete some steps for the exploit to succeed. For example, a user might be required to install some software. |
| `host.services.compromises.metrics.cvss_v40.components.value_density` | keyword |  |
| `host.services.compromises.metrics.cvss_v40.components.automatable` | keyword |  |
| `host.services.compromises.metrics.cvss_v40.components.vulnerability_response_effort` | keyword |  |
| `host.services.compromises.metrics.cvss_v40.components.attack_requirements` | keyword |  |
| `host.services.compromises.metrics.cvss_v40.components.attack_vector` | keyword | Indicates the level of access required for an attacker to exploit the vulnerability. The Attack Vector metric is scored in one of four levels: Network (N) – Vulnerabilities with this rating are remotely exploitable, from one or more hops away, up to, and including, remote exploitation over the Internet, Adjacent (A) – A vulnerability with this rating requires network adjacency for exploitation. The attack must be launched from the same physical or logical network, Local (L) – Vulnerabilities with this rating are not exploitable over a network, Physical (P) – An attacker must physically interact with the target system. |
| `host.services.compromises.metrics.cvss_v40.components.availability` | keyword | If an attack renders information unavailable, such as when a system crashes or through a DDoS attack, availability is negatively impacted. Availability has three possible values: None (N) – There is no loss of availability, Low (L) – Availability might be intermittently limited, or performance might be negatively impacted, as a result of a successful attack, High (H) – There is a complete loss of availability of the impacted system or information. |
| `host.services.compromises.metrics.cvss_v40.components.confidentiality` | keyword | Refers to the disclosure of sensitive information to authorized and unauthorized users, with the goal being that only authorized users are able to access the target data. Confidentiality has three potential values: High (H) – The attacker has full access to all resources in the impacted system, including highly sensitive information such as encryption keys, Low (L) – The attacker has partial access to information, with no control over what, specifically, they are able to access, None (N) – No data is accessible to unauthorized users as a result of the exploit. |
| `host.services.compromises.metrics.cvss_v40.components.recovery` | keyword |  |
| `host.services.compromises.metrics.cvss_v40.score` | double | Score of the vulnerability; 0.1 is the lowest, 10 is the maximum |
| `host.services.compromises.metrics.cvss_v40.vector` | text | The path, method, or scenario used to exploit the vulnerability. Each section represents components that contribute to the overall CVSS score. |
| `host.services.compromises.metrics.epss` | object |  |
| `host.services.compromises.metrics.epss.score` | double |  |
| `host.services.compromises.metrics.epss.percentile` | double |  |
| `host.services.compromises.metrics.cvss_v30` | object |  |
| `host.services.compromises.metrics.cvss_v30.score` | double | Score of the vulnerability; 0.1 is the lowest, 10 is the maximum |
| `host.services.compromises.metrics.cvss_v30.vector` | text | The path, method, or scenario used to exploit the vulnerability. Each section represents components that contribute to the overall CVSS score. |
| `host.services.compromises.metrics.cvss_v30.components` | object | These metrics contribute to how a CVE is scored. |
| `host.services.compromises.metrics.cvss_v30.components.user_interaction` | keyword | Describes whether a user, other than the attacker, is required to do anything or participate in exploitation of the vulnerability. User interaction has two possible values: None (N) – No user interaction is required, Required (R) – A user must complete some steps for the exploit to succeed. For example, a user might be required to install some software. |
| `host.services.compromises.metrics.cvss_v30.components.attack_complexity` | keyword | Indicates conditions beyond the attacker’s control that must exist in order to exploit the vulnerability. The Attack Complexity metric is scored as either Low or High. There are two possible values: Low (L) – There are no specific pre-conditions required for exploitation, High (H) – The attacker must complete some number of preparatory steps in order to get access. |
| `host.services.compromises.metrics.cvss_v30.components.attack_vector` | keyword | Indicates the level of access required for an attacker to exploit the vulnerability. The Attack Vector metric is scored in one of four levels: Network (N) – Vulnerabilities with this rating are remotely exploitable, from one or more hops away, up to, and including, remote exploitation over the Internet, Adjacent (A) – A vulnerability with this rating requires network adjacency for exploitation. The attack must be launched from the same physical or logical network, Local (L) – Vulnerabilities with this rating are not exploitable over a network, Physical (P) – An attacker must physically interact with the target system. |
| `host.services.compromises.metrics.cvss_v30.components.availability` | keyword | If an attack renders information unavailable, such as when a system crashes or through a DDoS attack, availability is negatively impacted. Availability has three possible values: None (N) – There is no loss of availability, Low (L) – Availability might be intermittently limited, or performance might be negatively impacted, as a result of a successful attack, High (H) – There is a complete loss of availability of the impacted system or information. |
| `host.services.compromises.metrics.cvss_v30.components.confidentiality` | keyword | Refers to the disclosure of sensitive information to authorized and unauthorized users, with the goal being that only authorized users are able to access the target data. Confidentiality has three potential values: High (H) – The attacker has full access to all resources in the impacted system, including highly sensitive information such as encryption keys, Low (L) – The attacker has partial access to information, with no control over what, specifically, they are able to access, None (N) – No data is accessible to unauthorized users as a result of the exploit. |
| `host.services.compromises.metrics.cvss_v30.components.integrity` | keyword | Refers to whether the protected information has been tampered with or changed in any way. If there is no way for an attacker to alter the accuracy or completeness of the information, integrity has been maintained. Integrity has three values: None (N) – There is no loss of the integrity of any information, Low (L) – A limited amount of information might be tampered with or modified, but there is no serious impact on the protected system, High (H) – The attacker can modify any/all information on the target system, resulting in a complete loss of integrity. |
| `host.services.compromises.metrics.cvss_v30.components.privileges_required` | keyword | Describes the level of privileges or access an attacker must have before successful exploitation. There are three possible values: None (N) – There is no privilege or special access required to conduct the attack, Low (L) – The attacker requires basic, “user” level privileges to leverage the exploit, High (H) – Administrative or similar access privileges are required for successful attack. |
| `host.services.compromises.metrics.cvss_v30.components.scope` | keyword | Determines whether a vulnerability in one system or component can impact another system or component. If a vulnerability in a vulnerable component can affect a component which is in a different security scope than the vulnerable component, a scope change occurs. Scope has two possible ratings: Changed (C) – An exploited vulnerability can have a carry over impact on another system, Unchanged (U) – The exploited vulnerability is limited in damage to only the local security authority. |
| `host.services.compromises.metrics.cvss_v31` | object |  |
| `host.services.compromises.metrics.cvss_v31.vector` | text | The path, method, or scenario used to exploit the vulnerability. Each section represents components that contribute to the overall CVSS score. |
| `host.services.compromises.metrics.cvss_v31.components` | object | These metrics contribute to how a CVE is scored. |
| `host.services.compromises.metrics.cvss_v31.components.user_interaction` | keyword | Describes whether a user, other than the attacker, is required to do anything or participate in exploitation of the vulnerability. User interaction has two possible values: None (N) – No user interaction is required, Required (R) – A user must complete some steps for the exploit to succeed. For example, a user might be required to install some software. |
| `host.services.compromises.metrics.cvss_v31.components.attack_complexity` | keyword | Indicates conditions beyond the attacker’s control that must exist in order to exploit the vulnerability. The Attack Complexity metric is scored as either Low or High. There are two possible values: Low (L) – There are no specific pre-conditions required for exploitation, High (H) – The attacker must complete some number of preparatory steps in order to get access. |
| `host.services.compromises.metrics.cvss_v31.components.attack_vector` | keyword | Indicates the level of access required for an attacker to exploit the vulnerability. The Attack Vector metric is scored in one of four levels: Network (N) – Vulnerabilities with this rating are remotely exploitable, from one or more hops away, up to, and including, remote exploitation over the Internet, Adjacent (A) – A vulnerability with this rating requires network adjacency for exploitation. The attack must be launched from the same physical or logical network, Local (L) – Vulnerabilities with this rating are not exploitable over a network, Physical (P) – An attacker must physically interact with the target system. |
| `host.services.compromises.metrics.cvss_v31.components.availability` | keyword | If an attack renders information unavailable, such as when a system crashes or through a DDoS attack, availability is negatively impacted. Availability has three possible values: None (N) – There is no loss of availability, Low (L) – Availability might be intermittently limited, or performance might be negatively impacted, as a result of a successful attack, High (H) – There is a complete loss of availability of the impacted system or information. |
| `host.services.compromises.metrics.cvss_v31.components.confidentiality` | keyword | Refers to the disclosure of sensitive information to authorized and unauthorized users, with the goal being that only authorized users are able to access the target data. Confidentiality has three potential values: High (H) – The attacker has full access to all resources in the impacted system, including highly sensitive information such as encryption keys, Low (L) – The attacker has partial access to information, with no control over what, specifically, they are able to access, None (N) – No data is accessible to unauthorized users as a result of the exploit. |
| `host.services.compromises.metrics.cvss_v31.components.integrity` | keyword | Refers to whether the protected information has been tampered with or changed in any way. If there is no way for an attacker to alter the accuracy or completeness of the information, integrity has been maintained. Integrity has three values: None (N) – There is no loss of the integrity of any information, Low (L) – A limited amount of information might be tampered with or modified, but there is no serious impact on the protected system, High (H) – The attacker can modify any/all information on the target system, resulting in a complete loss of integrity. |
| `host.services.compromises.metrics.cvss_v31.components.privileges_required` | keyword | Describes the level of privileges or access an attacker must have before successful exploitation. There are three possible values: None (N) – There is no privilege or special access required to conduct the attack, Low (L) – The attacker requires basic, “user” level privileges to leverage the exploit, High (H) – Administrative or similar access privileges are required for successful attack. |
| `host.services.compromises.metrics.cvss_v31.components.scope` | keyword | Determines whether a vulnerability in one system or component can impact another system or component. If a vulnerability in a vulnerable component can affect a component which is in a different security scope than the vulnerable component, a scope change occurs. Scope has two possible ratings: Changed (C) – An exploited vulnerability can have a carry over impact on another system, Unchanged (U) – The exploited vulnerability is limited in damage to only the local security authority. |
| `host.services.compromises.metrics.cvss_v31.score` | double | Score of the vulnerability; 0.1 is the lowest, 10 is the maximum |
| `host.services.compromises.cvss` | object |  |
| `host.services.compromises.cvss.vector` | text | The path, method, or scenario used to exploit the vulnerability. Each section represents components that contribute to the overall CVSS score. |
| `host.services.compromises.cvss.components` | object | These metrics contribute to how a CVE is scored. |
| `host.services.compromises.cvss.components.integrity` | keyword | Refers to whether the protected information has been tampered with or changed in any way. If there is no way for an attacker to alter the accuracy or completeness of the information, integrity has been maintained. Integrity has three values: None (N) – There is no loss of the integrity of any information, Low (L) – A limited amount of information might be tampered with or modified, but there is no serious impact on the protected system, High (H) – The attacker can modify any/all information on the target system, resulting in a complete loss of integrity. |
| `host.services.compromises.cvss.components.privileges_required` | keyword | Describes the level of privileges or access an attacker must have before successful exploitation. There are three possible values: None (N) – There is no privilege or special access required to conduct the attack, Low (L) – The attacker requires basic, “user” level privileges to leverage the exploit, High (H) – Administrative or similar access privileges are required for successful attack. |
| `host.services.compromises.cvss.components.scope` | keyword | Determines whether a vulnerability in one system or component can impact another system or component. If a vulnerability in a vulnerable component can affect a component which is in a different security scope than the vulnerable component, a scope change occurs. Scope has two possible ratings: Changed (C) – An exploited vulnerability can have a carry over impact on another system, Unchanged (U) – The exploited vulnerability is limited in damage to only the local security authority. |
| `host.services.compromises.cvss.components.user_interaction` | keyword | Describes whether a user, other than the attacker, is required to do anything or participate in exploitation of the vulnerability. User interaction has two possible values: None (N) – No user interaction is required, Required (R) – A user must complete some steps for the exploit to succeed. For example, a user might be required to install some software. |
| `host.services.compromises.cvss.components.attack_complexity` | keyword | Indicates conditions beyond the attacker’s control that must exist in order to exploit the vulnerability. The Attack Complexity metric is scored as either Low or High. There are two possible values: Low (L) – There are no specific pre-conditions required for exploitation, High (H) – The attacker must complete some number of preparatory steps in order to get access. |
| `host.services.compromises.cvss.components.attack_vector` | keyword | Indicates the level of access required for an attacker to exploit the vulnerability. The Attack Vector metric is scored in one of four levels: Network (N) – Vulnerabilities with this rating are remotely exploitable, from one or more hops away, up to, and including, remote exploitation over the Internet, Adjacent (A) – A vulnerability with this rating requires network adjacency for exploitation. The attack must be launched from the same physical or logical network, Local (L) – Vulnerabilities with this rating are not exploitable over a network, Physical (P) – An attacker must physically interact with the target system. |
| `host.services.compromises.cvss.components.availability` | keyword | If an attack renders information unavailable, such as when a system crashes or through a DDoS attack, availability is negatively impacted. Availability has three possible values: None (N) – There is no loss of availability, Low (L) – Availability might be intermittently limited, or performance might be negatively impacted, as a result of a successful attack, High (H) – There is a complete loss of availability of the impacted system or information. |
| `host.services.compromises.cvss.components.confidentiality` | keyword | Refers to the disclosure of sensitive information to authorized and unauthorized users, with the goal being that only authorized users are able to access the target data. Confidentiality has three potential values: High (H) – The attacker has full access to all resources in the impacted system, including highly sensitive information such as encryption keys, Low (L) – The attacker has partial access to information, with no control over what, specifically, they are able to access, None (N) – No data is accessible to unauthorized users as a result of the exploit. |
| `host.services.compromises.cvss.score` | double | Score of the vulnerability; 0.1 is the lowest, 10 is the maximum |
| `host.services.compromises.name` | text |  |
| `host.services.compromises.type` | text |  |
| `host.services.twamp_control` | object |  |
| `host.services.twamp_control.modes` | text |  |
| `host.services.twamp_control.process_start_time` | long |  |
| `host.services.rustdesk_relay` | object |  |
| `host.services.rustdesk_relay.open_relay` | boolean |  |
| `host.services.ventrilo` | object |  |
| `host.services.ventrilo.messages` | object |  |
| `host.services.ventrilo.messages.body` | text |  |
| `host.services.ventrilo.messages.error` | text |  |
| `host.services.ventrilo.messages.header` | object |  |
| `host.services.ventrilo.messages.header.id` | unsigned_long |  |
| `host.services.ventrilo.messages.header.total_length` | unsigned_long |  |
| `host.services.ventrilo.messages.header.cmd` | unsigned_long |  |
| `host.services.ventrilo.messages.header.data_key` | unsigned_long |  |
| `host.services.ventrilo.messages.header.header_key` | unsigned_long |  |
| `host.services.ventrilo.attributes` | text |  |
| `host.services.gemini` | object |  |
| `host.services.gemini.client_cert_required` | boolean |  |
| `host.services.gemini.meta` | text |  |
| `host.services.gemini.status_code` | integer |  |
| `host.services.gemini.body` | text |  |
| `host.services.dotnet_negotiate_stream` | object |  |
| `host.services.dotnet_negotiate_stream.message_id_name` | text |  |
| `host.services.dotnet_negotiate_stream.protocol_version` | text |  |
| `host.services.dotnet_negotiate_stream.supported_mech_oids` | text |  |
| `host.services.dotnet_negotiate_stream.supported_mechs` | text |  |
| `host.services.dotnet_negotiate_stream.hresult` | text |  |
| `host.services.mysqlx` | object |  |
| `host.services.mysqlx.doc_format` | text |  |
| `host.services.mysqlx.node_type` | text |  |
| `host.services.mysqlx.tls_supported` | boolean |  |
| `host.services.mysqlx.auth_mechanisms` | text |  |
| `host.services.mysqlx.capabilities` | text |  |
| `host.services.mysqlx.compression_algorithms` | text |  |
| `host.services.cwmp` | object |  |
| `host.services.cwmp.auth` | text |  |
| `host.services.cwmp.cookies` | text |  |
| `host.services.cwmp.server` | text |  |
| `host.services.chromecast` | object |  |
| `host.services.chromecast.volume` | object |  |
| `host.services.chromecast.volume.control_type` | text |  |
| `host.services.chromecast.volume.level` | float |  |
| `host.services.chromecast.volume.muted` | boolean |  |
| `host.services.chromecast.volume.step_interval` | float |  |
| `host.services.chromecast.applications` | object |  |
| `host.services.chromecast.applications.session_id` | text |  |
| `host.services.chromecast.applications.transport_id` | text |  |
| `host.services.chromecast.applications.app_id` | text |  |
| `host.services.chromecast.applications.app_type` | text |  |
| `host.services.chromecast.applications.display_name` | text |  |
| `host.services.chromecast.applications.namespaces` | object |  |
| `host.services.chromecast.applications.namespaces.name` | text |  |
| `host.services.chromecast.icon_url` | text |  |
| `host.services.chromecast.is_active_input` | boolean |  |
| `host.services.chromecast.protocol_version` | integer |  |
| `host.services.chromecast.status_text` | text |  |
| `host.services.chromecast.universal_app_id` | text |  |
| `host.services.sapient` | object |  |
| `host.services.sapient.error` | object |  |
| `host.services.sapient.error.error_message` | text |  |
| `host.services.sapient.error.packet` | text |  |
| `host.services.sapient.payload` | text |  |
| `host.services.sapient.registration_ack` | object |  |
| `host.services.sapient.registration_ack.ack_response_reason` | text |  |
| `host.services.sapient.registration_ack.acceptance` | boolean |  |
| `host.services.sapient.unknown` | text |  |
| `host.services.murmur` | object |  |
| `host.services.murmur.crypt_setup` | object |  |
| `host.services.murmur.crypt_setup.key` | text |  |
| `host.services.murmur.crypt_setup.server_nonce` | text |  |
| `host.services.murmur.crypt_setup.client_nonce` | text |  |
| `host.services.murmur.murmur_messages` | object |  |
| `host.services.murmur.murmur_messages.body` | text |  |
| `host.services.murmur.murmur_messages.header` | object |  |
| `host.services.murmur.murmur_messages.header.length` | unsigned_long |  |
| `host.services.murmur.murmur_messages.header.type` | text |  |
| `host.services.murmur.reject` | object |  |
| `host.services.murmur.reject.reason` | text |  |
| `host.services.murmur.reject.type` | keyword |  |
| `host.services.murmur.server_config` | object |  |
| `host.services.murmur.server_config.max_users` | unsigned_long |  |
| `host.services.murmur.server_config.message_length` | unsigned_long |  |
| `host.services.murmur.server_config.recording_allowed` | boolean |  |
| `host.services.murmur.server_config.welcome_text` | text |  |
| `host.services.murmur.server_config.allow_html` | boolean |  |
| `host.services.murmur.server_config.image_message_length` | unsigned_long |  |
| `host.services.murmur.server_config.max_bandwidth` | unsigned_long |  |
| `host.services.murmur.server_sync` | object |  |
| `host.services.murmur.server_sync.max_bandwidth` | unsigned_long |  |
| `host.services.murmur.server_sync.permissions` | text |  |
| `host.services.murmur.server_sync.welcome_text` | text |  |
| `host.services.murmur.text_messages` | object |  |
| `host.services.murmur.text_messages.actor` | unsigned_long |  |
| `host.services.murmur.text_messages.channel_id` | unsigned_long |  |
| `host.services.murmur.text_messages.message` | text |  |
| `host.services.murmur.text_messages.session` | unsigned_long |  |
| `host.services.murmur.text_messages.tree_id` | unsigned_long |  |
| `host.services.murmur.version` | object |  |
| `host.services.murmur.version.os_version` | text |  |
| `host.services.murmur.version.version_string` | text |  |
| `host.services.murmur.version.build` | unsigned_long |  |
| `host.services.murmur.version.major` | unsigned_long |  |
| `host.services.murmur.version.minor` | unsigned_long |  |
| `host.services.murmur.version.os` | text |  |
| `host.services.tacacs_plus` | object |  |
| `host.services.tacacs_plus.obfuscated` | text |  |
| `host.services.tacacs_plus.seq_num` | unsigned_long |  |
| `host.services.tacacs_plus.session_id` | unsigned_long |  |
| `host.services.tacacs_plus.type` | unsigned_long |  |
| `host.services.tacacs_plus.version` | unsigned_long |  |
| `host.services.tacacs_plus.data_length` | unsigned_long |  |
| `host.services.tacacs_plus.flags` | unsigned_long |  |
| `host.services.darkgate` | object |  |
| `host.services.darkgate.files` | object |  |
| `host.services.darkgate.files.length` | integer |  |
| `host.services.darkgate.files.name` | text |  |
| `host.services.dvr_ip` | object |  |
| `host.services.dvr_ip.version` | text |  |
| `host.services.dvr_ip.oem_info` | text |  |
| `host.services.dvr_ip.split_screen_capability` | text |  |
| `host.services.dvr_ip.function_list` | text |  |
| `host.services.dvr_ip.hard_drive` | text |  |
| `host.services.dvr_ip.language_support` | text |  |
| `host.services.dvr_ip.network_status` | text |  |
| `host.services.dvr_ip.partition_capability` | object |  |
| `host.services.dvr_ip.partition_capability.max_partition_number` | integer |  |
| `host.services.dvr_ip.partition_capability.supported` | boolean |  |
| `host.services.dvr_ip.wireless_alarm_capability` | text |  |
| `host.services.dvr_ip.function_capability` | text |  |
| `host.services.dvr_ip.access_url` | text |  |
| `host.services.dvr_ip.serial` | text |  |
| `host.services.mikrotik_winbox` | object |  |
| `host.services.mikrotik_winbox.version` | text |  |
| `host.services.mikrotik_winbox.components` | text |  |
| `host.services.cursor_on_target` | object |  |
| `host.services.cursor_on_target.events` | nested |  |
| `host.services.cursor_on_target.events.callsign` | text |  |
| `host.services.cursor_on_target.events.how` | text |  |
| `host.services.cursor_on_target.events.status` | object |  |
| `host.services.cursor_on_target.events.status.battery` | text |  |
| `host.services.cursor_on_target.events.takv` | object |  |
| `host.services.cursor_on_target.events.takv.platform` | text |  |
| `host.services.cursor_on_target.events.takv.version` | text |  |
| `host.services.cursor_on_target.events.takv.device` | text |  |
| `host.services.cursor_on_target.events.takv.os` | text |  |
| `host.services.cursor_on_target.events.type` | text |  |
| `host.services.cursor_on_target.events.point` | object |  |
| `host.services.cursor_on_target.events.point.lon` | double |  |
| `host.services.cursor_on_target.events.point.ce` | double |  |
| `host.services.cursor_on_target.events.point.hae` | double |  |
| `host.services.cursor_on_target.events.point.lat` | double |  |
| `host.services.cursor_on_target.events.point.le` | double |  |
| `host.services.cursor_on_target.events.video_url` | text |  |
| `host.services.cursor_on_target.events.stale` | date |  |
| `host.services.cursor_on_target.events.endpoint` | text |  |
| `host.services.cursor_on_target.events.start` | date |  |
| `host.services.cursor_on_target.events.time` | date |  |
| `host.services.cursor_on_target.events.uid` | text |  |
| `host.services.cursor_on_target.events.version` | text |  |
| `host.services.steam` | object |  |
| `host.services.steam.download_lan_peer_group` | unsigned_long |  |
| `host.services.steam.hostname` | text |  |
| `host.services.steam.supported_services` | unsigned_long |  |
| `host.services.steam.is64bit` | boolean |  |
| `host.services.steam.users` | object |  |
| `host.services.steam.users.auth_key_id` | text |  |
| `host.services.steam.users.steamid` | text |  |
| `host.services.steam.content_cache_port` | unsigned_long |  |
| `host.services.steam.public_ip_address` | text |  |
| `host.services.steam.version` | integer |  |
| `host.services.steam.steam_deck` | boolean |  |
| `host.services.steam.min_version` | integer |  |
| `host.services.steam.mac_addresses` | text |  |
| `host.services.steam.games_running` | boolean |  |
| `host.services.steam.broadcasting_active` | boolean |  |
| `host.services.steam.enabled_services` | unsigned_long |  |
| `host.services.steam.remoteplay_active` | boolean |  |
| `host.services.steam.screen_locked` | boolean |  |
| `host.services.steam.steam_version` | text |  |
| `host.services.steam.ip_addresses` | text |  |
| `host.services.steam.vr_active` | boolean |  |
| `host.services.steam.ostype` | integer |  |
| `host.services.steam.euniverse` | integer |  |
| `host.services.steam.vr_link_caps` | text |  |
| `host.services.steam.connect_port` | unsigned_long |  |
| `host.services.onvif` | object |  |
| `host.services.onvif.services` | object |  |
| `host.services.onvif.services.service_version_major` | unsigned_long |  |
| `host.services.onvif.services.service_version_minor` | unsigned_long |  |
| `host.services.onvif.services.xaddr` | text |  |
| `host.services.onvif.services.capabilities` | object |  |
| `host.services.onvif.services.capabilities.pan_tilt_zoom` | object |  |
| `host.services.onvif.services.capabilities.pan_tilt_zoom.status_position` | boolean |  |
| `host.services.onvif.services.capabilities.pan_tilt_zoom.eflip` | boolean |  |
| `host.services.onvif.services.capabilities.pan_tilt_zoom.get_compatible_configurations` | boolean |  |
| `host.services.onvif.services.capabilities.pan_tilt_zoom.move_status` | boolean |  |
| `host.services.onvif.services.capabilities.pan_tilt_zoom.reverse` | boolean |  |
| `host.services.onvif.services.capabilities.search` | object |  |
| `host.services.onvif.services.capabilities.search.metadata_search` | boolean |  |
| `host.services.onvif.services.capabilities.search.general_start_events` | boolean |  |
| `host.services.onvif.services.capabilities.device` | object |  |
| `host.services.onvif.services.capabilities.device.system` | object |  |
| `host.services.onvif.services.capabilities.device.system.storage_configuration` | boolean |  |
| `host.services.onvif.services.capabilities.device.system.discovery_bye` | boolean |  |
| `host.services.onvif.services.capabilities.device.system.remote_discovery` | boolean |  |
| `host.services.onvif.services.capabilities.device.system.system_backup` | boolean |  |
| `host.services.onvif.services.capabilities.device.system.system_logging` | boolean |  |
| `host.services.onvif.services.capabilities.device.system.firmware_upgrade` | boolean |  |
| `host.services.onvif.services.capabilities.device.system.http_firmware_upgrade` | boolean |  |
| `host.services.onvif.services.capabilities.device.system.http_system_logging` | boolean |  |
| `host.services.onvif.services.capabilities.device.system.http_support_information` | boolean |  |
| `host.services.onvif.services.capabilities.device.system.discovery_resolve` | boolean |  |
| `host.services.onvif.services.capabilities.device.system.http_system_backup` | boolean |  |
| `host.services.onvif.services.capabilities.device.network` | object |  |
| `host.services.onvif.services.capabilities.device.network.dynamic_dns` | boolean |  |
| `host.services.onvif.services.capabilities.device.network.ntp` | unsigned_long |  |
| `host.services.onvif.services.capabilities.device.network.zero_configuration` | boolean |  |
| `host.services.onvif.services.capabilities.device.network.dot1x_configurations` | unsigned_long |  |
| `host.services.onvif.services.capabilities.device.network.dot11_configuration` | boolean |  |
| `host.services.onvif.services.capabilities.device.network.ipv6` | boolean |  |
| `host.services.onvif.services.capabilities.device.network.dhcp_v6` | boolean |  |
| `host.services.onvif.services.capabilities.device.network.hostname_from_dhcp` | boolean |  |
| `host.services.onvif.services.capabilities.device.network.ip_filter` | boolean |  |
| `host.services.onvif.services.capabilities.device.security` | object |  |
| `host.services.onvif.services.capabilities.device.security.onboard_key_generation` | boolean |  |
| `host.services.onvif.services.capabilities.device.security.username_token` | boolean |  |
| `host.services.onvif.services.capabilities.device.security.dot1x` | boolean |  |
| `host.services.onvif.services.capabilities.device.security.max_username_length` | unsigned_long |  |
| `host.services.onvif.services.capabilities.device.security.max_password_length` | unsigned_long |  |
| `host.services.onvif.services.capabilities.device.security.rel_token` | boolean |  |
| `host.services.onvif.services.capabilities.device.security.tls_1_2` | boolean |  |
| `host.services.onvif.services.capabilities.device.security.default_access_policy` | boolean |  |
| `host.services.onvif.services.capabilities.device.security.kerberos_token` | boolean |  |
| `host.services.onvif.services.capabilities.device.security.saml_token` | boolean |  |
| `host.services.onvif.services.capabilities.device.security.supported_eap_methods` | unsigned_long |  |
| `host.services.onvif.services.capabilities.device.security.remote_user_handling` | boolean |  |
| `host.services.onvif.services.capabilities.device.security.http_digest` | boolean |  |
| `host.services.onvif.services.capabilities.device.security.x509_token` | boolean |  |
| `host.services.onvif.services.capabilities.device.security.access_policy_config` | boolean |  |
| `host.services.onvif.services.capabilities.device.security.tls_1_0` | boolean |  |
| `host.services.onvif.services.capabilities.device.security.max_users` | unsigned_long |  |
| `host.services.onvif.services.capabilities.device.security.tls_1_1` | boolean |  |
| `host.services.onvif.services.capabilities.media` | object |  |
| `host.services.onvif.services.capabilities.media.osd` | boolean |  |
| `host.services.onvif.services.capabilities.media.profile` | object |  |
| `host.services.onvif.services.capabilities.media.profile.max_profile_count` | unsigned_long |  |
| `host.services.onvif.services.capabilities.media.rotation` | boolean |  |
| `host.services.onvif.services.capabilities.media.snapshot_uri` | boolean |  |
| `host.services.onvif.services.capabilities.media.streaming` | object |  |
| `host.services.onvif.services.capabilities.media.streaming.non_aggregate_control` | boolean |  |
| `host.services.onvif.services.capabilities.media.streaming.rtp_multicast` | boolean |  |
| `host.services.onvif.services.capabilities.media.streaming.rtp_rtsp_tcp` | boolean |  |
| `host.services.onvif.services.capabilities.media.streaming.rtp_tcp` | boolean |  |
| `host.services.onvif.services.capabilities.media.video_source_mode` | boolean |  |
| `host.services.onvif.services.capabilities.recording` | object |  |
| `host.services.onvif.services.capabilities.recording.dynamic_tracks` | boolean |  |
| `host.services.onvif.services.capabilities.recording.encoding` | text |  |
| `host.services.onvif.services.capabilities.recording.max_rate` | unsigned_long |  |
| `host.services.onvif.services.capabilities.recording.max_recordings` | unsigned_long |  |
| `host.services.onvif.services.capabilities.recording.max_recordings_job` | unsigned_long |  |
| `host.services.onvif.services.capabilities.recording.max_total_rate` | unsigned_long |  |
| `host.services.onvif.services.capabilities.recording.options` | boolean |  |
| `host.services.onvif.services.capabilities.recording.dynamic_recordings` | boolean |  |
| `host.services.onvif.services.capabilities.events` | object |  |
| `host.services.onvif.services.capabilities.events.ws_subscription_policy_support` | boolean |  |
| `host.services.onvif.services.capabilities.events.max_notification_producers` | unsigned_long |  |
| `host.services.onvif.services.capabilities.events.max_pull_points` | unsigned_long |  |
| `host.services.onvif.services.capabilities.events.ws_pausable_subscription_manager_interface_support` | boolean |  |
| `host.services.onvif.services.capabilities.events.ws_pull_point_support` | boolean |  |
| `host.services.onvif.services.capabilities.image` | object |  |
| `host.services.onvif.services.capabilities.image.image_stabilization` | boolean |  |
| `host.services.onvif.services.capabilities.analytics` | object |  |
| `host.services.onvif.services.capabilities.analytics.analytics_module_support` | boolean |  |
| `host.services.onvif.services.capabilities.analytics.cell_based_scene_description_supported` | boolean |  |
| `host.services.onvif.services.capabilities.analytics.rule_options_supported` | boolean |  |
| `host.services.onvif.services.capabilities.analytics.rule_support` | boolean |  |
| `host.services.onvif.services.capabilities.replay` | object |  |
| `host.services.onvif.services.capabilities.replay.rtp_rtsp_tcp` | boolean |  |
| `host.services.onvif.services.capabilities.replay.session_timeout_range` | text |  |
| `host.services.onvif.services.capabilities.replay.reverse_playback` | boolean |  |
| `host.services.onvif.services.capabilities.device_io` | object |  |
| `host.services.onvif.services.capabilities.device_io.serial_ports` | unsigned_long |  |
| `host.services.onvif.services.capabilities.device_io.video_outputs` | unsigned_long |  |
| `host.services.onvif.services.capabilities.device_io.video_source` | unsigned_long |  |
| `host.services.onvif.services.capabilities.device_io.audio_outputs` | unsigned_long |  |
| `host.services.onvif.services.capabilities.device_io.audio_sources` | unsigned_long |  |
| `host.services.onvif.services.capabilities.device_io.digital_inputs` | unsigned_long |  |
| `host.services.onvif.services.capabilities.device_io.relay_outputs` | unsigned_long |  |
| `host.services.onvif.services.namespace` | text |  |
| `host.services.onvif.hostname` | object |  |
| `host.services.onvif.hostname.from_dhcp` | boolean |  |
| `host.services.onvif.hostname.name` | text |  |
| `host.services.unitronics_pcom` | object |  |
| `host.services.unitronics_pcom.model_op_executor` | text |  |
| `host.services.unitronics_pcom.name` | text |  |
| `host.services.unitronics_pcom.os_build` | text |  |
| `host.services.unitronics_pcom.hardware_version` | text |  |
| `host.services.unitronics_pcom.model_executor` | text |  |
| `host.services.unitronics_pcom.buffer_size` | text |  |
| `host.services.unitronics_pcom.os_version` | text |  |
| `host.services.unitronics_pcom.unique_id` | long |  |
| `host.services.unitronics_pcom.unit_id` | text |  |
| `host.services.unitronics_pcom.model` | text |  |
| `host.services.rtsp` | object |  |
| `host.services.rtsp.www_auth` | text |  |
| `host.services.rtsp.auth` | text |  |
| `host.services.rtsp.commands` | text |  |
| `host.services.rtsp.server` | text |  |
| `host.services.banner_hash_sha256` | text |  |
| `host.services.hajime` | object |  |
| `host.services.hajime.public_key` | text |  |
| `host.services.hikvision` | object |  |
| `host.services.hikvision.platforms` | object |  |
| `host.services.hikvision.platforms.libraries` | object |  |
| `host.services.hikvision.platforms.libraries.version` | text |  |
| `host.services.hikvision.platforms.libraries.name` | text |  |
| `host.services.hikvision.platforms.name` | text |  |
| `host.services.hikvision.plugin_version` | text |  |
| `host.services.hikvision.web_version` | text |  |
| `host.services.hikvision.custom_version` | text |  |
| `host.services.openvpn_mgmt` | object |  |
| `host.services.openvpn_mgmt.open_vpn_version` | text |  |
| `host.services.openvpn_mgmt.target_triple` | text |  |
| `host.services.openvpn_mgmt.build_date` | text |  |
| `host.services.openvpn_mgmt.features` | text |  |
| `host.services.openvpn_mgmt.management_version` | text |  |
| `host.services.routeros_api` | object |  |
| `host.services.routeros_api.message` | text |  |
| `host.services.routeros_api.raw_response` | text |  |
| `host.services.routeros_api.reply_word` | text |  |
| `host.services.rustdesk_heartbeat` | object |  |
| `host.services.rustdesk_heartbeat.register_peer_response` | object |  |
| `host.services.rustdesk_heartbeat.register_peer_response.request_public_key` | boolean |  |
| `host.services.rustdesk_heartbeat.message_type` | text |  |
| `host.services.clickhouse_native` | object |  |
| `host.services.clickhouse_native.version` | text |  |
| `host.services.clickhouse_native.version_major` | integer |  |
| `host.services.clickhouse_native.version_minor` | integer |  |
| `host.services.clickhouse_native.error` | object |  |
| `host.services.clickhouse_native.error.code` | integer |  |
| `host.services.clickhouse_native.error.message` | text |  |
| `host.services.clickhouse_native.error.name` | text |  |
| `host.services.clickhouse_native.display_name` | text |  |
| `host.services.clickhouse_native.server_name` | text |  |
| `host.services.clickhouse_native.version_patch` | integer |  |
| `host.services.clickhouse_native.timezone` | text |  |
| `host.services.clickhouse_native.revision` | integer |  |
| `host.services.spice` | object |  |
| `host.services.spice.x509_public_key` | text |  |
| `host.services.spice.major_version` | unsigned_long |  |
| `host.services.spice.minor_version` | unsigned_long |  |
| `host.services.spice.tls_only` | boolean |  |
| `host.services.crestron_din_ap2` | object |  |
| `host.services.crestron_din_ap2.version_string` | text |  |
| `host.services.transport_protocol` | keyword |  |
| `host.services.iec60870_5_104` | object |  |
| `host.services.iec60870_5_104.apci` | object |  |
| `host.services.iec60870_5_104.apci.format` | text |  |
| `host.services.iec60870_5_104.apci.u_subtype` | text |  |
| `host.services.iec60870_5_104.asdu` | object |  |
| `host.services.iec60870_5_104.asdu.common_address` | unsigned_long |  |
| `host.services.iec60870_5_104.asdu.cot_name` | text |  |
| `host.services.iec60870_5_104.asdu.type_id_name` | text |  |
| `host.services.rifatron` | object |  |
| `host.services.rifatron.model` | text |  |
| `host.services.crestron_cp3` | object |  |
| `host.services.crestron_cp3.version_string` | text |  |
| `host.services.portmap` | object |  |
| `host.services.portmap.v3_entries` | object |  |
| `host.services.portmap.v3_entries.universal_address` | text |  |
| `host.services.portmap.v3_entries.version` | unsigned_long |  |
| `host.services.portmap.v3_entries.description` | text |  |
| `host.services.portmap.v3_entries.network_id` | text |  |
| `host.services.portmap.v3_entries.owner` | text |  |
| `host.services.portmap.v3_entries.shorthand` | text |  |
| `host.services.portmap.v2_entries` | object |  |
| `host.services.portmap.v2_entries.protocol` | text |  |
| `host.services.portmap.v2_entries.shorthand` | text |  |
| `host.services.portmap.v2_entries.version` | unsigned_long |  |
| `host.services.portmap.v2_entries.description` | text |  |
| `host.services.portmap.v2_entries.port` | unsigned_long |  |
| `host.services.banner` | text |  |
| `host.services.lpd` | object |  |
| `host.services.lpd.short_state` | text |  |
| `host.services.lpd.text` | text |  |
| `host.services.lpd.jobs` | object |  |
| `host.services.lpd.jobs.body` | text |  |
| `host.services.lpd.jobs.status` | unsigned_long |  |
| `host.services.lpd.long_state` | text |  |
| `host.services.lpd.lpd_message` | object |  |
| `host.services.lpd.lpd_message.status` | unsigned_long |  |
| `host.services.lpd.lpd_message.body` | text |  |
| `host.services.lpd.printer` | text |  |
| `host.services.lpd.raw` | text |  |
| `host.services.redline` | object |  |
| `host.services.redline.action_response` | text |  |
| `host.services.redline.settings_response` | text |  |
| `host.services.redline.transport` | text |  |
| `host.services.jarm` | object |  |
| `host.services.jarm.ip` | text |  |
| `host.services.jarm.is_success` | boolean |  |
| `host.services.jarm.tls_extensions_sha256` | text | The second 32 character portion of the Jarm fingerprint |
| `host.services.jarm.cipher_and_version_fingerprint` | text | The first 30 character portion of the Jarm fingerprint. |
| `host.services.jarm.transport_protocol` | keyword |  |
| `host.services.jarm.fingerprint` | text | The 62 character Jarm fingerprint of the service. |
| `host.services.jarm.scan_time` | date | The time the service was fingerprinted |
| `host.services.jarm.hostname` | text |  |
| `host.services.jarm.port` | unsigned_long |  |
| `host.services.rtmp` | object |  |
| `host.services.rtmp.peer_bandwidth` | unsigned_long |  |
| `host.services.rtmp.protocol_version` | unsigned_long |  |
| `host.services.rtmp.server_software` | text |  |
| `host.services.rtmp.status` | object |  |
| `host.services.rtmp.status.code` | text |  |
| `host.services.rtmp.status.description` | text |  |
| `host.services.rtmp.status.level` | text |  |
| `host.services.rtmp.status.object_encoding` | unsigned_long |  |
| `host.services.rtmp.window_acknowledgement_size` | unsigned_long |  |
| `host.services.rtmp.capabilities` | unsigned_long |  |
| `host.services.rtmp.mode` | unsigned_long |  |
| `host.services.telexper_tlxp` | object |  |
| `host.services.telexper_tlxp.frame_type` | text |  |
| `host.services.telexper_tlxp.image_height_px` | unsigned_long |  |
| `host.services.telexper_tlxp.image_width_px` | unsigned_long |  |
| `host.services.onc` | object |  |
| `host.services.tarantool` | object |  |
| `host.services.tarantool.mode` | text |  |
| `host.services.tarantool.auth_type` | text |  |
| `host.services.tarantool.error_code` | long |  |
| `host.services.tarantool.error_file` | text |  |
| `host.services.tarantool.error_type` | text |  |
| `host.services.tarantool.server_features` | text |  |
| `host.services.tarantool.server_iproto_version` | unsigned_long |  |
| `host.services.tarantool.response_error` | text |  |
| `host.services.tarantool.error_message` | text |  |
| `host.services.tarantool.version` | text |  |
| `host.services.tarantool.instance_uuid` | text |  |
| `host.services.synergy` | object |  |
| `host.services.synergy.protocol_minor` | unsigned_long |  |
| `host.services.synergy.protocol_version` | text |  |
| `host.services.synergy.protocol_major` | unsigned_long |  |
| `host.services.representative_info` | object |  |
| `host.services.representative_info.excluded_ports` | unsigned_long |  |
| `host.services.representative_info.reason` | keyword |  |
| `host.services.representative_info.represented_ports` | unsigned_long |  |
| `host.services.representative_info.sampled_port` | unsigned_long |  |
| `host.services.gearman` | object |  |
| `host.services.gearman.version` | text |  |
| `host.services.gearman.workers` | object |  |
| `host.services.gearman.workers.ip` | text |  |
| `host.services.gearman.workers.client_id` | text |  |
| `host.services.gearman.workers.fd` | text |  |
| `host.services.gearman.workers.functions` | text |  |
| `host.services.gearman.status` | object |  |
| `host.services.gearman.status.running` | integer |  |
| `host.services.gearman.status.total` | integer |  |
| `host.services.gearman.status.available_workers` | integer |  |
| `host.services.gearman.status.function` | text |  |
| `host.services.nmea` | object |  |
| `host.services.nmea.messages` | object |  |
| `host.services.nmea.messages.talker_name` | text |  |
| `host.services.nmea.messages.fields` | text |  |
| `host.services.nmea.messages.sentence_id` | text |  |
| `host.services.nmea.messages.talker_id` | text |  |
| `host.services.dicom` | object |  |
| `host.services.dicom.a_abort` | object |  |
| `host.services.dicom.a_abort.reason_name` | text |  |
| `host.services.dicom.a_abort.source_name` | text |  |
| `host.services.dicom.associate_ac` | object |  |
| `host.services.dicom.associate_ac.implementation_version_name` | text |  |
| `host.services.dicom.associate_ac.implementation_class_uid` | text |  |
| `host.services.dicom.associate_rj` | object |  |
| `host.services.dicom.associate_rj.reason_name` | text |  |
| `host.services.dicom.associate_rj.result_name` | text |  |
| `host.services.dicom.associate_rj.source_name` | text |  |
| `host.services.dicom.pdu_type_name` | text |  |
| `host.services.redlion_crimson` | object |  |
| `host.services.redlion_crimson.current_software_level` | text |  |
| `host.services.redlion_crimson.execution_status` | text |  |
| `host.services.redlion_crimson.manufacturer` | text |  |
| `host.services.redlion_crimson.model` | text |  |
| `host.services.redlion_crimson.configs_exposed` | boolean |  |
| `host.services.redlion_crimson.control_engine_status` | text |  |
| `host.services.nats_io` | object |  |
| `host.services.nats_io.server_name` | text |  |
| `host.services.nats_io.server_id` | text |  |
| `host.services.nats_io.jetstream` | boolean |  |
| `host.services.nats_io.headers` | boolean |  |
| `host.services.nats_io.domain` | text |  |
| `host.services.nats_io.git_commit` | text |  |
| `host.services.nats_io.tls_available` | boolean |  |
| `host.services.nats_io.tls_required` | boolean |  |
| `host.services.nats_io.go` | text |  |
| `host.services.nats_io.connect_urls` | text |  |
| `host.services.nats_io.ws_connect_urls` | text |  |
| `host.services.nats_io.tls_verify` | boolean |  |
| `host.services.nats_io.cluster` | text |  |
| `host.services.nats_io.auth_required` | boolean |  |
| `host.services.nats_io.proto` | integer |  |
| `host.services.nats_io.version` | text |  |
| `host.services.java_rmi` | object |  |
| `host.services.java_rmi.codebase_url` | text |  |
| `host.services.java_rmi.software` | text |  |
| `host.services.java_rmi.stub_classes` | text |  |
| `host.services.java_rmi.unicast_refs` | nested |  |
| `host.services.java_rmi.unicast_refs.type` | text |  |
| `host.services.java_rmi.unicast_refs.host` | text |  |
| `host.services.java_rmi.unicast_refs.port` | unsigned_long |  |
| `host.services.ibmnje` | object |  |
| `host.services.ibmnje.rip` | text |  |
| `host.services.ibmnje.type` | text |  |
| `host.services.ibmnje.ohost` | text |  |
| `host.services.ibmnje.oip` | text |  |
| `host.services.ibmnje.reason` | unsigned_long |  |
| `host.services.ibmnje.rhost` | text |  |
| `host.services.winrm` | object |  |
| `host.services.winrm.auth_types` | text |  |
| `host.services.winrm.ntlm_info` | object |  |
| `host.services.winrm.ntlm_info.encryption_128bit_supported` | boolean |  |
| `host.services.winrm.ntlm_info.target_name` | text |  |
| `host.services.winrm.ntlm_info.challenge_type` | integer |  |
| `host.services.winrm.ntlm_info.dns_domain_name` | text |  |
| `host.services.winrm.ntlm_info.ntlm1_supported` | boolean |  |
| `host.services.winrm.ntlm_info.encryption_56bit_supported` | boolean |  |
| `host.services.winrm.ntlm_info.ntlm_version` | unsigned_long |  |
| `host.services.winrm.ntlm_info.dns_server_name` | text |  |
| `host.services.winrm.ntlm_info.dns_tree_name` | text |  |
| `host.services.winrm.ntlm_info.ntlm2_supported` | boolean |  |
| `host.services.winrm.ntlm_info.netbios_domain_name` | text |  |
| `host.services.winrm.ntlm_info.os_version` | text |  |
| `host.services.winrm.ntlm_info.always_sign_supported` | boolean |  |
| `host.services.winrm.ntlm_info.netbios_computer_name` | text |  |
| `host.services.hid_vertx` | object |  |
| `host.services.hid_vertx.version` | text |  |
| `host.services.hid_vertx.firmware_date` | text |  |
| `host.services.hid_vertx.id` | text |  |
| `host.services.hid_vertx.ip` | text |  |
| `host.services.hid_vertx.mac_address` | text |  |
| `host.services.hid_vertx.make_model` | text |  |
| `host.services.hid_vertx.model` | text |  |
| `host.services.flash_socket_policy` | object |  |
| `host.services.flash_socket_policy.allow_access_from` | nested |  |
| `host.services.flash_socket_policy.allow_access_from.domain` | text |  |
| `host.services.flash_socket_policy.allow_access_from.secure` | boolean |  |
| `host.services.flash_socket_policy.allow_access_from.to_ports` | text |  |
| `host.services.flash_socket_policy.policy` | text |  |
| `host.services.flash_socket_policy.site_control` | text |  |
| `host.services.elasticsearch_transport` | object |  |
| `host.services.elasticsearch_transport.protocol_version` | unsigned_long |  |
| `host.services.elasticsearch_transport.transport_version_id` | unsigned_long |  |
| `host.services.elasticsearch_transport.version` | text |  |
| `host.services.elasticsearch_transport.handshake_ok` | boolean |  |
| `host.services.cortex_xdr_p2p` | object |  |
| `host.services.cortex_xdr_p2p.uuid` | text |  |
| `host.services.wince_cerdisp` | object |  |
| `host.services.wince_cerdisp.selector` | unsigned_long |  |
| `host.services.wince_cerdisp.color_depth_bpp` | unsigned_long |  |
| `host.services.wince_cerdisp.device_family` | text |  |
| `host.services.wince_cerdisp.device_id` | text |  |
| `host.services.wince_cerdisp.flags` | unsigned_long |  |
| `host.services.wince_cerdisp.manufacturer` | text |  |
| `host.services.wince_cerdisp.screen_height` | unsigned_long |  |
| `host.services.wince_cerdisp.screen_width` | unsigned_long |  |
| `host.services.ser2net` | object |  |
| `host.services.ser2net.device` | text |  |
| `host.services.ser2net.os` | text |  |
| `host.services.ser2net.serial_parameters` | object |  |
| `host.services.ser2net.serial_parameters.stop_bits` | text |  |
| `host.services.ser2net.serial_parameters.baud_rate` | text |  |
| `host.services.ser2net.serial_parameters.data_bits` | text |  |
| `host.services.ser2net.serial_parameters.parity` | text |  |
| `host.services.ser2net.software` | text |  |
| `host.services.ser2net.software_version` | text |  |
| `host.services.rlogin` | object |  |
| `host.services.rlogin.operating_system` | text |  |
| `host.services.rlogin.software` | text |  |
| `host.services.rlogin.software_version` | text |  |
| `host.services.rlogin.error` | text |  |
| `host.services.nbd` | object |  |
| `host.services.nbd.policies` | text |  |
| `host.services.nbd.exports` | object |  |
| `host.services.nbd.exports.max_payload_size` | unsigned_long |  |
| `host.services.nbd.exports.min_block_size` | unsigned_long |  |
| `host.services.nbd.exports.name` | text |  |
| `host.services.nbd.exports.preferred_block_size` | unsigned_long |  |
| `host.services.nbd.exports.size` | unsigned_long |  |
| `host.services.nbd.exports.transmit_flags` | text |  |
| `host.services.nbd.exports.details` | text |  |
| `host.services.nbd.handshake_style` | text |  |
| `host.services.operating_systems` | nested |  |
| `host.services.operating_systems.confidence` | double |  |
| `host.services.operating_systems.edition` | text |  |
| `host.services.operating_systems.evidence` | nested |  |
| `host.services.operating_systems.evidence.semver_expression` | text |  |
| `host.services.operating_systems.evidence.data_path` | text |  |
| `host.services.operating_systems.evidence.exists` | boolean |  |
| `host.services.operating_systems.evidence.found_value` | text |  |
| `host.services.operating_systems.evidence.literal_match` | text |  |
| `host.services.operating_systems.evidence.negative` | boolean |  |
| `host.services.operating_systems.evidence.proprietary` | boolean |  |
| `host.services.operating_systems.evidence.regex` | text |  |
| `host.services.operating_systems.part` | text |  |
| `host.services.operating_systems.version` | text |  |
| `host.services.operating_systems.life_cycle` | object |  |
| `host.services.operating_systems.life_cycle.end_of_life_date` | date |  |
| `host.services.operating_systems.life_cycle.release_date` | date |  |
| `host.services.operating_systems.life_cycle.end_of_life` | boolean |  |
| `host.services.operating_systems.product` | text |  |
| `host.services.operating_systems.source` | keyword |  |
| `host.services.operating_systems.components` | object |  |
| `host.services.operating_systems.components.vendor` | text |  |
| `host.services.operating_systems.components.version` | text |  |
| `host.services.operating_systems.components.cpe` | text |  |
| `host.services.operating_systems.components.edition` | text |  |
| `host.services.operating_systems.components.life_cycle` | object |  |
| `host.services.operating_systems.components.life_cycle.end_of_life` | boolean |  |
| `host.services.operating_systems.components.life_cycle.end_of_life_date` | date |  |
| `host.services.operating_systems.components.life_cycle.release_date` | date |  |
| `host.services.operating_systems.components.part` | text |  |
| `host.services.operating_systems.components.product` | text |  |
| `host.services.operating_systems.components.update` | text |  |
| `host.services.operating_systems.type` | text |  |
| `host.services.operating_systems.update` | text |  |
| `host.services.operating_systems.cpe` | text |  |
| `host.services.operating_systems.vendor` | text |  |
| `host.services.screenshots` | nested |  |
| `host.services.screenshots.extracted_text` | text |  |
| `host.services.screenshots.handle` | text |  |
| `host.services.screenshots.palsimhash` | text |  |
| `host.services.screenshots.phash` | text |  |
| `host.services.port` | unsigned_long |  |
| `host.services.minecraft` | object |  |
| `host.services.minecraft.players_max` | long |  |
| `host.services.minecraft.players_online` | long |  |
| `host.services.minecraft.protocol_version` | text |  |
| `host.services.minecraft.server_version` | text |  |
| `host.services.minecraft.motd` | text |  |
| `host.services.stun` | object |  |
| `host.services.stun.response_type_name` | text |  |
| `host.services.stun.turn` | object |  |
| `host.services.stun.turn.response_type` | unsigned_long |  |
| `host.services.stun.turn.response_type_name` | text |  |
| `host.services.stun.turn.allocate_error_response` | object |  |
| `host.services.stun.turn.allocate_error_response.software` | text |  |
| `host.services.stun.turn.allocate_error_response.error_code` | integer |  |
| `host.services.stun.turn.allocate_error_response.error_reason` | text |  |
| `host.services.stun.turn.allocate_error_response.has_fingerprint` | boolean |  |
| `host.services.stun.turn.allocate_error_response.nonce` | text |  |
| `host.services.stun.turn.allocate_error_response.realm` | text |  |
| `host.services.stun.turn.allocate_success_response` | object |  |
| `host.services.stun.turn.allocate_success_response.has_fingerprint` | boolean |  |
| `host.services.stun.turn.allocate_success_response.relay_address` | object |  |
| `host.services.stun.turn.allocate_success_response.relay_address.ip` | ip |  |
| `host.services.stun.turn.allocate_success_response.relay_address.port` | unsigned_long |  |
| `host.services.stun.turn.allocate_success_response.software` | text |  |
| `host.services.stun.binding_error_response` | object |  |
| `host.services.stun.binding_error_response.error_code` | integer |  |
| `host.services.stun.binding_error_response.error_reason` | text |  |
| `host.services.stun.binding_error_response.has_fingerprint` | boolean |  |
| `host.services.stun.binding_error_response.software` | text |  |
| `host.services.stun.binding_success_response` | object |  |
| `host.services.stun.binding_success_response.has_fingerprint` | boolean |  |
| `host.services.stun.binding_success_response.other_address` | object |  |
| `host.services.stun.binding_success_response.other_address.ip` | ip |  |
| `host.services.stun.binding_success_response.other_address.port` | unsigned_long |  |
| `host.services.stun.binding_success_response.software` | text |  |
| `host.services.stun.response_type` | unsigned_long |  |
| `host.services.seven_days_to_die` | object |  |
| `host.services.seven_days_to_die.game_name` | text |  |
| `host.services.seven_days_to_die.game_type` | text |  |
| `host.services.seven_days_to_die.region` | text |  |
| `host.services.seven_days_to_die.server_url` | text |  |
| `host.services.seven_days_to_die.server_version` | text |  |
| `host.services.seven_days_to_die.steam_id` | text |  |
| `host.services.seven_days_to_die.version` | text |  |
| `host.services.dtls` | object |  |
| `host.services.openflow` | object |  |
| `host.services.openflow.mfr_desc` | text |  |
| `host.services.openflow.datapath_id` | unsigned_long |  |
| `host.services.openflow.hw_desc` | text |  |
| `host.services.openflow.n_buffers` | unsigned_long |  |
| `host.services.openflow.sw_desc` | text |  |
| `host.services.openflow.dp_desc` | text |  |
| `host.services.openflow.peer_role` | text |  |
| `host.services.openflow.capabilities` | text |  |
| `host.services.openflow.datapath_mac` | text |  |
| `host.services.openflow.hello_elements` | nested |  |
| `host.services.openflow.hello_elements.element_type` | text |  |
| `host.services.openflow.hello_elements.supported_versions` | text |  |
| `host.services.openflow.protocol_version_raw` | text |  |
| `host.services.openflow.serial_num` | text |  |
| `host.services.openflow.n_tables` | unsigned_long |  |
| `host.services.openflow.protocol_version` | text |  |
| `host.services.openflow.bare_hello` | boolean |  |
| `host.services.openflow.xid` | unsigned_long |  |
| `host.services.openflow.auxiliary_id` | unsigned_long |  |
| `host.services.cmore` | object |  |
| `host.services.reolink_baichuan` | object |  |
| `host.services.reolink_baichuan.status_code` | unsigned_long |  |
| `host.services.reolink_baichuan.ai_types_observed` | text |  |
| `host.services.reolink_baichuan.body_length` | unsigned_long |  |
| `host.services.reolink_baichuan.channel_count` | unsigned_long |  |
| `host.services.reolink_baichuan.channels` | nested |  |
| `host.services.reolink_baichuan.channels.channel_id` | unsigned_long |  |
| `host.services.reolink_baichuan.channels.recording` | unsigned_long |  |
| `host.services.reolink_baichuan.channels.status` | text |  |
| `host.services.reolink_baichuan.channels.timestamp` | unsigned_long |  |
| `host.services.reolink_baichuan.channels.ai_type` | text |  |
| `host.services.reolink_baichuan.command_id` | unsigned_long |  |
| `host.services.reolink_baichuan.raw_xml` | text |  |
| `host.services.icap` | object |  |
| `host.services.icap.options_response` | object |  |
| `host.services.icap.options_response.preview` | integer |  |
| `host.services.icap.options_response.status_text` | text |  |
| `host.services.icap.options_response.icap_version` | text |  |
| `host.services.icap.options_response.service` | text |  |
| `host.services.icap.options_response.service_id` | text |  |
| `host.services.icap.options_response.methods` | text |  |
| `host.services.icap.options_response.options_ttl` | integer |  |
| `host.services.icap.options_response.allow_204` | boolean |  |
| `host.services.icap.options_response.max_connections` | integer |  |
| `host.services.icap.options_response.server_header` | text |  |
| `host.services.icap.options_response.status_code` | integer |  |
| `host.services.icap.options_response.istag` | text |  |
| `host.services.ntrip` | object |  |
| `host.services.ntrip.data_streams` | object |  |
| `host.services.ntrip.data_streams.network` | text |  |
| `host.services.ntrip.data_streams.compression_or_encryption` | text |  |
| `host.services.ntrip.data_streams.solution` | text |  |
| `host.services.ntrip.data_streams.format_details` | text |  |
| `host.services.ntrip.data_streams.fee` | boolean |  |
| `host.services.ntrip.data_streams.misc` | text |  |
| `host.services.ntrip.data_streams.country_code` | text |  |
| `host.services.ntrip.data_streams.caster_mount_point` | text |  |
| `host.services.ntrip.data_streams.carrier_info` | text |  |
| `host.services.ntrip.data_streams.bitrate` | unsigned_long |  |
| `host.services.ntrip.data_streams.authentication` | text |  |
| `host.services.ntrip.data_streams.generator` | text |  |
| `host.services.ntrip.data_streams.nmea` | boolean |  |
| `host.services.ntrip.data_streams.longitude` | text |  |
| `host.services.ntrip.data_streams.source_identifier` | text |  |
| `host.services.ntrip.data_streams.nav_system` | text |  |
| `host.services.ntrip.data_streams.data_format` | text |  |
| `host.services.ntrip.data_streams.latitude` | text |  |
| `host.services.ntrip.server` | text |  |
| `host.services.ntrip.version` | text |  |
| `host.services.asterisk_manager_interface` | object |  |
| `host.services.asterisk_manager_interface.version` | text |  |
| `host.services.isc_dhcp_omapi` | object |  |
| `host.services.isc_dhcp_omapi.object_dict_present` | boolean |  |
| `host.services.isc_dhcp_omapi.object_state` | unsigned_long |  |
| `host.services.isc_dhcp_omapi.reply_header` | object |  |
| `host.services.isc_dhcp_omapi.reply_header.handle` | unsigned_long |  |
| `host.services.isc_dhcp_omapi.reply_header.opcode` | text |  |
| `host.services.isc_dhcp_omapi.reply_header.tid` | unsigned_long |  |
| `host.services.isc_dhcp_omapi.reply_header.authid` | unsigned_long |  |
| `host.services.isc_dhcp_omapi.reply_header.authlen` | unsigned_long |  |
| `host.services.isc_dhcp_omapi.status_message` | text |  |
| `host.services.isc_dhcp_omapi.auth_posture` | text |  |
| `host.services.isc_dhcp_omapi.message_dict_extra_keys` | text |  |
| `host.services.isc_dhcp_omapi.object_dict_keys` | text |  |
| `host.services.r1soft_buagent` | object |  |
| `host.services.r1soft_buagent.cpu_hypervisor_signature` | text |  |
| `host.services.r1soft_buagent.rsa_public_key_bits` | unsigned_long |  |
| `host.services.r1soft_buagent.rsa_public_key_sha256` | text |  |
| `host.services.fins` | object |  |
| `host.services.fins.status_run_mode` | text |  |
| `host.services.fins.version` | text |  |
| `host.services.fins.model` | text |  |
| `host.services.fins.status_error_message` | text |  |
| `host.services.gopher` | object |  |
| `host.services.gopher.body` | text |  |
| `host.services.gopher.items` | nested |  |
| `host.services.gopher.items.display_string` | text |  |
| `host.services.gopher.items.hostname` | text |  |
| `host.services.gopher.items.item_type` | text |  |
| `host.services.gopher.items.port` | integer |  |
| `host.services.gopher.items.selector` | text |  |
| `host.services.gopher.title` | text |  |
| `host.services.frps` | object |  |
| `host.services.frps.version` | text |  |
| `host.services.frps.error` | text |  |
| `host.services.frps.run_id` | text |  |
| `host.services.mdns` | object |  |
| `host.services.mdns.names` | text |  |
| `host.services.mdns.results` | object |  |
| `host.services.mdns.results.addresses` | text |  |
| `host.services.mdns.results.full_name` | text |  |
| `host.services.mdns.results.port` | integer |  |
| `host.services.mdns.results.priority` | integer |  |
| `host.services.mdns.results.target` | text |  |
| `host.services.mdns.results.texts` | text |  |
| `host.services.mdns.results.weight` | integer |  |
| `host.services.mdns.multiple_responses` | boolean |  |
| `host.services.rdate` | object |  |
| `host.services.rdate.date` | text |  |
| `host.services.sap_router` | object |  |
| `host.services.sap_router.router_info` | object |  |
| `host.services.sap_router.router_info.started_on` | date |  |
| `host.services.sap_router.router_info.port` | unsigned_long |  |
| `host.services.sap_router.router_info.routtab_relative_directory` | text |  |
| `host.services.sap_router.router_info.connected_client_info` | object |  |
| `host.services.sap_router.router_info.connected_client_info.service` | text |  |
| `host.services.sap_router.router_info.connected_client_info.traced` | boolean |  |
| `host.services.sap_router.router_info.connected_client_info.connected` | boolean |  |
| `host.services.sap_router.router_info.connected_client_info.connected_on` | date |  |
| `host.services.sap_router.router_info.connected_client_info.id` | unsigned_long |  |
| `host.services.sap_router.router_info.connected_client_info.routed` | boolean |  |
| `host.services.sap_router.router_info.parent_pid` | unsigned_long |  |
| `host.services.sap_router.router_info.pid` | unsigned_long |  |
| `host.services.sap_router.router_info.sap_router_absolute_directory` | text |  |
| `host.services.sap_router.router_info.parent_port` | unsigned_long |  |
| `host.services.sap_router.router_info.num_clients` | unsigned_long |  |
| `host.services.sap_router.router_version_info` | object |  |
| `host.services.sap_router.router_version_info.release` | unsigned_long |  |
| `host.services.sap_router.router_version_info.version` | unsigned_long |  |
| `host.services.sap_router.router_version_info.name` | text |  |
| `host.services.iota` | object |  |
| `host.services.iota.v0_info` | object |  |
| `host.services.iota.v0_info.latest_milestone` | long |  |
| `host.services.iota.v0_info.latest_uncommitted_milestone` | long |  |
| `host.services.iota.v0_info.name` | text |  |
| `host.services.iota.v0_info.neighbors` | long |  |
| `host.services.iota.v0_info.tips` | long |  |
| `host.services.iota.v0_info.version` | text |  |
| `host.services.iota.v0_info.features` | text |  |
| `host.services.iota.v0_info.is_healthy` | boolean |  |
| `host.services.iota.v1_info` | object |  |
| `host.services.iota.v1_info.network_id` | text |  |
| `host.services.iota.v1_info.version` | text |  |
| `host.services.iota.v1_info.confirmed_milestone_index` | long |  |
| `host.services.iota.v1_info.features` | text |  |
| `host.services.iota.v1_info.is_healthy` | boolean |  |
| `host.services.iota.v1_info.latest_milestone_index` | long |  |
| `host.services.iota.v1_info.name` | text |  |
| `host.services.iota.v2_info` | object |  |
| `host.services.iota.v2_info.network_name` | text |  |
| `host.services.iota.v2_info.latest_milestone` | long |  |
| `host.services.iota.v2_info.token_supply` | text |  |
| `host.services.iota.v2_info.decimals` | long |  |
| `host.services.iota.v2_info.subunit` | text |  |
| `host.services.iota.v2_info.name` | text |  |
| `host.services.iota.v2_info.features` | text |  |
| `host.services.iota.v2_info.latest_uncommitted_milestone` | long |  |
| `host.services.iota.v2_info.supported_protocol_versions` | long |  |
| `host.services.iota.v2_info.is_healthy` | boolean |  |
| `host.services.iota.v2_info.ticker_symbol` | text |  |
| `host.services.iota.v2_info.version` | text |  |
| `host.services.iota.v2_info.token_name` | text |  |
| `host.services.iota.v2_info.unit` | text |  |
| `host.services.iota.v2_info.protocol_version` | long |  |
| `host.services.weblogic_t3` | object |  |
| `host.services.weblogic_t3.error` | text |  |
| `host.services.weblogic_t3.error_message` | text |  |
| `host.services.weblogic_t3.weblogic_version` | text |  |
| `host.services.banner_hex` | text |  |
| `host.services.ip` | ip |  |
| `host.services.perforce_p4d` | object |  |
| `host.services.perforce_p4d.protocol` | object |  |
| `host.services.perforce_p4d.protocol.tz_offset` | text |  |
| `host.services.perforce_p4d.protocol.auto_tune` | text |  |
| `host.services.perforce_p4d.protocol.security_level_name` | text |  |
| `host.services.perforce_p4d.protocol.server_id` | text |  |
| `host.services.perforce_p4d.protocol.server_protocol` | text |  |
| `host.services.perforce_p4d.protocol.server_sub_protocol` | text |  |
| `host.services.perforce_p4d.info` | object |  |
| `host.services.perforce_p4d.info.server_version` | text |  |
| `host.services.perforce_p4d.info.server_uptime` | text |  |
| `host.services.perforce_p4d.info.case_handling` | text |  |
| `host.services.perforce_p4d.info.server_release` | text |  |
| `host.services.perforce_p4d.info.server_root` | text |  |
| `host.services.perforce_p4d.info.server_build_date` | text |  |
| `host.services.perforce_p4d.info.server_changelist` | text |  |
| `host.services.perforce_p4d.info.server_license` | text |  |
| `host.services.perforce_p4d.info.server_platform` | text |  |
| `host.services.perforce_p4d.info.server_timezone` | text |  |
| `host.services.perforce_p4d.info.server_addr` | text |  |
| `host.services.ja4tscan` | object |  |
| `host.services.ja4tscan.scan_time` | date |  |
| `host.services.ja4tscan.fingerprint` | text |  |
| `host.services.scpi` | object |  |
| `host.services.scpi.firmware` | text |  |
| `host.services.scpi.manufacturer` | text |  |
| `host.services.scpi.model` | text |  |
| `host.services.scpi.serial` | text |  |
| `host.services.profinet_cm` | object |  |
| `host.services.profinet_cm.lookup_response_raw` | text |  |
| `host.services.profinet_cm.multiple_fragments` | boolean |  |
| `host.services.profinet_cm.byte_order` | text |  |
| `host.services.exposures` | nested |  |
| `host.services.exposures.id` | text |  |
| `host.services.exposures.risk_source` | keyword |  |
| `host.services.exposures.type` | text |  |
| `host.services.exposures.year` | unsigned_long |  |
| `host.services.exposures.metrics` | object |  |
| `host.services.exposures.metrics.cvss_v30` | object |  |
| `host.services.exposures.metrics.cvss_v30.score` | double | Score of the vulnerability; 0.1 is the lowest, 10 is the maximum |
| `host.services.exposures.metrics.cvss_v30.vector` | text | The path, method, or scenario used to exploit the vulnerability. Each section represents components that contribute to the overall CVSS score. |
| `host.services.exposures.metrics.cvss_v30.components` | object | These metrics contribute to how a CVE is scored. |
| `host.services.exposures.metrics.cvss_v30.components.privileges_required` | keyword | Describes the level of privileges or access an attacker must have before successful exploitation. There are three possible values: None (N) – There is no privilege or special access required to conduct the attack, Low (L) – The attacker requires basic, “user” level privileges to leverage the exploit, High (H) – Administrative or similar access privileges are required for successful attack. |
| `host.services.exposures.metrics.cvss_v30.components.scope` | keyword | Determines whether a vulnerability in one system or component can impact another system or component. If a vulnerability in a vulnerable component can affect a component which is in a different security scope than the vulnerable component, a scope change occurs. Scope has two possible ratings: Changed (C) – An exploited vulnerability can have a carry over impact on another system, Unchanged (U) – The exploited vulnerability is limited in damage to only the local security authority. |
| `host.services.exposures.metrics.cvss_v30.components.user_interaction` | keyword | Describes whether a user, other than the attacker, is required to do anything or participate in exploitation of the vulnerability. User interaction has two possible values: None (N) – No user interaction is required, Required (R) – A user must complete some steps for the exploit to succeed. For example, a user might be required to install some software. |
| `host.services.exposures.metrics.cvss_v30.components.attack_complexity` | keyword | Indicates conditions beyond the attacker’s control that must exist in order to exploit the vulnerability. The Attack Complexity metric is scored as either Low or High. There are two possible values: Low (L) – There are no specific pre-conditions required for exploitation, High (H) – The attacker must complete some number of preparatory steps in order to get access. |
| `host.services.exposures.metrics.cvss_v30.components.attack_vector` | keyword | Indicates the level of access required for an attacker to exploit the vulnerability. The Attack Vector metric is scored in one of four levels: Network (N) – Vulnerabilities with this rating are remotely exploitable, from one or more hops away, up to, and including, remote exploitation over the Internet, Adjacent (A) – A vulnerability with this rating requires network adjacency for exploitation. The attack must be launched from the same physical or logical network, Local (L) – Vulnerabilities with this rating are not exploitable over a network, Physical (P) – An attacker must physically interact with the target system. |
| `host.services.exposures.metrics.cvss_v30.components.availability` | keyword | If an attack renders information unavailable, such as when a system crashes or through a DDoS attack, availability is negatively impacted. Availability has three possible values: None (N) – There is no loss of availability, Low (L) – Availability might be intermittently limited, or performance might be negatively impacted, as a result of a successful attack, High (H) – There is a complete loss of availability of the impacted system or information. |
| `host.services.exposures.metrics.cvss_v30.components.confidentiality` | keyword | Refers to the disclosure of sensitive information to authorized and unauthorized users, with the goal being that only authorized users are able to access the target data. Confidentiality has three potential values: High (H) – The attacker has full access to all resources in the impacted system, including highly sensitive information such as encryption keys, Low (L) – The attacker has partial access to information, with no control over what, specifically, they are able to access, None (N) – No data is accessible to unauthorized users as a result of the exploit. |
| `host.services.exposures.metrics.cvss_v30.components.integrity` | keyword | Refers to whether the protected information has been tampered with or changed in any way. If there is no way for an attacker to alter the accuracy or completeness of the information, integrity has been maintained. Integrity has three values: None (N) – There is no loss of the integrity of any information, Low (L) – A limited amount of information might be tampered with or modified, but there is no serious impact on the protected system, High (H) – The attacker can modify any/all information on the target system, resulting in a complete loss of integrity. |
| `host.services.exposures.metrics.cvss_v31` | object |  |
| `host.services.exposures.metrics.cvss_v31.vector` | text | The path, method, or scenario used to exploit the vulnerability. Each section represents components that contribute to the overall CVSS score. |
| `host.services.exposures.metrics.cvss_v31.components` | object | These metrics contribute to how a CVE is scored. |
| `host.services.exposures.metrics.cvss_v31.components.user_interaction` | keyword | Describes whether a user, other than the attacker, is required to do anything or participate in exploitation of the vulnerability. User interaction has two possible values: None (N) – No user interaction is required, Required (R) – A user must complete some steps for the exploit to succeed. For example, a user might be required to install some software. |
| `host.services.exposures.metrics.cvss_v31.components.attack_complexity` | keyword | Indicates conditions beyond the attacker’s control that must exist in order to exploit the vulnerability. The Attack Complexity metric is scored as either Low or High. There are two possible values: Low (L) – There are no specific pre-conditions required for exploitation, High (H) – The attacker must complete some number of preparatory steps in order to get access. |
| `host.services.exposures.metrics.cvss_v31.components.attack_vector` | keyword | Indicates the level of access required for an attacker to exploit the vulnerability. The Attack Vector metric is scored in one of four levels: Network (N) – Vulnerabilities with this rating are remotely exploitable, from one or more hops away, up to, and including, remote exploitation over the Internet, Adjacent (A) – A vulnerability with this rating requires network adjacency for exploitation. The attack must be launched from the same physical or logical network, Local (L) – Vulnerabilities with this rating are not exploitable over a network, Physical (P) – An attacker must physically interact with the target system. |
| `host.services.exposures.metrics.cvss_v31.components.availability` | keyword | If an attack renders information unavailable, such as when a system crashes or through a DDoS attack, availability is negatively impacted. Availability has three possible values: None (N) – There is no loss of availability, Low (L) – Availability might be intermittently limited, or performance might be negatively impacted, as a result of a successful attack, High (H) – There is a complete loss of availability of the impacted system or information. |
| `host.services.exposures.metrics.cvss_v31.components.confidentiality` | keyword | Refers to the disclosure of sensitive information to authorized and unauthorized users, with the goal being that only authorized users are able to access the target data. Confidentiality has three potential values: High (H) – The attacker has full access to all resources in the impacted system, including highly sensitive information such as encryption keys, Low (L) – The attacker has partial access to information, with no control over what, specifically, they are able to access, None (N) – No data is accessible to unauthorized users as a result of the exploit. |
| `host.services.exposures.metrics.cvss_v31.components.integrity` | keyword | Refers to whether the protected information has been tampered with or changed in any way. If there is no way for an attacker to alter the accuracy or completeness of the information, integrity has been maintained. Integrity has three values: None (N) – There is no loss of the integrity of any information, Low (L) – A limited amount of information might be tampered with or modified, but there is no serious impact on the protected system, High (H) – The attacker can modify any/all information on the target system, resulting in a complete loss of integrity. |
| `host.services.exposures.metrics.cvss_v31.components.privileges_required` | keyword | Describes the level of privileges or access an attacker must have before successful exploitation. There are three possible values: None (N) – There is no privilege or special access required to conduct the attack, Low (L) – The attacker requires basic, “user” level privileges to leverage the exploit, High (H) – Administrative or similar access privileges are required for successful attack. |
| `host.services.exposures.metrics.cvss_v31.components.scope` | keyword | Determines whether a vulnerability in one system or component can impact another system or component. If a vulnerability in a vulnerable component can affect a component which is in a different security scope than the vulnerable component, a scope change occurs. Scope has two possible ratings: Changed (C) – An exploited vulnerability can have a carry over impact on another system, Unchanged (U) – The exploited vulnerability is limited in damage to only the local security authority. |
| `host.services.exposures.metrics.cvss_v31.score` | double | Score of the vulnerability; 0.1 is the lowest, 10 is the maximum |
| `host.services.exposures.metrics.cvss_v40` | object |  |
| `host.services.exposures.metrics.cvss_v40.vector` | text | The path, method, or scenario used to exploit the vulnerability. Each section represents components that contribute to the overall CVSS score. |
| `host.services.exposures.metrics.cvss_v40.components` | object | These metrics contribute to how a CVE is scored. |
| `host.services.exposures.metrics.cvss_v40.components.privileges_required` | keyword | Describes the level of privileges or access an attacker must have before successful exploitation. There are three possible values: None (N) – There is no privilege or special access required to conduct the attack, Low (L) – The attacker requires basic, “user” level privileges to leverage the exploit, High (H) – Administrative or similar access privileges are required for successful attack. |
| `host.services.exposures.metrics.cvss_v40.components.provider_urgency` | keyword |  |
| `host.services.exposures.metrics.cvss_v40.components.confidentiality` | keyword | Refers to the disclosure of sensitive information to authorized and unauthorized users, with the goal being that only authorized users are able to access the target data. Confidentiality has three potential values: High (H) – The attacker has full access to all resources in the impacted system, including highly sensitive information such as encryption keys, Low (L) – The attacker has partial access to information, with no control over what, specifically, they are able to access, None (N) – No data is accessible to unauthorized users as a result of the exploit. |
| `host.services.exposures.metrics.cvss_v40.components.integrity` | keyword | Refers to whether the protected information has been tampered with or changed in any way. If there is no way for an attacker to alter the accuracy or completeness of the information, integrity has been maintained. Integrity has three values: None (N) – There is no loss of the integrity of any information, Low (L) – A limited amount of information might be tampered with or modified, but there is no serious impact on the protected system, High (H) – The attacker can modify any/all information on the target system, resulting in a complete loss of integrity. |
| `host.services.exposures.metrics.cvss_v40.components.automatable` | keyword |  |
| `host.services.exposures.metrics.cvss_v40.components.attack_requirements` | keyword |  |
| `host.services.exposures.metrics.cvss_v40.components.safety` | keyword |  |
| `host.services.exposures.metrics.cvss_v40.components.vulnerability_response_effort` | keyword |  |
| `host.services.exposures.metrics.cvss_v40.components.attack_vector` | keyword | Indicates the level of access required for an attacker to exploit the vulnerability. The Attack Vector metric is scored in one of four levels: Network (N) – Vulnerabilities with this rating are remotely exploitable, from one or more hops away, up to, and including, remote exploitation over the Internet, Adjacent (A) – A vulnerability with this rating requires network adjacency for exploitation. The attack must be launched from the same physical or logical network, Local (L) – Vulnerabilities with this rating are not exploitable over a network, Physical (P) – An attacker must physically interact with the target system. |
| `host.services.exposures.metrics.cvss_v40.components.recovery` | keyword |  |
| `host.services.exposures.metrics.cvss_v40.components.value_density` | keyword |  |
| `host.services.exposures.metrics.cvss_v40.components.user_interaction` | keyword | Describes whether a user, other than the attacker, is required to do anything or participate in exploitation of the vulnerability. User interaction has two possible values: None (N) – No user interaction is required, Required (R) – A user must complete some steps for the exploit to succeed. For example, a user might be required to install some software. |
| `host.services.exposures.metrics.cvss_v40.components.attack_complexity` | keyword | Indicates conditions beyond the attacker’s control that must exist in order to exploit the vulnerability. The Attack Complexity metric is scored as either Low or High. There are two possible values: Low (L) – There are no specific pre-conditions required for exploitation, High (H) – The attacker must complete some number of preparatory steps in order to get access. |
| `host.services.exposures.metrics.cvss_v40.components.availability` | keyword | If an attack renders information unavailable, such as when a system crashes or through a DDoS attack, availability is negatively impacted. Availability has three possible values: None (N) – There is no loss of availability, Low (L) – Availability might be intermittently limited, or performance might be negatively impacted, as a result of a successful attack, High (H) – There is a complete loss of availability of the impacted system or information. |
| `host.services.exposures.metrics.cvss_v40.score` | double | Score of the vulnerability; 0.1 is the lowest, 10 is the maximum |
| `host.services.exposures.metrics.epss` | object |  |
| `host.services.exposures.metrics.epss.score` | double |  |
| `host.services.exposures.metrics.epss.percentile` | double |  |
| `host.services.exposures.name` | text |  |
| `host.services.exposures.severity` | keyword |  |
| `host.services.exposures.cvss` | object |  |
| `host.services.exposures.cvss.score` | double | Score of the vulnerability; 0.1 is the lowest, 10 is the maximum |
| `host.services.exposures.cvss.vector` | text | The path, method, or scenario used to exploit the vulnerability. Each section represents components that contribute to the overall CVSS score. |
| `host.services.exposures.cvss.components` | object | These metrics contribute to how a CVE is scored. |
| `host.services.exposures.cvss.components.attack_vector` | keyword | Indicates the level of access required for an attacker to exploit the vulnerability. The Attack Vector metric is scored in one of four levels: Network (N) – Vulnerabilities with this rating are remotely exploitable, from one or more hops away, up to, and including, remote exploitation over the Internet, Adjacent (A) – A vulnerability with this rating requires network adjacency for exploitation. The attack must be launched from the same physical or logical network, Local (L) – Vulnerabilities with this rating are not exploitable over a network, Physical (P) – An attacker must physically interact with the target system. |
| `host.services.exposures.cvss.components.availability` | keyword | If an attack renders information unavailable, such as when a system crashes or through a DDoS attack, availability is negatively impacted. Availability has three possible values: None (N) – There is no loss of availability, Low (L) – Availability might be intermittently limited, or performance might be negatively impacted, as a result of a successful attack, High (H) – There is a complete loss of availability of the impacted system or information. |
| `host.services.exposures.cvss.components.confidentiality` | keyword | Refers to the disclosure of sensitive information to authorized and unauthorized users, with the goal being that only authorized users are able to access the target data. Confidentiality has three potential values: High (H) – The attacker has full access to all resources in the impacted system, including highly sensitive information such as encryption keys, Low (L) – The attacker has partial access to information, with no control over what, specifically, they are able to access, None (N) – No data is accessible to unauthorized users as a result of the exploit. |
| `host.services.exposures.cvss.components.integrity` | keyword | Refers to whether the protected information has been tampered with or changed in any way. If there is no way for an attacker to alter the accuracy or completeness of the information, integrity has been maintained. Integrity has three values: None (N) – There is no loss of the integrity of any information, Low (L) – A limited amount of information might be tampered with or modified, but there is no serious impact on the protected system, High (H) – The attacker can modify any/all information on the target system, resulting in a complete loss of integrity. |
| `host.services.exposures.cvss.components.privileges_required` | keyword | Describes the level of privileges or access an attacker must have before successful exploitation. There are three possible values: None (N) – There is no privilege or special access required to conduct the attack, Low (L) – The attacker requires basic, “user” level privileges to leverage the exploit, High (H) – Administrative or similar access privileges are required for successful attack. |
| `host.services.exposures.cvss.components.scope` | keyword | Determines whether a vulnerability in one system or component can impact another system or component. If a vulnerability in a vulnerable component can affect a component which is in a different security scope than the vulnerable component, a scope change occurs. Scope has two possible ratings: Changed (C) – An exploited vulnerability can have a carry over impact on another system, Unchanged (U) – The exploited vulnerability is limited in damage to only the local security authority. |
| `host.services.exposures.cvss.components.user_interaction` | keyword | Describes whether a user, other than the attacker, is required to do anything or participate in exploitation of the vulnerability. User interaction has two possible values: None (N) – No user interaction is required, Required (R) – A user must complete some steps for the exploit to succeed. For example, a user might be required to install some software. |
| `host.services.exposures.cvss.components.attack_complexity` | keyword | Indicates conditions beyond the attacker’s control that must exist in order to exploit the vulnerability. The Attack Complexity metric is scored as either Low or High. There are two possible values: Low (L) – There are no specific pre-conditions required for exploitation, High (H) – The attacker must complete some number of preparatory steps in order to get access. |
| `host.services.exposures.source` | keyword |  |
| `host.services.exposures.confidence` | double |  |
| `host.services.exposures.evidence` | nested |  |
| `host.services.exposures.evidence.literal_match` | text |  |
| `host.services.exposures.evidence.negative` | boolean |  |
| `host.services.exposures.evidence.proprietary` | boolean |  |
| `host.services.exposures.evidence.regex` | text |  |
| `host.services.exposures.evidence.semver_expression` | text |  |
| `host.services.exposures.evidence.data_path` | text |  |
| `host.services.exposures.evidence.exists` | boolean |  |
| `host.services.exposures.evidence.found_value` | text |  |
| `host.services.threats` | nested |  |
| `host.services.threats.id` | text |  |
| `host.services.threats.malware` | object |  |
| `host.services.threats.malware.id` | text |  |
| `host.services.threats.malware.last_updated_at` | date |  |
| `host.services.threats.malware.malpedia_id` | text |  |
| `host.services.threats.malware.primary_name` | text |  |
| `host.services.threats.malware.all_names` | text |  |
| `host.services.threats.name` | text |  |
| `host.services.threats.type` | keyword |  |
| `host.services.threats.tactic` | keyword |  |
| `host.services.threats.confidence` | double |  |
| `host.services.threats.source` | keyword |  |
| `host.services.threats.evidence` | nested |  |
| `host.services.threats.evidence.regex` | text |  |
| `host.services.threats.evidence.semver_expression` | text |  |
| `host.services.threats.evidence.data_path` | text |  |
| `host.services.threats.evidence.exists` | boolean |  |
| `host.services.threats.evidence.found_value` | text |  |
| `host.services.threats.evidence.literal_match` | text |  |
| `host.services.threats.evidence.negative` | boolean |  |
| `host.services.threats.evidence.proprietary` | boolean |  |
| `host.services.threats.actors` | object |  |
| `host.services.threats.actors.mitre_group_id` | text |  |
| `host.services.threats.actors.primary_name` | text |  |
| `host.services.threats.actors.all_names` | text |  |
| `host.services.threats.actors.id` | text |  |
| `host.services.threats.actors.malpedia_group_id` | text |  |
| `host.services.threats.details` | object |  |
| `host.services.threats.details.version` | text |  |
| `host.services.threats.details.campaign_id` | text |  |
| `host.services.threats.details.campaign_theme` | text |  |
| `host.services.threats.details.control_servers` | text |  |
| `host.services.cert` | object |  |
| `host.services.cert.parent_spki_fingerprint_sha256` | text | DEPRECATED: Use parent_spki_subject_fingerprint_sha256 |
| `host.services.cert.spki_fingerprint_sha256` | text | DEPRECATED: Use spki_subject_fingerprint_sha256 |
| `host.services.cert.precert` | boolean | Whether the X.509 "poison" extension (OID: 1.3.6.1.4.1.11129.2.4.3) is marked critical, which prohibits the pre-certificate from being trusted. |
| `host.services.cert.fingerprint_md5` | text | The MD-5 digest of the entire raw certificate. An identifier used by some systems. |
| `host.services.cert.tbs_no_ct_fingerprint_sha256` | text | The SHA-256 digest of the unsigned certificate with the CT Poison extension removed, if present. This represents the shared contents of a certificate and its corresponding pre-certificate. |
| `host.services.cert.ever_seen_in_scan` | boolean | Whether the certificate has ever been presented by a service during a scan. |
| `host.services.cert.names` | text | All the names contained in the certificate from various fields. |
| `host.services.cert.fingerprint_sha1` | text | The SHA-1 digest of the entire raw certificate. An identifier used by some systems. |
| `host.services.cert.added_at` | date | When the certificate was added to the Censys dataset. |
| `host.services.cert.spki_subject_fingerprint_sha256` | text | The SHA-256 digest of the certificate's DER-encoded SubjectPublicKeyInfo concatenated with its Subject. |
| `host.services.cert.ct` | object |  |
| `host.services.cert.ct.entries` | nested |  |
| `host.services.cert.ct.entries.key` | text |  |
| `host.services.cert.ct.entries.value` | object |  |
| `host.services.cert.ct.entries.value.added_to_ct_at` | date | An RFC-3339-formatted timestamp indicating when the certificate was entered into the CT log. |
| `host.services.cert.ct.entries.value.ct_to_censys_at` | date | An RFC-3339-formated timestamp indicating when the certificate was ingested from the CT log into the Censys dataset. |
| `host.services.cert.ct.entries.value.index` | long | Numerical marker of the certificate's place in the CT log. |
| `host.services.cert.validation_level` | keyword | The extent to which the certificate's issuer validated the identity of the entity requesting the certificate. Options include Domain validated (DV), Organization Validated (OV), or Extended Validation (EV). |
| `host.services.cert.parse_status` | keyword |  |
| `host.services.cert.validated_at` | date | When the certificate record's trust was last checked. |
| `host.services.cert.parsed` | object | A record containing all of the data parsed from the certificate. |
| `host.services.cert.parsed.issuer` | object | A record containing the parsed contents of the issuer_dn. |
| `host.services.cert.parsed.issuer.email_address` | text | The emailAddress (E) elements of the Distinguished Name (OID: 1.2.840.113549.1.9.1). |
| `host.services.cert.parsed.issuer.country` | text | The countryName (C) elements of the Distinguished Name (OID: 2.5.4.6). |
| `host.services.cert.parsed.issuer.given_name` | text | The givenName (G) elements of the Distinguished Name (OID: 2.5.4.42). |
| `host.services.cert.parsed.issuer.province` | text | The stateOrProvinceName (ST) elements of the Distinguished Name (OID: 2.5.4.8). |
| `host.services.cert.parsed.issuer.serial_number` | keyword | The serialNumber elements of the Distinguished Name (OID: 2.5.4.5). |
| `host.services.cert.parsed.issuer.jurisdiction_country` | text | The jurisdictionCountry elements of the Distinguished Name (OID: 1.3.6.1.4.1.311.60.2.1.3). |
| `host.services.cert.parsed.issuer.street_address` | text | The streetAddress (STREET) elements of the Distinguished Name (OID: 2.5.4.9). |
| `host.services.cert.parsed.issuer.jurisdiction_locality` | text | The jurisdictionLocality elements of the Distinguished Name (OID: 1.3.6.1.4.1.311.60.2.1.1). |
| `host.services.cert.parsed.issuer.organization` | text | The organizationName (O) elements of the Distinguished Name (OID: 2.5.4.10). |
| `host.services.cert.parsed.issuer.common_name` | text | The commonName (CN) elements of the Distinguished Name (OID: 2.5.4.3). |
| `host.services.cert.parsed.issuer.domain_component` | text | The domainComponent (DC) elements of the Distinguished Name (OID: 0.9.2342.19200300.100.1.25). |
| `host.services.cert.parsed.issuer.organizational_unit` | text | The organizationalUnit (OU) elements of the Distinguished Name (OID: 2.5.4.11). |
| `host.services.cert.parsed.issuer.organization_id` | text |  |
| `host.services.cert.parsed.issuer.locality` | text | The localityName (L) elements of the Distinguished Name (OID: 2.5.4.7). |
| `host.services.cert.parsed.issuer.surname` | text | The surname (SN) elements of the Distinguished Name (OID: 2.5.4.4). |
| `host.services.cert.parsed.issuer.jurisdiction_province` | text | The jurisdictionStateOrProvince elements of the Distinguished Name (OID: 1.3.6.1.4.1.311.60.2.1.2). |
| `host.services.cert.parsed.issuer.postal_code` | keyword | The postalCode elements of the Distinguished Name (OID: 2.5.4.17). |
| `host.services.cert.parsed.signature` | object |  |
| `host.services.cert.parsed.signature.self_signed` | boolean | Whether the certificate was signed by its own key. |
| `host.services.cert.parsed.signature.signature_algorithm` | object |  |
| `host.services.cert.parsed.signature.signature_algorithm.oid` | text |  |
| `host.services.cert.parsed.signature.signature_algorithm.name` | text | Name of public key type, such as RSA or ECDSA. Information specific to the key type is available in the named sub-record. |
| `host.services.cert.parsed.signature.valid` | boolean | Whether the signature is valid. |
| `host.services.cert.parsed.signature.value` | text | Contents of the signature. |
| `host.services.cert.parsed.redacted` | boolean |  |
| `host.services.cert.parsed.version` | integer |  |
| `host.services.cert.parsed.subject_dn` | text | Distinguished Name of the entity associated with the public key. |
| `host.services.cert.parsed.validity_period` | object | Information about the time for which the certificate is valid. |
| `host.services.cert.parsed.validity_period.length_seconds` | long | The duration of the certificate's validity period, in seconds. |
| `host.services.cert.parsed.validity_period.not_after` | date | An RFC-3339-formatted timestamp after which the certificate is no longer valid. |
| `host.services.cert.parsed.validity_period.not_before` | date | An RFC-3339-formatted timestamp before which the certificate is not valid. |
| `host.services.cert.parsed.extensions` | object | A record containing parsed X.509 extensions that provide additional identification information or additional cryptographic capabilities. |
| `host.services.cert.parsed.extensions.authority_key_id` | text | A key identifier, usually a digest of the DER-encoded SubjectPublicKeyInfo. |
| `host.services.cert.parsed.extensions.crl_distribution_points` | text | The parsed id-ce-cRLDistributionPoints extension (OID: 2.5.29.31). Contents are a list of distributionPoint URLs; other distributionPoint types are omitted). |
| `host.services.cert.parsed.extensions.qc_statements` | object |  |
| `host.services.cert.parsed.extensions.qc_statements.parsed` | object |  |
| `host.services.cert.parsed.extensions.qc_statements.parsed.etsi_compliance` | boolean |  |
| `host.services.cert.parsed.extensions.qc_statements.parsed.legislation` | nested |  |
| `host.services.cert.parsed.extensions.qc_statements.parsed.legislation.country_codes` | text |  |
| `host.services.cert.parsed.extensions.qc_statements.parsed.limit` | nested |  |
| `host.services.cert.parsed.extensions.qc_statements.parsed.limit.currency` | text |  |
| `host.services.cert.parsed.extensions.qc_statements.parsed.limit.currency_number` | long |  |
| `host.services.cert.parsed.extensions.qc_statements.parsed.limit.exponent` | long |  |
| `host.services.cert.parsed.extensions.qc_statements.parsed.limit.amount` | long |  |
| `host.services.cert.parsed.extensions.qc_statements.parsed.pds_locations` | nested |  |
| `host.services.cert.parsed.extensions.qc_statements.parsed.pds_locations.language` | text |  |
| `host.services.cert.parsed.extensions.qc_statements.parsed.pds_locations.url` | text |  |
| `host.services.cert.parsed.extensions.qc_statements.parsed.retention_period` | long |  |
| `host.services.cert.parsed.extensions.qc_statements.parsed.sscd` | boolean |  |
| `host.services.cert.parsed.extensions.qc_statements.parsed.types` | nested |  |
| `host.services.cert.parsed.extensions.qc_statements.parsed.types.ids` | text |  |
| `host.services.cert.parsed.extensions.qc_statements.ids` | text |  |
| `host.services.cert.parsed.extensions.issuer_alt_name` | object | The parsed id-ce-issuerAltName extension (OID: 2.5.29.18). |
| `host.services.cert.parsed.extensions.issuer_alt_name.registered_ids` | text | The parsed registeredID entries in the GeneralName. Stored in dotted-decimal format. |
| `host.services.cert.parsed.extensions.issuer_alt_name.uniform_resource_identifiers` | text | The parsed uniformResourceIdentifier entries in the GeneralName. |
| `host.services.cert.parsed.extensions.issuer_alt_name.directory_names` | nested | The parsed directoryName entries in the GeneralName. |
| `host.services.cert.parsed.extensions.issuer_alt_name.directory_names.organization_id` | text |  |
| `host.services.cert.parsed.extensions.issuer_alt_name.directory_names.organization` | text | The organizationName (O) elements of the Distinguished Name (OID: 2.5.4.10). |
| `host.services.cert.parsed.extensions.issuer_alt_name.directory_names.serial_number` | keyword | The serialNumber elements of the Distinguished Name (OID: 2.5.4.5). |
| `host.services.cert.parsed.extensions.issuer_alt_name.directory_names.jurisdiction_province` | text | The jurisdictionStateOrProvince elements of the Distinguished Name (OID: 1.3.6.1.4.1.311.60.2.1.2). |
| `host.services.cert.parsed.extensions.issuer_alt_name.directory_names.jurisdiction_locality` | text | The jurisdictionLocality elements of the Distinguished Name (OID: 1.3.6.1.4.1.311.60.2.1.1). |
| `host.services.cert.parsed.extensions.issuer_alt_name.directory_names.common_name` | text | The commonName (CN) elements of the Distinguished Name (OID: 2.5.4.3). |
| `host.services.cert.parsed.extensions.issuer_alt_name.directory_names.locality` | text | The localityName (L) elements of the Distinguished Name (OID: 2.5.4.7). |
| `host.services.cert.parsed.extensions.issuer_alt_name.directory_names.street_address` | text | The streetAddress (STREET) elements of the Distinguished Name (OID: 2.5.4.9). |
| `host.services.cert.parsed.extensions.issuer_alt_name.directory_names.country` | text | The countryName (C) elements of the Distinguished Name (OID: 2.5.4.6). |
| `host.services.cert.parsed.extensions.issuer_alt_name.directory_names.surname` | text | The surname (SN) elements of the Distinguished Name (OID: 2.5.4.4). |
| `host.services.cert.parsed.extensions.issuer_alt_name.directory_names.province` | text | The stateOrProvinceName (ST) elements of the Distinguished Name (OID: 2.5.4.8). |
| `host.services.cert.parsed.extensions.issuer_alt_name.directory_names.domain_component` | text | The domainComponent (DC) elements of the Distinguished Name (OID: 0.9.2342.19200300.100.1.25). |
| `host.services.cert.parsed.extensions.issuer_alt_name.directory_names.email_address` | text | The emailAddress (E) elements of the Distinguished Name (OID: 1.2.840.113549.1.9.1). |
| `host.services.cert.parsed.extensions.issuer_alt_name.directory_names.jurisdiction_country` | text | The jurisdictionCountry elements of the Distinguished Name (OID: 1.3.6.1.4.1.311.60.2.1.3). |
| `host.services.cert.parsed.extensions.issuer_alt_name.directory_names.organizational_unit` | text | The organizationalUnit (OU) elements of the Distinguished Name (OID: 2.5.4.11). |
| `host.services.cert.parsed.extensions.issuer_alt_name.directory_names.postal_code` | keyword | The postalCode elements of the Distinguished Name (OID: 2.5.4.17). |
| `host.services.cert.parsed.extensions.issuer_alt_name.directory_names.given_name` | text | The givenName (G) elements of the Distinguished Name (OID: 2.5.4.42). |
| `host.services.cert.parsed.extensions.issuer_alt_name.dns_names` | text | The parsed dNSName entries in the GeneralName. |
| `host.services.cert.parsed.extensions.issuer_alt_name.edi_party_names` | nested | The parsed eDIPartyName entries in the GeneralName. |
| `host.services.cert.parsed.extensions.issuer_alt_name.edi_party_names.name_assigner` | text |  |
| `host.services.cert.parsed.extensions.issuer_alt_name.edi_party_names.party_name` | text |  |
| `host.services.cert.parsed.extensions.issuer_alt_name.email_addresses` | text | The parsed rfc822Name entries in the GeneralName. |
| `host.services.cert.parsed.extensions.issuer_alt_name.ip_addresses` | text | The parsed ipAddress entries in the GeneralName. |
| `host.services.cert.parsed.extensions.issuer_alt_name.other_names` | nested | The parsed otherName entries in the GeneralName. An arbitrary binary value identified by an OID. |
| `host.services.cert.parsed.extensions.issuer_alt_name.other_names.id` | text | The OID identifying the syntax of the otherName value. |
| `host.services.cert.parsed.extensions.issuer_alt_name.other_names.value` | text | The raw otherName value. |
| `host.services.cert.parsed.extensions.signed_certificate_timestamps` | nested |  |
| `host.services.cert.parsed.extensions.signed_certificate_timestamps.timestamp` | date |  |
| `host.services.cert.parsed.extensions.signed_certificate_timestamps.version` | integer |  |
| `host.services.cert.parsed.extensions.signed_certificate_timestamps.log_id` | text |  |
| `host.services.cert.parsed.extensions.signed_certificate_timestamps.signature` | object |  |
| `host.services.cert.parsed.extensions.signed_certificate_timestamps.signature.signature` | text |  |
| `host.services.cert.parsed.extensions.signed_certificate_timestamps.signature.signature_algorithm` | text |  |
| `host.services.cert.parsed.extensions.signed_certificate_timestamps.signature.hash_algorithm` | text |  |
| `host.services.cert.parsed.extensions.extended_key_usage` | object | The parsed id-ce-extKeyUsage extension (OID: 2.5.29.37). |
| `host.services.cert.parsed.extensions.extended_key_usage.microsoft_license_server` | boolean |  |
| `host.services.cert.parsed.extensions.extended_key_usage.microsoft_qualified_subordinate` | boolean |  |
| `host.services.cert.parsed.extensions.extended_key_usage.microsoft_timestamp_signing` | boolean |  |
| `host.services.cert.parsed.extensions.extended_key_usage.microsoft_root_list_signer` | boolean |  |
| `host.services.cert.parsed.extensions.extended_key_usage.ocsp_signing` | boolean |  |
| `host.services.cert.parsed.extensions.extended_key_usage.sbgp_cert_aa_service_auth` | boolean |  |
| `host.services.cert.parsed.extensions.extended_key_usage.apple_code_signing_development` | boolean |  |
| `host.services.cert.parsed.extensions.extended_key_usage.dvcs` | boolean |  |
| `host.services.cert.parsed.extensions.extended_key_usage.microsoft_csp_signature` | boolean |  |
| `host.services.cert.parsed.extensions.extended_key_usage.microsoft_drm` | boolean |  |
| `host.services.cert.parsed.extensions.extended_key_usage.microsoft_licenses` | boolean |  |
| `host.services.cert.parsed.extensions.extended_key_usage.apple_crypto_tier2_qos` | boolean |  |
| `host.services.cert.parsed.extensions.extended_key_usage.microsoft_system_health` | boolean |  |
| `host.services.cert.parsed.extensions.extended_key_usage.microsoft_nt5_crypto` | boolean |  |
| `host.services.cert.parsed.extensions.extended_key_usage.apple_crypto_env` | boolean |  |
| `host.services.cert.parsed.extensions.extended_key_usage.microsoft_drm_individualization` | boolean |  |
| `host.services.cert.parsed.extensions.extended_key_usage.apple_crypto_test_env` | boolean |  |
| `host.services.cert.parsed.extensions.extended_key_usage.microsoft_whql_crypto` | boolean |  |
| `host.services.cert.parsed.extensions.extended_key_usage.apple_crypto_development_env` | boolean |  |
| `host.services.cert.parsed.extensions.extended_key_usage.microsoft_encrypted_file_system` | boolean |  |
| `host.services.cert.parsed.extensions.extended_key_usage.email_protection` | boolean |  |
| `host.services.cert.parsed.extensions.extended_key_usage.ipsec_user` | boolean |  |
| `host.services.cert.parsed.extensions.extended_key_usage.ipsec_end_system` | boolean |  |
| `host.services.cert.parsed.extensions.extended_key_usage.netscape_server_gated_crypto` | boolean |  |
| `host.services.cert.parsed.extensions.extended_key_usage.microsoft_smartcard_logon` | boolean |  |
| `host.services.cert.parsed.extensions.extended_key_usage.microsoft_document_signing` | boolean |  |
| `host.services.cert.parsed.extensions.extended_key_usage.apple_crypto_maintenance_env` | boolean |  |
| `host.services.cert.parsed.extensions.extended_key_usage.apple_ichat_signing` | boolean |  |
| `host.services.cert.parsed.extensions.extended_key_usage.server_auth` | boolean |  |
| `host.services.cert.parsed.extensions.extended_key_usage.apple_software_update_signing` | boolean |  |
| `host.services.cert.parsed.extensions.extended_key_usage.microsoft_lifetime_signing` | boolean |  |
| `host.services.cert.parsed.extensions.extended_key_usage.apple_crypto_qos` | boolean |  |
| `host.services.cert.parsed.extensions.extended_key_usage.microsoft_enrollment_agent` | boolean |  |
| `host.services.cert.parsed.extensions.extended_key_usage.microsoft_smart_display` | boolean |  |
| `host.services.cert.parsed.extensions.extended_key_usage.unknown` | text |  |
| `host.services.cert.parsed.extensions.extended_key_usage.any` | boolean |  |
| `host.services.cert.parsed.extensions.extended_key_usage.apple_code_signing_third_party` | boolean |  |
| `host.services.cert.parsed.extensions.extended_key_usage.ipsec_tunnel` | boolean |  |
| `host.services.cert.parsed.extensions.extended_key_usage.ipsec_intermediate_system_usage` | boolean |  |
| `host.services.cert.parsed.extensions.extended_key_usage.microsoft_key_recovery_21` | boolean |  |
| `host.services.cert.parsed.extensions.extended_key_usage.eap_over_ppp` | boolean |  |
| `host.services.cert.parsed.extensions.extended_key_usage.microsoft_system_health_loophole` | boolean |  |
| `host.services.cert.parsed.extensions.extended_key_usage.code_signing` | boolean |  |
| `host.services.cert.parsed.extensions.extended_key_usage.apple_code_signing` | boolean |  |
| `host.services.cert.parsed.extensions.extended_key_usage.apple_crypto_tier3_qos` | boolean |  |
| `host.services.cert.parsed.extensions.extended_key_usage.microsoft_oem_whql_crypto` | boolean |  |
| `host.services.cert.parsed.extensions.extended_key_usage.apple_ichat_encryption` | boolean |  |
| `host.services.cert.parsed.extensions.extended_key_usage.microsoft_embedded_nt_crypto` | boolean |  |
| `host.services.cert.parsed.extensions.extended_key_usage.microsoft_key_recovery_3` | boolean |  |
| `host.services.cert.parsed.extensions.extended_key_usage.eap_over_lan` | boolean |  |
| `host.services.cert.parsed.extensions.extended_key_usage.apple_crypto_production_env` | boolean |  |
| `host.services.cert.parsed.extensions.extended_key_usage.microsoft_efs_recovery` | boolean |  |
| `host.services.cert.parsed.extensions.extended_key_usage.time_stamping` | boolean |  |
| `host.services.cert.parsed.extensions.extended_key_usage.microsoft_ca_exchange` | boolean |  |
| `host.services.cert.parsed.extensions.extended_key_usage.apple_crypto_tier0_qos` | boolean |  |
| `host.services.cert.parsed.extensions.extended_key_usage.apple_system_identity` | boolean |  |
| `host.services.cert.parsed.extensions.extended_key_usage.microsoft_server_gated_crypto` | boolean |  |
| `host.services.cert.parsed.extensions.extended_key_usage.apple_resource_signing` | boolean |  |
| `host.services.cert.parsed.extensions.extended_key_usage.apple_crypto_tier1_qos` | boolean |  |
| `host.services.cert.parsed.extensions.extended_key_usage.microsoft_cert_trust_list_signing` | boolean |  |
| `host.services.cert.parsed.extensions.extended_key_usage.microsoft_kernel_mode_code_signing` | boolean |  |
| `host.services.cert.parsed.extensions.extended_key_usage.microsoft_mobile_device_software` | boolean |  |
| `host.services.cert.parsed.extensions.extended_key_usage.microsoft_sgc_serialized` | boolean |  |
| `host.services.cert.parsed.extensions.extended_key_usage.client_auth` | boolean |  |
| `host.services.cert.parsed.extensions.name_constraints` | object | The parsed id-ce-nameConstraints extension (OID: 2.5.29.30). Specifies a name space within which all child certificates' subject names MUST be located. |
| `host.services.cert.parsed.extensions.name_constraints.excluded_names` | text | A record providing a range of excluded names of the type dNSName in leaf certificates whose trust path includes this certificate. |
| `host.services.cert.parsed.extensions.name_constraints.permitted_registered_ids` | text | A record providing permitted names of the type registeredID in leaf certificates whose trust path includes this certificate. |
| `host.services.cert.parsed.extensions.name_constraints.permitted_edi_party_names` | nested | A record providing permitted names of the type ediPartyName in leaf certificates whose trust path includes this certificate. |
| `host.services.cert.parsed.extensions.name_constraints.permitted_edi_party_names.name_assigner` | text |  |
| `host.services.cert.parsed.extensions.name_constraints.permitted_edi_party_names.party_name` | text |  |
| `host.services.cert.parsed.extensions.name_constraints.critical` | boolean |  |
| `host.services.cert.parsed.extensions.name_constraints.excluded_directory_names` | nested | A record providing excluded names of the type directoryName in leaf certificates whose trust path includes this certificate. |
| `host.services.cert.parsed.extensions.name_constraints.excluded_directory_names.given_name` | text | The givenName (G) elements of the Distinguished Name (OID: 2.5.4.42). |
| `host.services.cert.parsed.extensions.name_constraints.excluded_directory_names.jurisdiction_province` | text | The jurisdictionStateOrProvince elements of the Distinguished Name (OID: 1.3.6.1.4.1.311.60.2.1.2). |
| `host.services.cert.parsed.extensions.name_constraints.excluded_directory_names.organization_id` | text |  |
| `host.services.cert.parsed.extensions.name_constraints.excluded_directory_names.domain_component` | text | The domainComponent (DC) elements of the Distinguished Name (OID: 0.9.2342.19200300.100.1.25). |
| `host.services.cert.parsed.extensions.name_constraints.excluded_directory_names.locality` | text | The localityName (L) elements of the Distinguished Name (OID: 2.5.4.7). |
| `host.services.cert.parsed.extensions.name_constraints.excluded_directory_names.email_address` | text | The emailAddress (E) elements of the Distinguished Name (OID: 1.2.840.113549.1.9.1). |
| `host.services.cert.parsed.extensions.name_constraints.excluded_directory_names.postal_code` | keyword | The postalCode elements of the Distinguished Name (OID: 2.5.4.17). |
| `host.services.cert.parsed.extensions.name_constraints.excluded_directory_names.country` | text | The countryName (C) elements of the Distinguished Name (OID: 2.5.4.6). |
| `host.services.cert.parsed.extensions.name_constraints.excluded_directory_names.serial_number` | keyword | The serialNumber elements of the Distinguished Name (OID: 2.5.4.5). |
| `host.services.cert.parsed.extensions.name_constraints.excluded_directory_names.jurisdiction_locality` | text | The jurisdictionLocality elements of the Distinguished Name (OID: 1.3.6.1.4.1.311.60.2.1.1). |
| `host.services.cert.parsed.extensions.name_constraints.excluded_directory_names.street_address` | text | The streetAddress (STREET) elements of the Distinguished Name (OID: 2.5.4.9). |
| `host.services.cert.parsed.extensions.name_constraints.excluded_directory_names.common_name` | text | The commonName (CN) elements of the Distinguished Name (OID: 2.5.4.3). |
| `host.services.cert.parsed.extensions.name_constraints.excluded_directory_names.organization` | text | The organizationName (O) elements of the Distinguished Name (OID: 2.5.4.10). |
| `host.services.cert.parsed.extensions.name_constraints.excluded_directory_names.jurisdiction_country` | text | The jurisdictionCountry elements of the Distinguished Name (OID: 1.3.6.1.4.1.311.60.2.1.3). |
| `host.services.cert.parsed.extensions.name_constraints.excluded_directory_names.province` | text | The stateOrProvinceName (ST) elements of the Distinguished Name (OID: 2.5.4.8). |
| `host.services.cert.parsed.extensions.name_constraints.excluded_directory_names.surname` | text | The surname (SN) elements of the Distinguished Name (OID: 2.5.4.4). |
| `host.services.cert.parsed.extensions.name_constraints.excluded_directory_names.organizational_unit` | text | The organizationalUnit (OU) elements of the Distinguished Name (OID: 2.5.4.11). |
| `host.services.cert.parsed.extensions.name_constraints.permitted_names` | text | A record providing a range of permitted names of the type dNSName in leaf certificates whose trust path includes this certificate. |
| `host.services.cert.parsed.extensions.name_constraints.permitted_email_addresses` | text | A record providing a range of permitted names of the type rfc822Name in leaf certificates whose trust path includes this certificate. |
| `host.services.cert.parsed.extensions.name_constraints.excluded_ip_addresses` | nested | A record providing a range of excluded names of the type iPAddress in leaf certificates whose trust path includes this certificate. |
| `host.services.cert.parsed.extensions.name_constraints.excluded_ip_addresses.cidr` | text | The CIDR specifying the subtree. |
| `host.services.cert.parsed.extensions.name_constraints.excluded_ip_addresses.end` | text | The last IP address in the range. |
| `host.services.cert.parsed.extensions.name_constraints.excluded_ip_addresses.mask` | text | The subnet mask of the CIDR. |
| `host.services.cert.parsed.extensions.name_constraints.excluded_ip_addresses.begin` | text | The first IP address in the range. |
| `host.services.cert.parsed.extensions.name_constraints.excluded_email_addresses` | text | A record providing a range of excluded names of the type rfc822Name in leaf certificates whose trust path includes this certificate. |
| `host.services.cert.parsed.extensions.name_constraints.excluded_registered_ids` | text | A record providing excluded names of the type registeredID in leaf certificates whose trust path includes this certificate. |
| `host.services.cert.parsed.extensions.name_constraints.excluded_edi_party_names` | nested | A record providing excluded names of the type ediPartyName in leaf certificates whose trust path includes this certificate. |
| `host.services.cert.parsed.extensions.name_constraints.excluded_edi_party_names.name_assigner` | text |  |
| `host.services.cert.parsed.extensions.name_constraints.excluded_edi_party_names.party_name` | text |  |
| `host.services.cert.parsed.extensions.name_constraints.excluded_uris` | text | A record providing a range of excluded uniform resource identifiers in leaf certificates whose trust path includes this certificate. |
| `host.services.cert.parsed.extensions.name_constraints.permitted_directory_names` | nested | A record providing permitted names of the type directoryName in leaf certificates whose trust path includes this certificate. |
| `host.services.cert.parsed.extensions.name_constraints.permitted_directory_names.jurisdiction_province` | text | The jurisdictionStateOrProvince elements of the Distinguished Name (OID: 1.3.6.1.4.1.311.60.2.1.2). |
| `host.services.cert.parsed.extensions.name_constraints.permitted_directory_names.serial_number` | keyword | The serialNumber elements of the Distinguished Name (OID: 2.5.4.5). |
| `host.services.cert.parsed.extensions.name_constraints.permitted_directory_names.surname` | text | The surname (SN) elements of the Distinguished Name (OID: 2.5.4.4). |
| `host.services.cert.parsed.extensions.name_constraints.permitted_directory_names.organization_id` | text |  |
| `host.services.cert.parsed.extensions.name_constraints.permitted_directory_names.postal_code` | keyword | The postalCode elements of the Distinguished Name (OID: 2.5.4.17). |
| `host.services.cert.parsed.extensions.name_constraints.permitted_directory_names.email_address` | text | The emailAddress (E) elements of the Distinguished Name (OID: 1.2.840.113549.1.9.1). |
| `host.services.cert.parsed.extensions.name_constraints.permitted_directory_names.country` | text | The countryName (C) elements of the Distinguished Name (OID: 2.5.4.6). |
| `host.services.cert.parsed.extensions.name_constraints.permitted_directory_names.organization` | text | The organizationName (O) elements of the Distinguished Name (OID: 2.5.4.10). |
| `host.services.cert.parsed.extensions.name_constraints.permitted_directory_names.street_address` | text | The streetAddress (STREET) elements of the Distinguished Name (OID: 2.5.4.9). |
| `host.services.cert.parsed.extensions.name_constraints.permitted_directory_names.locality` | text | The localityName (L) elements of the Distinguished Name (OID: 2.5.4.7). |
| `host.services.cert.parsed.extensions.name_constraints.permitted_directory_names.jurisdiction_locality` | text | The jurisdictionLocality elements of the Distinguished Name (OID: 1.3.6.1.4.1.311.60.2.1.1). |
| `host.services.cert.parsed.extensions.name_constraints.permitted_directory_names.common_name` | text | The commonName (CN) elements of the Distinguished Name (OID: 2.5.4.3). |
| `host.services.cert.parsed.extensions.name_constraints.permitted_directory_names.given_name` | text | The givenName (G) elements of the Distinguished Name (OID: 2.5.4.42). |
| `host.services.cert.parsed.extensions.name_constraints.permitted_directory_names.domain_component` | text | The domainComponent (DC) elements of the Distinguished Name (OID: 0.9.2342.19200300.100.1.25). |
| `host.services.cert.parsed.extensions.name_constraints.permitted_directory_names.organizational_unit` | text | The organizationalUnit (OU) elements of the Distinguished Name (OID: 2.5.4.11). |
| `host.services.cert.parsed.extensions.name_constraints.permitted_directory_names.jurisdiction_country` | text | The jurisdictionCountry elements of the Distinguished Name (OID: 1.3.6.1.4.1.311.60.2.1.3). |
| `host.services.cert.parsed.extensions.name_constraints.permitted_directory_names.province` | text | The stateOrProvinceName (ST) elements of the Distinguished Name (OID: 2.5.4.8). |
| `host.services.cert.parsed.extensions.name_constraints.permitted_uris` | text | A record providing a range of permitted uniform resource identifiers in leaf certificates whose trust path includes this certificate. |
| `host.services.cert.parsed.extensions.name_constraints.permitted_ip_addresses` | nested | A record providing a range of permitted names of the type iPAddress in leaf certificates whose trust path includes this certificate. |
| `host.services.cert.parsed.extensions.name_constraints.permitted_ip_addresses.cidr` | text | The CIDR specifying the subtree. |
| `host.services.cert.parsed.extensions.name_constraints.permitted_ip_addresses.end` | text | The last IP address in the range. |
| `host.services.cert.parsed.extensions.name_constraints.permitted_ip_addresses.mask` | text | The subnet mask of the CIDR. |
| `host.services.cert.parsed.extensions.name_constraints.permitted_ip_addresses.begin` | text | The first IP address in the range. |
| `host.services.cert.parsed.extensions.cabf_organization_id` | object | CA/Browser Forum organization ID extensions (OID: 2.23.140.3.1). |
| `host.services.cert.parsed.extensions.cabf_organization_id.state` | text |  |
| `host.services.cert.parsed.extensions.cabf_organization_id.country` | text |  |
| `host.services.cert.parsed.extensions.cabf_organization_id.reference` | text |  |
| `host.services.cert.parsed.extensions.cabf_organization_id.scheme` | text |  |
| `host.services.cert.parsed.extensions.subject_alt_name` | object | The parsed id-ce-subjectAltName extension (OID: 2.5.29.17). |
| `host.services.cert.parsed.extensions.subject_alt_name.email_addresses` | text | The parsed rfc822Name entries in the GeneralName. |
| `host.services.cert.parsed.extensions.subject_alt_name.ip_addresses` | text | The parsed ipAddress entries in the GeneralName. |
| `host.services.cert.parsed.extensions.subject_alt_name.other_names` | nested | The parsed otherName entries in the GeneralName. An arbitrary binary value identified by an OID. |
| `host.services.cert.parsed.extensions.subject_alt_name.other_names.id` | text | The OID identifying the syntax of the otherName value. |
| `host.services.cert.parsed.extensions.subject_alt_name.other_names.value` | text | The raw otherName value. |
| `host.services.cert.parsed.extensions.subject_alt_name.registered_ids` | text | The parsed registeredID entries in the GeneralName. Stored in dotted-decimal format. |
| `host.services.cert.parsed.extensions.subject_alt_name.uniform_resource_identifiers` | text | The parsed uniformResourceIdentifier entries in the GeneralName. |
| `host.services.cert.parsed.extensions.subject_alt_name.directory_names` | nested | The parsed directoryName entries in the GeneralName. |
| `host.services.cert.parsed.extensions.subject_alt_name.directory_names.jurisdiction_province` | text | The jurisdictionStateOrProvince elements of the Distinguished Name (OID: 1.3.6.1.4.1.311.60.2.1.2). |
| `host.services.cert.parsed.extensions.subject_alt_name.directory_names.province` | text | The stateOrProvinceName (ST) elements of the Distinguished Name (OID: 2.5.4.8). |
| `host.services.cert.parsed.extensions.subject_alt_name.directory_names.postal_code` | keyword | The postalCode elements of the Distinguished Name (OID: 2.5.4.17). |
| `host.services.cert.parsed.extensions.subject_alt_name.directory_names.jurisdiction_country` | text | The jurisdictionCountry elements of the Distinguished Name (OID: 1.3.6.1.4.1.311.60.2.1.3). |
| `host.services.cert.parsed.extensions.subject_alt_name.directory_names.jurisdiction_locality` | text | The jurisdictionLocality elements of the Distinguished Name (OID: 1.3.6.1.4.1.311.60.2.1.1). |
| `host.services.cert.parsed.extensions.subject_alt_name.directory_names.country` | text | The countryName (C) elements of the Distinguished Name (OID: 2.5.4.6). |
| `host.services.cert.parsed.extensions.subject_alt_name.directory_names.domain_component` | text | The domainComponent (DC) elements of the Distinguished Name (OID: 0.9.2342.19200300.100.1.25). |
| `host.services.cert.parsed.extensions.subject_alt_name.directory_names.organization_id` | text |  |
| `host.services.cert.parsed.extensions.subject_alt_name.directory_names.serial_number` | keyword | The serialNumber elements of the Distinguished Name (OID: 2.5.4.5). |
| `host.services.cert.parsed.extensions.subject_alt_name.directory_names.locality` | text | The localityName (L) elements of the Distinguished Name (OID: 2.5.4.7). |
| `host.services.cert.parsed.extensions.subject_alt_name.directory_names.organization` | text | The organizationName (O) elements of the Distinguished Name (OID: 2.5.4.10). |
| `host.services.cert.parsed.extensions.subject_alt_name.directory_names.email_address` | text | The emailAddress (E) elements of the Distinguished Name (OID: 1.2.840.113549.1.9.1). |
| `host.services.cert.parsed.extensions.subject_alt_name.directory_names.common_name` | text | The commonName (CN) elements of the Distinguished Name (OID: 2.5.4.3). |
| `host.services.cert.parsed.extensions.subject_alt_name.directory_names.given_name` | text | The givenName (G) elements of the Distinguished Name (OID: 2.5.4.42). |
| `host.services.cert.parsed.extensions.subject_alt_name.directory_names.surname` | text | The surname (SN) elements of the Distinguished Name (OID: 2.5.4.4). |
| `host.services.cert.parsed.extensions.subject_alt_name.directory_names.organizational_unit` | text | The organizationalUnit (OU) elements of the Distinguished Name (OID: 2.5.4.11). |
| `host.services.cert.parsed.extensions.subject_alt_name.directory_names.street_address` | text | The streetAddress (STREET) elements of the Distinguished Name (OID: 2.5.4.9). |
| `host.services.cert.parsed.extensions.subject_alt_name.dns_names` | text | The parsed dNSName entries in the GeneralName. |
| `host.services.cert.parsed.extensions.subject_alt_name.edi_party_names` | nested | The parsed eDIPartyName entries in the GeneralName. |
| `host.services.cert.parsed.extensions.subject_alt_name.edi_party_names.party_name` | text |  |
| `host.services.cert.parsed.extensions.subject_alt_name.edi_party_names.name_assigner` | text |  |
| `host.services.cert.parsed.extensions.authority_info_access` | object | The parsed id-pe-authorityInfoAccess extension (OID: 1.3.6.1.5.7.1.1). Only id-ad-caIssuers and id-ad-ocsp accessMethods are supported; others are omitted. |
| `host.services.cert.parsed.extensions.authority_info_access.ocsp_urls` | text |  |
| `host.services.cert.parsed.extensions.authority_info_access.issuer_urls` | text |  |
| `host.services.cert.parsed.extensions.basic_constraints` | object | The parsed id-ce-basicConstraints extension (OID: 2.5.29.19). |
| `host.services.cert.parsed.extensions.basic_constraints.is_ca` | boolean | Whether the certificate is permitted to sign other certificates. |
| `host.services.cert.parsed.extensions.basic_constraints.max_path_len` | integer | When present, provides the maximum number of intermediate certificates that may follow this certificate in a trusted certification path. |
| `host.services.cert.parsed.extensions.ct_poison` | boolean | Whether the certificate possesses the pre-certificate "poison" extension (OID: 1.3.6.1.4.1.11129.2.4.3). |
| `host.services.cert.parsed.extensions.tor_service_descriptors` | nested |  |
| `host.services.cert.parsed.extensions.tor_service_descriptors.algorithm_name` | text |  |
| `host.services.cert.parsed.extensions.tor_service_descriptors.hash` | text |  |
| `host.services.cert.parsed.extensions.tor_service_descriptors.hash_bits` | integer |  |
| `host.services.cert.parsed.extensions.tor_service_descriptors.onion` | text |  |
| `host.services.cert.parsed.extensions.key_usage` | object | The parsed id-ce-keyUsage extension (OID: 2.5.29.15). |
| `host.services.cert.parsed.extensions.key_usage.content_commitment` | boolean | Whether the contentCommitment (formerly called nonRepudiation) bit is set. |
| `host.services.cert.parsed.extensions.key_usage.digital_signature` | boolean | Whether the digitalSignature bit is set. |
| `host.services.cert.parsed.extensions.key_usage.key_agreement` | boolean | Whether the keyAgreement bit is set. |
| `host.services.cert.parsed.extensions.key_usage.decipher_only` | boolean | Whether the decipherOnly bit is set. |
| `host.services.cert.parsed.extensions.key_usage.certificate_sign` | boolean | Whether the keyCertSign bit is set. |
| `host.services.cert.parsed.extensions.key_usage.key_encipherment` | boolean | Whether the keyEncipherment bit is set. |
| `host.services.cert.parsed.extensions.key_usage.crl_sign` | boolean | Whether the cRLSign bit is set. |
| `host.services.cert.parsed.extensions.key_usage.value` | unsigned_long | The integer value of the bitmask in the extension. |
| `host.services.cert.parsed.extensions.key_usage.data_encipherment` | boolean | Whether the dataEncipherment bit is set. |
| `host.services.cert.parsed.extensions.key_usage.encipher_only` | boolean | Whether the encipherOnly bit is set. |
| `host.services.cert.parsed.extensions.certificate_policies` | nested | The parsed id-ce-certificatePolicies extension (OID: 2.5.29.32). |
| `host.services.cert.parsed.extensions.certificate_policies.cps` | text |  |
| `host.services.cert.parsed.extensions.certificate_policies.id` | text |  |
| `host.services.cert.parsed.extensions.certificate_policies.user_notice` | nested |  |
| `host.services.cert.parsed.extensions.certificate_policies.user_notice.notice_reference` | object |  |
| `host.services.cert.parsed.extensions.certificate_policies.user_notice.notice_reference.notice_numbers` | integer |  |
| `host.services.cert.parsed.extensions.certificate_policies.user_notice.notice_reference.organization` | text |  |
| `host.services.cert.parsed.extensions.certificate_policies.user_notice.explicit_text` | text |  |
| `host.services.cert.parsed.extensions.subject_key_id` | text | A key identifier, usually a digest of the DER-encoded SubjectPublicKeyInfo.. |
| `host.services.cert.parsed.issuer_dn` | text | Distinguished Name of the entity that has signed and issued the certificate. |
| `host.services.cert.parsed.serial_number_hex` | text | Issuer-specific identifier of the certificate, represented as hexadecimal. |
| `host.services.cert.parsed.ja4x` | text |  |
| `host.services.cert.parsed.serial_number` | text | Issuer-specific identifier of the certificate. |
| `host.services.cert.parsed.subject` | object | A record containing the parsed contents of the subject_dn. |
| `host.services.cert.parsed.subject.organization_id` | text |  |
| `host.services.cert.parsed.subject.street_address` | text | The streetAddress (STREET) elements of the Distinguished Name (OID: 2.5.4.9). |
| `host.services.cert.parsed.subject.given_name` | text | The givenName (G) elements of the Distinguished Name (OID: 2.5.4.42). |
| `host.services.cert.parsed.subject.common_name` | text | The commonName (CN) elements of the Distinguished Name (OID: 2.5.4.3). |
| `host.services.cert.parsed.subject.domain_component` | text | The domainComponent (DC) elements of the Distinguished Name (OID: 0.9.2342.19200300.100.1.25). |
| `host.services.cert.parsed.subject.serial_number` | keyword | The serialNumber elements of the Distinguished Name (OID: 2.5.4.5). |
| `host.services.cert.parsed.subject.email_address` | text | The emailAddress (E) elements of the Distinguished Name (OID: 1.2.840.113549.1.9.1). |
| `host.services.cert.parsed.subject.surname` | text | The surname (SN) elements of the Distinguished Name (OID: 2.5.4.4). |
| `host.services.cert.parsed.subject.postal_code` | keyword | The postalCode elements of the Distinguished Name (OID: 2.5.4.17). |
| `host.services.cert.parsed.subject.province` | text | The stateOrProvinceName (ST) elements of the Distinguished Name (OID: 2.5.4.8). |
| `host.services.cert.parsed.subject.locality` | text | The localityName (L) elements of the Distinguished Name (OID: 2.5.4.7). |
| `host.services.cert.parsed.subject.jurisdiction_locality` | text | The jurisdictionLocality elements of the Distinguished Name (OID: 1.3.6.1.4.1.311.60.2.1.1). |
| `host.services.cert.parsed.subject.jurisdiction_country` | text | The jurisdictionCountry elements of the Distinguished Name (OID: 1.3.6.1.4.1.311.60.2.1.3). |
| `host.services.cert.parsed.subject.jurisdiction_province` | text | The jurisdictionStateOrProvince elements of the Distinguished Name (OID: 1.3.6.1.4.1.311.60.2.1.2). |
| `host.services.cert.parsed.subject.country` | text | The countryName (C) elements of the Distinguished Name (OID: 2.5.4.6). |
| `host.services.cert.parsed.subject.organization` | text | The organizationName (O) elements of the Distinguished Name (OID: 2.5.4.10). |
| `host.services.cert.parsed.subject.organizational_unit` | text | The organizationalUnit (OU) elements of the Distinguished Name (OID: 2.5.4.11). |
| `host.services.cert.parsed.unknown_extensions` | nested |  |
| `host.services.cert.parsed.unknown_extensions.critical` | boolean |  |
| `host.services.cert.parsed.unknown_extensions.id` | text |  |
| `host.services.cert.parsed.unknown_extensions.value` | text |  |
| `host.services.cert.parsed.subject_key_info` | object | Information about the certificate's public key. |
| `host.services.cert.parsed.subject_key_info.ecdsa` | object | A record containing the public portion of an ECDSA asymmetric key. |
| `host.services.cert.parsed.subject_key_info.ecdsa.n` | text |  |
| `host.services.cert.parsed.subject_key_info.ecdsa.length` | long |  |
| `host.services.cert.parsed.subject_key_info.ecdsa.y` | text |  |
| `host.services.cert.parsed.subject_key_info.ecdsa.curve` | text |  |
| `host.services.cert.parsed.subject_key_info.ecdsa.b` | text |  |
| `host.services.cert.parsed.subject_key_info.ecdsa.gy` | text |  |
| `host.services.cert.parsed.subject_key_info.ecdsa.p` | text |  |
| `host.services.cert.parsed.subject_key_info.ecdsa.x` | text |  |
| `host.services.cert.parsed.subject_key_info.ecdsa.pub` | text |  |
| `host.services.cert.parsed.subject_key_info.ecdsa.gx` | text |  |
| `host.services.cert.parsed.subject_key_info.fingerprint_sha256` | text | The SHA-256 digest of the certificate's DER-encoded SubjectPublicKeyInfo. |
| `host.services.cert.parsed.subject_key_info.key_algorithm` | object | A record containing information about the type of subject key algorithm and any relevant parameters. |
| `host.services.cert.parsed.subject_key_info.key_algorithm.name` | text | Name of public key type, such as RSA or ECDSA. Information specific to the key type is available in the named sub-record. |
| `host.services.cert.parsed.subject_key_info.key_algorithm.oid` | text |  |
| `host.services.cert.parsed.subject_key_info.rsa` | object | A record containing the public portion of an RSA asymmetric key. |
| `host.services.cert.parsed.subject_key_info.rsa.modulus` | text | The RSA key's modulus (n) in big-endian encoding. |
| `host.services.cert.parsed.subject_key_info.rsa.exponent` | long | The RSA key's public exponent (e). |
| `host.services.cert.parsed.subject_key_info.rsa.length` | long | Bit-length of the RSA modulus. |
| `host.services.cert.parsed.subject_key_info.unrecognized` | object | A record containing known information about an unrecognized key type. |
| `host.services.cert.parsed.subject_key_info.unrecognized.raw` | text |  |
| `host.services.cert.parsed.subject_key_info.dsa` | object | A record containing the public portion of a DSA asymmetric key. |
| `host.services.cert.parsed.subject_key_info.dsa.g` | text |  |
| `host.services.cert.parsed.subject_key_info.dsa.p` | text |  |
| `host.services.cert.parsed.subject_key_info.dsa.q` | text |  |
| `host.services.cert.parsed.subject_key_info.dsa.y` | text |  |
| `host.services.cert.revoked` | boolean | Whether the certificate has been revoked before its expiry date by the issuer. |
| `host.services.cert.revocation` | object | A record containing revocation information, if the certificate has been revoked. |
| `host.services.cert.revocation.crl` | object |  |
| `host.services.cert.revocation.crl.revocation_time` | date | The issuer-supplied timestamp indicating when the certificate was revoked. |
| `host.services.cert.revocation.crl.revoked` | boolean | Whether the certificate has been revoked before its expiry date by the issuer. |
| `host.services.cert.revocation.crl.next_update` | date |  |
| `host.services.cert.revocation.crl.reason` | keyword | An enumerated value indicating the issuer-supplied reason for the revocation. |
| `host.services.cert.revocation.ocsp` | object |  |
| `host.services.cert.revocation.ocsp.next_update` | date |  |
| `host.services.cert.revocation.ocsp.reason` | keyword | An enumerated value indicating the issuer-supplied reason for the revocation. |
| `host.services.cert.revocation.ocsp.revocation_time` | date | The issuer-supplied timestamp indicating when the certificate was revoked. |
| `host.services.cert.revocation.ocsp.revoked` | boolean | Whether the certificate has been revoked before its expiry date by the issuer. |
| `host.services.cert.modified_at` | date | When the certificate record was last modified. |
| `host.services.cert.zlint` | object | A record containing the results of linting the certificate for conformance to the X.509 standard using Zlint. |
| `host.services.cert.zlint.failed_lints` | text | A list of lint names which failed, if applicable. |
| `host.services.cert.zlint.fatals_present` | boolean | Whether the certificate's attributes triggered any fatal lints for non-conformance to the X.509 standard. |
| `host.services.cert.zlint.notices_present` | boolean | Whether the certificate's attributes triggered any notice lints for non-conformance to the X.509 standard. |
| `host.services.cert.zlint.timestamp` | date | An RFC-3339-formated timestamp indicating when the certificate was linted. |
| `host.services.cert.zlint.version` | long | The version of Zlint used to lint the certificate. |
| `host.services.cert.zlint.warnings_present` | boolean | Whether the certificate's attributes triggered any warning lints for non-conformance to the X.509 standard. |
| `host.services.cert.zlint.errors_present` | boolean | Whether the certificate's attributes triggered any error lints for non-conformance to the X.509 standard. |
| `host.services.cert.tbs_fingerprint_sha256` | text | The SHA-256 digest of the unsigned certificate's contents. |
| `host.services.cert.parent_spki_subject_fingerprint_sha256` | text | The SHA-256 digest of the parent certificate's DER-encoded SubjectPublicKeyInfo concatenated with its Subject. |
| `host.services.cert.validation` | object | A record containing information from the maintainers of major root certificate stores related to their trust assessment. |
| `host.services.cert.validation.chrome` | object | A record containing validation information about the certificate from the Chrome root store. |
| `host.services.cert.validation.chrome.had_trusted_path` | boolean | Whether there ever existed a trusted path of signing certificates from a certificate present in the root certificate store. |
| `host.services.cert.validation.chrome.has_trusted_path` | boolean | Whether there currently exists a trusted path of signing certificates from a certificate present in the root certificate store. |
| `host.services.cert.validation.chrome.in_revocation_set` | boolean | Whether the certificate is in the revocation set (e.g. OneCRL) associated with the root store. |
| `host.services.cert.validation.chrome.is_valid` | boolean | Whether the certificate is currently considered valid by the root store: a summary of the trust path, revoked, blocklisted/allowlisted, and expired fields. |
| `host.services.cert.validation.chrome.parents` | text | The SHA-256 fingerprints of the certificate's immediate parents in its trust path(s). |
| `host.services.cert.validation.chrome.type` | keyword | The certificate's type. Options include root, intermediate, or leaf. |
| `host.services.cert.validation.chrome.chains` | nested | A path of trusted signing certificates up to a root certificate present in a root store, represented as an ordered list of SHA-256 fingerprints. |
| `host.services.cert.validation.chrome.chains.sha256fp` | text |  |
| `host.services.cert.validation.chrome.ever_valid` | boolean | Whether the certificate has ever been considered valid by the root store. |
| `host.services.cert.validation.microsoft` | object | A record containing validation information about the certificate from the Microsoft root store. |
| `host.services.cert.validation.microsoft.is_valid` | boolean | Whether the certificate is currently considered valid by the root store: a summary of the trust path, revoked, blocklisted/allowlisted, and expired fields. |
| `host.services.cert.validation.microsoft.parents` | text | The SHA-256 fingerprints of the certificate's immediate parents in its trust path(s). |
| `host.services.cert.validation.microsoft.type` | keyword | The certificate's type. Options include root, intermediate, or leaf. |
| `host.services.cert.validation.microsoft.chains` | nested | A path of trusted signing certificates up to a root certificate present in a root store, represented as an ordered list of SHA-256 fingerprints. |
| `host.services.cert.validation.microsoft.chains.sha256fp` | text |  |
| `host.services.cert.validation.microsoft.ever_valid` | boolean | Whether the certificate has ever been considered valid by the root store. |
| `host.services.cert.validation.microsoft.had_trusted_path` | boolean | Whether there ever existed a trusted path of signing certificates from a certificate present in the root certificate store. |
| `host.services.cert.validation.microsoft.has_trusted_path` | boolean | Whether there currently exists a trusted path of signing certificates from a certificate present in the root certificate store. |
| `host.services.cert.validation.microsoft.in_revocation_set` | boolean | Whether the certificate is in the revocation set (e.g. OneCRL) associated with the root store. |
| `host.services.cert.validation.nss` | object | A record containing validation information about the certificate from the Mozilla NSS root store. |
| `host.services.cert.validation.nss.had_trusted_path` | boolean | Whether there ever existed a trusted path of signing certificates from a certificate present in the root certificate store. |
| `host.services.cert.validation.nss.has_trusted_path` | boolean | Whether there currently exists a trusted path of signing certificates from a certificate present in the root certificate store. |
| `host.services.cert.validation.nss.in_revocation_set` | boolean | Whether the certificate is in the revocation set (e.g. OneCRL) associated with the root store. |
| `host.services.cert.validation.nss.is_valid` | boolean | Whether the certificate is currently considered valid by the root store: a summary of the trust path, revoked, blocklisted/allowlisted, and expired fields. |
| `host.services.cert.validation.nss.parents` | text | The SHA-256 fingerprints of the certificate's immediate parents in its trust path(s). |
| `host.services.cert.validation.nss.type` | keyword | The certificate's type. Options include root, intermediate, or leaf. |
| `host.services.cert.validation.nss.chains` | nested | A path of trusted signing certificates up to a root certificate present in a root store, represented as an ordered list of SHA-256 fingerprints. |
| `host.services.cert.validation.nss.chains.sha256fp` | text |  |
| `host.services.cert.validation.nss.ever_valid` | boolean | Whether the certificate has ever been considered valid by the root store. |
| `host.services.cert.validation.apple` | object | A record containing validation information about the certificate from the Apple root store. |
| `host.services.cert.validation.apple.had_trusted_path` | boolean | Whether there ever existed a trusted path of signing certificates from a certificate present in the root certificate store. |
| `host.services.cert.validation.apple.has_trusted_path` | boolean | Whether there currently exists a trusted path of signing certificates from a certificate present in the root certificate store. |
| `host.services.cert.validation.apple.in_revocation_set` | boolean | Whether the certificate is in the revocation set (e.g. OneCRL) associated with the root store. |
| `host.services.cert.validation.apple.is_valid` | boolean | Whether the certificate is currently considered valid by the root store: a summary of the trust path, revoked, blocklisted/allowlisted, and expired fields. |
| `host.services.cert.validation.apple.parents` | text | The SHA-256 fingerprints of the certificate's immediate parents in its trust path(s). |
| `host.services.cert.validation.apple.type` | keyword | The certificate's type. Options include root, intermediate, or leaf. |
| `host.services.cert.validation.apple.chains` | nested | A path of trusted signing certificates up to a root certificate present in a root store, represented as an ordered list of SHA-256 fingerprints. |
| `host.services.cert.validation.apple.chains.sha256fp` | text |  |
| `host.services.cert.validation.apple.ever_valid` | boolean | Whether the certificate has ever been considered valid by the root store. |
| `host.services.cert.fingerprint_sha256` | text | The SHA-256 digest of the entire raw certificate. Its unique identifier, which Censys uses to index certificates records. |
| `host.services.misconfigs` | nested |  |
| `host.services.misconfigs.cvss` | object |  |
| `host.services.misconfigs.cvss.score` | double | Score of the vulnerability; 0.1 is the lowest, 10 is the maximum |
| `host.services.misconfigs.cvss.vector` | text | The path, method, or scenario used to exploit the vulnerability. Each section represents components that contribute to the overall CVSS score. |
| `host.services.misconfigs.cvss.components` | object | These metrics contribute to how a CVE is scored. |
| `host.services.misconfigs.cvss.components.availability` | keyword | If an attack renders information unavailable, such as when a system crashes or through a DDoS attack, availability is negatively impacted. Availability has three possible values: None (N) – There is no loss of availability, Low (L) – Availability might be intermittently limited, or performance might be negatively impacted, as a result of a successful attack, High (H) – There is a complete loss of availability of the impacted system or information. |
| `host.services.misconfigs.cvss.components.confidentiality` | keyword | Refers to the disclosure of sensitive information to authorized and unauthorized users, with the goal being that only authorized users are able to access the target data. Confidentiality has three potential values: High (H) – The attacker has full access to all resources in the impacted system, including highly sensitive information such as encryption keys, Low (L) – The attacker has partial access to information, with no control over what, specifically, they are able to access, None (N) – No data is accessible to unauthorized users as a result of the exploit. |
| `host.services.misconfigs.cvss.components.integrity` | keyword | Refers to whether the protected information has been tampered with or changed in any way. If there is no way for an attacker to alter the accuracy or completeness of the information, integrity has been maintained. Integrity has three values: None (N) – There is no loss of the integrity of any information, Low (L) – A limited amount of information might be tampered with or modified, but there is no serious impact on the protected system, High (H) – The attacker can modify any/all information on the target system, resulting in a complete loss of integrity. |
| `host.services.misconfigs.cvss.components.privileges_required` | keyword | Describes the level of privileges or access an attacker must have before successful exploitation. There are three possible values: None (N) – There is no privilege or special access required to conduct the attack, Low (L) – The attacker requires basic, “user” level privileges to leverage the exploit, High (H) – Administrative or similar access privileges are required for successful attack. |
| `host.services.misconfigs.cvss.components.scope` | keyword | Determines whether a vulnerability in one system or component can impact another system or component. If a vulnerability in a vulnerable component can affect a component which is in a different security scope than the vulnerable component, a scope change occurs. Scope has two possible ratings: Changed (C) – An exploited vulnerability can have a carry over impact on another system, Unchanged (U) – The exploited vulnerability is limited in damage to only the local security authority. |
| `host.services.misconfigs.cvss.components.user_interaction` | keyword | Describes whether a user, other than the attacker, is required to do anything or participate in exploitation of the vulnerability. User interaction has two possible values: None (N) – No user interaction is required, Required (R) – A user must complete some steps for the exploit to succeed. For example, a user might be required to install some software. |
| `host.services.misconfigs.cvss.components.attack_complexity` | keyword | Indicates conditions beyond the attacker’s control that must exist in order to exploit the vulnerability. The Attack Complexity metric is scored as either Low or High. There are two possible values: Low (L) – There are no specific pre-conditions required for exploitation, High (H) – The attacker must complete some number of preparatory steps in order to get access. |
| `host.services.misconfigs.cvss.components.attack_vector` | keyword | Indicates the level of access required for an attacker to exploit the vulnerability. The Attack Vector metric is scored in one of four levels: Network (N) – Vulnerabilities with this rating are remotely exploitable, from one or more hops away, up to, and including, remote exploitation over the Internet, Adjacent (A) – A vulnerability with this rating requires network adjacency for exploitation. The attack must be launched from the same physical or logical network, Local (L) – Vulnerabilities with this rating are not exploitable over a network, Physical (P) – An attacker must physically interact with the target system. |
| `host.services.misconfigs.evidence` | nested |  |
| `host.services.misconfigs.evidence.found_value` | text |  |
| `host.services.misconfigs.evidence.literal_match` | text |  |
| `host.services.misconfigs.evidence.negative` | boolean |  |
| `host.services.misconfigs.evidence.proprietary` | boolean |  |
| `host.services.misconfigs.evidence.regex` | text |  |
| `host.services.misconfigs.evidence.semver_expression` | text |  |
| `host.services.misconfigs.evidence.data_path` | text |  |
| `host.services.misconfigs.evidence.exists` | boolean |  |
| `host.services.misconfigs.name` | text |  |
| `host.services.misconfigs.type` | text |  |
| `host.services.misconfigs.id` | text |  |
| `host.services.misconfigs.source` | keyword |  |
| `host.services.misconfigs.year` | unsigned_long |  |
| `host.services.misconfigs.severity` | keyword |  |
| `host.services.misconfigs.metrics` | object |  |
| `host.services.misconfigs.metrics.cvss_v31` | object |  |
| `host.services.misconfigs.metrics.cvss_v31.score` | double | Score of the vulnerability; 0.1 is the lowest, 10 is the maximum |
| `host.services.misconfigs.metrics.cvss_v31.vector` | text | The path, method, or scenario used to exploit the vulnerability. Each section represents components that contribute to the overall CVSS score. |
| `host.services.misconfigs.metrics.cvss_v31.components` | object | These metrics contribute to how a CVE is scored. |
| `host.services.misconfigs.metrics.cvss_v31.components.scope` | keyword | Determines whether a vulnerability in one system or component can impact another system or component. If a vulnerability in a vulnerable component can affect a component which is in a different security scope than the vulnerable component, a scope change occurs. Scope has two possible ratings: Changed (C) – An exploited vulnerability can have a carry over impact on another system, Unchanged (U) – The exploited vulnerability is limited in damage to only the local security authority. |
| `host.services.misconfigs.metrics.cvss_v31.components.user_interaction` | keyword | Describes whether a user, other than the attacker, is required to do anything or participate in exploitation of the vulnerability. User interaction has two possible values: None (N) – No user interaction is required, Required (R) – A user must complete some steps for the exploit to succeed. For example, a user might be required to install some software. |
| `host.services.misconfigs.metrics.cvss_v31.components.attack_complexity` | keyword | Indicates conditions beyond the attacker’s control that must exist in order to exploit the vulnerability. The Attack Complexity metric is scored as either Low or High. There are two possible values: Low (L) – There are no specific pre-conditions required for exploitation, High (H) – The attacker must complete some number of preparatory steps in order to get access. |
| `host.services.misconfigs.metrics.cvss_v31.components.attack_vector` | keyword | Indicates the level of access required for an attacker to exploit the vulnerability. The Attack Vector metric is scored in one of four levels: Network (N) – Vulnerabilities with this rating are remotely exploitable, from one or more hops away, up to, and including, remote exploitation over the Internet, Adjacent (A) – A vulnerability with this rating requires network adjacency for exploitation. The attack must be launched from the same physical or logical network, Local (L) – Vulnerabilities with this rating are not exploitable over a network, Physical (P) – An attacker must physically interact with the target system. |
| `host.services.misconfigs.metrics.cvss_v31.components.availability` | keyword | If an attack renders information unavailable, such as when a system crashes or through a DDoS attack, availability is negatively impacted. Availability has three possible values: None (N) – There is no loss of availability, Low (L) – Availability might be intermittently limited, or performance might be negatively impacted, as a result of a successful attack, High (H) – There is a complete loss of availability of the impacted system or information. |
| `host.services.misconfigs.metrics.cvss_v31.components.confidentiality` | keyword | Refers to the disclosure of sensitive information to authorized and unauthorized users, with the goal being that only authorized users are able to access the target data. Confidentiality has three potential values: High (H) – The attacker has full access to all resources in the impacted system, including highly sensitive information such as encryption keys, Low (L) – The attacker has partial access to information, with no control over what, specifically, they are able to access, None (N) – No data is accessible to unauthorized users as a result of the exploit. |
| `host.services.misconfigs.metrics.cvss_v31.components.integrity` | keyword | Refers to whether the protected information has been tampered with or changed in any way. If there is no way for an attacker to alter the accuracy or completeness of the information, integrity has been maintained. Integrity has three values: None (N) – There is no loss of the integrity of any information, Low (L) – A limited amount of information might be tampered with or modified, but there is no serious impact on the protected system, High (H) – The attacker can modify any/all information on the target system, resulting in a complete loss of integrity. |
| `host.services.misconfigs.metrics.cvss_v31.components.privileges_required` | keyword | Describes the level of privileges or access an attacker must have before successful exploitation. There are three possible values: None (N) – There is no privilege or special access required to conduct the attack, Low (L) – The attacker requires basic, “user” level privileges to leverage the exploit, High (H) – Administrative or similar access privileges are required for successful attack. |
| `host.services.misconfigs.metrics.cvss_v40` | object |  |
| `host.services.misconfigs.metrics.cvss_v40.vector` | text | The path, method, or scenario used to exploit the vulnerability. Each section represents components that contribute to the overall CVSS score. |
| `host.services.misconfigs.metrics.cvss_v40.components` | object | These metrics contribute to how a CVE is scored. |
| `host.services.misconfigs.metrics.cvss_v40.components.user_interaction` | keyword | Describes whether a user, other than the attacker, is required to do anything or participate in exploitation of the vulnerability. User interaction has two possible values: None (N) – No user interaction is required, Required (R) – A user must complete some steps for the exploit to succeed. For example, a user might be required to install some software. |
| `host.services.misconfigs.metrics.cvss_v40.components.provider_urgency` | keyword |  |
| `host.services.misconfigs.metrics.cvss_v40.components.confidentiality` | keyword | Refers to the disclosure of sensitive information to authorized and unauthorized users, with the goal being that only authorized users are able to access the target data. Confidentiality has three potential values: High (H) – The attacker has full access to all resources in the impacted system, including highly sensitive information such as encryption keys, Low (L) – The attacker has partial access to information, with no control over what, specifically, they are able to access, None (N) – No data is accessible to unauthorized users as a result of the exploit. |
| `host.services.misconfigs.metrics.cvss_v40.components.availability` | keyword | If an attack renders information unavailable, such as when a system crashes or through a DDoS attack, availability is negatively impacted. Availability has three possible values: None (N) – There is no loss of availability, Low (L) – Availability might be intermittently limited, or performance might be negatively impacted, as a result of a successful attack, High (H) – There is a complete loss of availability of the impacted system or information. |
| `host.services.misconfigs.metrics.cvss_v40.components.privileges_required` | keyword | Describes the level of privileges or access an attacker must have before successful exploitation. There are three possible values: None (N) – There is no privilege or special access required to conduct the attack, Low (L) – The attacker requires basic, “user” level privileges to leverage the exploit, High (H) – Administrative or similar access privileges are required for successful attack. |
| `host.services.misconfigs.metrics.cvss_v40.components.recovery` | keyword |  |
| `host.services.misconfigs.metrics.cvss_v40.components.value_density` | keyword |  |
| `host.services.misconfigs.metrics.cvss_v40.components.attack_requirements` | keyword |  |
| `host.services.misconfigs.metrics.cvss_v40.components.automatable` | keyword |  |
| `host.services.misconfigs.metrics.cvss_v40.components.vulnerability_response_effort` | keyword |  |
| `host.services.misconfigs.metrics.cvss_v40.components.integrity` | keyword | Refers to whether the protected information has been tampered with or changed in any way. If there is no way for an attacker to alter the accuracy or completeness of the information, integrity has been maintained. Integrity has three values: None (N) – There is no loss of the integrity of any information, Low (L) – A limited amount of information might be tampered with or modified, but there is no serious impact on the protected system, High (H) – The attacker can modify any/all information on the target system, resulting in a complete loss of integrity. |
| `host.services.misconfigs.metrics.cvss_v40.components.safety` | keyword |  |
| `host.services.misconfigs.metrics.cvss_v40.components.attack_complexity` | keyword | Indicates conditions beyond the attacker’s control that must exist in order to exploit the vulnerability. The Attack Complexity metric is scored as either Low or High. There are two possible values: Low (L) – There are no specific pre-conditions required for exploitation, High (H) – The attacker must complete some number of preparatory steps in order to get access. |
| `host.services.misconfigs.metrics.cvss_v40.components.attack_vector` | keyword | Indicates the level of access required for an attacker to exploit the vulnerability. The Attack Vector metric is scored in one of four levels: Network (N) – Vulnerabilities with this rating are remotely exploitable, from one or more hops away, up to, and including, remote exploitation over the Internet, Adjacent (A) – A vulnerability with this rating requires network adjacency for exploitation. The attack must be launched from the same physical or logical network, Local (L) – Vulnerabilities with this rating are not exploitable over a network, Physical (P) – An attacker must physically interact with the target system. |
| `host.services.misconfigs.metrics.cvss_v40.score` | double | Score of the vulnerability; 0.1 is the lowest, 10 is the maximum |
| `host.services.misconfigs.metrics.epss` | object |  |
| `host.services.misconfigs.metrics.epss.percentile` | double |  |
| `host.services.misconfigs.metrics.epss.score` | double |  |
| `host.services.misconfigs.metrics.cvss_v30` | object |  |
| `host.services.misconfigs.metrics.cvss_v30.vector` | text | The path, method, or scenario used to exploit the vulnerability. Each section represents components that contribute to the overall CVSS score. |
| `host.services.misconfigs.metrics.cvss_v30.components` | object | These metrics contribute to how a CVE is scored. |
| `host.services.misconfigs.metrics.cvss_v30.components.user_interaction` | keyword | Describes whether a user, other than the attacker, is required to do anything or participate in exploitation of the vulnerability. User interaction has two possible values: None (N) – No user interaction is required, Required (R) – A user must complete some steps for the exploit to succeed. For example, a user might be required to install some software. |
| `host.services.misconfigs.metrics.cvss_v30.components.attack_complexity` | keyword | Indicates conditions beyond the attacker’s control that must exist in order to exploit the vulnerability. The Attack Complexity metric is scored as either Low or High. There are two possible values: Low (L) – There are no specific pre-conditions required for exploitation, High (H) – The attacker must complete some number of preparatory steps in order to get access. |
| `host.services.misconfigs.metrics.cvss_v30.components.attack_vector` | keyword | Indicates the level of access required for an attacker to exploit the vulnerability. The Attack Vector metric is scored in one of four levels: Network (N) – Vulnerabilities with this rating are remotely exploitable, from one or more hops away, up to, and including, remote exploitation over the Internet, Adjacent (A) – A vulnerability with this rating requires network adjacency for exploitation. The attack must be launched from the same physical or logical network, Local (L) – Vulnerabilities with this rating are not exploitable over a network, Physical (P) – An attacker must physically interact with the target system. |
| `host.services.misconfigs.metrics.cvss_v30.components.availability` | keyword | If an attack renders information unavailable, such as when a system crashes or through a DDoS attack, availability is negatively impacted. Availability has three possible values: None (N) – There is no loss of availability, Low (L) – Availability might be intermittently limited, or performance might be negatively impacted, as a result of a successful attack, High (H) – There is a complete loss of availability of the impacted system or information. |
| `host.services.misconfigs.metrics.cvss_v30.components.confidentiality` | keyword | Refers to the disclosure of sensitive information to authorized and unauthorized users, with the goal being that only authorized users are able to access the target data. Confidentiality has three potential values: High (H) – The attacker has full access to all resources in the impacted system, including highly sensitive information such as encryption keys, Low (L) – The attacker has partial access to information, with no control over what, specifically, they are able to access, None (N) – No data is accessible to unauthorized users as a result of the exploit. |
| `host.services.misconfigs.metrics.cvss_v30.components.integrity` | keyword | Refers to whether the protected information has been tampered with or changed in any way. If there is no way for an attacker to alter the accuracy or completeness of the information, integrity has been maintained. Integrity has three values: None (N) – There is no loss of the integrity of any information, Low (L) – A limited amount of information might be tampered with or modified, but there is no serious impact on the protected system, High (H) – The attacker can modify any/all information on the target system, resulting in a complete loss of integrity. |
| `host.services.misconfigs.metrics.cvss_v30.components.privileges_required` | keyword | Describes the level of privileges or access an attacker must have before successful exploitation. There are three possible values: None (N) – There is no privilege or special access required to conduct the attack, Low (L) – The attacker requires basic, “user” level privileges to leverage the exploit, High (H) – Administrative or similar access privileges are required for successful attack. |
| `host.services.misconfigs.metrics.cvss_v30.components.scope` | keyword | Determines whether a vulnerability in one system or component can impact another system or component. If a vulnerability in a vulnerable component can affect a component which is in a different security scope than the vulnerable component, a scope change occurs. Scope has two possible ratings: Changed (C) – An exploited vulnerability can have a carry over impact on another system, Unchanged (U) – The exploited vulnerability is limited in damage to only the local security authority. |
| `host.services.misconfigs.metrics.cvss_v30.score` | double | Score of the vulnerability; 0.1 is the lowest, 10 is the maximum |
| `host.services.misconfigs.risk_source` | keyword |  |
| `host.services.misconfigs.confidence` | double |  |
| `host.location` | object |  |
| `host.location.province` | text | The state or province name of the detected location. |
| `host.location.city` | text | The English name of the detected city. |
| `host.location.country` | text | The English name of the detected country. |
| `host.location.registered_country` | text | The English name of the registered country. |
| `host.location.continent` | keyword | The English name of the detected continent (North America, Europe, Asia, South America, Africa, Oceania, Antarctica). |
| `host.location.country_code` | keyword | The detected two-letter ISO 3166-1 alpha-2 country code (US, CN, GB, RU, ...). |
| `host.location.postal_code` | keyword | The postal code (if applicable) of the detected location. |
| `host.location.registered_country_code` | keyword | The registered country's two-letter ISO 3166-1 alpha-2 country code (US, CN, GB, RU, ...). |
| `host.location.coordinates` | object | The estimated coordinates of the detected location. |
| `host.location.coordinates.longitude` | double |  |
| `host.location.coordinates.latitude` | double |  |
| `host.location.timezone` | text | The IANA time zone database name of the detected location. |
| `host.autonomous_system` | object |  |
| `host.autonomous_system.organization` | text | The name of the organization managning the autonomous system. |
| `host.autonomous_system.asn` | unsigned_long | The ASN (autonomous system number) of the host's autonomous system. |
| `host.autonomous_system.bgp_prefix` | ip_range | The autonomous system's CIDR. |
| `host.autonomous_system.country_code` | keyword | The autonomous system's two-letter ISO 3166-1 alpha-2 country code (US, CN, GB, RU, ...). |
| `host.autonomous_system.description` | text | Brief description of the autonomous system. |
| `host.autonomous_system.name` | text | The friendly name of the autonomous system. |
| `host.services.mssql` | object |  |
| `host.services.mssql.encrypt_mode` | text | The negotiated ENCRYPT_MODE with the server |
| `host.services.mssql.instance_name` | text |  |
| `host.services.mssql.prelogin_options` | object |  |
| `host.services.mssql.prelogin_options.nonce` | text |  |
| `host.services.mssql.prelogin_options.trace_id` | text |  |
| `host.services.mssql.prelogin_options.server_version` | object |  |
| `host.services.mssql.prelogin_options.server_version.build_number` | unsigned_long |  |
| `host.services.mssql.prelogin_options.server_version.major` | unsigned_long |  |
| `host.services.mssql.prelogin_options.server_version.minor` | unsigned_long |  |
| `host.services.mssql.prelogin_options.thread_id` | unsigned_long |  |
| `host.services.mssql.prelogin_options.encrypt_mode` | text |  |
| `host.services.mssql.prelogin_options.unknown` | object |  |
| `host.services.mssql.prelogin_options.unknown.key` | unsigned_long |  |
| `host.services.mssql.prelogin_options.unknown.value` | text |  |
| `host.services.mssql.prelogin_options.instance` | text |  |
| `host.services.mssql.prelogin_options.mars` | boolean |  |
| `host.services.mssql.prelogin_options.fed_auth_required` | boolean |  |
| `host.services.mssql.version` | text |  |
| `host.services.smb` | object |  |
| `host.services.smb.has_ntlm` | boolean | Server supports the NTLM authentication method |
| `host.services.smb.ntlm` | text | Native LAN manager |
| `host.services.smb.smbv1_support` | boolean |  |
| `host.services.smb.smb_version` | object |  |
| `host.services.smb.smb_version.major` | unsigned_long | Major version |
| `host.services.smb.smb_version.minor` | unsigned_long | Minor version |
| `host.services.smb.smb_version.revision` | unsigned_long | Protocol Revision |
| `host.services.smb.smb_version.version_string` | text | Full SMB Version String |
| `host.services.smb.negotiation_log` | object |  |
| `host.services.smb.negotiation_log.capabilities` | unsigned_long |  |
| `host.services.smb.negotiation_log.dialect_revision` | unsigned_long |  |
| `host.services.smb.negotiation_log.header_log` | object |  |
| `host.services.smb.negotiation_log.header_log.flags` | unsigned_long |  |
| `host.services.smb.negotiation_log.header_log.protocol_id` | text |  |
| `host.services.smb.negotiation_log.header_log.status` | unsigned_long |  |
| `host.services.smb.negotiation_log.header_log.command` | unsigned_long |  |
| `host.services.smb.negotiation_log.header_log.credits` | unsigned_long |  |
| `host.services.smb.negotiation_log.security_mode` | unsigned_long |  |
| `host.services.smb.negotiation_log.server_guid` | text |  |
| `host.services.smb.negotiation_log.server_start_time` | unsigned_long |  |
| `host.services.smb.negotiation_log.system_time` | unsigned_long |  |
| `host.services.smb.negotiation_log.authentication_types` | text |  |
| `host.services.smb.native_os` | text | Server-identified operating system |
| `host.services.smb.smb_capabilities` | object | Capabilities flags for the connection. See [MS-SMB2] Sect. 2.2.4. |
| `host.services.smb.smb_capabilities.smb_leasing_support` | boolean | Server supports Leasing |
| `host.services.smb.smb_capabilities.smb_multichan_support` | boolean | Server supports multiple channels per session |
| `host.services.smb.smb_capabilities.smb_multicredit_support` | boolean | Server supports multi-credit operations |
| `host.services.smb.smb_capabilities.smb_persistent_handle_support` | boolean | Server supports persistent handles |
| `host.services.smb.smb_capabilities.smb_dfs_support` | boolean | Server supports Distributed File System |
| `host.services.smb.smb_capabilities.smb_directory_leasing_support` | boolean | Server supports directory leasing |
| `host.services.smb.smb_capabilities.smb_encryption_support` | boolean | Server supports encryption |
| `host.services.smb.group_name` | text | Default group name |
| `host.services.smb.session_setup_log` | object |  |
| `host.services.smb.session_setup_log.header_log` | object |  |
| `host.services.smb.session_setup_log.header_log.command` | unsigned_long |  |
| `host.services.smb.session_setup_log.header_log.credits` | unsigned_long |  |
| `host.services.smb.session_setup_log.header_log.flags` | unsigned_long |  |
| `host.services.smb.session_setup_log.header_log.protocol_id` | text |  |
| `host.services.smb.session_setup_log.header_log.status` | unsigned_long |  |
| `host.services.smb.session_setup_log.negotiate_flags` | unsigned_long |  |
| `host.services.smb.session_setup_log.setup_flags` | unsigned_long |  |
| `host.services.smb.session_setup_log.target_name` | text |  |
| `host.services.ike` | object |  |
| `host.services.ike.v1` | object |  |
| `host.services.ike.v1.accepted_proposal` | boolean | Did the host accept our security proposal? When false, the host responded with an error. |
| `host.services.ike.v1.notify_message_types` | unsigned_long | Which types of NOTIFY messages did the host send us? |
| `host.services.ike.v1.vendor_ids` | text | The list of Vendor ID "extensions" the host claimed to support in its handshake |
| `host.services.ike.v2` | object |  |
| `host.services.ike.v2.vendor_ids` | text |  |
| `host.services.ike.v2.accepted_proposal` | boolean |  |
| `host.services.ike.v2.notify_message_types` | unsigned_long |  |
| `host.services.memcached` | object |  |
| `host.services.memcached.ascii_binding_protocol_enabled` | boolean | Whether server responds to a handshake using the ASCII wire format of the protocol. |
| `host.services.memcached.binary_binding_protocol_enabled` | boolean | Whether server responds to a handshake using the binary wire format of the protocol. |
| `host.services.memcached.responds_to_udp` | boolean | Whether the server on the UDP port with the same number responds to a handshake using the ASCII wire format of the protocol. |
| `host.services.memcached.stats` | nested | Server information returned in response to the stats command, as a set of key:value pairs. |
| `host.services.memcached.stats.key` | text |  |
| `host.services.memcached.stats.value` | text |  |
| `host.services.memcached.version` | text | The Memcached version indicated in the server's response. |
| `host.services.sip` | object |  |
| `host.services.sip.version` | text | SIP version |
| `host.services.sip.code` | integer |  |
| `host.services.sip.server` | text | Server software reported by service |
| `host.services.sip.status` | text |  |
| `host.services.vnc` | object |  |
| `host.services.vnc.screen_info` | object |  |
| `host.services.vnc.screen_info.height` | unsigned_long |  |
| `host.services.vnc.screen_info.name_len` | unsigned_long |  |
| `host.services.vnc.screen_info.pixel_format` | object |  |
| `host.services.vnc.screen_info.pixel_format.green_max` | unsigned_long | Max value of green pixel |
| `host.services.vnc.screen_info.pixel_format.big_endian` | boolean | If pixel RGB data are in big-endian |
| `host.services.vnc.screen_info.pixel_format.blue_max` | unsigned_long | Max value of blue pixel |
| `host.services.vnc.screen_info.pixel_format.depth` | unsigned_long | Color depth |
| `host.services.vnc.screen_info.pixel_format.red_max` | unsigned_long | Max value of red pixel |
| `host.services.vnc.screen_info.pixel_format.bits_per_pixel` | unsigned_long | How many bits in a single full pixel datum. Valid values are: 8, 16, 32 |
| `host.services.vnc.screen_info.pixel_format.padding2` | unsigned_long |  |
| `host.services.vnc.screen_info.pixel_format.red_shift` | unsigned_long | How many bits to right shift a pixel datum to get red bits in lsb |
| `host.services.vnc.screen_info.pixel_format.true_color` | boolean | If false, color maps are used |
| `host.services.vnc.screen_info.pixel_format.green_shift` | unsigned_long | How many bits to right shift a pixel datum to get green bits in lsb |
| `host.services.vnc.screen_info.pixel_format.padding1` | unsigned_long |  |
| `host.services.vnc.screen_info.pixel_format.padding3` | unsigned_long |  |
| `host.services.vnc.screen_info.pixel_format.blue_shift` | unsigned_long | How many bits to right shift a pixel datum to get blue bits in lsb |
| `host.services.vnc.screen_info.width` | unsigned_long |  |
| `host.services.vnc.security_types` | object | server-specified security options |
| `host.services.vnc.security_types.name` | text |  |
| `host.services.vnc.security_types.value` | integer |  |
| `host.services.vnc.version` | text |  |
| `host.services.vnc.connection_failed_reason` | text | If server terminates handshake, the reason offered (if any) |
| `host.services.vnc.desktop_name` | text | Desktop name provided by the server, capped at 255 bytes |
| `host.services.vnc.pixel_encoding` | object |  |
| `host.services.vnc.pixel_encoding.value` | integer |  |
| `host.services.vnc.pixel_encoding.name` | text |  |
| `host.services.ftp` | object |  |
| `host.services.ftp.status_code` | integer |  |
| `host.services.ftp.status_meaning` | text |  |
| `host.services.ftp.auth_ssl_response` | text |  |
| `host.services.ftp.auth_tls_response` | text |  |
| `host.services.ftp.implicit_tls` | boolean |  |
| `host.services.pptp` | object |  |
| `host.services.pptp.hostname` | text |  |
| `host.services.pptp.maximum_channels` | unsigned_long |  |
| `host.services.pptp.result_message` | object |  |
| `host.services.pptp.result_message.code` | unsigned_long |  |
| `host.services.pptp.result_message.meaning` | text |  |
| `host.services.pptp.bearer_message` | object |  |
| `host.services.pptp.bearer_message.code` | unsigned_long |  |
| `host.services.pptp.bearer_message.meaning` | text |  |
| `host.services.pptp.protocol` | object |  |
| `host.services.pptp.protocol.major` | unsigned_long |  |
| `host.services.pptp.protocol.minor` | unsigned_long |  |
| `host.services.pptp.firmware` | object |  |
| `host.services.pptp.firmware.minor` | unsigned_long |  |
| `host.services.pptp.firmware.major` | unsigned_long |  |
| `host.services.pptp.framing_message` | object |  |
| `host.services.pptp.framing_message.code` | unsigned_long |  |
| `host.services.pptp.framing_message.meaning` | text |  |
| `host.services.pptp.vendor` | text |  |
| `host.services.pptp.error_message` | object |  |
| `host.services.pptp.error_message.meaning` | text |  |
| `host.services.pptp.error_message.code` | unsigned_long |  |
| `host.services.rdp` | object |  |
| `host.services.rdp.protocol_flags` | object |  |
| `host.services.rdp.protocol_flags.restricted_auth_mode` | boolean |  |
| `host.services.rdp.protocol_flags.dynvc_graphics_pipeline` | boolean |  |
| `host.services.rdp.protocol_flags.extended_client_data_supported` | boolean |  |
| `host.services.rdp.protocol_flags.neg_resp_reserved` | boolean |  |
| `host.services.rdp.protocol_flags.restricted_admin_mode` | boolean |  |
| `host.services.rdp.selected_security_protocol` | object |  |
| `host.services.rdp.selected_security_protocol.credssp` | boolean |  |
| `host.services.rdp.selected_security_protocol.error_bad_flags` | boolean |  |
| `host.services.rdp.selected_security_protocol.error_ssl_cert_missing` | boolean |  |
| `host.services.rdp.selected_security_protocol.error_ssl_required` | boolean |  |
| `host.services.rdp.selected_security_protocol.error` | boolean |  |
| `host.services.rdp.selected_security_protocol.error_ssl_user_auth_required` | boolean |  |
| `host.services.rdp.selected_security_protocol.raw_value` | unsigned_long |  |
| `host.services.rdp.selected_security_protocol.error_ssl_forbidden` | boolean |  |
| `host.services.rdp.selected_security_protocol.error_unknown` | boolean |  |
| `host.services.rdp.selected_security_protocol.standard_rdp` | boolean |  |
| `host.services.rdp.selected_security_protocol.credssp_early_auth` | boolean |  |
| `host.services.rdp.selected_security_protocol.error_hybrid_required` | boolean |  |
| `host.services.rdp.selected_security_protocol.rdstls` | boolean |  |
| `host.services.rdp.selected_security_protocol.tls` | boolean |  |
| `host.services.rdp.version` | object |  |
| `host.services.rdp.version.major` | integer |  |
| `host.services.rdp.version.minor` | integer |  |
| `host.services.rdp.version.raw` | unsigned_long | Raw Version Response, Major version is stored in upper 2 bytes, minor in lower 2 bytes. |
| `host.services.rdp.x224_cc_pdu_dstref` | unsigned_long |  |
| `host.services.rdp.x224_cc_pdu_srcref` | unsigned_long |  |
| `host.services.rdp.certificate_info` | object |  |
| `host.services.rdp.certificate_info.internal_x509_chain_fps` | keyword |  |
| `host.services.rdp.certificate_info.proprietary_rsa_key` | object |  |
| `host.services.rdp.certificate_info.proprietary_rsa_key.magic` | unsigned_long |  |
| `host.services.rdp.certificate_info.proprietary_rsa_key.max_bytes_datalen` | unsigned_long |  |
| `host.services.rdp.certificate_info.proprietary_rsa_key.modulus` | text |  |
| `host.services.rdp.certificate_info.proprietary_rsa_key.modulus_bitlen` | unsigned_long |  |
| `host.services.rdp.certificate_info.proprietary_rsa_key.public_exponent` | unsigned_long |  |
| `host.services.rdp.certificate_info.proprietary_rsa_key.signature` | text |  |
| `host.services.rdp.certificate_info.proprietary_rsa_key.key_length` | unsigned_long |  |
| `host.services.rdp.connect_response` | object |  |
| `host.services.rdp.connect_response.connect_id` | unsigned_long |  |
| `host.services.rdp.connect_response.domain_parameters` | object |  |
| `host.services.rdp.connect_response.domain_parameters.domain_protocol_version` | long |  |
| `host.services.rdp.connect_response.domain_parameters.max_channel_ids` | long |  |
| `host.services.rdp.connect_response.domain_parameters.max_mcspdu_size` | long |  |
| `host.services.rdp.connect_response.domain_parameters.max_provider_height` | long |  |
| `host.services.rdp.connect_response.domain_parameters.max_token_ids` | long |  |
| `host.services.rdp.connect_response.domain_parameters.max_user_id_channels` | long |  |
| `host.services.rdp.connect_response.domain_parameters.min_throughput` | long |  |
| `host.services.rdp.connect_response.domain_parameters.num_priorities` | long |  |
| `host.services.mqtt` | object |  |
| `host.services.mqtt.subscription_ack_return` | object |  |
| `host.services.mqtt.subscription_ack_return.return_value` | text | Subscription response |
| `host.services.mqtt.subscription_ack_return.raw` | unsigned_long | Raw subscription response value |
| `host.services.mqtt.connection_ack_raw` | text | Raw CONNACK response packet |
| `host.services.mqtt.connection_ack_return` | object |  |
| `host.services.mqtt.connection_ack_return.raw` | unsigned_long | Raw connect status value |
| `host.services.mqtt.connection_ack_return.return_value` | text | Connection status |
| `host.services.ethereum` | object |  |
| `host.services.ethereum.hashrate` | text |  |
| `host.services.ethereum.version` | object |  |
| `host.services.ethereum.version.client` | text |  |
| `host.services.ethereum.version.compiler` | text |  |
| `host.services.ethereum.version.platform` | text |  |
| `host.services.ethereum.version.trailing` | text |  |
| `host.services.ethereum.version.version` | text |  |
| `host.services.ethereum.accounts` | text |  |
| `host.services.ssdp` | object |  |
| `host.services.ssdp.upnp_url` | text |  |
| `host.services.ssdp.headers` | nested |  |
| `host.services.ssdp.headers.key` | text |  |
| `host.services.ssdp.headers.value` | text | The values provided in the corresponding header. |
| `host.services.s7` | object |  |
| `host.services.s7.reserved_for_os` | text |  |
| `host.services.s7.copyright` | text |  |
| `host.services.s7.module` | text |  |
| `host.services.s7.oem_id` | text |  |
| `host.services.s7.cpu_profile` | text |  |
| `host.services.s7.location` | text |  |
| `host.services.s7.module_type` | text |  |
| `host.services.s7.system` | text |  |
| `host.services.s7.firmware` | text |  |
| `host.services.s7.hardware` | text |  |
| `host.services.s7.memory_serial_number` | text |  |
| `host.services.s7.serial_number` | text |  |
| `host.services.s7.module_id` | text |  |
| `host.services.s7.plant_id` | text |  |
| `host.services.any_connect` | object |  |
| `host.services.any_connect.raw` | text | XML content of the config-auth response |
| `host.services.any_connect.response_type` | text | Type of the response packet received after initializing the config-auth exchange |
| `host.services.any_connect.aggregate_auth_version` | integer | Version number indicated by the response for config-auth exchange |
| `host.services.any_connect.auth_methods` | text | Supported methods for users to enter credentials for this VPN |
| `host.services.any_connect.groups` | text | List of groups a user can authenticate with to use this VPN |
| `host.services.endpoints.kubernetes` | object |  |
| `host.services.endpoints.kubernetes.kubernetes_dashboard_found` | boolean | True if the dashboard is running and accessible |
| `host.services.endpoints.kubernetes.nodes` | object |  |
| `host.services.endpoints.kubernetes.nodes.operating_system` | text | The Operating System reported by the node. |
| `host.services.endpoints.kubernetes.nodes.images` | text | List of container images on this node |
| `host.services.endpoints.kubernetes.nodes.architecture` | text | The Architecture reported by the node. |
| `host.services.endpoints.kubernetes.nodes.container_runtime_version` | text | ContainerRuntime Version reported by the node through runtime remote API (e.g. docker://1.5.0). |
| `host.services.endpoints.kubernetes.nodes.kube_proxy_version` | text | KubeProxy Version reported by the node. |
| `host.services.endpoints.kubernetes.nodes.name` | text |  |
| `host.services.endpoints.kubernetes.nodes.os_image` | text | OS Image reported by the node from /etc/os-release (e.g. Debian GNU/Linux 7 (wheezy)). |
| `host.services.endpoints.kubernetes.nodes.addresses` | object |  |
| `host.services.endpoints.kubernetes.nodes.addresses.address` | keyword | Node address, IP/URL. |
| `host.services.endpoints.kubernetes.nodes.addresses.address_type` | text | Node address type, one of Hostname, ExternalIP or InternalIP. |
| `host.services.endpoints.kubernetes.nodes.kernel_version` | text | Kernel Version reported by the node from 'uname -r' (e.g. 3.16.0-0.bpo.4-amd64). |
| `host.services.endpoints.kubernetes.nodes.kubelet_version` | text | Kubelet Version reported by the node. |
| `host.services.endpoints.kubernetes.pod_names` | text |  |
| `host.services.endpoints.kubernetes.roles` | object |  |
| `host.services.endpoints.kubernetes.roles.name` | text |  |
| `host.services.endpoints.kubernetes.roles.rules` | object | Rules set for this role. |
| `host.services.endpoints.kubernetes.roles.rules.api_groups` | text | APIGroups is the name of the APIGroup that contains the resources. If multiple API groups are specified, any action requested against one of the enumerated resources in any API group will be allowed. |
| `host.services.endpoints.kubernetes.roles.rules.resources` | text | Resources is a list of resources this rule applies to. ResourceAll represents all resources |
| `host.services.endpoints.kubernetes.roles.rules.verbs` | text | Verbs is a list of Verbs that apply to ALL the ResourceKinds and AttributeRestrictions contained in this rule. VerbAll represents all kinds. |
| `host.services.endpoints.kubernetes.version_info` | object |  |
| `host.services.endpoints.kubernetes.version_info.major` | text | Kubernetes major version |
| `host.services.endpoints.kubernetes.version_info.compiler` | text | Go Compiler used |
| `host.services.endpoints.kubernetes.version_info.go_version` | text | Version of GO used to build version. |
| `host.services.endpoints.kubernetes.version_info.git_tree_state` | text | State of the tree when built. |
| `host.services.endpoints.kubernetes.version_info.git_version` | text |  |
| `host.services.endpoints.kubernetes.version_info.minor` | text | Kubernetes minor version |
| `host.services.endpoints.kubernetes.version_info.platform` | text | Platform compiled for |
| `host.services.endpoints.kubernetes.version_info.build_date` | text | Date version was built. |
| `host.services.endpoints.kubernetes.version_info.git_commit` | text | Git commit version built from. |
| `host.services.endpoints.kubernetes.endpoints` | object |  |
| `host.services.endpoints.kubernetes.endpoints.name` | text |  |
| `host.services.endpoints.kubernetes.endpoints.self_link` | text |  |
| `host.services.endpoints.kubernetes.endpoints.subsets` | object |  |
| `host.services.endpoints.kubernetes.endpoints.subsets.addresses` | object |  |
| `host.services.endpoints.kubernetes.endpoints.subsets.addresses.hostname` | text |  |
| `host.services.endpoints.kubernetes.endpoints.subsets.addresses.ip` | ip |  |
| `host.services.endpoints.kubernetes.endpoints.subsets.addresses.node_name` | text |  |
| `host.services.endpoints.kubernetes.endpoints.subsets.ports` | object |  |
| `host.services.endpoints.kubernetes.endpoints.subsets.ports.name` | text |  |
| `host.services.endpoints.kubernetes.endpoints.subsets.ports.port` | unsigned_long |  |
| `host.services.endpoints.kubernetes.endpoints.subsets.ports.protocol` | text |  |
| `host.services.endpoints.pprof` | object |  |
| `host.services.endpoints.pprof.trace` | integer |  |
| `host.services.endpoints.pprof.goroutine` | integer |  |
| `host.services.endpoints.pprof.profile` | integer |  |
| `host.services.endpoints.pprof.mutex` | integer |  |
| `host.services.endpoints.pprof.block` | integer |  |
| `host.services.endpoints.pprof.heap` | integer |  |
| `host.services.endpoints.pprof.cmdline` | text |  |
| `host.services.endpoints.pprof.threadcreate` | integer |  |
| `host.services.endpoints.pprof.allocs` | integer |  |
| `host.services.endpoints.elasticsearch` | object |  |
| `host.services.endpoints.elasticsearch.results_node_info` | object |  |
| `host.services.endpoints.elasticsearch.results_node_info.cluster_combined_info` | object |  |
| `host.services.endpoints.elasticsearch.results_node_info.cluster_combined_info.indices` | object |  |
| `host.services.endpoints.elasticsearch.results_node_info.cluster_combined_info.indices.store` | object |  |
| `host.services.endpoints.elasticsearch.results_node_info.cluster_combined_info.indices.store.reserved_in_bytes` | unsigned_long |  |
| `host.services.endpoints.elasticsearch.results_node_info.cluster_combined_info.indices.store.size_in_bytes` | unsigned_long |  |
| `host.services.endpoints.elasticsearch.results_node_info.cluster_combined_info.indices.count` | unsigned_long |  |
| `host.services.endpoints.elasticsearch.results_node_info.cluster_combined_info.indices.docs` | object |  |
| `host.services.endpoints.elasticsearch.results_node_info.cluster_combined_info.indices.docs.count` | unsigned_long |  |
| `host.services.endpoints.elasticsearch.results_node_info.cluster_combined_info.indices.docs.deleted` | unsigned_long |  |
| `host.services.endpoints.elasticsearch.results_node_info.cluster_combined_info.name` | text |  |
| `host.services.endpoints.elasticsearch.results_node_info.cluster_combined_info.status` | text |  |
| `host.services.endpoints.elasticsearch.results_node_info.cluster_combined_info.timestamp` | unsigned_long |  |
| `host.services.endpoints.elasticsearch.results_node_info.cluster_combined_info.uuid` | text |  |
| `host.services.endpoints.elasticsearch.results_node_info.cluster_combined_info.filesystem` | object |  |
| `host.services.endpoints.elasticsearch.results_node_info.cluster_combined_info.filesystem.free_in_bytes` | unsigned_long |  |
| `host.services.endpoints.elasticsearch.results_node_info.cluster_combined_info.filesystem.total` | text |  |
| `host.services.endpoints.elasticsearch.results_node_info.cluster_combined_info.filesystem.total_in_bytes` | unsigned_long |  |
| `host.services.endpoints.elasticsearch.results_node_info.cluster_combined_info.filesystem.available` | text |  |
| `host.services.endpoints.elasticsearch.results_node_info.cluster_combined_info.filesystem.available_in_bytes` | unsigned_long |  |
| `host.services.endpoints.elasticsearch.results_node_info.cluster_combined_info.filesystem.free` | text |  |
| `host.services.endpoints.elasticsearch.results_node_info.node_info` | object |  |
| `host.services.endpoints.elasticsearch.results_node_info.node_info.node_data` | object |  |
| `host.services.endpoints.elasticsearch.results_node_info.node_info.node_data.version` | text |  |
| `host.services.endpoints.elasticsearch.results_node_info.node_info.node_data.name` | text |  |
| `host.services.endpoints.elasticsearch.results_node_info.node_info.node_data.ip_raw` | text |  |
| `host.services.endpoints.elasticsearch.results_node_info.node_info.node_data.build_type` | text |  |
| `host.services.endpoints.elasticsearch.results_node_info.node_info.node_data.host` | text |  |
| `host.services.endpoints.elasticsearch.results_node_info.node_info.node_data.build_hash` | text |  |
| `host.services.endpoints.elasticsearch.results_node_info.node_info.node_data.jvm` | object |  |
| `host.services.endpoints.elasticsearch.results_node_info.node_info.node_data.jvm.vm_version` | text |  |
| `host.services.endpoints.elasticsearch.results_node_info.node_info.node_data.jvm.start_time_ms` | unsigned_long |  |
| `host.services.endpoints.elasticsearch.results_node_info.node_info.node_data.jvm.start_time` | text |  |
| `host.services.endpoints.elasticsearch.results_node_info.node_info.node_data.jvm.version` | text |  |
| `host.services.endpoints.elasticsearch.results_node_info.node_info.node_data.jvm.input_args` | text |  |
| `host.services.endpoints.elasticsearch.results_node_info.node_info.node_data.jvm.vm_name` | text |  |
| `host.services.endpoints.elasticsearch.results_node_info.node_info.node_data.jvm.memory_pools` | text |  |
| `host.services.endpoints.elasticsearch.results_node_info.node_info.node_data.jvm.vm_vendor` | text |  |
| `host.services.endpoints.elasticsearch.results_node_info.node_info.node_data.jvm.gc` | text |  |
| `host.services.endpoints.elasticsearch.results_node_info.node_info.node_data.build_flavor` | text |  |
| `host.services.endpoints.elasticsearch.results_node_info.node_info.node_data.ip` | text |  |
| `host.services.endpoints.elasticsearch.results_node_info.node_info.node_data.thread_pool_list` | object |  |
| `host.services.endpoints.elasticsearch.results_node_info.node_info.node_data.thread_pool_list.type` | text |  |
| `host.services.endpoints.elasticsearch.results_node_info.node_info.node_data.thread_pool_list.keep_alive` | text |  |
| `host.services.endpoints.elasticsearch.results_node_info.node_info.node_data.thread_pool_list.max` | integer |  |
| `host.services.endpoints.elasticsearch.results_node_info.node_info.node_data.thread_pool_list.min` | integer |  |
| `host.services.endpoints.elasticsearch.results_node_info.node_info.node_data.thread_pool_list.queue_size` | integer |  |
| `host.services.endpoints.elasticsearch.results_node_info.node_info.node_data.total_indexing_buffer` | unsigned_long |  |
| `host.services.endpoints.elasticsearch.results_node_info.node_info.node_data.os` | object |  |
| `host.services.endpoints.elasticsearch.results_node_info.node_info.node_data.os.arch` | text |  |
| `host.services.endpoints.elasticsearch.results_node_info.node_info.node_data.os.available_proc` | integer |  |
| `host.services.endpoints.elasticsearch.results_node_info.node_info.node_data.os.name` | text |  |
| `host.services.endpoints.elasticsearch.results_node_info.node_info.node_data.os.pretty_name` | text |  |
| `host.services.endpoints.elasticsearch.results_node_info.node_info.node_data.os.refresh_interval_ms` | unsigned_long |  |
| `host.services.endpoints.elasticsearch.results_node_info.node_info.node_data.os.version` | text |  |
| `host.services.endpoints.elasticsearch.results_node_info.node_info.node_data.os.allocated_proc` | integer |  |
| `host.services.endpoints.elasticsearch.results_node_info.node_info.node_data.settings` | object |  |
| `host.services.endpoints.elasticsearch.results_node_info.node_info.node_data.settings.cluster_name` | text |  |
| `host.services.endpoints.elasticsearch.results_node_info.node_info.node_data.settings.node` | object |  |
| `host.services.endpoints.elasticsearch.results_node_info.node_info.node_data.settings.node.name` | text |  |
| `host.services.endpoints.elasticsearch.results_node_info.node_info.node_data.settings.node.attr` | object |  |
| `host.services.endpoints.elasticsearch.results_node_info.node_info.node_data.settings.node.attr.ml` | object |  |
| `host.services.endpoints.elasticsearch.results_node_info.node_info.node_data.settings.node.attr.ml.machine_memory` | text |  |
| `host.services.endpoints.elasticsearch.results_node_info.node_info.node_data.settings.node.attr.ml.max_open_jobs` | text |  |
| `host.services.endpoints.elasticsearch.results_node_info.node_info.node_data.settings.node.attr.ml.enabled` | text |  |
| `host.services.endpoints.elasticsearch.results_node_info.node_info.node_data.settings.node.attr.xpack_installed` | text |  |
| `host.services.endpoints.elasticsearch.results_node_info.node_info.node_data.ingest_processors` | text |  |
| `host.services.endpoints.elasticsearch.results_node_info.node_info.node_data.roles` | text |  |
| `host.services.endpoints.elasticsearch.results_node_info.node_info.node_data.modules` | object |  |
| `host.services.endpoints.elasticsearch.results_node_info.node_info.node_data.modules.desc` | text |  |
| `host.services.endpoints.elasticsearch.results_node_info.node_info.node_data.modules.elastic_version` | text |  |
| `host.services.endpoints.elasticsearch.results_node_info.node_info.node_data.modules.ext_plugins` | text |  |
| `host.services.endpoints.elasticsearch.results_node_info.node_info.node_data.modules.has_native_ctrl` | boolean |  |
| `host.services.endpoints.elasticsearch.results_node_info.node_info.node_data.modules.java_version` | text |  |
| `host.services.endpoints.elasticsearch.results_node_info.node_info.node_data.modules.name` | text |  |
| `host.services.endpoints.elasticsearch.results_node_info.node_info.node_data.modules.version` | text |  |
| `host.services.endpoints.elasticsearch.results_node_info.node_info.node_data.modules.class_name` | text |  |
| `host.services.endpoints.elasticsearch.results_node_info.node_info.node_name` | text |  |
| `host.services.endpoints.elasticsearch.system_info` | object |  |
| `host.services.endpoints.elasticsearch.system_info.tagline` | text |  |
| `host.services.endpoints.elasticsearch.system_info.version` | object |  |
| `host.services.endpoints.elasticsearch.system_info.version.build_flavor` | text |  |
| `host.services.endpoints.elasticsearch.system_info.version.build_hash` | text |  |
| `host.services.endpoints.elasticsearch.system_info.version.min_wire_compat_ver` | text |  |
| `host.services.endpoints.elasticsearch.system_info.version.build_type` | text |  |
| `host.services.endpoints.elasticsearch.system_info.version.lucene_version` | text |  |
| `host.services.endpoints.elasticsearch.system_info.version.build_snapshot` | boolean |  |
| `host.services.endpoints.elasticsearch.system_info.version.number` | text |  |
| `host.services.endpoints.elasticsearch.system_info.version.build_date` | text |  |
| `host.services.endpoints.elasticsearch.system_info.version.min_idx_compat_ver` | text |  |
| `host.services.endpoints.elasticsearch.system_info.cluster_uuid` | text |  |
| `host.services.endpoints.elasticsearch.system_info.name` | text |  |
| `host.services.endpoints.elasticsearch.error_message` | object |  |
| `host.services.endpoints.elasticsearch.error_message.header` | text |  |
| `host.services.endpoints.elasticsearch.error_message.reason` | text |  |
| `host.services.endpoints.elasticsearch.error_message.type` | text |  |
| `host.services.endpoints.http` | object |  |
| `host.services.endpoints.http.html_tags` | text | A list of the <title> and <meta> tags from services.http.response.body. |
| `host.services.endpoints.http.redirect_chain` | nested | If the scan redirects, the list of followup scans performed |
| `host.services.endpoints.http.redirect_chain.http_status` | object | The HTTP status code and reason of the redirecting response. |
| `host.services.endpoints.http.redirect_chain.http_status.code` | integer | A 3-digit integer result code indicating the result of the redirecting response. |
| `host.services.endpoints.http.redirect_chain.http_status.reason` | text | A human-readable phrase describing the status code. |
| `host.services.endpoints.http.redirect_chain.path` | text |  |
| `host.services.endpoints.http.redirect_chain.port` | unsigned_long |  |
| `host.services.endpoints.http.redirect_chain.reason` | text |  |
| `host.services.endpoints.http.redirect_chain.scheme` | text |  |
| `host.services.endpoints.http.redirect_chain.transport_protocol` | keyword |  |
| `host.services.endpoints.http.redirect_chain.hostname` | text |  |
| `host.services.endpoints.http.body_hash_sha1` | text |  |
| `host.services.endpoints.http.status_code` | integer | A 3-digit integer result code indicating the result of the services.http.request. |
| `host.services.endpoints.http.favicons` | object |  |
| `host.services.endpoints.http.favicons.hash_shodan` | integer | A hash expressed as a signed decimal integer, provided for compatability with Shodan search. |
| `host.services.endpoints.http.favicons.name` | text | The URI used to retrieve the favicon, which most commonly use the http(s) or data schemes. URIs using the data scheme are truncated: the first 48 and last 24 characters are preserved. |
| `host.services.endpoints.http.favicons.size` | integer | The size of the favicon retrieved, in bytes. |
| `host.services.endpoints.http.favicons.hash_md5` | text |  |
| `host.services.endpoints.http.favicons.hash_phash` | text | A 64-bit 'perceptual' hash of the favicon |
| `host.services.endpoints.http.favicons.hash_sha256` | text |  |
| `host.services.endpoints.http.body_size` | integer | The length, in bytes, of services.http.response.body; at most, 64KB. |
| `host.services.endpoints.http.body` | text | The body of the HTTP response. For hosts without a name, the first 64KB are available. For hosts with a name, only 6KB are available. |
| `host.services.endpoints.http.network_log` | object | List of all resources fetched when visiting this page as browser |
| `host.services.endpoints.http.network_log.resources` | nested | Resources fetched during page load. |
| `host.services.endpoints.http.network_log.resources.md5` | text | MD5 hash of the resource content. |
| `host.services.endpoints.http.network_log.resources.path` | text | Path from the URL. |
| `host.services.endpoints.http.network_log.resources.sha1` | text | SHA-1 hash of the resource content. |
| `host.services.endpoints.http.network_log.resources.port` | text | Port from the URL. |
| `host.services.endpoints.http.network_log.resources.mime_type` | text | MIME type of the resource. |
| `host.services.endpoints.http.network_log.resources.sha256` | text | SHA-256 hash of the resource content. |
| `host.services.endpoints.http.network_log.resources.url` | text | Full URL of the resource. |
| `host.services.endpoints.http.network_log.resources.host` | text | Hostname from the URL. |
| `host.services.endpoints.http.network_log.resources.scheme` | text | URL scheme (e.g., http, https). |
| `host.services.endpoints.http.network_log.resources.size` | integer | Size of the resource in bytes. |
| `host.services.endpoints.http.network_log.har_handle` | text | Storage handle for the full HAR network log. |
| `host.services.endpoints.http.body_hash_sha256` | text |  |
| `host.services.endpoints.http.supported_versions` | text |  |
| `host.services.endpoints.http.uri` | text | The full path used to make the request, which includes the scheme, host, port (when non-standard), and endpoint. |
| `host.services.endpoints.http.html_title` | text | The title of the HTML page: the inner contents of the <title> tag in the response body, if present. |
| `host.services.endpoints.http.protocol` | text | The protocol field of the response, which includes the claimed HTTP version number. |
| `host.services.endpoints.http.headers` | nested | The key-value header pairs included in the response. |
| `host.services.endpoints.http.headers.key` | text |  |
| `host.services.endpoints.http.headers.value` | text | The values provided in the corresponding header. |
| `host.services.endpoints.http.body_hash_tlsh` | text |  |
| `host.services.endpoints.http.status_reason` | text | A human-readable phrase describing the status code. |
| `host.services.endpoints.fortigate` | object |  |
| `host.services.endpoints.fortigate.version` | text |  |
| `host.services.endpoints.fortigate.api_version` | text |  |
| `host.services.endpoints.fortigate.build` | integer |  |
| `host.services.endpoints.fortigate.serial` | text |  |
| `host.services.endpoints.fortigate.status_code` | integer |  |
| `host.services.endpoints.fortigate.status_msg` | text |  |
| `host.services.endpoints.cobalt_strike` | object |  |
| `host.services.endpoints.cobalt_strike.x64` | object |  |
| `host.services.endpoints.cobalt_strike.x64.host_header` | text |  |
| `host.services.endpoints.cobalt_strike.x64.user_agent` | text |  |
| `host.services.endpoints.cobalt_strike.x64.unknown_int` | object |  |
| `host.services.endpoints.cobalt_strike.x64.unknown_int.key` | unsigned_long |  |
| `host.services.endpoints.cobalt_strike.x64.unknown_int.value` | unsigned_long |  |
| `host.services.endpoints.cobalt_strike.x64.watermark` | unsigned_long |  |
| `host.services.endpoints.cobalt_strike.x64.dns` | boolean |  |
| `host.services.endpoints.cobalt_strike.x64.http_post` | object |  |
| `host.services.endpoints.cobalt_strike.x64.http_post.verb` | text |  |
| `host.services.endpoints.cobalt_strike.x64.http_post.client` | text |  |
| `host.services.endpoints.cobalt_strike.x64.http_post.uri` | text |  |
| `host.services.endpoints.cobalt_strike.x64.ssl` | boolean |  |
| `host.services.endpoints.cobalt_strike.x64.post_ex` | object |  |
| `host.services.endpoints.cobalt_strike.x64.post_ex.x64` | text |  |
| `host.services.endpoints.cobalt_strike.x64.post_ex.x86` | text |  |
| `host.services.endpoints.cobalt_strike.x64.public_key` | text |  |
| `host.services.endpoints.cobalt_strike.x64.cookie_beacon` | unsigned_long |  |
| `host.services.endpoints.cobalt_strike.x64.jitter` | unsigned_long |  |
| `host.services.endpoints.cobalt_strike.x64.sleep_time` | unsigned_long |  |
| `host.services.endpoints.cobalt_strike.x64.killdate` | unsigned_long |  |
| `host.services.endpoints.cobalt_strike.x64.crypto_scheme` | unsigned_long |  |
| `host.services.endpoints.cobalt_strike.x64.http_get` | object |  |
| `host.services.endpoints.cobalt_strike.x64.http_get.uri` | text |  |
| `host.services.endpoints.cobalt_strike.x64.http_get.verb` | text |  |
| `host.services.endpoints.cobalt_strike.x64.http_get.client` | text |  |
| `host.services.endpoints.cobalt_strike.x64.unknown_bytes` | object |  |
| `host.services.endpoints.cobalt_strike.x64.unknown_bytes.value` | text |  |
| `host.services.endpoints.cobalt_strike.x64.unknown_bytes.key` | unsigned_long |  |
| `host.services.endpoints.cobalt_strike.x86` | object |  |
| `host.services.endpoints.cobalt_strike.x86.http_get` | object |  |
| `host.services.endpoints.cobalt_strike.x86.http_get.client` | text |  |
| `host.services.endpoints.cobalt_strike.x86.http_get.uri` | text |  |
| `host.services.endpoints.cobalt_strike.x86.http_get.verb` | text |  |
| `host.services.endpoints.cobalt_strike.x86.user_agent` | text |  |
| `host.services.endpoints.cobalt_strike.x86.dns` | boolean |  |
| `host.services.endpoints.cobalt_strike.x86.ssl` | boolean |  |
| `host.services.endpoints.cobalt_strike.x86.unknown_bytes` | object |  |
| `host.services.endpoints.cobalt_strike.x86.unknown_bytes.value` | text |  |
| `host.services.endpoints.cobalt_strike.x86.unknown_bytes.key` | unsigned_long |  |
| `host.services.endpoints.cobalt_strike.x86.host_header` | text |  |
| `host.services.endpoints.cobalt_strike.x86.sleep_time` | unsigned_long |  |
| `host.services.endpoints.cobalt_strike.x86.post_ex` | object |  |
| `host.services.endpoints.cobalt_strike.x86.post_ex.x64` | text |  |
| `host.services.endpoints.cobalt_strike.x86.post_ex.x86` | text |  |
| `host.services.endpoints.cobalt_strike.x86.killdate` | unsigned_long |  |
| `host.services.endpoints.cobalt_strike.x86.cookie_beacon` | unsigned_long |  |
| `host.services.endpoints.cobalt_strike.x86.jitter` | unsigned_long |  |
| `host.services.endpoints.cobalt_strike.x86.watermark` | unsigned_long |  |
| `host.services.endpoints.cobalt_strike.x86.public_key` | text |  |
| `host.services.endpoints.cobalt_strike.x86.crypto_scheme` | unsigned_long |  |
| `host.services.endpoints.cobalt_strike.x86.http_post` | object |  |
| `host.services.endpoints.cobalt_strike.x86.http_post.client` | text |  |
| `host.services.endpoints.cobalt_strike.x86.http_post.uri` | text |  |
| `host.services.endpoints.cobalt_strike.x86.http_post.verb` | text |  |
| `host.services.endpoints.cobalt_strike.x86.unknown_int` | object |  |
| `host.services.endpoints.cobalt_strike.x86.unknown_int.value` | unsigned_long |  |
| `host.services.endpoints.cobalt_strike.x86.unknown_int.key` | unsigned_long |  |
| `host.services.elf_file` | object |  |
| `host.services.elf_file.class` | text |  |
| `host.services.elf_file.data` | text |  |
| `host.services.elf_file.machine` | text |  |
| `host.services.elf_file.os_abi` | text |  |
| `host.services.elf_file.type` | text |  |
| `host.services.ssh` | object |  |
| `host.services.ssh.hassh_fingerprint` | text |  |
| `host.services.ssh.kex_init_message` | object |  |
| `host.services.ssh.kex_init_message.server_to_client_compression` | text | A list of ssh compression algorithm identifiers, named according to section 6 of https://www.ietf.org/rfc/rfc4251.txt; see https://www.iana.org/assignments/ssh-parameters/ssh-parameters.xhtml#ssh-parameters-20 for standard values. |
| `host.services.ssh.kex_init_message.server_to_client_languages` | text | A name-list of language tags in order of preference. As Defined in https://www.ietf.org/rfc/rfc3066.txt. |
| `host.services.ssh.kex_init_message.server_to_client_macs` | text | A list of ssh MAC algorithm identifiers, named according to section 6 of https://www.ietf.org/rfc/rfc4251.txt; see https://www.iana.org/assignments/ssh-parameters/ssh-parameters.xhtml#ssh-parameters-18 for standard values. |
| `host.services.ssh.kex_init_message.client_to_server_compression` | text | A list of ssh compression algorithm identifiers, named according to section 6 of https://www.ietf.org/rfc/rfc4251.txt; see https://www.iana.org/assignments/ssh-parameters/ssh-parameters.xhtml#ssh-parameters-20 for standard values. |
| `host.services.ssh.kex_init_message.first_kex_follows` | boolean |  |
| `host.services.ssh.kex_init_message.client_to_server_ciphers` | text | A list of ssh cipher algorithm identifiers, named according to section 6 of https://www.ietf.org/rfc/rfc4251.txt; see https://www.iana.org/assignments/ssh-parameters/ssh-parameters.xhtml#ssh-parameters-16 for standard values. |
| `host.services.ssh.kex_init_message.kex_algorithms` | text | Key exchange algorithms used in the handshake. |
| `host.services.ssh.kex_init_message.client_to_server_languages` | text | A name-list of language tags in order of preference. As Defined in https://www.ietf.org/rfc/rfc3066.txt. |
| `host.services.ssh.kex_init_message.client_to_server_macs` | text | A list of ssh MAC algorithm identifiers, named according to section 6 of https://www.ietf.org/rfc/rfc4251.txt; see https://www.iana.org/assignments/ssh-parameters/ssh-parameters.xhtml#ssh-parameters-18 for standard values. |
| `host.services.ssh.kex_init_message.server_to_client_ciphers` | text | A list of ssh cipher algorithm identifiers, named according to section 6 of https://www.ietf.org/rfc/rfc4251.txt; see https://www.iana.org/assignments/ssh-parameters/ssh-parameters.xhtml#ssh-parameters-16 for standard values. |
| `host.services.ssh.kex_init_message.host_key_algorithms` | text | Asymmetric key algorithms for the host key supported by the client. |
| `host.services.ssh.server_host_key` | object |  |
| `host.services.ssh.server_host_key.ecdsa_public_key` | object |  |
| `host.services.ssh.server_host_key.ecdsa_public_key.y` | text |  |
| `host.services.ssh.server_host_key.ecdsa_public_key.curve` | keyword |  |
| `host.services.ssh.server_host_key.ecdsa_public_key.pub` | text |  |
| `host.services.ssh.server_host_key.ecdsa_public_key.gx` | text |  |
| `host.services.ssh.server_host_key.ecdsa_public_key.n` | text |  |
| `host.services.ssh.server_host_key.ecdsa_public_key.gy` | text |  |
| `host.services.ssh.server_host_key.ecdsa_public_key.length` | unsigned_long |  |
| `host.services.ssh.server_host_key.ecdsa_public_key.x` | text |  |
| `host.services.ssh.server_host_key.ecdsa_public_key.b` | text |  |
| `host.services.ssh.server_host_key.ecdsa_public_key.p` | text |  |
| `host.services.ssh.server_host_key.ed25519_public_key` | object |  |
| `host.services.ssh.server_host_key.ed25519_public_key.public_bytes` | text |  |
| `host.services.ssh.server_host_key.fingerprint_sha256` | text |  |
| `host.services.ssh.server_host_key.rsa_public_key` | object |  |
| `host.services.ssh.server_host_key.rsa_public_key.length` | unsigned_long |  |
| `host.services.ssh.server_host_key.rsa_public_key.modulus` | text |  |
| `host.services.ssh.server_host_key.rsa_public_key.exponent` | text |  |
| `host.services.ssh.server_host_key.certkey_public_key` | text |  |
| `host.services.ssh.server_host_key.dsa_public_key` | object |  |
| `host.services.ssh.server_host_key.dsa_public_key.y` | text |  |
| `host.services.ssh.server_host_key.dsa_public_key.g` | text |  |
| `host.services.ssh.server_host_key.dsa_public_key.p` | text |  |
| `host.services.ssh.server_host_key.dsa_public_key.q` | text |  |
| `host.services.ssh.algorithm_selection` | object |  |
| `host.services.ssh.algorithm_selection.kex_algorithm` | text |  |
| `host.services.ssh.algorithm_selection.server_to_client_alg_group` | object |  |
| `host.services.ssh.algorithm_selection.server_to_client_alg_group.compression` | text |  |
| `host.services.ssh.algorithm_selection.server_to_client_alg_group.mac` | text |  |
| `host.services.ssh.algorithm_selection.server_to_client_alg_group.cipher` | text |  |
| `host.services.ssh.algorithm_selection.client_to_server_alg_group` | object |  |
| `host.services.ssh.algorithm_selection.client_to_server_alg_group.compression` | text |  |
| `host.services.ssh.algorithm_selection.client_to_server_alg_group.mac` | text |  |
| `host.services.ssh.algorithm_selection.client_to_server_alg_group.cipher` | text |  |
| `host.services.ssh.algorithm_selection.host_key_algorithm` | text |  |
| `host.services.ssh.endpoint_id` | object |  |
| `host.services.ssh.endpoint_id.raw` | text |  |
| `host.services.ssh.endpoint_id.software_version` | text |  |
| `host.services.ssh.endpoint_id.comment` | text |  |
| `host.services.ssh.endpoint_id.protocol_version` | text |  |
| `host.services.checkpoint_topology` | object |  |
| `host.services.checkpoint_topology.common_name` | text |  |
| `host.services.checkpoint_topology.organization` | text |  |
| `host.services.bacnet` | object |  |
| `host.services.bacnet.description` | text |  |
| `host.services.bacnet.firmware_revision` | text |  |
| `host.services.bacnet.model_name` | text |  |
| `host.services.bacnet.object_name` | text |  |
| `host.services.bacnet.instance_number` | unsigned_long |  |
| `host.services.bacnet.vendor_name` | text |  |
| `host.services.bacnet.vendor_id` | unsigned_long |  |
| `host.services.bacnet.application_software_revision` | text |  |
| `host.services.bacnet.location` | text |  |
| `host.services.imap` | object |  |
| `host.services.imap.start_tls` | text | The server's response to the STARTTLS command. |
| `host.services.mms` | object |  |
| `host.services.mms.vendor` | text |  |
| `host.services.mms.model` | text |  |
| `host.services.mms.revision` | text |  |
| `host.services.openvpn` | object |  |
| `host.services.openvpn.accepts_v2` | boolean |  |
| `host.services.openvpn.accepts_v1` | boolean |  |
| `host.services.upnp` | object |  |
| `host.services.upnp.spec` | object |  |
| `host.services.upnp.spec.major` | text |  |
| `host.services.upnp.spec.minor` | text |  |
| `host.services.upnp.devices` | object |  |
| `host.services.upnp.devices.device_type` | text |  |
| `host.services.upnp.devices.manufacturer` | text |  |
| `host.services.upnp.devices.udn` | text |  |
| `host.services.upnp.devices.id` | integer | Censys-generated IDs representing a device tree |
| `host.services.upnp.devices.model_url` | text |  |
| `host.services.upnp.devices.friendly_name` | text |  |
| `host.services.upnp.devices.serial_number` | text |  |
| `host.services.upnp.devices.model_name` | text |  |
| `host.services.upnp.devices.model_number` | text |  |
| `host.services.upnp.devices.parent_id` | integer |  |
| `host.services.upnp.devices.service_list` | object |  |
| `host.services.upnp.devices.service_list.service_type` | text |  |
| `host.services.upnp.devices.service_list.control_url` | text |  |
| `host.services.upnp.devices.service_list.event_sub_url` | text |  |
| `host.services.upnp.devices.service_list.scpd_url` | text |  |
| `host.services.upnp.devices.service_list.service_id` | text |  |
| `host.services.upnp.devices.upc` | text |  |
| `host.services.upnp.devices.model_description` | text |  |
| `host.services.upnp.devices.manufacturer_url` | text |  |
| `host.services.upnp.devices.presentation_url` | text |  |
| `host.services.upnp.endpoint` | text |  |
| `host.services.upnp.headers` | nested |  |
| `host.services.upnp.headers.key` | text |  |
| `host.services.upnp.headers.value` | text | The values provided in the corresponding header. |
| `host.services.l2tp` | object |  |
| `host.services.l2tp.hello_received` | boolean |  |
| `host.services.l2tp.stop_sccn` | object |  |
| `host.services.l2tp.stop_sccn.attribute_values` | object |  |
| `host.services.l2tp.stop_sccn.attribute_values.error_meaning` | text |  |
| `host.services.l2tp.stop_sccn.attribute_values.hostname` | text |  |
| `host.services.l2tp.stop_sccn.attribute_values.error_message` | text |  |
| `host.services.l2tp.stop_sccn.attribute_values.error_code` | unsigned_long |  |
| `host.services.l2tp.stop_sccn.attribute_values.firmware_revision` | unsigned_long |  |
| `host.services.l2tp.stop_sccn.attribute_values.result_code` | unsigned_long |  |
| `host.services.l2tp.stop_sccn.attribute_values.protocol_version` | unsigned_long |  |
| `host.services.l2tp.stop_sccn.attribute_values.vendor_name` | text |  |
| `host.services.l2tp.stop_sccn.attribute_values.result_meaning` | text |  |
| `host.services.l2tp.stop_sccn.attribute_values.window_size` | unsigned_long |  |
| `host.services.l2tp.stop_sccn.attribute_values.protocol_revision` | unsigned_long |  |
| `host.services.l2tp.sccrq_received` | boolean |  |
| `host.services.l2tp.zlb_received` | boolean |  |
| `host.services.l2tp.sccn_received` | boolean |  |
| `host.services.l2tp.sccrp` | object |  |
| `host.services.l2tp.sccrp.attribute_values` | object |  |
| `host.services.l2tp.sccrp.attribute_values.protocol_version` | unsigned_long |  |
| `host.services.l2tp.sccrp.attribute_values.error_code` | unsigned_long |  |
| `host.services.l2tp.sccrp.attribute_values.error_message` | text |  |
| `host.services.l2tp.sccrp.attribute_values.hostname` | text |  |
| `host.services.l2tp.sccrp.attribute_values.result_meaning` | text |  |
| `host.services.l2tp.sccrp.attribute_values.error_meaning` | text |  |
| `host.services.l2tp.sccrp.attribute_values.window_size` | unsigned_long |  |
| `host.services.l2tp.sccrp.attribute_values.result_code` | unsigned_long |  |
| `host.services.l2tp.sccrp.attribute_values.firmware_revision` | unsigned_long |  |
| `host.services.l2tp.sccrp.attribute_values.protocol_revision` | unsigned_long |  |
| `host.services.l2tp.sccrp.attribute_values.vendor_name` | text |  |
| `host.services.l2tp.sccrp_received` | boolean |  |
| `host.services.l2tp.stop_sccn_received` | boolean |  |
| `host.services.l2tp.ordered_messages_raw` | text |  |
| `host.services.team_viewer` | object |  |
| `host.services.team_viewer.response` | text |  |
| `host.services.smtp` | object |  |
| `host.services.smtp.ehlo` | text | The server's response to the EHLO command. |
| `host.services.smtp.start_tls` | text | The server's response to the STARTTLS command. |
| `host.services.eip` | object |  |
| `host.services.eip.identity` | object |  |
| `host.services.eip.identity.device_type` | text |  |
| `host.services.eip.identity.device_type_code` | unsigned_long |  |
| `host.services.eip.identity.state` | unsigned_long |  |
| `host.services.eip.identity.status` | unsigned_long |  |
| `host.services.eip.identity.socket_addr` | text |  |
| `host.services.eip.identity.product_name` | text |  |
| `host.services.eip.identity.vendor_id` | text |  |
| `host.services.eip.identity.socket_port` | unsigned_long |  |
| `host.services.eip.identity.product_code` | unsigned_long |  |
| `host.services.eip.identity.revision` | text |  |
| `host.services.eip.identity.vendor_name` | text |  |
| `host.services.eip.identity.serial_number` | unsigned_long |  |
| `host.services.eip.interfaces` | object |  |
| `host.services.eip.interfaces.name` | text |  |
| `host.services.eip.interfaces.index` | unsigned_long |  |
| `host.services.eip.services` | object |  |
| `host.services.eip.services.supports_tcp` | boolean |  |
| `host.services.eip.services.supports_udp` | boolean |  |
| `host.services.eip.services.capabilities` | unsigned_long |  |
| `host.services.eip.services.service_name` | text |  |
| `host.services.tplink_kasa` | object |  |
| `host.services.tplink_kasa.hw_ver` | text |  |
| `host.services.tplink_kasa.on_time` | long |  |
| `host.services.tplink_kasa.active_mode` | text |  |
| `host.services.tplink_kasa.feature` | text |  |
| `host.services.tplink_kasa.brightness` | long |  |
| `host.services.tplink_kasa.icon_hash` | text |  |
| `host.services.tplink_kasa.err_code` | long |  |
| `host.services.tplink_kasa.mic_type` | text |  |
| `host.services.tplink_kasa.dev_name` | text |  |
| `host.services.tplink_kasa.model` | text |  |
| `host.services.tplink_kasa.relay_state` | long |  |
| `host.services.tplink_kasa.sw_ver` | text |  |
| `host.services.tplink_kasa.rssi` | long |  |
| `host.services.tplink_kasa.updating` | long |  |
| `host.services.tplink_kasa.led_off` | long |  |
| `host.services.mysql` | object |  |
| `host.services.mysql.status_flags` | nested | The set of status flags the server returned in the initial HandshakePacket. Each entry corresponds to a bit being set in the flags; key names correspond to the #defines in the MySQL docs. |
| `host.services.mysql.status_flags.key` | text |  |
| `host.services.mysql.status_flags.value` | boolean |  |
| `host.services.mysql.auth_plugin_data` | text | Optional plugin-specific data, whose meaning depends on the value of auth_plugin_name. Returned in the initial HandshakePacket. |
| `host.services.mysql.auth_plugin_name` | text | The name of the authentication plugin, returned in the initial HandshakePacket. |
| `host.services.mysql.capability_flags` | nested | The set of capability flags the server returned in the initial HandshakePacket. Each entry corresponds to a bit being set in the flags; key names correspond to the #defines in the MySQL docs. |
| `host.services.mysql.capability_flags.key` | text |  |
| `host.services.mysql.capability_flags.value` | boolean |  |
| `host.services.mysql.character_set` | unsigned_long | The identifier for the character set the server is using. Returned in the initial HandshakePacket. |
| `host.services.mysql.error_code` | long | Only set if there is an error returned by the server, for example if the scanner is not on the allowed hosts list. |
| `host.services.mysql.server_version` | text | The specific server version returned in the initial HandshakePacket. Often in the form x.y.z, but not always. |
| `host.services.mysql.error_id` | text | The friendly name for the error code as defined at https://dev.mysql.com/doc/refman/8.0/en/error-messages-server.html, or UNKNOWN |
| `host.services.mysql.protocol_version` | unsigned_long | 8-bit unsigned integer representing the server's protocol version sent in the initial HandshakePacket from the server. |
| `host.services.mysql.connection_id` | unsigned_long | The server's internal identifier for this client's connection, sent in the initial HandshakePacket. |
| `host.services.mysql.error_message` | text | Optional string describing the error. Only set if there is an error. |
| `host.services.ldap` | object |  |
| `host.services.ldap.allows_anonymous_bind` | boolean | Ability to connect with anonymous bind (empty username and password) |
| `host.services.ldap.attributes` | nested | All root DN attributes available via anonymous bind |
| `host.services.ldap.attributes.name` | text | Name of the LDAP attribute in the root DN |
| `host.services.ldap.attributes.values` | text | Values for the respective LDAP attribute |
| `host.services.ldap.result_code` | unsigned_long | Result or error code returned by LDAP instance upon bind |
| `host.services.mongodb` | object |  |
| `host.services.mongodb.build_info` | object |  |
| `host.services.mongodb.build_info.build_environment` | object |  |
| `host.services.mongodb.build_info.build_environment.cc_flags` | text |  |
| `host.services.mongodb.build_info.build_environment.cxx_flags` | text |  |
| `host.services.mongodb.build_info.build_environment.cc` | text |  |
| `host.services.mongodb.build_info.build_environment.dist_mod` | text |  |
| `host.services.mongodb.build_info.build_environment.target_arch` | text |  |
| `host.services.mongodb.build_info.build_environment.dist_arch` | text |  |
| `host.services.mongodb.build_info.build_environment.target_os` | text |  |
| `host.services.mongodb.build_info.build_environment.cxx` | text |  |
| `host.services.mongodb.build_info.build_environment.link_flags` | text |  |
| `host.services.mongodb.build_info.git_version` | text | Version of mongodb server |
| `host.services.mongodb.build_info.version` | text | Version of mongodb server |
| `host.services.mongodb.is_master` | object |  |
| `host.services.mongodb.is_master.min_wire_version` | integer |  |
| `host.services.mongodb.is_master.read_only` | boolean |  |
| `host.services.mongodb.is_master.is_master` | boolean |  |
| `host.services.mongodb.is_master.logical_session_timeout_minutes` | integer |  |
| `host.services.mongodb.is_master.max_bson_object_size` | integer |  |
| `host.services.mongodb.is_master.max_message_size_bytes` | integer |  |
| `host.services.mongodb.is_master.max_wire_version` | integer |  |
| `host.services.mongodb.is_master.max_write_batch_size` | integer |  |
| `host.services.oracle` | object |  |
| `host.services.oracle.refuse_version` | text | The version declared by the service when it refuses the handshake, if applicable. |
| `host.services.oracle.did_resend` | boolean | Whether the server requested that the scanner resend its initial connection packet. |
| `host.services.oracle.global_service_options` | nested | Set of flags that the server returns in the Accept packet. |
| `host.services.oracle.global_service_options.key` | text |  |
| `host.services.oracle.global_service_options.value` | boolean |  |
| `host.services.oracle.refuse_error` | object | The parsed descriptor returned by the server in the Refuse packet; it is empty if the server does not return a Refuse packet. The keys are strings like 'DESCRIPTION.ERROR_STACK.ERROR.CODE |
| `host.services.oracle.refuse_error.value` | text | The parsed value from the error received when the initial handshake is refused. |
| `host.services.oracle.refuse_error.key` | text | The dot-delimited path to the parsed value from the error received when the initial handshake is refused. |
| `host.services.oracle.refuse_reason_sys` | text | The 'SysReason' returned by the server in the RefusePacket, as an 8-bit unsigned hex string. |
| `host.services.oracle.nsn_service_versions` | nested | A map from the native Service Negotation service names to the ReleaseVersion (in dotted-decimal format) in that service packet. |
| `host.services.oracle.nsn_service_versions.value` | text |  |
| `host.services.oracle.nsn_service_versions.key` | text |  |
| `host.services.oracle.connect_flags0` | nested | The first set of ConnectFlags returned in the Accept packet. |
| `host.services.oracle.connect_flags0.value` | boolean |  |
| `host.services.oracle.connect_flags0.key` | text |  |
| `host.services.oracle.refuse_reason_app` | text | The 'AppReason' returned by the server in the RefusePacket, as an 8-bit unsigned hex string. |
| `host.services.oracle.accept_version` | unsigned_long | The version declared by the service when it accepts the handshake, if applicable. |
| `host.services.oracle.refuse_error_raw` | text | The unparsed error received when the initial handshake is refused. |
| `host.services.oracle.nsn_version` | text | The version string in the root of the native service negotiation packet, if applicable. |
| `host.services.oracle.connect_flags1` | nested | The second set of ConnectFlags returned in the Accept packet. |
| `host.services.oracle.connect_flags1.key` | text |  |
| `host.services.oracle.connect_flags1.value` | boolean |  |
| `host.services.pc_anywhere` | object |  |
| `host.services.pc_anywhere.nr` | text | Full 'NR' query response |
| `host.services.pc_anywhere.status` | object |  |
| `host.services.pc_anywhere.status.raw` | text | Full 'ST' query response |
| `host.services.pc_anywhere.status.in_use` | boolean | Workstation is In Use if true, Available if false |
| `host.services.pc_anywhere.name` | text | Workstation Name, with padding bytes removed |
| `host.services.dns` | object |  |
| `host.services.dns.authorities` | object | A list of resource records (RRs) contained in the AUTHORITIES section of the response. |
| `host.services.dns.authorities.type` | keyword | An enumerated field indicating what type of data is in the "services.dns.additionals.response" field. For example, "A" signifies that the value in "services.dns.additionals.response" is an IPv4 address for the FQDN in "services.dns.additionals.name". |
| `host.services.dns.authorities.name` | text | The Fully Qualified Domain Name (FQDN) this RR is for. |
| `host.services.dns.authorities.response` | text | The RDATA field of the RR. |
| `host.services.dns.r_code` | keyword | A enumerated field indicating the result of the request. The most common values are defined in RFC 1035. |
| `host.services.dns.resolves_correctly` | boolean | Whether the server returns an IP address for ip.parrotdns.com that matches the authoritative server, which is controlled by Censys. |
| `host.services.dns.server_type` | keyword | An enumerated value indicating the behavior of the server. An AUTHORITATIVE server fulfills requests for domain names it controls, which are not listed by the server. FORWARDING and RECURSIVE_RESOLVER servers fulfill requests indirectly for domain names they do not control. A RECURSIVE_RESOLVER will query ip.parrotdns.com itself, resulting in its own IP address being present in the dns.answers.response field. |
| `host.services.dns.version` | text |  |
| `host.services.dns.additionals` | object | A list of resource records (RRs) contained in the ADDITIONAL section of the response. |
| `host.services.dns.additionals.name` | text | The Fully Qualified Domain Name (FQDN) this RR is for. |
| `host.services.dns.additionals.response` | text | The RDATA field of the RR. |
| `host.services.dns.additionals.type` | keyword | An enumerated field indicating what type of data is in the "services.dns.additionals.response" field. For example, "A" signifies that the value in "services.dns.additionals.response" is an IPv4 address for the FQDN in "services.dns.additionals.name". |
| `host.services.dns.questions` | object | A list of resource records (RRs) contained in the QUESTION section of the response, which may echo the request that the server is responding to. |
| `host.services.dns.questions.type` | keyword | An enumerated field indicating what type of data is in the "services.dns.additionals.response" field. For example, "A" signifies that the value in "services.dns.additionals.response" is an IPv4 address for the FQDN in "services.dns.additionals.name". |
| `host.services.dns.questions.name` | text | The Fully Qualified Domain Name (FQDN) this RR is for. |
| `host.services.dns.questions.response` | text | The RDATA field of the RR. |
| `host.services.dns.edns` | object |  |
| `host.services.dns.edns.version` | unsigned_long |  |
| `host.services.dns.edns.do` | boolean |  |
| `host.services.dns.edns.options` | text |  |
| `host.services.dns.edns.udp` | unsigned_long |  |
| `host.services.dns.answers` | object | A list of resource records (RRs) contained in the ANSWER section of the response. |
| `host.services.dns.answers.response` | text | The RDATA field of the RR. |
| `host.services.dns.answers.type` | keyword | An enumerated field indicating what type of data is in the "services.dns.additionals.response" field. For example, "A" signifies that the value in "services.dns.additionals.response" is an IPv4 address for the FQDN in "services.dns.additionals.name". |
| `host.services.dns.answers.name` | text | The Fully Qualified Domain Name (FQDN) this RR is for. |
| `host.services.socks` | object |  |
| `host.services.socks.no_authentication_required` | boolean |  |
| `host.services.socks.preferred_authentication` | text |  |
| `host.services.socks.preferred_authentication_value` | unsigned_long |  |
| `host.services.socks.socks_version` | long |  |
| `host.services.socks.supported_versions` | long |  |
| `host.services.darkcomet` | object |  |
| `host.services.darkcomet.version` | text |  |
| `host.services.vulns` | nested |  |
| `host.services.vulns.severity` | keyword |  |
| `host.services.vulns.year` | unsigned_long |  |
| `host.services.vulns.cwes` | object |  |
| `host.services.vulns.cwes.entry` | text | A unique identifier associated with a class of a software or hardware weakness. |
| `host.services.vulns.risk_source` | keyword |  |
| `host.services.vulns.type` | text |  |
| `host.services.vulns.name` | text |  |
| `host.services.vulns.source` | keyword |  |
| `host.services.vulns.confidence` | double |  |
| `host.services.vulns.evidence` | nested |  |
| `host.services.vulns.evidence.literal_match` | text |  |
| `host.services.vulns.evidence.negative` | boolean |  |
| `host.services.vulns.evidence.proprietary` | boolean |  |
| `host.services.vulns.evidence.regex` | text |  |
| `host.services.vulns.evidence.semver_expression` | text |  |
| `host.services.vulns.evidence.data_path` | text |  |
| `host.services.vulns.evidence.exists` | boolean |  |
| `host.services.vulns.evidence.found_value` | text |  |
| `host.services.vulns.kev` | object |  |
| `host.services.vulns.kev.source` | keyword | The source checked to determine whether the CVE is in the KEV catalog. |
| `host.services.vulns.kev.date_added` | date | The date the vulnerability was added to the KEV catalog. |
| `host.services.vulns.kev.date_due` | date | Per CISA’s Binding Operation Directive 22-01, the date all federal civilian executive branch (FCEB) agencies are required to remediate vulnerabilities in the KEV catalog. |
| `host.services.vulns.id` | text |  |
| `host.services.vulns.metrics` | object |  |
| `host.services.vulns.metrics.cvss_v40` | object |  |
| `host.services.vulns.metrics.cvss_v40.vector` | text | The path, method, or scenario used to exploit the vulnerability. Each section represents components that contribute to the overall CVSS score. |
| `host.services.vulns.metrics.cvss_v40.components` | object | These metrics contribute to how a CVE is scored. |
| `host.services.vulns.metrics.cvss_v40.components.attack_complexity` | keyword | Indicates conditions beyond the attacker’s control that must exist in order to exploit the vulnerability. The Attack Complexity metric is scored as either Low or High. There are two possible values: Low (L) – There are no specific pre-conditions required for exploitation, High (H) – The attacker must complete some number of preparatory steps in order to get access. |
| `host.services.vulns.metrics.cvss_v40.components.confidentiality` | keyword | Refers to the disclosure of sensitive information to authorized and unauthorized users, with the goal being that only authorized users are able to access the target data. Confidentiality has three potential values: High (H) – The attacker has full access to all resources in the impacted system, including highly sensitive information such as encryption keys, Low (L) – The attacker has partial access to information, with no control over what, specifically, they are able to access, None (N) – No data is accessible to unauthorized users as a result of the exploit. |
| `host.services.vulns.metrics.cvss_v40.components.privileges_required` | keyword | Describes the level of privileges or access an attacker must have before successful exploitation. There are three possible values: None (N) – There is no privilege or special access required to conduct the attack, Low (L) – The attacker requires basic, “user” level privileges to leverage the exploit, High (H) – Administrative or similar access privileges are required for successful attack. |
| `host.services.vulns.metrics.cvss_v40.components.automatable` | keyword |  |
| `host.services.vulns.metrics.cvss_v40.components.vulnerability_response_effort` | keyword |  |
| `host.services.vulns.metrics.cvss_v40.components.provider_urgency` | keyword |  |
| `host.services.vulns.metrics.cvss_v40.components.recovery` | keyword |  |
| `host.services.vulns.metrics.cvss_v40.components.attack_vector` | keyword | Indicates the level of access required for an attacker to exploit the vulnerability. The Attack Vector metric is scored in one of four levels: Network (N) – Vulnerabilities with this rating are remotely exploitable, from one or more hops away, up to, and including, remote exploitation over the Internet, Adjacent (A) – A vulnerability with this rating requires network adjacency for exploitation. The attack must be launched from the same physical or logical network, Local (L) – Vulnerabilities with this rating are not exploitable over a network, Physical (P) – An attacker must physically interact with the target system. |
| `host.services.vulns.metrics.cvss_v40.components.availability` | keyword | If an attack renders information unavailable, such as when a system crashes or through a DDoS attack, availability is negatively impacted. Availability has three possible values: None (N) – There is no loss of availability, Low (L) – Availability might be intermittently limited, or performance might be negatively impacted, as a result of a successful attack, High (H) – There is a complete loss of availability of the impacted system or information. |
| `host.services.vulns.metrics.cvss_v40.components.value_density` | keyword |  |
| `host.services.vulns.metrics.cvss_v40.components.integrity` | keyword | Refers to whether the protected information has been tampered with or changed in any way. If there is no way for an attacker to alter the accuracy or completeness of the information, integrity has been maintained. Integrity has three values: None (N) – There is no loss of the integrity of any information, Low (L) – A limited amount of information might be tampered with or modified, but there is no serious impact on the protected system, High (H) – The attacker can modify any/all information on the target system, resulting in a complete loss of integrity. |
| `host.services.vulns.metrics.cvss_v40.components.attack_requirements` | keyword |  |
| `host.services.vulns.metrics.cvss_v40.components.safety` | keyword |  |
| `host.services.vulns.metrics.cvss_v40.components.user_interaction` | keyword | Describes whether a user, other than the attacker, is required to do anything or participate in exploitation of the vulnerability. User interaction has two possible values: None (N) – No user interaction is required, Required (R) – A user must complete some steps for the exploit to succeed. For example, a user might be required to install some software. |
| `host.services.vulns.metrics.cvss_v40.score` | double | Score of the vulnerability; 0.1 is the lowest, 10 is the maximum |
| `host.services.vulns.metrics.epss` | object |  |
| `host.services.vulns.metrics.epss.percentile` | double |  |
| `host.services.vulns.metrics.epss.score` | double |  |
| `host.services.vulns.metrics.cvss_v30` | object |  |
| `host.services.vulns.metrics.cvss_v30.components` | object | These metrics contribute to how a CVE is scored. |
| `host.services.vulns.metrics.cvss_v30.components.scope` | keyword | Determines whether a vulnerability in one system or component can impact another system or component. If a vulnerability in a vulnerable component can affect a component which is in a different security scope than the vulnerable component, a scope change occurs. Scope has two possible ratings: Changed (C) – An exploited vulnerability can have a carry over impact on another system, Unchanged (U) – The exploited vulnerability is limited in damage to only the local security authority. |
| `host.services.vulns.metrics.cvss_v30.components.user_interaction` | keyword | Describes whether a user, other than the attacker, is required to do anything or participate in exploitation of the vulnerability. User interaction has two possible values: None (N) – No user interaction is required, Required (R) – A user must complete some steps for the exploit to succeed. For example, a user might be required to install some software. |
| `host.services.vulns.metrics.cvss_v30.components.attack_complexity` | keyword | Indicates conditions beyond the attacker’s control that must exist in order to exploit the vulnerability. The Attack Complexity metric is scored as either Low or High. There are two possible values: Low (L) – There are no specific pre-conditions required for exploitation, High (H) – The attacker must complete some number of preparatory steps in order to get access. |
| `host.services.vulns.metrics.cvss_v30.components.attack_vector` | keyword | Indicates the level of access required for an attacker to exploit the vulnerability. The Attack Vector metric is scored in one of four levels: Network (N) – Vulnerabilities with this rating are remotely exploitable, from one or more hops away, up to, and including, remote exploitation over the Internet, Adjacent (A) – A vulnerability with this rating requires network adjacency for exploitation. The attack must be launched from the same physical or logical network, Local (L) – Vulnerabilities with this rating are not exploitable over a network, Physical (P) – An attacker must physically interact with the target system. |
| `host.services.vulns.metrics.cvss_v30.components.availability` | keyword | If an attack renders information unavailable, such as when a system crashes or through a DDoS attack, availability is negatively impacted. Availability has three possible values: None (N) – There is no loss of availability, Low (L) – Availability might be intermittently limited, or performance might be negatively impacted, as a result of a successful attack, High (H) – There is a complete loss of availability of the impacted system or information. |
| `host.services.vulns.metrics.cvss_v30.components.confidentiality` | keyword | Refers to the disclosure of sensitive information to authorized and unauthorized users, with the goal being that only authorized users are able to access the target data. Confidentiality has three potential values: High (H) – The attacker has full access to all resources in the impacted system, including highly sensitive information such as encryption keys, Low (L) – The attacker has partial access to information, with no control over what, specifically, they are able to access, None (N) – No data is accessible to unauthorized users as a result of the exploit. |
| `host.services.vulns.metrics.cvss_v30.components.integrity` | keyword | Refers to whether the protected information has been tampered with or changed in any way. If there is no way for an attacker to alter the accuracy or completeness of the information, integrity has been maintained. Integrity has three values: None (N) – There is no loss of the integrity of any information, Low (L) – A limited amount of information might be tampered with or modified, but there is no serious impact on the protected system, High (H) – The attacker can modify any/all information on the target system, resulting in a complete loss of integrity. |
| `host.services.vulns.metrics.cvss_v30.components.privileges_required` | keyword | Describes the level of privileges or access an attacker must have before successful exploitation. There are three possible values: None (N) – There is no privilege or special access required to conduct the attack, Low (L) – The attacker requires basic, “user” level privileges to leverage the exploit, High (H) – Administrative or similar access privileges are required for successful attack. |
| `host.services.vulns.metrics.cvss_v30.score` | double | Score of the vulnerability; 0.1 is the lowest, 10 is the maximum |
| `host.services.vulns.metrics.cvss_v30.vector` | text | The path, method, or scenario used to exploit the vulnerability. Each section represents components that contribute to the overall CVSS score. |
| `host.services.vulns.metrics.cvss_v31` | object |  |
| `host.services.vulns.metrics.cvss_v31.components` | object | These metrics contribute to how a CVE is scored. |
| `host.services.vulns.metrics.cvss_v31.components.confidentiality` | keyword | Refers to the disclosure of sensitive information to authorized and unauthorized users, with the goal being that only authorized users are able to access the target data. Confidentiality has three potential values: High (H) – The attacker has full access to all resources in the impacted system, including highly sensitive information such as encryption keys, Low (L) – The attacker has partial access to information, with no control over what, specifically, they are able to access, None (N) – No data is accessible to unauthorized users as a result of the exploit. |
| `host.services.vulns.metrics.cvss_v31.components.integrity` | keyword | Refers to whether the protected information has been tampered with or changed in any way. If there is no way for an attacker to alter the accuracy or completeness of the information, integrity has been maintained. Integrity has three values: None (N) – There is no loss of the integrity of any information, Low (L) – A limited amount of information might be tampered with or modified, but there is no serious impact on the protected system, High (H) – The attacker can modify any/all information on the target system, resulting in a complete loss of integrity. |
| `host.services.vulns.metrics.cvss_v31.components.privileges_required` | keyword | Describes the level of privileges or access an attacker must have before successful exploitation. There are three possible values: None (N) – There is no privilege or special access required to conduct the attack, Low (L) – The attacker requires basic, “user” level privileges to leverage the exploit, High (H) – Administrative or similar access privileges are required for successful attack. |
| `host.services.vulns.metrics.cvss_v31.components.scope` | keyword | Determines whether a vulnerability in one system or component can impact another system or component. If a vulnerability in a vulnerable component can affect a component which is in a different security scope than the vulnerable component, a scope change occurs. Scope has two possible ratings: Changed (C) – An exploited vulnerability can have a carry over impact on another system, Unchanged (U) – The exploited vulnerability is limited in damage to only the local security authority. |
| `host.services.vulns.metrics.cvss_v31.components.user_interaction` | keyword | Describes whether a user, other than the attacker, is required to do anything or participate in exploitation of the vulnerability. User interaction has two possible values: None (N) – No user interaction is required, Required (R) – A user must complete some steps for the exploit to succeed. For example, a user might be required to install some software. |
| `host.services.vulns.metrics.cvss_v31.components.attack_complexity` | keyword | Indicates conditions beyond the attacker’s control that must exist in order to exploit the vulnerability. The Attack Complexity metric is scored as either Low or High. There are two possible values: Low (L) – There are no specific pre-conditions required for exploitation, High (H) – The attacker must complete some number of preparatory steps in order to get access. |
| `host.services.vulns.metrics.cvss_v31.components.attack_vector` | keyword | Indicates the level of access required for an attacker to exploit the vulnerability. The Attack Vector metric is scored in one of four levels: Network (N) – Vulnerabilities with this rating are remotely exploitable, from one or more hops away, up to, and including, remote exploitation over the Internet, Adjacent (A) – A vulnerability with this rating requires network adjacency for exploitation. The attack must be launched from the same physical or logical network, Local (L) – Vulnerabilities with this rating are not exploitable over a network, Physical (P) – An attacker must physically interact with the target system. |
| `host.services.vulns.metrics.cvss_v31.components.availability` | keyword | If an attack renders information unavailable, such as when a system crashes or through a DDoS attack, availability is negatively impacted. Availability has three possible values: None (N) – There is no loss of availability, Low (L) – Availability might be intermittently limited, or performance might be negatively impacted, as a result of a successful attack, High (H) – There is a complete loss of availability of the impacted system or information. |
| `host.services.vulns.metrics.cvss_v31.score` | double | Score of the vulnerability; 0.1 is the lowest, 10 is the maximum |
| `host.services.vulns.metrics.cvss_v31.vector` | text | The path, method, or scenario used to exploit the vulnerability. Each section represents components that contribute to the overall CVSS score. |
| `host.services.telnet` | object |  |
| `host.services.telnet.do` | object |  |
| `host.services.telnet.do.key` | unsigned_long |  |
| `host.services.telnet.do.value` | text |  |
| `host.services.telnet.dont` | object |  |
| `host.services.telnet.dont.key` | unsigned_long |  |
| `host.services.telnet.dont.value` | text |  |
| `host.services.telnet.will` | object |  |
| `host.services.telnet.will.key` | unsigned_long |  |
| `host.services.telnet.will.value` | text |  |
| `host.services.telnet.wont` | object |  |
| `host.services.telnet.wont.key` | unsigned_long |  |
| `host.services.telnet.wont.value` | text |  |
| `host.services.dhcpdiscover` | object |  |
| `host.services.dhcpdiscover.params` | object |  |
| `host.services.dhcpdiscover.params.device_info` | object |  |
| `host.services.dhcpdiscover.params.device_info.http_port` | long |  |
| `host.services.dhcpdiscover.params.device_info.alarm_input_channels` | long |  |
| `host.services.dhcpdiscover.params.device_info.video_output_channels` | long |  |
| `host.services.dhcpdiscover.params.device_info.vendor` | text |  |
| `host.services.dhcpdiscover.params.device_info.ipv4_address` | object |  |
| `host.services.dhcpdiscover.params.device_info.ipv4_address.dhcp_enable` | boolean |  |
| `host.services.dhcpdiscover.params.device_info.ipv4_address.ip_address` | text |  |
| `host.services.dhcpdiscover.params.device_info.ipv4_address.link_local_address` | text |  |
| `host.services.dhcpdiscover.params.device_info.ipv4_address.subnetmask` | text |  |
| `host.services.dhcpdiscover.params.device_info.ipv4_address.default_gateway` | text |  |
| `host.services.dhcpdiscover.params.device_info.device_class` | text |  |
| `host.services.dhcpdiscover.params.device_info.manufacturer` | text |  |
| `host.services.dhcpdiscover.params.device_info.port` | long |  |
| `host.services.dhcpdiscover.params.device_info.remote_video_input_channels` | long |  |
| `host.services.dhcpdiscover.params.device_info.unlogin_func_mask` | long |  |
| `host.services.dhcpdiscover.params.device_info.alarm_output_channels` | long |  |
| `host.services.dhcpdiscover.params.device_info.device_id` | text |  |
| `host.services.dhcpdiscover.params.device_info.video_input_channels` | long |  |
| `host.services.dhcpdiscover.params.device_info.machine_group` | text |  |
| `host.services.dhcpdiscover.params.device_info.machine_name` | text |  |
| `host.services.dhcpdiscover.params.device_info.device_type` | text |  |
| `host.services.dhcpdiscover.params.device_info.serial_number` | text |  |
| `host.services.dhcpdiscover.params.device_info.ipv6_address` | object |  |
| `host.services.dhcpdiscover.params.device_info.ipv6_address.dhcp_enable` | boolean |  |
| `host.services.dhcpdiscover.params.device_info.ipv6_address.ip_address` | text |  |
| `host.services.dhcpdiscover.params.device_info.ipv6_address.link_local_address` | text |  |
| `host.services.dhcpdiscover.params.device_info.ipv6_address.subnetmask` | text |  |
| `host.services.dhcpdiscover.params.device_info.ipv6_address.default_gateway` | text |  |
| `host.services.dhcpdiscover.params.device_info.version` | text |  |
| `host.services.dhcpdiscover.method` | text |  |
| `host.services.fox` | object |  |
| `host.services.fox.version` | text |  |
| `host.services.fox.host_address` | text |  |
| `host.services.fox.id` | unsigned_long |  |
| `host.services.fox.host_id` | text |  |
| `host.services.fox.hostname` | text |  |
| `host.services.fox.vm_name` | text |  |
| `host.services.fox.brand_id` | text |  |
| `host.services.fox.time_zone` | text |  |
| `host.services.fox.os_name` | text |  |
| `host.services.fox.language` | text |  |
| `host.services.fox.app_name` | text |  |
| `host.services.fox.vm_uuid` | text |  |
| `host.services.fox.app_version` | text |  |
| `host.services.fox.os_version` | text |  |
| `host.services.fox.auth_agent_type` | text |  |
| `host.services.fox.vm_version` | text |  |
| `host.services.fox.sys_info` | text |  |
| `host.services.fox.station_name` | text |  |
| `host.services.redis` | object |  |
| `host.services.redis.connections_received` | unsigned_long | The total number of connections accepted by the server. |
| `host.services.redis.used_memory` | unsigned_long | The total number of bytes allocated by Redis using its allocator. |
| `host.services.redis.ping_response` | text | The response from the PING command; should either be "PONG" or an authentication error. |
| `host.services.redis.gcc_version` | text | The version of the GCC compiler used to compile the Redis server. |
| `host.services.redis.raw_command_output` | object | The raw output returned by the server for each command sent; the indices match those of commands. |
| `host.services.redis.raw_command_output.output` | text |  |
| `host.services.redis.commands_processed` | unsigned_long | The total number of commands processed by the server. |
| `host.services.redis.mem_allocator` | text | The memory allocator. |
| `host.services.redis.arch_bits` | text | The architecture bits (32 or 64) the Redis server used to build. |
| `host.services.redis.build_id` | text | The Build ID of the Redis server. |
| `host.services.redis.major` | unsigned_long | Major is the version's major number. |
| `host.services.redis.uptime` | unsigned_long | The number of seconds since Redis server start. |
| `host.services.redis.commands` | text | The list of commands actually sent to the server, serialized in inline format, like 'PING' or 'AUTH somePassword'. |
| `host.services.redis.auth_response` | text | The response from the AUTH command, if sent. |
| `host.services.redis.os` | text | The OS the Redis server is running, read from the the info_response (if available). |
| `host.services.redis.git_sha1` | text | The Sha-1 Git commit hash the Redis server used. |
| `host.services.redis.mode` | text | The mode the Redis server is running (standalone or cluster), read from the the info_response (if available). |
| `host.services.redis.patch_level` | unsigned_long | Patchlevel is the version's patchlevel number. |
| `host.services.redis.quit_response` | text | The response to the QUIT command. |
| `host.services.redis.nonexistent_response` | text | The response from the NONEXISTENT command. |
| `host.services.redis.info_response` | object | The response from the INFO command. Should be a series of key:value pairs separated by CRLFs. |
| `host.services.redis.info_response.value` | text |  |
| `host.services.redis.info_response.key` | text |  |
| `host.services.redis.minor` | unsigned_long | Minor is the version's major number. |
| `host.services.ntp` | object |  |
| `host.services.ntp.get_time_header` | object | The header of the server's response to a GetTime request. |
| `host.services.ntp.get_time_header.mode` | unsigned_long | An enumerated value from 0 to 7 signifying the operational mode of the server. |
| `host.services.ntp.get_time_header.poll` | integer | The interval within which the server will expect a subsequent synchronization message, in log2 seconds. |
| `host.services.ntp.get_time_header.precision` | integer | The precision of the system's clock, in log2 seconds. |
| `host.services.ntp.get_time_header.reference_id` | text | The identifier of the reference clock. For servers in stratum 1, one of an IANA-maintained list of sources. For servers in stratum 2, the ID of the stratum 1 server from which the time was retrieved (usually, its IP address), etc. |
| `host.services.ntp.get_time_header.stratum` | unsigned_long | The number of servers between a client and a non-NTP time source. 1 signifies that the server is authoritative, having direct access to a sensor. 2 signifies that the server got its time from a "stratum 1" server, etc. 16 means the clock is unsynchronized. |
| `host.services.ntp.get_time_header.version` | unsigned_long | The NTP version indicated in the server's response. |
| `host.services.ntp.get_time_header.leap_indicator` | unsigned_long | An enumerated value from 0 to 3 signifying whether a leap second will occur at the end of the current month. 0 signifies no leap second, 1 signifies an additive leap second, 2 signifies a subtractive leap second, and 3 signifies the state is unknown. |
| `host.services.dcerpc` | object |  |
| `host.services.dcerpc.could_bind` | boolean |  |
| `host.services.dcerpc.could_query_epm` | boolean |  |
| `host.services.dcerpc.endpoints` | object |  |
| `host.services.dcerpc.endpoints.explained_uuid` | text |  |
| `host.services.dcerpc.endpoints.protocol` | text |  |
| `host.services.dcerpc.endpoints.bindings` | text |  |
| `host.services.dcerpc.endpoints.executable` | text |  |
| `host.services.epmd` | object |  |
| `host.services.epmd.names` | text |  |
| `host.services.modbus` | object |  |
| `host.services.modbus.exception_response` | object |  |
| `host.services.modbus.exception_response.exception_function` | unsigned_long |  |
| `host.services.modbus.exception_response.exception_type` | unsigned_long |  |
| `host.services.modbus.function` | unsigned_long |  |
| `host.services.modbus.mei_response` | object |  |
| `host.services.modbus.mei_response.conformity_level` | long |  |
| `host.services.modbus.mei_response.more_follows` | boolean |  |
| `host.services.modbus.mei_response.objects` | nested |  |
| `host.services.modbus.mei_response.objects.key` | text |  |
| `host.services.modbus.mei_response.objects.value` | text |  |
| `host.services.modbus.unit_id` | long |  |
| `host.services.x11` | object |  |
| `host.services.x11.version` | text |  |
| `host.services.x11.refusal_reason` | text |  |
| `host.services.x11.requires_authentication` | boolean |  |
| `host.services.x11.vendor` | text |  |
| `host.services.postgres` | object |  |
| `host.services.postgres.protocol_error` | nested | The error received in response to a StartupMessage with an unexpected protocol version. |
| `host.services.postgres.protocol_error.key` | text |  |
| `host.services.postgres.protocol_error.value` | text |  |
| `host.services.postgres.startup_error` | nested | The error received in response to a StartupMessage without providing the User field. |
| `host.services.postgres.startup_error.key` | text |  |
| `host.services.postgres.startup_error.value` | text |  |
| `host.services.postgres.supported_versions` | text |  |
| `host.services.rocketmq` | object |  |
| `host.services.rocketmq.topics` | object |  |
| `host.services.rocketmq.topics.topic_list` | text |  |
| `host.services.rocketmq.topics.header` | object |  |
| `host.services.rocketmq.topics.header.serialize_type_current_rpc` | text |  |
| `host.services.rocketmq.topics.header.code` | long |  |
| `host.services.rocketmq.topics.header.flag` | long |  |
| `host.services.rocketmq.topics.header.language` | text |  |
| `host.services.rocketmq.topics.header.opaque` | long |  |
| `host.services.rocketmq.version` | text |  |
| `host.services.rocketmq.cluster_info` | object |  |
| `host.services.rocketmq.cluster_info.header` | object |  |
| `host.services.rocketmq.cluster_info.header.serialize_type_current_rpc` | text |  |
| `host.services.rocketmq.cluster_info.header.code` | long |  |
| `host.services.rocketmq.cluster_info.header.flag` | long |  |
| `host.services.rocketmq.cluster_info.header.language` | text |  |
| `host.services.rocketmq.cluster_info.header.opaque` | long |  |
| `host.services.rocketmq.cluster_info.payload` | text |  |
| `host.services.monero_p2p` | object |  |
| `host.services.monero_p2p.ping_response` | object |  |
| `host.services.monero_p2p.ping_response.response_header` | object |  |
| `host.services.monero_p2p.ping_response.response_header.signature` | unsigned_long |  |
| `host.services.monero_p2p.ping_response.response_header.version` | unsigned_long |  |
| `host.services.monero_p2p.ping_response.response_header.command` | unsigned_long |  |
| `host.services.monero_p2p.ping_response.response_header.expects_response` | boolean |  |
| `host.services.monero_p2p.ping_response.response_header.flags` | unsigned_long |  |
| `host.services.monero_p2p.ping_response.response_header.length` | unsigned_long |  |
| `host.services.monero_p2p.ping_response.response_header.return_code` | integer |  |
| `host.services.monero_p2p.ping_response.payload` | object |  |
| `host.services.monero_p2p.ping_response.payload.entries` | object |  |
| `host.services.monero_p2p.ping_response.payload.entries.name` | text |  |
| `host.services.monero_p2p.ping_response.payload.entries.data` | text |  |
| `host.services.opc_ua` | object |  |
| `host.services.opc_ua.max_message_size` | unsigned_long |  |
| `host.services.opc_ua.protocol_version` | unsigned_long |  |
| `host.services.opc_ua.receive_buffer_size` | unsigned_long |  |
| `host.services.opc_ua.send_buffer_size` | unsigned_long |  |
| `host.services.opc_ua.endpoints` | object |  |
| `host.services.opc_ua.endpoints.security_mode` | unsigned_long |  |
| `host.services.opc_ua.endpoints.security_policy_uri` | text |  |
| `host.services.opc_ua.endpoints.serve_cert` | text |  |
| `host.services.opc_ua.endpoints.server` | object |  |
| `host.services.opc_ua.endpoints.server.product_uri` | text |  |
| `host.services.opc_ua.endpoints.server.application_name` | object |  |
| `host.services.opc_ua.endpoints.server.application_name.text` | text |  |
| `host.services.opc_ua.endpoints.server.application_name.flags` | unsigned_long |  |
| `host.services.opc_ua.endpoints.server.application_name.locale` | text |  |
| `host.services.opc_ua.endpoints.server.application_type` | unsigned_long |  |
| `host.services.opc_ua.endpoints.server.application_uri` | text |  |
| `host.services.opc_ua.endpoints.server.discovery_profile_uri` | text |  |
| `host.services.opc_ua.endpoints.server.discovery_urls` | text |  |
| `host.services.opc_ua.endpoints.server.gateway_server_uri` | text |  |
| `host.services.opc_ua.endpoints.transport_profile_uri` | text |  |
| `host.services.opc_ua.endpoints.user_identity_token` | object |  |
| `host.services.opc_ua.endpoints.user_identity_token.issuer_endpoint_url` | text |  |
| `host.services.opc_ua.endpoints.user_identity_token.policy_id` | text |  |
| `host.services.opc_ua.endpoints.user_identity_token.security_policy_uri` | text |  |
| `host.services.opc_ua.endpoints.user_identity_token.token_type` | integer |  |
| `host.services.opc_ua.endpoints.user_identity_token.issued_token_type` | text |  |
| `host.services.opc_ua.endpoints.endpoint_url` | text |  |
| `host.services.opc_ua.endpoints.security_level` | unsigned_long |  |
| `host.services.opc_ua.max_chunk_size` | unsigned_long |  |
| `host.services.zeromq` | object |  |
| `host.services.zeromq.subscription_data` | text |  |
| `host.services.zeromq.subscription_match` | object |  |
| `host.services.zeromq.subscription_match.key` | text |  |
| `host.services.zeromq.subscription_match.value` | boolean |  |
| `host.services.zeromq.greeting` | object |  |
| `host.services.zeromq.greeting.version_major` | unsigned_long |  |
| `host.services.zeromq.greeting.version_minor` | unsigned_long |  |
| `host.services.zeromq.greeting.as_server` | boolean |  |
| `host.services.zeromq.greeting.mechanism` | text |  |
| `host.services.zeromq.greeting.signature` | text |  |
| `host.services.zeromq.handshake` | object |  |
| `host.services.zeromq.handshake.socket_type` | text |  |
| `host.services.zeromq.handshake.raw` | text |  |
| `host.services.zeromq.handshake.ready` | boolean |  |
| `host.services.activemq` | object |  |
| `host.services.activemq.max_inactivity_duration_initial_delay` | integer |  |
| `host.services.activemq.provider_name` | text |  |
| `host.services.activemq.cache_size` | integer |  |
| `host.services.activemq.max_frame_size` | long |  |
| `host.services.activemq.size_prefix_disabled` | boolean |  |
| `host.services.activemq.stack_trace_enabled` | boolean |  |
| `host.services.activemq.max_inactivity_duration` | long |  |
| `host.services.activemq.tcp_no_delay_enabled` | boolean |  |
| `host.services.activemq.platform_details` | text |  |
| `host.services.activemq.tight_encoding_enabled` | boolean |  |
| `host.services.activemq.provider_version` | text |  |
| `host.services.activemq.cache_enabled` | boolean |  |
| `host.services.ipmi` | object |  |
| `host.services.ipmi.raw` | text | The raw data returned by the server |
| `host.services.ipmi.rmcp_header` | object | The RMCP header of the response, (section 13.1.3) |
| `host.services.ipmi.rmcp_header.message_class` | object | The class of the message. |
| `host.services.ipmi.rmcp_header.message_class.raw` | integer | The raw message class byte. |
| `host.services.ipmi.rmcp_header.message_class.class` | integer | Just the class part of the byte (lower 5 bits of raw) |
| `host.services.ipmi.rmcp_header.message_class.is_ack` | boolean | True if the message is an acknowledgment to a previous message. |
| `host.services.ipmi.rmcp_header.message_class.name` | text | The human-readable name of the message class |
| `host.services.ipmi.rmcp_header.sequence_number` | integer | Sequence number of this packet in the session. |
| `host.services.ipmi.rmcp_header.version` | integer | The version. This scanner supports version 6. |
| `host.services.ipmi.session_header` | object | The IPMI sesssion header of the response |
| `host.services.ipmi.session_header.auth_type` | object | The authentication type for this request (see section 13.6) |
| `host.services.ipmi.session_header.auth_type.type` | integer | Just the auth type (reserved bits omitted) |
| `host.services.ipmi.session_header.auth_type.name` | text | The raw value of the auth_type |
| `host.services.ipmi.session_header.auth_type.raw` | integer | The raw value of the auth_type |
| `host.services.ipmi.session_header.session_id` | long | The ID of this sessiod. |
| `host.services.ipmi.session_header.session_sequence_number` | long | The session sequence number of this packet in the session |
| `host.services.ipmi.session_header.auth_code` | text | The 16-byte authentication code; not present if auth_type is None. |
| `host.services.ipmi.capabilities` | object | The Get Channel Authentication Capabilities response (section 22.13) |
| `host.services.ipmi.capabilities.auth_status` | object | The authentication status |
| `host.services.ipmi.capabilities.auth_status.auth_each_message` | boolean | If true, each message must be authenticated. |
| `host.services.ipmi.capabilities.auth_status.has_anonymous_users` | boolean | If true, the server has anonymous users. |
| `host.services.ipmi.capabilities.auth_status.has_named_users` | boolean | If true, the server supports named users. |
| `host.services.ipmi.capabilities.auth_status.two_key_login_required` | boolean | The KG field. |
| `host.services.ipmi.capabilities.auth_status.user_auth_disabled` | boolean | If true, user authentication is disabled. |
| `host.services.ipmi.capabilities.auth_status.anonymous_login_enabled` | boolean | If true, the server allows anonymous login. |
| `host.services.ipmi.capabilities.channel_number` | integer | The response channel number |
| `host.services.ipmi.capabilities.completion_code` | object | The status code of the response |
| `host.services.ipmi.capabilities.completion_code.raw` | integer | The raw completion code |
| `host.services.ipmi.capabilities.completion_code.name` | text | The human-readable name of the code |
| `host.services.ipmi.capabilities.extended_capabilities` | object | Extended auth capabilities (if present) |
| `host.services.ipmi.capabilities.extended_capabilities.supports_ipmi_v2_0` | boolean | True if IPMI v2.0 is supported |
| `host.services.ipmi.capabilities.extended_capabilities.supports_ipmi_v1_5` | boolean | True if IPMI v1.5 is supported |
| `host.services.ipmi.capabilities.oem_data` | integer | The OEM-specific data |
| `host.services.ipmi.capabilities.oem_id` | text | The 3-byte OEM identifier |
| `host.services.ipmi.capabilities.supported_auth_types` | object | The auth types supported by the server |
| `host.services.ipmi.capabilities.supported_auth_types.md5` | boolean | True if the MD5 AuthType is supported. |
| `host.services.ipmi.capabilities.supported_auth_types.none` | boolean | True if the None AuthType is supported. |
| `host.services.ipmi.capabilities.supported_auth_types.oem_proprietary` | boolean | True if the OEM Proprietary AuthType is supported |
| `host.services.ipmi.capabilities.supported_auth_types.password` | boolean | True if the Password AuthType is supported. |
| `host.services.ipmi.capabilities.supported_auth_types.raw` | integer | The raw byte, with the bit mask etc |
| `host.services.ipmi.capabilities.supported_auth_types.extended` | boolean | If true, the extended capabilities are present. |
| `host.services.ipmi.capabilities.supported_auth_types.md2` | boolean | True if the MD2 AuthType is supported. |
| `host.services.ipmi.command_payload` | object | The IPMI command payload |
| `host.services.ipmi.command_payload.network_function_code` | object | The NetFn and LUN |
| `host.services.ipmi.command_payload.network_function_code.raw` | integer | The raw value of the (NetFn << 2) \| LUN |
| `host.services.ipmi.command_payload.network_function_code.logical_unit_number` | object | The parsed LUN (logical unit number -- the lower 2 bits of raw) |
| `host.services.ipmi.command_payload.network_function_code.logical_unit_number.name` | text | The human-readable name of the LUN |
| `host.services.ipmi.command_payload.network_function_code.logical_unit_number.raw` | integer | The value of the LUN (3 bits) |
| `host.services.ipmi.command_payload.network_function_code.net_fn` | object | The parsed NetFn value (the upper 6 bits of raw) |
| `host.services.ipmi.command_payload.network_function_code.net_fn.is_request` | boolean | True if the least-significant bit is zero |
| `host.services.ipmi.command_payload.network_function_code.net_fn.is_response` | boolean | True if the least-significant bit is one |
| `host.services.ipmi.command_payload.network_function_code.net_fn.name` | text | The human-readable name of the NetFn |
| `host.services.ipmi.command_payload.network_function_code.net_fn.raw` | integer | The raw value of the NetFn (6 bits, least significant indicates request/response) |
| `host.services.ipmi.command_payload.network_function_code.net_fn.value` | integer | The normalized value of the NetFn (i.e. raw & 0xfe, so it is always even) |
| `host.services.ipmi.command_payload.requestor_sequence_number` | integer | The request sequence number. |
| `host.services.ipmi.command_payload.checksum_error` | boolean | This is set to true if the values of chk1 / chk2 do not match the command data |
| `host.services.ipmi.command_payload.data` | text | The raw data. On success, this should be the value of the GetAuthenticationCapabilities resopnse |
| `host.services.ipmi.command_payload.ipmi_command_number` | object | The parsed IPMI command number |
| `host.services.ipmi.command_payload.ipmi_command_number.name` | text | The human-readable name of the cmd + NetFn |
| `host.services.ipmi.command_payload.ipmi_command_number.raw` | integer | The raw value of the cmd value |
| `host.services.snmp` | object |  |
| `host.services.snmp.oid_system` | object | 1.3.6.1.2.1.1 - System Variables |
| `host.services.snmp.oid_system.name` | text | 1.3.6.1.2.1.1.5 - Name, usually FQDN |
| `host.services.snmp.oid_system.object_id` | text | 1.3.6.1.2.1.1.2 - Vendor ID |
| `host.services.snmp.oid_system.services` | object | 1.3.6.1.2.1.1.7 - Set of services offered by entity |
| `host.services.snmp.oid_system.services.layer_6` | boolean | OSI layer 6 |
| `host.services.snmp.oid_system.services.layer_7` | boolean | Applications (e.g. mail relays) |
| `host.services.snmp.oid_system.services.layer_1` | boolean | Physical (e.g. repeaters) |
| `host.services.snmp.oid_system.services.layer_2` | boolean | Datalink/subnetwork (e.g. bridges) |
| `host.services.snmp.oid_system.services.layer_3` | boolean | Internet (e.g. IP gateways) |
| `host.services.snmp.oid_system.services.layer_4` | boolean | End-to-end (e.g. IP hosts) |
| `host.services.snmp.oid_system.services.layer_5` | boolean | OSI layer 5 |
| `host.services.snmp.oid_system.contact` | text | 1.3.6.1.2.1.1.4 - Contact info |
| `host.services.snmp.oid_system.desc` | text | 1.3.6.1.2.1.1.1 - Description of entity |
| `host.services.snmp.oid_system.init_time` | unsigned_long | 1.3.6.1.2.1.1.3 - 1/100ths of sec |
| `host.services.snmp.oid_system.location` | text | 1.3.6.1.2.1.1.6 - Physical location |
| `host.services.snmp.versions` | text |  |
| `host.services.snmp.engine` | object |  |
| `host.services.snmp.engine.description` | text |  |
| `host.services.snmp.engine.organization` | text |  |
| `host.services.snmp.engine.format_data` | text |  |
| `host.services.snmp.engine.engine_time` | unsigned_long |  |
| `host.services.snmp.engine.pen` | unsigned_long |  |
| `host.services.snmp.engine.rfc3411` | boolean |  |
| `host.services.snmp.engine.format` | text |  |
| `host.services.snmp.engine.raw_id` | text |  |
| `host.services.snmp.engine.engine_boots` | unsigned_long |  |
| `host.services.snmp.oid_interfaces` | object | 1.3.6.1.2.1.2 - Interfaces |
| `host.services.snmp.oid_interfaces.num_ifaces` | unsigned_long | 1.3.6.1.2.1.2.1 - Number of network interfaces |
| `host.services.snmp.oid_physical` | object | 1.3.6.1.2.1.47.1.1.1.1 - Entity Physical |
| `host.services.snmp.oid_physical.mfg_name` | text | 1.3.6.1.2.1.47.1.1.1.1.12 - Name of mfg |
| `host.services.snmp.oid_physical.model_name` | text | 1.3.6.1.2.1.47.1.1.1.1.13 - Model name of component |
| `host.services.snmp.oid_physical.name` | text | 1.3.6.1.2.1.47.1.1.1.1.7 - Entity name |
| `host.services.snmp.oid_physical.serial_num` | text | 1.3.6.1.2.1.47.1.1.1.1.11 - Serial number string |
| `host.services.snmp.oid_physical.software_rev` | text | 1.3.6.1.2.1.47.1.1.1.1.10 - Software revision string |
| `host.services.snmp.oid_physical.firmware_rev` | text | 1.3.6.1.2.1.47.1.1.1.1.9 - Firmware revision string |
| `host.services.snmp.oid_physical.hardware_rev` | text | 1.3.6.1.2.1.47.1.1.1.1.8 - Hardware revision string |
| `host.services.tls` | object |  |
| `host.services.tls.fingerprint_sha256` | text | The SHA-256 digest of the entire raw certificate. Its unique identifier, which Censys uses to index certificates records. |
| `host.services.tls.ja3s` | text | The JA3S fingerprint for this service. |
| `host.services.tls.ja4s` | text |  |
| `host.services.tls.presented_chain` | object | Certificate chain information. |
| `host.services.tls.presented_chain.subject_dn` | text | Distinguished name of the entity that the certificate belongs to. |
| `host.services.tls.presented_chain.fingerprint_sha256` | text | SHA 256 fingerprint of the certificate in the certificate chain. |
| `host.services.tls.presented_chain.issuer_dn` | text | Distinguished name of the entity that has signed and issued the certificate. |
| `host.services.tls.version_selected` | keyword | Certificate version v1(0), v2(1), v3(2). |
| `host.services.tls.versions` | object |  |
| `host.services.tls.versions.ja3s` | text |  |
| `host.services.tls.versions.ja4s` | text |  |
| `host.services.tls.versions.version` | keyword |  |
| `host.services.tls.cipher_selected` | text | Cipher suite chosen for the exchange. |
| `host.services.ipp` | object |  |
| `host.services.ipp.version_string` | text | The specific IPP version returned in response to an IPP get-printer-attributes request. Always in the form 'IPP/x.y' |
| `host.services.ipp.attribute_cups_version` | text | The CUPS version, if any, specified in the list of attributes returned in a get-printer-attributes response or CUPS-get-printers response. Generally in the form 'x.y.z'. |
| `host.services.ipp.attribute_ipp_versions` | text | Each IPP version, if any, specified in the list of attributes returned in a get-printer-attributes response or CUPS-get-printers response. Always in the form 'x.y'. |
| `host.services.ipp.attribute_printer_uris` | text | Each printer URI, if any, specified in the list of attributes returned in a get-printer-attributes response or CUPS-get-printers response. Uses ipp(s) or http(s) scheme, followed by a hostname or IP, and then the path to a particular printer. |
| `host.services.ipp.attributes` | object | All IPP attributes included in any contentful responses obtained. Each has a name, list of values (potentially only one), and a tag denoting how the value should be interpreted. |
| `host.services.ipp.attributes.name` | text |  |
| `host.services.ipp.attributes.value_tag` | unsigned_long |  |
| `host.services.ipp.cups_version` | text | The CUPS version, if any, specified in the Server header of an IPP get-attributes response. |
| `host.services.ipp.major_version` | unsigned_long | Major component of IPP version listed in the Server header of a response to an IPP get-printer-attributes request. |
| `host.services.ipp.minor_version` | unsigned_long | Minor component of IPP version listed in the Server header of a response to an IPP get-printer-attributes request. |
| `host.services.pop3` | object |  |
| `host.services.pop3.start_tls` | text | The server's response to the STARTTLS command. |
| `host.services.amqp` | object |  |
| `host.services.amqp.explicit_tls` | boolean | Connected via a TLS connection after initial handshake |
| `host.services.amqp.implicit_tls` | boolean | Connected via a TLS wrapped connection (AMQPS) |
| `host.services.amqp.protocol_id` | object |  |
| `host.services.amqp.protocol_id.id` | unsigned_long |  |
| `host.services.amqp.protocol_id.name` | text |  |
| `host.services.amqp.version` | object |  |
| `host.services.amqp.version.major` | unsigned_long |  |
| `host.services.amqp.version.minor` | unsigned_long |  |
| `host.services.amqp.version.revision` | unsigned_long |  |
| `host.services.coap` | object |  |
| `host.services.coap.version` | unsigned_long |  |
| `host.services.coap.code` | text |  |
| `host.services.coap.message_id` | unsigned_long |  |
| `host.services.coap.message_type` | text |  |
| `host.services.coap.payload` | text |  |
| `host.services.coap.token` | text |  |
| `host.services.skinny` | object |  |
| `host.services.skinny.response` | text |  |
