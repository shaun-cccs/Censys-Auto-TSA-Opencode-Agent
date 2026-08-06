# Censys Platform Queryable Fields

Parsed from `Web Censys Data Definitions.html` (in-app data definitions, <https://platform.censys.io/home/definitions>).

**Total fields: 1382**

| Dataset | Field count |
| --- | --- |
| `web` | 1382 |

## web (1382 fields)

| Field | Type | Description |
| --- | --- | --- |
| `web` | object |  |
| `web.hostname` | text |  |
| `web.scan_time` | date |  |
| `web.endpoints` | nested |  |
| `web.endpoints.plex_media_server` | object |  |
| `web.endpoints.plex_media_server.version` | text |  |
| `web.endpoints.pprof` | object |  |
| `web.endpoints.pprof.block` | integer |  |
| `web.endpoints.pprof.goroutine` | integer |  |
| `web.endpoints.pprof.cmdline` | text |  |
| `web.endpoints.pprof.profile` | integer |  |
| `web.endpoints.pprof.heap` | integer |  |
| `web.endpoints.pprof.mutex` | integer |  |
| `web.endpoints.pprof.threadcreate` | integer |  |
| `web.endpoints.pprof.trace` | integer |  |
| `web.endpoints.pprof.allocs` | integer |  |
| `web.endpoints.banner_hash_sha256` | text |  |
| `web.endpoints.synology_dsm` | object |  |
| `web.endpoints.synology_dsm.apis` | text |  |
| `web.endpoints.fortigate` | object |  |
| `web.endpoints.fortigate.api_version` | text |  |
| `web.endpoints.fortigate.build` | integer |  |
| `web.endpoints.fortigate.serial` | text |  |
| `web.endpoints.fortigate.status_code` | integer |  |
| `web.endpoints.fortigate.status_msg` | text |  |
| `web.endpoints.fortigate.version` | text |  |
| `web.endpoints.scan_time` | date |  |
| `web.endpoints.wordpress` | object |  |
| `web.endpoints.wordpress.name` | text |  |
| `web.endpoints.wordpress.namespaces` | text |  |
| `web.endpoints.wordpress.timezone_string` | text |  |
| `web.endpoints.wordpress.description` | text |  |
| `web.endpoints.wordpress.gmt_offset` | text |  |
| `web.endpoints.wordpress.home` | text |  |
| `web.endpoints.vault` | object |  |
| `web.endpoints.vault.cluster_name` | text |  |
| `web.endpoints.vault.enterprise` | boolean |  |
| `web.endpoints.vault.initialized` | boolean |  |
| `web.endpoints.vault.license_state` | text |  |
| `web.endpoints.vault.sealed` | boolean |  |
| `web.endpoints.vault.version` | text |  |
| `web.endpoints.endpoint_type` | text |  |
| `web.endpoints.nginx_proxy_manager` | object |  |
| `web.endpoints.nginx_proxy_manager.version` | text |  |
| `web.endpoints.nginx_proxy_manager.setup` | boolean |  |
| `web.endpoints.proxmox_ve` | object |  |
| `web.endpoints.proxmox_ve.realms` | nested |  |
| `web.endpoints.proxmox_ve.realms.comment` | text |  |
| `web.endpoints.proxmox_ve.realms.realm` | text |  |
| `web.endpoints.proxmox_ve.realms.tfa` | text |  |
| `web.endpoints.proxmox_ve.realms.type` | text |  |
| `web.endpoints.proxmox_ve.api_daemon_version` | text |  |
| `web.endpoints.ivanti_avalanche` | object |  |
| `web.endpoints.ivanti_avalanche.version` | text |  |
| `web.endpoints.ivanti_avalanche.body` | text |  |
| `web.endpoints.ivanti_avalanche.status_code` | integer |  |
| `web.endpoints.graphql` | object |  |
| `web.endpoints.graphql.response` | text |  |
| `web.endpoints.graphql.supports_introspection` | boolean |  |
| `web.endpoints.scada_view` | object |  |
| `web.endpoints.scada_view.title` | text |  |
| `web.endpoints.scada_view.description` | text |  |
| `web.endpoints.screenshots` | nested |  |
| `web.endpoints.screenshots.palsimhash` | text |  |
| `web.endpoints.screenshots.phash` | text |  |
| `web.endpoints.screenshots.extracted_text` | text |  |
| `web.endpoints.screenshots.handle` | text |  |
| `web.endpoints.path` | text |  |
| `web.endpoints.banner` | text |  |
| `web.endpoints.prometheus_target` | object |  |
| `web.endpoints.prometheus_target.metric_families` | object |  |
| `web.endpoints.prometheus_target.metric_families.help` | text |  |
| `web.endpoints.prometheus_target.metric_families.name` | text |  |
| `web.endpoints.keycloak` | object |  |
| `web.endpoints.keycloak.token_service` | text |  |
| `web.endpoints.keycloak.grant_types_supported` | text |  |
| `web.endpoints.keycloak.id_token_signing_alg_values_supported` | text |  |
| `web.endpoints.keycloak.public_key` | text |  |
| `web.endpoints.keycloak.realm_base_path` | text |  |
| `web.endpoints.chrome_devtools` | object |  |
| `web.endpoints.chrome_devtools.protocol_version` | text |  |
| `web.endpoints.chrome_devtools.targets` | nested |  |
| `web.endpoints.chrome_devtools.targets.title` | text |  |
| `web.endpoints.chrome_devtools.targets.type` | text |  |
| `web.endpoints.chrome_devtools.targets.url` | text |  |
| `web.endpoints.chrome_devtools.user_agent` | text |  |
| `web.endpoints.chrome_devtools.v8_version` | text |  |
| `web.endpoints.chrome_devtools.webkit_version` | text |  |
| `web.endpoints.chrome_devtools.browser` | text |  |
| `web.endpoints.mcp` | object |  |
| `web.endpoints.mcp.prompts` | nested |  |
| `web.endpoints.mcp.prompts.name` | text |  |
| `web.endpoints.mcp.protocol_version` | text |  |
| `web.endpoints.mcp.resources` | nested |  |
| `web.endpoints.mcp.resources.description` | text |  |
| `web.endpoints.mcp.resources.mime_type` | text |  |
| `web.endpoints.mcp.resources.name` | text |  |
| `web.endpoints.mcp.resources.uri` | text |  |
| `web.endpoints.mcp.resources.content` | text |  |
| `web.endpoints.mcp.server_name` | text |  |
| `web.endpoints.mcp.server_version` | text |  |
| `web.endpoints.mcp.tools` | nested |  |
| `web.endpoints.mcp.tools.description` | text |  |
| `web.endpoints.mcp.tools.name` | text |  |
| `web.endpoints.jupyter` | object |  |
| `web.endpoints.jupyter.version` | text |  |
| `web.endpoints.ollama` | object |  |
| `web.endpoints.ollama.models` | nested |  |
| `web.endpoints.ollama.models.size` | unsigned_long |  |
| `web.endpoints.ollama.models.size_vram` | unsigned_long |  |
| `web.endpoints.ollama.models.digest` | text |  |
| `web.endpoints.ollama.models.expires_at` | text |  |
| `web.endpoints.ollama.models.family` | text |  |
| `web.endpoints.ollama.models.model` | text |  |
| `web.endpoints.ollama.models.name` | text |  |
| `web.endpoints.ollama.models.parent_model` | text |  |
| `web.endpoints.ollama.running_models` | nested |  |
| `web.endpoints.ollama.running_models.family` | text |  |
| `web.endpoints.ollama.running_models.model` | text |  |
| `web.endpoints.ollama.running_models.name` | text |  |
| `web.endpoints.ollama.running_models.parent_model` | text |  |
| `web.endpoints.ollama.running_models.size` | unsigned_long |  |
| `web.endpoints.ollama.running_models.size_vram` | unsigned_long |  |
| `web.endpoints.ollama.running_models.digest` | text |  |
| `web.endpoints.ollama.running_models.expires_at` | text |  |
| `web.endpoints.ollama.version` | text |  |
| `web.endpoints.open_directory` | object |  |
| `web.endpoints.open_directory.files` | nested |  |
| `web.endpoints.open_directory.files.extension` | text |  |
| `web.endpoints.open_directory.files.last_modified` | date |  |
| `web.endpoints.open_directory.files.name` | text |  |
| `web.endpoints.open_directory.files.path` | text |  |
| `web.endpoints.open_directory.files.size` | long |  |
| `web.endpoints.open_directory.files.suspicious_score` | double |  |
| `web.endpoints.open_directory.files.type` | text |  |
| `web.endpoints.open_directory.recursive` | boolean |  |
| `web.endpoints.influxdb` | object |  |
| `web.endpoints.influxdb.setup_allowed` | boolean |  |
| `web.endpoints.influxdb.version` | text |  |
| `web.endpoints.influxdb.build` | text |  |
| `web.endpoints.extracted` | object |  |
| `web.endpoints.extracted.mac_addresses` | text |  |
| `web.endpoints.extracted.analytics_services` | nested |  |
| `web.endpoints.extracted.analytics_services.ids` | text |  |
| `web.endpoints.extracted.analytics_services.provider` | text |  |
| `web.endpoints.extracted.copyrights` | nested |  |
| `web.endpoints.extracted.copyrights.holder` | text |  |
| `web.endpoints.extracted.copyrights.start_year` | integer |  |
| `web.endpoints.extracted.copyrights.text` | text |  |
| `web.endpoints.extracted.copyrights.end_year` | integer |  |
| `web.endpoints.extracted.ip_addresses` | ip |  |
| `web.endpoints.extracted.languages` | text |  |
| `web.endpoints.extracted.links` | text |  |
| `web.endpoints.ip` | ip |  |
| `web.endpoints.clickhouse_http` | object |  |
| `web.endpoints.clickhouse_http.display_name` | text |  |
| `web.endpoints.clickhouse_http.error` | object |  |
| `web.endpoints.clickhouse_http.error.code` | text |  |
| `web.endpoints.clickhouse_http.error.message` | text |  |
| `web.endpoints.clickhouse_http.timezone` | text |  |
| `web.endpoints.clickhouse_http.version` | text |  |
| `web.endpoints.clickhouse_http.databases` | text |  |
| `web.endpoints.clickhouse_http.databases_exposed` | boolean |  |
| `web.endpoints.redlion_web` | object |  |
| `web.endpoints.redlion_web.title` | text |  |
| `web.endpoints.redlion_web.enhanced_web_server` | boolean |  |
| `web.endpoints.redlion_web.log_names` | text |  |
| `web.endpoints.argocd` | object |  |
| `web.endpoints.argocd.settings` | object |  |
| `web.endpoints.argocd.settings.impersonation_enabled` | boolean |  |
| `web.endpoints.argocd.settings.installation_id` | text |  |
| `web.endpoints.argocd.settings.oidc_config` | object |  |
| `web.endpoints.argocd.settings.oidc_config.client_id` | text |  |
| `web.endpoints.argocd.settings.oidc_config.issuer` | text |  |
| `web.endpoints.argocd.settings.sync_with_replace_allowed` | boolean |  |
| `web.endpoints.argocd.settings.url` | text |  |
| `web.endpoints.argocd.settings.user_logins_disabled` | boolean |  |
| `web.endpoints.argocd.settings.apps_in_any_namespace_enabled` | boolean |  |
| `web.endpoints.argocd.settings.exec_enabled` | boolean |  |
| `web.endpoints.argocd.version` | text |  |
| `web.endpoints.argocd.anonymous_exposure` | object |  |
| `web.endpoints.argocd.anonymous_exposure.application_count` | integer |  |
| `web.endpoints.argocd.anonymous_exposure.applications_anonymously_readable` | boolean |  |
| `web.endpoints.argocd.anonymous_exposure.cluster_count` | integer |  |
| `web.endpoints.argocd.anonymous_exposure.clusters_anonymously_readable` | boolean |  |
| `web.endpoints.hostname` | text |  |
| `web.endpoints.transport_protocol` | keyword |  |
| `web.endpoints.jenkins` | object |  |
| `web.endpoints.jenkins.use_security` | boolean |  |
| `web.endpoints.jenkins.assigned_labels` | nested |  |
| `web.endpoints.jenkins.assigned_labels.value` | text |  |
| `web.endpoints.jenkins.assigned_labels.name` | text |  |
| `web.endpoints.jenkins.jobs` | nested |  |
| `web.endpoints.jenkins.jobs.url` | text |  |
| `web.endpoints.jenkins.jobs.description` | text |  |
| `web.endpoints.jenkins.jobs.last_build` | object |  |
| `web.endpoints.jenkins.jobs.last_build.number` | long |  |
| `web.endpoints.jenkins.jobs.last_build.result` | text |  |
| `web.endpoints.jenkins.jobs.last_build.timestamp` | long |  |
| `web.endpoints.jenkins.jobs.last_build.url` | text |  |
| `web.endpoints.jenkins.jobs.last_build.duration_seconds` | long |  |
| `web.endpoints.jenkins.jobs.name` | text |  |
| `web.endpoints.jenkins.mode` | text |  |
| `web.endpoints.jenkins.node_description` | text |  |
| `web.endpoints.jenkins.node_name` | text |  |
| `web.endpoints.jenkins.slave_agent_port` | integer |  |
| `web.endpoints.port` | unsigned_long |  |
| `web.compromises` | nested |  |
| `web.compromises.severity` | keyword |  |
| `web.compromises.source` | keyword |  |
| `web.compromises.confidence` | double |  |
| `web.compromises.name` | text |  |
| `web.compromises.cvss` | object |  |
| `web.compromises.cvss.components` | object | These metrics contribute to how a CVE is scored. |
| `web.compromises.cvss.components.availability` | keyword | If an attack renders information unavailable, such as when a system crashes or through a DDoS attack, availability is negatively impacted. Availability has three possible values: None (N) – There is no loss of availability, Low (L) – Availability might be intermittently limited, or performance might be negatively impacted, as a result of a successful attack, High (H) – There is a complete loss of availability of the impacted system or information. |
| `web.compromises.cvss.components.confidentiality` | keyword | Refers to the disclosure of sensitive information to authorized and unauthorized users, with the goal being that only authorized users are able to access the target data. Confidentiality has three potential values: High (H) – The attacker has full access to all resources in the impacted system, including highly sensitive information such as encryption keys, Low (L) – The attacker has partial access to information, with no control over what, specifically, they are able to access, None (N) – No data is accessible to unauthorized users as a result of the exploit. |
| `web.compromises.cvss.components.integrity` | keyword | Refers to whether the protected information has been tampered with or changed in any way. If there is no way for an attacker to alter the accuracy or completeness of the information, integrity has been maintained. Integrity has three values: None (N) – There is no loss of the integrity of any information, Low (L) – A limited amount of information might be tampered with or modified, but there is no serious impact on the protected system, High (H) – The attacker can modify any/all information on the target system, resulting in a complete loss of integrity. |
| `web.compromises.cvss.components.privileges_required` | keyword | Describes the level of privileges or access an attacker must have before successful exploitation. There are three possible values: None (N) – There is no privilege or special access required to conduct the attack, Low (L) – The attacker requires basic, “user” level privileges to leverage the exploit, High (H) – Administrative or similar access privileges are required for successful attack. |
| `web.compromises.cvss.components.scope` | keyword | Determines whether a vulnerability in one system or component can impact another system or component. If a vulnerability in a vulnerable component can affect a component which is in a different security scope than the vulnerable component, a scope change occurs. Scope has two possible ratings: Changed (C) – An exploited vulnerability can have a carry over impact on another system, Unchanged (U) – The exploited vulnerability is limited in damage to only the local security authority. |
| `web.compromises.cvss.components.user_interaction` | keyword | Describes whether a user, other than the attacker, is required to do anything or participate in exploitation of the vulnerability. User interaction has two possible values: None (N) – No user interaction is required, Required (R) – A user must complete some steps for the exploit to succeed. For example, a user might be required to install some software. |
| `web.compromises.cvss.components.attack_complexity` | keyword | Indicates conditions beyond the attacker’s control that must exist in order to exploit the vulnerability. The Attack Complexity metric is scored as either Low or High. There are two possible values: Low (L) – There are no specific pre-conditions required for exploitation, High (H) – The attacker must complete some number of preparatory steps in order to get access. |
| `web.compromises.cvss.components.attack_vector` | keyword | Indicates the level of access required for an attacker to exploit the vulnerability. The Attack Vector metric is scored in one of four levels: Network (N) – Vulnerabilities with this rating are remotely exploitable, from one or more hops away, up to, and including, remote exploitation over the Internet, Adjacent (A) – A vulnerability with this rating requires network adjacency for exploitation. The attack must be launched from the same physical or logical network, Local (L) – Vulnerabilities with this rating are not exploitable over a network, Physical (P) – An attacker must physically interact with the target system. |
| `web.compromises.cvss.score` | double | Score of the vulnerability; 0.1 is the lowest, 10 is the maximum |
| `web.compromises.cvss.vector` | text | The path, method, or scenario used to exploit the vulnerability. Each section represents components that contribute to the overall CVSS score. |
| `web.compromises.evidence` | nested |  |
| `web.compromises.evidence.literal_match` | text |  |
| `web.compromises.evidence.negative` | boolean |  |
| `web.compromises.evidence.proprietary` | boolean |  |
| `web.compromises.evidence.regex` | text |  |
| `web.compromises.evidence.semver_expression` | text |  |
| `web.compromises.evidence.data_path` | text |  |
| `web.compromises.evidence.exists` | boolean |  |
| `web.compromises.evidence.found_value` | text |  |
| `web.compromises.type` | text |  |
| `web.compromises.id` | text |  |
| `web.compromises.metrics` | object |  |
| `web.compromises.metrics.cvss_v31` | object |  |
| `web.compromises.metrics.cvss_v31.components` | object | These metrics contribute to how a CVE is scored. |
| `web.compromises.metrics.cvss_v31.components.attack_vector` | keyword | Indicates the level of access required for an attacker to exploit the vulnerability. The Attack Vector metric is scored in one of four levels: Network (N) – Vulnerabilities with this rating are remotely exploitable, from one or more hops away, up to, and including, remote exploitation over the Internet, Adjacent (A) – A vulnerability with this rating requires network adjacency for exploitation. The attack must be launched from the same physical or logical network, Local (L) – Vulnerabilities with this rating are not exploitable over a network, Physical (P) – An attacker must physically interact with the target system. |
| `web.compromises.metrics.cvss_v31.components.availability` | keyword | If an attack renders information unavailable, such as when a system crashes or through a DDoS attack, availability is negatively impacted. Availability has three possible values: None (N) – There is no loss of availability, Low (L) – Availability might be intermittently limited, or performance might be negatively impacted, as a result of a successful attack, High (H) – There is a complete loss of availability of the impacted system or information. |
| `web.compromises.metrics.cvss_v31.components.confidentiality` | keyword | Refers to the disclosure of sensitive information to authorized and unauthorized users, with the goal being that only authorized users are able to access the target data. Confidentiality has three potential values: High (H) – The attacker has full access to all resources in the impacted system, including highly sensitive information such as encryption keys, Low (L) – The attacker has partial access to information, with no control over what, specifically, they are able to access, None (N) – No data is accessible to unauthorized users as a result of the exploit. |
| `web.compromises.metrics.cvss_v31.components.integrity` | keyword | Refers to whether the protected information has been tampered with or changed in any way. If there is no way for an attacker to alter the accuracy or completeness of the information, integrity has been maintained. Integrity has three values: None (N) – There is no loss of the integrity of any information, Low (L) – A limited amount of information might be tampered with or modified, but there is no serious impact on the protected system, High (H) – The attacker can modify any/all information on the target system, resulting in a complete loss of integrity. |
| `web.compromises.metrics.cvss_v31.components.privileges_required` | keyword | Describes the level of privileges or access an attacker must have before successful exploitation. There are three possible values: None (N) – There is no privilege or special access required to conduct the attack, Low (L) – The attacker requires basic, “user” level privileges to leverage the exploit, High (H) – Administrative or similar access privileges are required for successful attack. |
| `web.compromises.metrics.cvss_v31.components.scope` | keyword | Determines whether a vulnerability in one system or component can impact another system or component. If a vulnerability in a vulnerable component can affect a component which is in a different security scope than the vulnerable component, a scope change occurs. Scope has two possible ratings: Changed (C) – An exploited vulnerability can have a carry over impact on another system, Unchanged (U) – The exploited vulnerability is limited in damage to only the local security authority. |
| `web.compromises.metrics.cvss_v31.components.user_interaction` | keyword | Describes whether a user, other than the attacker, is required to do anything or participate in exploitation of the vulnerability. User interaction has two possible values: None (N) – No user interaction is required, Required (R) – A user must complete some steps for the exploit to succeed. For example, a user might be required to install some software. |
| `web.compromises.metrics.cvss_v31.components.attack_complexity` | keyword | Indicates conditions beyond the attacker’s control that must exist in order to exploit the vulnerability. The Attack Complexity metric is scored as either Low or High. There are two possible values: Low (L) – There are no specific pre-conditions required for exploitation, High (H) – The attacker must complete some number of preparatory steps in order to get access. |
| `web.compromises.metrics.cvss_v31.score` | double | Score of the vulnerability; 0.1 is the lowest, 10 is the maximum |
| `web.compromises.metrics.cvss_v31.vector` | text | The path, method, or scenario used to exploit the vulnerability. Each section represents components that contribute to the overall CVSS score. |
| `web.compromises.metrics.cvss_v40` | object |  |
| `web.compromises.metrics.cvss_v40.vector` | text | The path, method, or scenario used to exploit the vulnerability. Each section represents components that contribute to the overall CVSS score. |
| `web.compromises.metrics.cvss_v40.components` | object | These metrics contribute to how a CVE is scored. |
| `web.compromises.metrics.cvss_v40.components.availability` | keyword | If an attack renders information unavailable, such as when a system crashes or through a DDoS attack, availability is negatively impacted. Availability has three possible values: None (N) – There is no loss of availability, Low (L) – Availability might be intermittently limited, or performance might be negatively impacted, as a result of a successful attack, High (H) – There is a complete loss of availability of the impacted system or information. |
| `web.compromises.metrics.cvss_v40.components.safety` | keyword |  |
| `web.compromises.metrics.cvss_v40.components.attack_complexity` | keyword | Indicates conditions beyond the attacker’s control that must exist in order to exploit the vulnerability. The Attack Complexity metric is scored as either Low or High. There are two possible values: Low (L) – There are no specific pre-conditions required for exploitation, High (H) – The attacker must complete some number of preparatory steps in order to get access. |
| `web.compromises.metrics.cvss_v40.components.attack_vector` | keyword | Indicates the level of access required for an attacker to exploit the vulnerability. The Attack Vector metric is scored in one of four levels: Network (N) – Vulnerabilities with this rating are remotely exploitable, from one or more hops away, up to, and including, remote exploitation over the Internet, Adjacent (A) – A vulnerability with this rating requires network adjacency for exploitation. The attack must be launched from the same physical or logical network, Local (L) – Vulnerabilities with this rating are not exploitable over a network, Physical (P) – An attacker must physically interact with the target system. |
| `web.compromises.metrics.cvss_v40.components.privileges_required` | keyword | Describes the level of privileges or access an attacker must have before successful exploitation. There are three possible values: None (N) – There is no privilege or special access required to conduct the attack, Low (L) – The attacker requires basic, “user” level privileges to leverage the exploit, High (H) – Administrative or similar access privileges are required for successful attack. |
| `web.compromises.metrics.cvss_v40.components.user_interaction` | keyword | Describes whether a user, other than the attacker, is required to do anything or participate in exploitation of the vulnerability. User interaction has two possible values: None (N) – No user interaction is required, Required (R) – A user must complete some steps for the exploit to succeed. For example, a user might be required to install some software. |
| `web.compromises.metrics.cvss_v40.components.confidentiality` | keyword | Refers to the disclosure of sensitive information to authorized and unauthorized users, with the goal being that only authorized users are able to access the target data. Confidentiality has three potential values: High (H) – The attacker has full access to all resources in the impacted system, including highly sensitive information such as encryption keys, Low (L) – The attacker has partial access to information, with no control over what, specifically, they are able to access, None (N) – No data is accessible to unauthorized users as a result of the exploit. |
| `web.compromises.metrics.cvss_v40.components.integrity` | keyword | Refers to whether the protected information has been tampered with or changed in any way. If there is no way for an attacker to alter the accuracy or completeness of the information, integrity has been maintained. Integrity has three values: None (N) – There is no loss of the integrity of any information, Low (L) – A limited amount of information might be tampered with or modified, but there is no serious impact on the protected system, High (H) – The attacker can modify any/all information on the target system, resulting in a complete loss of integrity. |
| `web.compromises.metrics.cvss_v40.components.provider_urgency` | keyword |  |
| `web.compromises.metrics.cvss_v40.components.recovery` | keyword |  |
| `web.compromises.metrics.cvss_v40.components.attack_requirements` | keyword |  |
| `web.compromises.metrics.cvss_v40.components.vulnerability_response_effort` | keyword |  |
| `web.compromises.metrics.cvss_v40.components.automatable` | keyword |  |
| `web.compromises.metrics.cvss_v40.components.value_density` | keyword |  |
| `web.compromises.metrics.cvss_v40.score` | double | Score of the vulnerability; 0.1 is the lowest, 10 is the maximum |
| `web.compromises.metrics.epss` | object |  |
| `web.compromises.metrics.epss.percentile` | double |  |
| `web.compromises.metrics.epss.score` | double |  |
| `web.compromises.metrics.cvss_v30` | object |  |
| `web.compromises.metrics.cvss_v30.components` | object | These metrics contribute to how a CVE is scored. |
| `web.compromises.metrics.cvss_v30.components.attack_vector` | keyword | Indicates the level of access required for an attacker to exploit the vulnerability. The Attack Vector metric is scored in one of four levels: Network (N) – Vulnerabilities with this rating are remotely exploitable, from one or more hops away, up to, and including, remote exploitation over the Internet, Adjacent (A) – A vulnerability with this rating requires network adjacency for exploitation. The attack must be launched from the same physical or logical network, Local (L) – Vulnerabilities with this rating are not exploitable over a network, Physical (P) – An attacker must physically interact with the target system. |
| `web.compromises.metrics.cvss_v30.components.availability` | keyword | If an attack renders information unavailable, such as when a system crashes or through a DDoS attack, availability is negatively impacted. Availability has three possible values: None (N) – There is no loss of availability, Low (L) – Availability might be intermittently limited, or performance might be negatively impacted, as a result of a successful attack, High (H) – There is a complete loss of availability of the impacted system or information. |
| `web.compromises.metrics.cvss_v30.components.confidentiality` | keyword | Refers to the disclosure of sensitive information to authorized and unauthorized users, with the goal being that only authorized users are able to access the target data. Confidentiality has three potential values: High (H) – The attacker has full access to all resources in the impacted system, including highly sensitive information such as encryption keys, Low (L) – The attacker has partial access to information, with no control over what, specifically, they are able to access, None (N) – No data is accessible to unauthorized users as a result of the exploit. |
| `web.compromises.metrics.cvss_v30.components.integrity` | keyword | Refers to whether the protected information has been tampered with or changed in any way. If there is no way for an attacker to alter the accuracy or completeness of the information, integrity has been maintained. Integrity has three values: None (N) – There is no loss of the integrity of any information, Low (L) – A limited amount of information might be tampered with or modified, but there is no serious impact on the protected system, High (H) – The attacker can modify any/all information on the target system, resulting in a complete loss of integrity. |
| `web.compromises.metrics.cvss_v30.components.privileges_required` | keyword | Describes the level of privileges or access an attacker must have before successful exploitation. There are three possible values: None (N) – There is no privilege or special access required to conduct the attack, Low (L) – The attacker requires basic, “user” level privileges to leverage the exploit, High (H) – Administrative or similar access privileges are required for successful attack. |
| `web.compromises.metrics.cvss_v30.components.scope` | keyword | Determines whether a vulnerability in one system or component can impact another system or component. If a vulnerability in a vulnerable component can affect a component which is in a different security scope than the vulnerable component, a scope change occurs. Scope has two possible ratings: Changed (C) – An exploited vulnerability can have a carry over impact on another system, Unchanged (U) – The exploited vulnerability is limited in damage to only the local security authority. |
| `web.compromises.metrics.cvss_v30.components.user_interaction` | keyword | Describes whether a user, other than the attacker, is required to do anything or participate in exploitation of the vulnerability. User interaction has two possible values: None (N) – No user interaction is required, Required (R) – A user must complete some steps for the exploit to succeed. For example, a user might be required to install some software. |
| `web.compromises.metrics.cvss_v30.components.attack_complexity` | keyword | Indicates conditions beyond the attacker’s control that must exist in order to exploit the vulnerability. The Attack Complexity metric is scored as either Low or High. There are two possible values: Low (L) – There are no specific pre-conditions required for exploitation, High (H) – The attacker must complete some number of preparatory steps in order to get access. |
| `web.compromises.metrics.cvss_v30.score` | double | Score of the vulnerability; 0.1 is the lowest, 10 is the maximum |
| `web.compromises.metrics.cvss_v30.vector` | text | The path, method, or scenario used to exploit the vulnerability. Each section represents components that contribute to the overall CVSS score. |
| `web.compromises.risk_source` | keyword |  |
| `web.compromises.year` | unsigned_long |  |
| `web.labels` | nested |  |
| `web.labels.confidence` | double |  |
| `web.labels.evidence` | nested |  |
| `web.labels.evidence.negative` | boolean |  |
| `web.labels.evidence.proprietary` | boolean |  |
| `web.labels.evidence.regex` | text |  |
| `web.labels.evidence.semver_expression` | text |  |
| `web.labels.evidence.data_path` | text |  |
| `web.labels.evidence.exists` | boolean |  |
| `web.labels.evidence.found_value` | text |  |
| `web.labels.evidence.literal_match` | text |  |
| `web.labels.source` | keyword |  |
| `web.labels.value` | text |  |
| `web.port` | unsigned_long |  |
| `web.jarm` | object |  |
| `web.jarm.ip` | text |  |
| `web.jarm.tls_extensions_sha256` | text | The second 32 character portion of the Jarm fingerprint |
| `web.jarm.cipher_and_version_fingerprint` | text | The first 30 character portion of the Jarm fingerprint. |
| `web.jarm.transport_protocol` | keyword |  |
| `web.jarm.scan_time` | date | The time the service was fingerprinted |
| `web.jarm.fingerprint` | text | The 62 character Jarm fingerprint of the service. |
| `web.jarm.hostname` | text |  |
| `web.jarm.is_success` | boolean |  |
| `web.jarm.port` | unsigned_long |  |
| `web.operating_systems` | nested |  |
| `web.operating_systems.cpe` | text |  |
| `web.operating_systems.source` | keyword |  |
| `web.operating_systems.vendor` | text |  |
| `web.operating_systems.confidence` | double |  |
| `web.operating_systems.version` | text |  |
| `web.operating_systems.evidence` | nested |  |
| `web.operating_systems.evidence.exists` | boolean |  |
| `web.operating_systems.evidence.found_value` | text |  |
| `web.operating_systems.evidence.literal_match` | text |  |
| `web.operating_systems.evidence.negative` | boolean |  |
| `web.operating_systems.evidence.proprietary` | boolean |  |
| `web.operating_systems.evidence.regex` | text |  |
| `web.operating_systems.evidence.semver_expression` | text |  |
| `web.operating_systems.evidence.data_path` | text |  |
| `web.operating_systems.product` | text |  |
| `web.operating_systems.edition` | text |  |
| `web.operating_systems.update` | text |  |
| `web.operating_systems.life_cycle` | object |  |
| `web.operating_systems.life_cycle.end_of_life` | boolean |  |
| `web.operating_systems.life_cycle.end_of_life_date` | date |  |
| `web.operating_systems.life_cycle.release_date` | date |  |
| `web.operating_systems.components` | object |  |
| `web.operating_systems.components.update` | text |  |
| `web.operating_systems.components.vendor` | text |  |
| `web.operating_systems.components.version` | text |  |
| `web.operating_systems.components.cpe` | text |  |
| `web.operating_systems.components.edition` | text |  |
| `web.operating_systems.components.life_cycle` | object |  |
| `web.operating_systems.components.life_cycle.end_of_life` | boolean |  |
| `web.operating_systems.components.life_cycle.end_of_life_date` | date |  |
| `web.operating_systems.components.life_cycle.release_date` | date |  |
| `web.operating_systems.components.part` | text |  |
| `web.operating_systems.components.product` | text |  |
| `web.operating_systems.part` | text |  |
| `web.operating_systems.type` | text |  |
| `web.threats` | nested |  |
| `web.threats.type` | keyword |  |
| `web.threats.name` | text |  |
| `web.threats.actors` | object |  |
| `web.threats.actors.primary_name` | text |  |
| `web.threats.actors.all_names` | text |  |
| `web.threats.actors.id` | text |  |
| `web.threats.actors.malpedia_group_id` | text |  |
| `web.threats.actors.mitre_group_id` | text |  |
| `web.threats.confidence` | double |  |
| `web.threats.malware` | object |  |
| `web.threats.malware.malpedia_id` | text |  |
| `web.threats.malware.primary_name` | text |  |
| `web.threats.malware.all_names` | text |  |
| `web.threats.malware.id` | text |  |
| `web.threats.malware.last_updated_at` | date |  |
| `web.threats.details` | object |  |
| `web.threats.details.version` | text |  |
| `web.threats.details.campaign_id` | text |  |
| `web.threats.details.campaign_theme` | text |  |
| `web.threats.details.control_servers` | text |  |
| `web.threats.evidence` | nested |  |
| `web.threats.evidence.literal_match` | text |  |
| `web.threats.evidence.negative` | boolean |  |
| `web.threats.evidence.proprietary` | boolean |  |
| `web.threats.evidence.regex` | text |  |
| `web.threats.evidence.semver_expression` | text |  |
| `web.threats.evidence.data_path` | text |  |
| `web.threats.evidence.exists` | boolean |  |
| `web.threats.evidence.found_value` | text |  |
| `web.threats.id` | text |  |
| `web.threats.source` | keyword |  |
| `web.threats.tactic` | keyword |  |
| `web.hardware` | nested |  |
| `web.hardware.part` | text |  |
| `web.hardware.product` | text |  |
| `web.hardware.vendor` | text |  |
| `web.hardware.edition` | text |  |
| `web.hardware.version` | text |  |
| `web.hardware.components` | object |  |
| `web.hardware.components.cpe` | text |  |
| `web.hardware.components.edition` | text |  |
| `web.hardware.components.life_cycle` | object |  |
| `web.hardware.components.life_cycle.end_of_life_date` | date |  |
| `web.hardware.components.life_cycle.release_date` | date |  |
| `web.hardware.components.life_cycle.end_of_life` | boolean |  |
| `web.hardware.components.part` | text |  |
| `web.hardware.components.product` | text |  |
| `web.hardware.components.update` | text |  |
| `web.hardware.components.vendor` | text |  |
| `web.hardware.components.version` | text |  |
| `web.hardware.update` | text |  |
| `web.hardware.cpe` | text |  |
| `web.hardware.evidence` | nested |  |
| `web.hardware.evidence.proprietary` | boolean |  |
| `web.hardware.evidence.regex` | text |  |
| `web.hardware.evidence.semver_expression` | text |  |
| `web.hardware.evidence.data_path` | text |  |
| `web.hardware.evidence.exists` | boolean |  |
| `web.hardware.evidence.found_value` | text |  |
| `web.hardware.evidence.literal_match` | text |  |
| `web.hardware.evidence.negative` | boolean |  |
| `web.hardware.life_cycle` | object |  |
| `web.hardware.life_cycle.end_of_life_date` | date |  |
| `web.hardware.life_cycle.release_date` | date |  |
| `web.hardware.life_cycle.end_of_life` | boolean |  |
| `web.hardware.source` | keyword |  |
| `web.hardware.confidence` | double |  |
| `web.hardware.type` | text |  |
| `web.software` | nested |  |
| `web.software.confidence` | double |  |
| `web.software.evidence` | nested |  |
| `web.software.evidence.found_value` | text |  |
| `web.software.evidence.literal_match` | text |  |
| `web.software.evidence.negative` | boolean |  |
| `web.software.evidence.proprietary` | boolean |  |
| `web.software.evidence.regex` | text |  |
| `web.software.evidence.semver_expression` | text |  |
| `web.software.evidence.data_path` | text |  |
| `web.software.evidence.exists` | boolean |  |
| `web.software.product` | text |  |
| `web.software.type` | text |  |
| `web.software.version` | text |  |
| `web.software.part` | text |  |
| `web.software.update` | text |  |
| `web.software.life_cycle` | object |  |
| `web.software.life_cycle.end_of_life` | boolean |  |
| `web.software.life_cycle.end_of_life_date` | date |  |
| `web.software.life_cycle.release_date` | date |  |
| `web.software.components` | object |  |
| `web.software.components.life_cycle` | object |  |
| `web.software.components.life_cycle.release_date` | date |  |
| `web.software.components.life_cycle.end_of_life` | boolean |  |
| `web.software.components.life_cycle.end_of_life_date` | date |  |
| `web.software.components.part` | text |  |
| `web.software.components.product` | text |  |
| `web.software.components.update` | text |  |
| `web.software.components.vendor` | text |  |
| `web.software.components.version` | text |  |
| `web.software.components.cpe` | text |  |
| `web.software.components.edition` | text |  |
| `web.software.cpe` | text |  |
| `web.software.edition` | text |  |
| `web.software.source` | keyword |  |
| `web.software.vendor` | text |  |
| `web.cert` | object |  |
| `web.cert.names` | text | All the names contained in the certificate from various fields. |
| `web.cert.revoked` | boolean | Whether the certificate has been revoked before its expiry date by the issuer. |
| `web.cert.tbs_no_ct_fingerprint_sha256` | text | The SHA-256 digest of the unsigned certificate with the CT Poison extension removed, if present. This represents the shared contents of a certificate and its corresponding pre-certificate. |
| `web.cert.validated_at` | date | When the certificate record's trust was last checked. |
| `web.cert.fingerprint_sha256` | text | The SHA-256 digest of the entire raw certificate. Its unique identifier, which Censys uses to index certificates records. |
| `web.cert.parse_status` | keyword |  |
| `web.cert.validation` | object | A record containing information from the maintainers of major root certificate stores related to their trust assessment. |
| `web.cert.validation.chrome` | object | A record containing validation information about the certificate from the Chrome root store. |
| `web.cert.validation.chrome.has_trusted_path` | boolean | Whether there currently exists a trusted path of signing certificates from a certificate present in the root certificate store. |
| `web.cert.validation.chrome.in_revocation_set` | boolean | Whether the certificate is in the revocation set (e.g. OneCRL) associated with the root store. |
| `web.cert.validation.chrome.is_valid` | boolean | Whether the certificate is currently considered valid by the root store: a summary of the trust path, revoked, blocklisted/allowlisted, and expired fields. |
| `web.cert.validation.chrome.parents` | text | The SHA-256 fingerprints of the certificate's immediate parents in its trust path(s). |
| `web.cert.validation.chrome.type` | keyword | The certificate's type. Options include root, intermediate, or leaf. |
| `web.cert.validation.chrome.chains` | nested | A path of trusted signing certificates up to a root certificate present in a root store, represented as an ordered list of SHA-256 fingerprints. |
| `web.cert.validation.chrome.chains.sha256fp` | text |  |
| `web.cert.validation.chrome.ever_valid` | boolean | Whether the certificate has ever been considered valid by the root store. |
| `web.cert.validation.chrome.had_trusted_path` | boolean | Whether there ever existed a trusted path of signing certificates from a certificate present in the root certificate store. |
| `web.cert.validation.microsoft` | object | A record containing validation information about the certificate from the Microsoft root store. |
| `web.cert.validation.microsoft.parents` | text | The SHA-256 fingerprints of the certificate's immediate parents in its trust path(s). |
| `web.cert.validation.microsoft.type` | keyword | The certificate's type. Options include root, intermediate, or leaf. |
| `web.cert.validation.microsoft.chains` | nested | A path of trusted signing certificates up to a root certificate present in a root store, represented as an ordered list of SHA-256 fingerprints. |
| `web.cert.validation.microsoft.chains.sha256fp` | text |  |
| `web.cert.validation.microsoft.ever_valid` | boolean | Whether the certificate has ever been considered valid by the root store. |
| `web.cert.validation.microsoft.had_trusted_path` | boolean | Whether there ever existed a trusted path of signing certificates from a certificate present in the root certificate store. |
| `web.cert.validation.microsoft.has_trusted_path` | boolean | Whether there currently exists a trusted path of signing certificates from a certificate present in the root certificate store. |
| `web.cert.validation.microsoft.in_revocation_set` | boolean | Whether the certificate is in the revocation set (e.g. OneCRL) associated with the root store. |
| `web.cert.validation.microsoft.is_valid` | boolean | Whether the certificate is currently considered valid by the root store: a summary of the trust path, revoked, blocklisted/allowlisted, and expired fields. |
| `web.cert.validation.nss` | object | A record containing validation information about the certificate from the Mozilla NSS root store. |
| `web.cert.validation.nss.parents` | text | The SHA-256 fingerprints of the certificate's immediate parents in its trust path(s). |
| `web.cert.validation.nss.type` | keyword | The certificate's type. Options include root, intermediate, or leaf. |
| `web.cert.validation.nss.chains` | nested | A path of trusted signing certificates up to a root certificate present in a root store, represented as an ordered list of SHA-256 fingerprints. |
| `web.cert.validation.nss.chains.sha256fp` | text |  |
| `web.cert.validation.nss.ever_valid` | boolean | Whether the certificate has ever been considered valid by the root store. |
| `web.cert.validation.nss.had_trusted_path` | boolean | Whether there ever existed a trusted path of signing certificates from a certificate present in the root certificate store. |
| `web.cert.validation.nss.has_trusted_path` | boolean | Whether there currently exists a trusted path of signing certificates from a certificate present in the root certificate store. |
| `web.cert.validation.nss.in_revocation_set` | boolean | Whether the certificate is in the revocation set (e.g. OneCRL) associated with the root store. |
| `web.cert.validation.nss.is_valid` | boolean | Whether the certificate is currently considered valid by the root store: a summary of the trust path, revoked, blocklisted/allowlisted, and expired fields. |
| `web.cert.validation.apple` | object | A record containing validation information about the certificate from the Apple root store. |
| `web.cert.validation.apple.type` | keyword | The certificate's type. Options include root, intermediate, or leaf. |
| `web.cert.validation.apple.chains` | nested | A path of trusted signing certificates up to a root certificate present in a root store, represented as an ordered list of SHA-256 fingerprints. |
| `web.cert.validation.apple.chains.sha256fp` | text |  |
| `web.cert.validation.apple.ever_valid` | boolean | Whether the certificate has ever been considered valid by the root store. |
| `web.cert.validation.apple.had_trusted_path` | boolean | Whether there ever existed a trusted path of signing certificates from a certificate present in the root certificate store. |
| `web.cert.validation.apple.has_trusted_path` | boolean | Whether there currently exists a trusted path of signing certificates from a certificate present in the root certificate store. |
| `web.cert.validation.apple.in_revocation_set` | boolean | Whether the certificate is in the revocation set (e.g. OneCRL) associated with the root store. |
| `web.cert.validation.apple.is_valid` | boolean | Whether the certificate is currently considered valid by the root store: a summary of the trust path, revoked, blocklisted/allowlisted, and expired fields. |
| `web.cert.validation.apple.parents` | text | The SHA-256 fingerprints of the certificate's immediate parents in its trust path(s). |
| `web.cert.parent_spki_subject_fingerprint_sha256` | text | The SHA-256 digest of the parent certificate's DER-encoded SubjectPublicKeyInfo concatenated with its Subject. |
| `web.cert.spki_fingerprint_sha256` | text | DEPRECATED: Use spki_subject_fingerprint_sha256 |
| `web.cert.modified_at` | date | When the certificate record was last modified. |
| `web.cert.zlint` | object | A record containing the results of linting the certificate for conformance to the X.509 standard using Zlint. |
| `web.cert.zlint.version` | long | The version of Zlint used to lint the certificate. |
| `web.cert.zlint.warnings_present` | boolean | Whether the certificate's attributes triggered any warning lints for non-conformance to the X.509 standard. |
| `web.cert.zlint.errors_present` | boolean | Whether the certificate's attributes triggered any error lints for non-conformance to the X.509 standard. |
| `web.cert.zlint.failed_lints` | text | A list of lint names which failed, if applicable. |
| `web.cert.zlint.fatals_present` | boolean | Whether the certificate's attributes triggered any fatal lints for non-conformance to the X.509 standard. |
| `web.cert.zlint.notices_present` | boolean | Whether the certificate's attributes triggered any notice lints for non-conformance to the X.509 standard. |
| `web.cert.zlint.timestamp` | date | An RFC-3339-formated timestamp indicating when the certificate was linted. |
| `web.cert.added_at` | date | When the certificate was added to the Censys dataset. |
| `web.cert.precert` | boolean | Whether the X.509 "poison" extension (OID: 1.3.6.1.4.1.11129.2.4.3) is marked critical, which prohibits the pre-certificate from being trusted. |
| `web.cert.tbs_fingerprint_sha256` | text | The SHA-256 digest of the unsigned certificate's contents. |
| `web.cert.parent_spki_fingerprint_sha256` | text | DEPRECATED: Use parent_spki_subject_fingerprint_sha256 |
| `web.cert.ct` | object |  |
| `web.cert.ct.entries` | nested |  |
| `web.cert.ct.entries.key` | text |  |
| `web.cert.ct.entries.value` | object |  |
| `web.cert.ct.entries.value.added_to_ct_at` | date | An RFC-3339-formatted timestamp indicating when the certificate was entered into the CT log. |
| `web.cert.ct.entries.value.ct_to_censys_at` | date | An RFC-3339-formated timestamp indicating when the certificate was ingested from the CT log into the Censys dataset. |
| `web.cert.ct.entries.value.index` | long | Numerical marker of the certificate's place in the CT log. |
| `web.cert.parsed` | object | A record containing all of the data parsed from the certificate. |
| `web.cert.parsed.unknown_extensions` | nested |  |
| `web.cert.parsed.unknown_extensions.critical` | boolean |  |
| `web.cert.parsed.unknown_extensions.id` | text |  |
| `web.cert.parsed.unknown_extensions.value` | text |  |
| `web.cert.parsed.version` | integer |  |
| `web.cert.parsed.subject_dn` | text | Distinguished Name of the entity associated with the public key. |
| `web.cert.parsed.subject_key_info` | object | Information about the certificate's public key. |
| `web.cert.parsed.subject_key_info.fingerprint_sha256` | text | The SHA-256 digest of the certificate's DER-encoded SubjectPublicKeyInfo. |
| `web.cert.parsed.subject_key_info.key_algorithm` | object | A record containing information about the type of subject key algorithm and any relevant parameters. |
| `web.cert.parsed.subject_key_info.key_algorithm.name` | text | Name of public key type, such as RSA or ECDSA. Information specific to the key type is available in the named sub-record. |
| `web.cert.parsed.subject_key_info.key_algorithm.oid` | text |  |
| `web.cert.parsed.subject_key_info.rsa` | object | A record containing the public portion of an RSA asymmetric key. |
| `web.cert.parsed.subject_key_info.rsa.length` | long | Bit-length of the RSA modulus. |
| `web.cert.parsed.subject_key_info.rsa.modulus` | text | The RSA key's modulus (n) in big-endian encoding. |
| `web.cert.parsed.subject_key_info.rsa.exponent` | long | The RSA key's public exponent (e). |
| `web.cert.parsed.subject_key_info.unrecognized` | object | A record containing known information about an unrecognized key type. |
| `web.cert.parsed.subject_key_info.unrecognized.raw` | text |  |
| `web.cert.parsed.subject_key_info.dsa` | object | A record containing the public portion of a DSA asymmetric key. |
| `web.cert.parsed.subject_key_info.dsa.g` | text |  |
| `web.cert.parsed.subject_key_info.dsa.p` | text |  |
| `web.cert.parsed.subject_key_info.dsa.q` | text |  |
| `web.cert.parsed.subject_key_info.dsa.y` | text |  |
| `web.cert.parsed.subject_key_info.ecdsa` | object | A record containing the public portion of an ECDSA asymmetric key. |
| `web.cert.parsed.subject_key_info.ecdsa.length` | long |  |
| `web.cert.parsed.subject_key_info.ecdsa.pub` | text |  |
| `web.cert.parsed.subject_key_info.ecdsa.gy` | text |  |
| `web.cert.parsed.subject_key_info.ecdsa.p` | text |  |
| `web.cert.parsed.subject_key_info.ecdsa.y` | text |  |
| `web.cert.parsed.subject_key_info.ecdsa.gx` | text |  |
| `web.cert.parsed.subject_key_info.ecdsa.n` | text |  |
| `web.cert.parsed.subject_key_info.ecdsa.x` | text |  |
| `web.cert.parsed.subject_key_info.ecdsa.curve` | text |  |
| `web.cert.parsed.subject_key_info.ecdsa.b` | text |  |
| `web.cert.parsed.extensions` | object | A record containing parsed X.509 extensions that provide additional identification information or additional cryptographic capabilities. |
| `web.cert.parsed.extensions.key_usage` | object | The parsed id-ce-keyUsage extension (OID: 2.5.29.15). |
| `web.cert.parsed.extensions.key_usage.content_commitment` | boolean | Whether the contentCommitment (formerly called nonRepudiation) bit is set. |
| `web.cert.parsed.extensions.key_usage.digital_signature` | boolean | Whether the digitalSignature bit is set. |
| `web.cert.parsed.extensions.key_usage.value` | unsigned_long | The integer value of the bitmask in the extension. |
| `web.cert.parsed.extensions.key_usage.crl_sign` | boolean | Whether the cRLSign bit is set. |
| `web.cert.parsed.extensions.key_usage.encipher_only` | boolean | Whether the encipherOnly bit is set. |
| `web.cert.parsed.extensions.key_usage.key_agreement` | boolean | Whether the keyAgreement bit is set. |
| `web.cert.parsed.extensions.key_usage.data_encipherment` | boolean | Whether the dataEncipherment bit is set. |
| `web.cert.parsed.extensions.key_usage.certificate_sign` | boolean | Whether the keyCertSign bit is set. |
| `web.cert.parsed.extensions.key_usage.decipher_only` | boolean | Whether the decipherOnly bit is set. |
| `web.cert.parsed.extensions.key_usage.key_encipherment` | boolean | Whether the keyEncipherment bit is set. |
| `web.cert.parsed.extensions.signed_certificate_timestamps` | nested |  |
| `web.cert.parsed.extensions.signed_certificate_timestamps.timestamp` | date |  |
| `web.cert.parsed.extensions.signed_certificate_timestamps.version` | integer |  |
| `web.cert.parsed.extensions.signed_certificate_timestamps.log_id` | text |  |
| `web.cert.parsed.extensions.signed_certificate_timestamps.signature` | object |  |
| `web.cert.parsed.extensions.signed_certificate_timestamps.signature.hash_algorithm` | text |  |
| `web.cert.parsed.extensions.signed_certificate_timestamps.signature.signature` | text |  |
| `web.cert.parsed.extensions.signed_certificate_timestamps.signature.signature_algorithm` | text |  |
| `web.cert.parsed.extensions.authority_key_id` | text | A key identifier, usually a digest of the DER-encoded SubjectPublicKeyInfo. |
| `web.cert.parsed.extensions.qc_statements` | object |  |
| `web.cert.parsed.extensions.qc_statements.parsed` | object |  |
| `web.cert.parsed.extensions.qc_statements.parsed.sscd` | boolean |  |
| `web.cert.parsed.extensions.qc_statements.parsed.types` | nested |  |
| `web.cert.parsed.extensions.qc_statements.parsed.types.ids` | text |  |
| `web.cert.parsed.extensions.qc_statements.parsed.etsi_compliance` | boolean |  |
| `web.cert.parsed.extensions.qc_statements.parsed.legislation` | nested |  |
| `web.cert.parsed.extensions.qc_statements.parsed.legislation.country_codes` | text |  |
| `web.cert.parsed.extensions.qc_statements.parsed.limit` | nested |  |
| `web.cert.parsed.extensions.qc_statements.parsed.limit.amount` | long |  |
| `web.cert.parsed.extensions.qc_statements.parsed.limit.currency` | text |  |
| `web.cert.parsed.extensions.qc_statements.parsed.limit.currency_number` | long |  |
| `web.cert.parsed.extensions.qc_statements.parsed.limit.exponent` | long |  |
| `web.cert.parsed.extensions.qc_statements.parsed.pds_locations` | nested |  |
| `web.cert.parsed.extensions.qc_statements.parsed.pds_locations.language` | text |  |
| `web.cert.parsed.extensions.qc_statements.parsed.pds_locations.url` | text |  |
| `web.cert.parsed.extensions.qc_statements.parsed.retention_period` | long |  |
| `web.cert.parsed.extensions.qc_statements.ids` | text |  |
| `web.cert.parsed.extensions.subject_key_id` | text | A key identifier, usually a digest of the DER-encoded SubjectPublicKeyInfo.. |
| `web.cert.parsed.extensions.tor_service_descriptors` | nested |  |
| `web.cert.parsed.extensions.tor_service_descriptors.algorithm_name` | text |  |
| `web.cert.parsed.extensions.tor_service_descriptors.hash` | text |  |
| `web.cert.parsed.extensions.tor_service_descriptors.hash_bits` | integer |  |
| `web.cert.parsed.extensions.tor_service_descriptors.onion` | text |  |
| `web.cert.parsed.extensions.certificate_policies` | nested | The parsed id-ce-certificatePolicies extension (OID: 2.5.29.32). |
| `web.cert.parsed.extensions.certificate_policies.id` | text |  |
| `web.cert.parsed.extensions.certificate_policies.user_notice` | nested |  |
| `web.cert.parsed.extensions.certificate_policies.user_notice.explicit_text` | text |  |
| `web.cert.parsed.extensions.certificate_policies.user_notice.notice_reference` | object |  |
| `web.cert.parsed.extensions.certificate_policies.user_notice.notice_reference.notice_numbers` | integer |  |
| `web.cert.parsed.extensions.certificate_policies.user_notice.notice_reference.organization` | text |  |
| `web.cert.parsed.extensions.certificate_policies.cps` | text |  |
| `web.cert.parsed.extensions.extended_key_usage` | object | The parsed id-ce-extKeyUsage extension (OID: 2.5.29.37). |
| `web.cert.parsed.extensions.extended_key_usage.microsoft_timestamp_signing` | boolean |  |
| `web.cert.parsed.extensions.extended_key_usage.microsoft_document_signing` | boolean |  |
| `web.cert.parsed.extensions.extended_key_usage.apple_code_signing_development` | boolean |  |
| `web.cert.parsed.extensions.extended_key_usage.apple_crypto_tier0_qos` | boolean |  |
| `web.cert.parsed.extensions.extended_key_usage.netscape_server_gated_crypto` | boolean |  |
| `web.cert.parsed.extensions.extended_key_usage.microsoft_enrollment_agent` | boolean |  |
| `web.cert.parsed.extensions.extended_key_usage.code_signing` | boolean |  |
| `web.cert.parsed.extensions.extended_key_usage.any` | boolean |  |
| `web.cert.parsed.extensions.extended_key_usage.microsoft_sgc_serialized` | boolean |  |
| `web.cert.parsed.extensions.extended_key_usage.microsoft_key_recovery_21` | boolean |  |
| `web.cert.parsed.extensions.extended_key_usage.ipsec_intermediate_system_usage` | boolean |  |
| `web.cert.parsed.extensions.extended_key_usage.microsoft_oem_whql_crypto` | boolean |  |
| `web.cert.parsed.extensions.extended_key_usage.apple_code_signing_third_party` | boolean |  |
| `web.cert.parsed.extensions.extended_key_usage.apple_crypto_maintenance_env` | boolean |  |
| `web.cert.parsed.extensions.extended_key_usage.eap_over_lan` | boolean |  |
| `web.cert.parsed.extensions.extended_key_usage.sbgp_cert_aa_service_auth` | boolean |  |
| `web.cert.parsed.extensions.extended_key_usage.dvcs` | boolean |  |
| `web.cert.parsed.extensions.extended_key_usage.unknown` | text |  |
| `web.cert.parsed.extensions.extended_key_usage.ipsec_user` | boolean |  |
| `web.cert.parsed.extensions.extended_key_usage.microsoft_drm` | boolean |  |
| `web.cert.parsed.extensions.extended_key_usage.apple_ichat_signing` | boolean |  |
| `web.cert.parsed.extensions.extended_key_usage.apple_ichat_encryption` | boolean |  |
| `web.cert.parsed.extensions.extended_key_usage.microsoft_smartcard_logon` | boolean |  |
| `web.cert.parsed.extensions.extended_key_usage.apple_crypto_env` | boolean |  |
| `web.cert.parsed.extensions.extended_key_usage.email_protection` | boolean |  |
| `web.cert.parsed.extensions.extended_key_usage.apple_crypto_production_env` | boolean |  |
| `web.cert.parsed.extensions.extended_key_usage.server_auth` | boolean |  |
| `web.cert.parsed.extensions.extended_key_usage.microsoft_licenses` | boolean |  |
| `web.cert.parsed.extensions.extended_key_usage.ocsp_signing` | boolean |  |
| `web.cert.parsed.extensions.extended_key_usage.microsoft_license_server` | boolean |  |
| `web.cert.parsed.extensions.extended_key_usage.eap_over_ppp` | boolean |  |
| `web.cert.parsed.extensions.extended_key_usage.microsoft_qualified_subordinate` | boolean |  |
| `web.cert.parsed.extensions.extended_key_usage.microsoft_ca_exchange` | boolean |  |
| `web.cert.parsed.extensions.extended_key_usage.apple_crypto_test_env` | boolean |  |
| `web.cert.parsed.extensions.extended_key_usage.microsoft_cert_trust_list_signing` | boolean |  |
| `web.cert.parsed.extensions.extended_key_usage.microsoft_csp_signature` | boolean |  |
| `web.cert.parsed.extensions.extended_key_usage.microsoft_mobile_device_software` | boolean |  |
| `web.cert.parsed.extensions.extended_key_usage.apple_crypto_tier3_qos` | boolean |  |
| `web.cert.parsed.extensions.extended_key_usage.microsoft_whql_crypto` | boolean |  |
| `web.cert.parsed.extensions.extended_key_usage.apple_software_update_signing` | boolean |  |
| `web.cert.parsed.extensions.extended_key_usage.microsoft_root_list_signer` | boolean |  |
| `web.cert.parsed.extensions.extended_key_usage.microsoft_encrypted_file_system` | boolean |  |
| `web.cert.parsed.extensions.extended_key_usage.microsoft_system_health_loophole` | boolean |  |
| `web.cert.parsed.extensions.extended_key_usage.apple_crypto_qos` | boolean |  |
| `web.cert.parsed.extensions.extended_key_usage.microsoft_server_gated_crypto` | boolean |  |
| `web.cert.parsed.extensions.extended_key_usage.ipsec_end_system` | boolean |  |
| `web.cert.parsed.extensions.extended_key_usage.apple_crypto_development_env` | boolean |  |
| `web.cert.parsed.extensions.extended_key_usage.microsoft_efs_recovery` | boolean |  |
| `web.cert.parsed.extensions.extended_key_usage.microsoft_embedded_nt_crypto` | boolean |  |
| `web.cert.parsed.extensions.extended_key_usage.microsoft_drm_individualization` | boolean |  |
| `web.cert.parsed.extensions.extended_key_usage.microsoft_nt5_crypto` | boolean |  |
| `web.cert.parsed.extensions.extended_key_usage.ipsec_tunnel` | boolean |  |
| `web.cert.parsed.extensions.extended_key_usage.client_auth` | boolean |  |
| `web.cert.parsed.extensions.extended_key_usage.apple_resource_signing` | boolean |  |
| `web.cert.parsed.extensions.extended_key_usage.microsoft_lifetime_signing` | boolean |  |
| `web.cert.parsed.extensions.extended_key_usage.apple_code_signing` | boolean |  |
| `web.cert.parsed.extensions.extended_key_usage.microsoft_kernel_mode_code_signing` | boolean |  |
| `web.cert.parsed.extensions.extended_key_usage.apple_system_identity` | boolean |  |
| `web.cert.parsed.extensions.extended_key_usage.apple_crypto_tier1_qos` | boolean |  |
| `web.cert.parsed.extensions.extended_key_usage.time_stamping` | boolean |  |
| `web.cert.parsed.extensions.extended_key_usage.microsoft_system_health` | boolean |  |
| `web.cert.parsed.extensions.extended_key_usage.microsoft_key_recovery_3` | boolean |  |
| `web.cert.parsed.extensions.extended_key_usage.apple_crypto_tier2_qos` | boolean |  |
| `web.cert.parsed.extensions.extended_key_usage.microsoft_smart_display` | boolean |  |
| `web.cert.parsed.extensions.authority_info_access` | object | The parsed id-pe-authorityInfoAccess extension (OID: 1.3.6.1.5.7.1.1). Only id-ad-caIssuers and id-ad-ocsp accessMethods are supported; others are omitted. |
| `web.cert.parsed.extensions.authority_info_access.ocsp_urls` | text |  |
| `web.cert.parsed.extensions.authority_info_access.issuer_urls` | text |  |
| `web.cert.parsed.extensions.name_constraints` | object | The parsed id-ce-nameConstraints extension (OID: 2.5.29.30). Specifies a name space within which all child certificates' subject names MUST be located. |
| `web.cert.parsed.extensions.name_constraints.permitted_edi_party_names` | nested | A record providing permitted names of the type ediPartyName in leaf certificates whose trust path includes this certificate. |
| `web.cert.parsed.extensions.name_constraints.permitted_edi_party_names.name_assigner` | text |  |
| `web.cert.parsed.extensions.name_constraints.permitted_edi_party_names.party_name` | text |  |
| `web.cert.parsed.extensions.name_constraints.excluded_edi_party_names` | nested | A record providing excluded names of the type ediPartyName in leaf certificates whose trust path includes this certificate. |
| `web.cert.parsed.extensions.name_constraints.excluded_edi_party_names.party_name` | text |  |
| `web.cert.parsed.extensions.name_constraints.excluded_edi_party_names.name_assigner` | text |  |
| `web.cert.parsed.extensions.name_constraints.excluded_directory_names` | nested | A record providing excluded names of the type directoryName in leaf certificates whose trust path includes this certificate. |
| `web.cert.parsed.extensions.name_constraints.excluded_directory_names.given_name` | text | The givenName (G) elements of the Distinguished Name (OID: 2.5.4.42). |
| `web.cert.parsed.extensions.name_constraints.excluded_directory_names.jurisdiction_country` | text | The jurisdictionCountry elements of the Distinguished Name (OID: 1.3.6.1.4.1.311.60.2.1.3). |
| `web.cert.parsed.extensions.name_constraints.excluded_directory_names.street_address` | text | The streetAddress (STREET) elements of the Distinguished Name (OID: 2.5.4.9). |
| `web.cert.parsed.extensions.name_constraints.excluded_directory_names.jurisdiction_province` | text | The jurisdictionStateOrProvince elements of the Distinguished Name (OID: 1.3.6.1.4.1.311.60.2.1.2). |
| `web.cert.parsed.extensions.name_constraints.excluded_directory_names.common_name` | text | The commonName (CN) elements of the Distinguished Name (OID: 2.5.4.3). |
| `web.cert.parsed.extensions.name_constraints.excluded_directory_names.postal_code` | keyword | The postalCode elements of the Distinguished Name (OID: 2.5.4.17). |
| `web.cert.parsed.extensions.name_constraints.excluded_directory_names.jurisdiction_locality` | text | The jurisdictionLocality elements of the Distinguished Name (OID: 1.3.6.1.4.1.311.60.2.1.1). |
| `web.cert.parsed.extensions.name_constraints.excluded_directory_names.organization` | text | The organizationName (O) elements of the Distinguished Name (OID: 2.5.4.10). |
| `web.cert.parsed.extensions.name_constraints.excluded_directory_names.email_address` | text | The emailAddress (E) elements of the Distinguished Name (OID: 1.2.840.113549.1.9.1). |
| `web.cert.parsed.extensions.name_constraints.excluded_directory_names.locality` | text | The localityName (L) elements of the Distinguished Name (OID: 2.5.4.7). |
| `web.cert.parsed.extensions.name_constraints.excluded_directory_names.domain_component` | text | The domainComponent (DC) elements of the Distinguished Name (OID: 0.9.2342.19200300.100.1.25). |
| `web.cert.parsed.extensions.name_constraints.excluded_directory_names.province` | text | The stateOrProvinceName (ST) elements of the Distinguished Name (OID: 2.5.4.8). |
| `web.cert.parsed.extensions.name_constraints.excluded_directory_names.country` | text | The countryName (C) elements of the Distinguished Name (OID: 2.5.4.6). |
| `web.cert.parsed.extensions.name_constraints.excluded_directory_names.organization_id` | text |  |
| `web.cert.parsed.extensions.name_constraints.excluded_directory_names.surname` | text | The surname (SN) elements of the Distinguished Name (OID: 2.5.4.4). |
| `web.cert.parsed.extensions.name_constraints.excluded_directory_names.organizational_unit` | text | The organizationalUnit (OU) elements of the Distinguished Name (OID: 2.5.4.11). |
| `web.cert.parsed.extensions.name_constraints.excluded_directory_names.serial_number` | keyword | The serialNumber elements of the Distinguished Name (OID: 2.5.4.5). |
| `web.cert.parsed.extensions.name_constraints.permitted_uris` | text | A record providing a range of permitted uniform resource identifiers in leaf certificates whose trust path includes this certificate. |
| `web.cert.parsed.extensions.name_constraints.excluded_email_addresses` | text | A record providing a range of excluded names of the type rfc822Name in leaf certificates whose trust path includes this certificate. |
| `web.cert.parsed.extensions.name_constraints.excluded_ip_addresses` | nested | A record providing a range of excluded names of the type iPAddress in leaf certificates whose trust path includes this certificate. |
| `web.cert.parsed.extensions.name_constraints.excluded_ip_addresses.begin` | text | The first IP address in the range. |
| `web.cert.parsed.extensions.name_constraints.excluded_ip_addresses.cidr` | text | The CIDR specifying the subtree. |
| `web.cert.parsed.extensions.name_constraints.excluded_ip_addresses.end` | text | The last IP address in the range. |
| `web.cert.parsed.extensions.name_constraints.excluded_ip_addresses.mask` | text | The subnet mask of the CIDR. |
| `web.cert.parsed.extensions.name_constraints.permitted_ip_addresses` | nested | A record providing a range of permitted names of the type iPAddress in leaf certificates whose trust path includes this certificate. |
| `web.cert.parsed.extensions.name_constraints.permitted_ip_addresses.begin` | text | The first IP address in the range. |
| `web.cert.parsed.extensions.name_constraints.permitted_ip_addresses.cidr` | text | The CIDR specifying the subtree. |
| `web.cert.parsed.extensions.name_constraints.permitted_ip_addresses.end` | text | The last IP address in the range. |
| `web.cert.parsed.extensions.name_constraints.permitted_ip_addresses.mask` | text | The subnet mask of the CIDR. |
| `web.cert.parsed.extensions.name_constraints.excluded_registered_ids` | text | A record providing excluded names of the type registeredID in leaf certificates whose trust path includes this certificate. |
| `web.cert.parsed.extensions.name_constraints.excluded_names` | text | A record providing a range of excluded names of the type dNSName in leaf certificates whose trust path includes this certificate. |
| `web.cert.parsed.extensions.name_constraints.permitted_email_addresses` | text | A record providing a range of permitted names of the type rfc822Name in leaf certificates whose trust path includes this certificate. |
| `web.cert.parsed.extensions.name_constraints.critical` | boolean |  |
| `web.cert.parsed.extensions.name_constraints.permitted_registered_ids` | text | A record providing permitted names of the type registeredID in leaf certificates whose trust path includes this certificate. |
| `web.cert.parsed.extensions.name_constraints.permitted_directory_names` | nested | A record providing permitted names of the type directoryName in leaf certificates whose trust path includes this certificate. |
| `web.cert.parsed.extensions.name_constraints.permitted_directory_names.domain_component` | text | The domainComponent (DC) elements of the Distinguished Name (OID: 0.9.2342.19200300.100.1.25). |
| `web.cert.parsed.extensions.name_constraints.permitted_directory_names.surname` | text | The surname (SN) elements of the Distinguished Name (OID: 2.5.4.4). |
| `web.cert.parsed.extensions.name_constraints.permitted_directory_names.street_address` | text | The streetAddress (STREET) elements of the Distinguished Name (OID: 2.5.4.9). |
| `web.cert.parsed.extensions.name_constraints.permitted_directory_names.locality` | text | The localityName (L) elements of the Distinguished Name (OID: 2.5.4.7). |
| `web.cert.parsed.extensions.name_constraints.permitted_directory_names.organizational_unit` | text | The organizationalUnit (OU) elements of the Distinguished Name (OID: 2.5.4.11). |
| `web.cert.parsed.extensions.name_constraints.permitted_directory_names.serial_number` | keyword | The serialNumber elements of the Distinguished Name (OID: 2.5.4.5). |
| `web.cert.parsed.extensions.name_constraints.permitted_directory_names.country` | text | The countryName (C) elements of the Distinguished Name (OID: 2.5.4.6). |
| `web.cert.parsed.extensions.name_constraints.permitted_directory_names.jurisdiction_province` | text | The jurisdictionStateOrProvince elements of the Distinguished Name (OID: 1.3.6.1.4.1.311.60.2.1.2). |
| `web.cert.parsed.extensions.name_constraints.permitted_directory_names.province` | text | The stateOrProvinceName (ST) elements of the Distinguished Name (OID: 2.5.4.8). |
| `web.cert.parsed.extensions.name_constraints.permitted_directory_names.postal_code` | keyword | The postalCode elements of the Distinguished Name (OID: 2.5.4.17). |
| `web.cert.parsed.extensions.name_constraints.permitted_directory_names.jurisdiction_country` | text | The jurisdictionCountry elements of the Distinguished Name (OID: 1.3.6.1.4.1.311.60.2.1.3). |
| `web.cert.parsed.extensions.name_constraints.permitted_directory_names.email_address` | text | The emailAddress (E) elements of the Distinguished Name (OID: 1.2.840.113549.1.9.1). |
| `web.cert.parsed.extensions.name_constraints.permitted_directory_names.given_name` | text | The givenName (G) elements of the Distinguished Name (OID: 2.5.4.42). |
| `web.cert.parsed.extensions.name_constraints.permitted_directory_names.jurisdiction_locality` | text | The jurisdictionLocality elements of the Distinguished Name (OID: 1.3.6.1.4.1.311.60.2.1.1). |
| `web.cert.parsed.extensions.name_constraints.permitted_directory_names.organization` | text | The organizationName (O) elements of the Distinguished Name (OID: 2.5.4.10). |
| `web.cert.parsed.extensions.name_constraints.permitted_directory_names.common_name` | text | The commonName (CN) elements of the Distinguished Name (OID: 2.5.4.3). |
| `web.cert.parsed.extensions.name_constraints.permitted_directory_names.organization_id` | text |  |
| `web.cert.parsed.extensions.name_constraints.permitted_names` | text | A record providing a range of permitted names of the type dNSName in leaf certificates whose trust path includes this certificate. |
| `web.cert.parsed.extensions.name_constraints.excluded_uris` | text | A record providing a range of excluded uniform resource identifiers in leaf certificates whose trust path includes this certificate. |
| `web.cert.parsed.extensions.subject_alt_name` | object | The parsed id-ce-subjectAltName extension (OID: 2.5.29.17). |
| `web.cert.parsed.extensions.subject_alt_name.uniform_resource_identifiers` | text | The parsed uniformResourceIdentifier entries in the GeneralName. |
| `web.cert.parsed.extensions.subject_alt_name.directory_names` | nested | The parsed directoryName entries in the GeneralName. |
| `web.cert.parsed.extensions.subject_alt_name.directory_names.organization_id` | text |  |
| `web.cert.parsed.extensions.subject_alt_name.directory_names.common_name` | text | The commonName (CN) elements of the Distinguished Name (OID: 2.5.4.3). |
| `web.cert.parsed.extensions.subject_alt_name.directory_names.street_address` | text | The streetAddress (STREET) elements of the Distinguished Name (OID: 2.5.4.9). |
| `web.cert.parsed.extensions.subject_alt_name.directory_names.locality` | text | The localityName (L) elements of the Distinguished Name (OID: 2.5.4.7). |
| `web.cert.parsed.extensions.subject_alt_name.directory_names.organizational_unit` | text | The organizationalUnit (OU) elements of the Distinguished Name (OID: 2.5.4.11). |
| `web.cert.parsed.extensions.subject_alt_name.directory_names.domain_component` | text | The domainComponent (DC) elements of the Distinguished Name (OID: 0.9.2342.19200300.100.1.25). |
| `web.cert.parsed.extensions.subject_alt_name.directory_names.jurisdiction_locality` | text | The jurisdictionLocality elements of the Distinguished Name (OID: 1.3.6.1.4.1.311.60.2.1.1). |
| `web.cert.parsed.extensions.subject_alt_name.directory_names.postal_code` | keyword | The postalCode elements of the Distinguished Name (OID: 2.5.4.17). |
| `web.cert.parsed.extensions.subject_alt_name.directory_names.serial_number` | keyword | The serialNumber elements of the Distinguished Name (OID: 2.5.4.5). |
| `web.cert.parsed.extensions.subject_alt_name.directory_names.email_address` | text | The emailAddress (E) elements of the Distinguished Name (OID: 1.2.840.113549.1.9.1). |
| `web.cert.parsed.extensions.subject_alt_name.directory_names.jurisdiction_country` | text | The jurisdictionCountry elements of the Distinguished Name (OID: 1.3.6.1.4.1.311.60.2.1.3). |
| `web.cert.parsed.extensions.subject_alt_name.directory_names.jurisdiction_province` | text | The jurisdictionStateOrProvince elements of the Distinguished Name (OID: 1.3.6.1.4.1.311.60.2.1.2). |
| `web.cert.parsed.extensions.subject_alt_name.directory_names.surname` | text | The surname (SN) elements of the Distinguished Name (OID: 2.5.4.4). |
| `web.cert.parsed.extensions.subject_alt_name.directory_names.given_name` | text | The givenName (G) elements of the Distinguished Name (OID: 2.5.4.42). |
| `web.cert.parsed.extensions.subject_alt_name.directory_names.organization` | text | The organizationName (O) elements of the Distinguished Name (OID: 2.5.4.10). |
| `web.cert.parsed.extensions.subject_alt_name.directory_names.province` | text | The stateOrProvinceName (ST) elements of the Distinguished Name (OID: 2.5.4.8). |
| `web.cert.parsed.extensions.subject_alt_name.directory_names.country` | text | The countryName (C) elements of the Distinguished Name (OID: 2.5.4.6). |
| `web.cert.parsed.extensions.subject_alt_name.dns_names` | text | The parsed dNSName entries in the GeneralName. |
| `web.cert.parsed.extensions.subject_alt_name.edi_party_names` | nested | The parsed eDIPartyName entries in the GeneralName. |
| `web.cert.parsed.extensions.subject_alt_name.edi_party_names.name_assigner` | text |  |
| `web.cert.parsed.extensions.subject_alt_name.edi_party_names.party_name` | text |  |
| `web.cert.parsed.extensions.subject_alt_name.email_addresses` | text | The parsed rfc822Name entries in the GeneralName. |
| `web.cert.parsed.extensions.subject_alt_name.ip_addresses` | text | The parsed ipAddress entries in the GeneralName. |
| `web.cert.parsed.extensions.subject_alt_name.other_names` | nested | The parsed otherName entries in the GeneralName. An arbitrary binary value identified by an OID. |
| `web.cert.parsed.extensions.subject_alt_name.other_names.value` | text | The raw otherName value. |
| `web.cert.parsed.extensions.subject_alt_name.other_names.id` | text | The OID identifying the syntax of the otherName value. |
| `web.cert.parsed.extensions.subject_alt_name.registered_ids` | text | The parsed registeredID entries in the GeneralName. Stored in dotted-decimal format. |
| `web.cert.parsed.extensions.issuer_alt_name` | object | The parsed id-ce-issuerAltName extension (OID: 2.5.29.18). |
| `web.cert.parsed.extensions.issuer_alt_name.registered_ids` | text | The parsed registeredID entries in the GeneralName. Stored in dotted-decimal format. |
| `web.cert.parsed.extensions.issuer_alt_name.uniform_resource_identifiers` | text | The parsed uniformResourceIdentifier entries in the GeneralName. |
| `web.cert.parsed.extensions.issuer_alt_name.directory_names` | nested | The parsed directoryName entries in the GeneralName. |
| `web.cert.parsed.extensions.issuer_alt_name.directory_names.country` | text | The countryName (C) elements of the Distinguished Name (OID: 2.5.4.6). |
| `web.cert.parsed.extensions.issuer_alt_name.directory_names.email_address` | text | The emailAddress (E) elements of the Distinguished Name (OID: 1.2.840.113549.1.9.1). |
| `web.cert.parsed.extensions.issuer_alt_name.directory_names.domain_component` | text | The domainComponent (DC) elements of the Distinguished Name (OID: 0.9.2342.19200300.100.1.25). |
| `web.cert.parsed.extensions.issuer_alt_name.directory_names.jurisdiction_country` | text | The jurisdictionCountry elements of the Distinguished Name (OID: 1.3.6.1.4.1.311.60.2.1.3). |
| `web.cert.parsed.extensions.issuer_alt_name.directory_names.organizational_unit` | text | The organizationalUnit (OU) elements of the Distinguished Name (OID: 2.5.4.11). |
| `web.cert.parsed.extensions.issuer_alt_name.directory_names.postal_code` | keyword | The postalCode elements of the Distinguished Name (OID: 2.5.4.17). |
| `web.cert.parsed.extensions.issuer_alt_name.directory_names.locality` | text | The localityName (L) elements of the Distinguished Name (OID: 2.5.4.7). |
| `web.cert.parsed.extensions.issuer_alt_name.directory_names.organization_id` | text |  |
| `web.cert.parsed.extensions.issuer_alt_name.directory_names.jurisdiction_locality` | text | The jurisdictionLocality elements of the Distinguished Name (OID: 1.3.6.1.4.1.311.60.2.1.1). |
| `web.cert.parsed.extensions.issuer_alt_name.directory_names.common_name` | text | The commonName (CN) elements of the Distinguished Name (OID: 2.5.4.3). |
| `web.cert.parsed.extensions.issuer_alt_name.directory_names.serial_number` | keyword | The serialNumber elements of the Distinguished Name (OID: 2.5.4.5). |
| `web.cert.parsed.extensions.issuer_alt_name.directory_names.surname` | text | The surname (SN) elements of the Distinguished Name (OID: 2.5.4.4). |
| `web.cert.parsed.extensions.issuer_alt_name.directory_names.organization` | text | The organizationName (O) elements of the Distinguished Name (OID: 2.5.4.10). |
| `web.cert.parsed.extensions.issuer_alt_name.directory_names.province` | text | The stateOrProvinceName (ST) elements of the Distinguished Name (OID: 2.5.4.8). |
| `web.cert.parsed.extensions.issuer_alt_name.directory_names.street_address` | text | The streetAddress (STREET) elements of the Distinguished Name (OID: 2.5.4.9). |
| `web.cert.parsed.extensions.issuer_alt_name.directory_names.given_name` | text | The givenName (G) elements of the Distinguished Name (OID: 2.5.4.42). |
| `web.cert.parsed.extensions.issuer_alt_name.directory_names.jurisdiction_province` | text | The jurisdictionStateOrProvince elements of the Distinguished Name (OID: 1.3.6.1.4.1.311.60.2.1.2). |
| `web.cert.parsed.extensions.issuer_alt_name.dns_names` | text | The parsed dNSName entries in the GeneralName. |
| `web.cert.parsed.extensions.issuer_alt_name.edi_party_names` | nested | The parsed eDIPartyName entries in the GeneralName. |
| `web.cert.parsed.extensions.issuer_alt_name.edi_party_names.name_assigner` | text |  |
| `web.cert.parsed.extensions.issuer_alt_name.edi_party_names.party_name` | text |  |
| `web.cert.parsed.extensions.issuer_alt_name.email_addresses` | text | The parsed rfc822Name entries in the GeneralName. |
| `web.cert.parsed.extensions.issuer_alt_name.ip_addresses` | text | The parsed ipAddress entries in the GeneralName. |
| `web.cert.parsed.extensions.issuer_alt_name.other_names` | nested | The parsed otherName entries in the GeneralName. An arbitrary binary value identified by an OID. |
| `web.cert.parsed.extensions.issuer_alt_name.other_names.value` | text | The raw otherName value. |
| `web.cert.parsed.extensions.issuer_alt_name.other_names.id` | text | The OID identifying the syntax of the otherName value. |
| `web.cert.parsed.extensions.cabf_organization_id` | object | CA/Browser Forum organization ID extensions (OID: 2.23.140.3.1). |
| `web.cert.parsed.extensions.cabf_organization_id.scheme` | text |  |
| `web.cert.parsed.extensions.cabf_organization_id.state` | text |  |
| `web.cert.parsed.extensions.cabf_organization_id.country` | text |  |
| `web.cert.parsed.extensions.cabf_organization_id.reference` | text |  |
| `web.cert.parsed.extensions.ct_poison` | boolean | Whether the certificate possesses the pre-certificate "poison" extension (OID: 1.3.6.1.4.1.11129.2.4.3). |
| `web.cert.parsed.extensions.crl_distribution_points` | text | The parsed id-ce-cRLDistributionPoints extension (OID: 2.5.29.31). Contents are a list of distributionPoint URLs; other distributionPoint types are omitted). |
| `web.cert.parsed.extensions.basic_constraints` | object | The parsed id-ce-basicConstraints extension (OID: 2.5.29.19). |
| `web.cert.parsed.extensions.basic_constraints.max_path_len` | integer | When present, provides the maximum number of intermediate certificates that may follow this certificate in a trusted certification path. |
| `web.cert.parsed.extensions.basic_constraints.is_ca` | boolean | Whether the certificate is permitted to sign other certificates. |
| `web.cert.parsed.redacted` | boolean |  |
| `web.cert.parsed.serial_number_hex` | text | Issuer-specific identifier of the certificate, represented as hexadecimal. |
| `web.cert.parsed.subject` | object | A record containing the parsed contents of the subject_dn. |
| `web.cert.parsed.subject.organizational_unit` | text | The organizationalUnit (OU) elements of the Distinguished Name (OID: 2.5.4.11). |
| `web.cert.parsed.subject.postal_code` | keyword | The postalCode elements of the Distinguished Name (OID: 2.5.4.17). |
| `web.cert.parsed.subject.jurisdiction_province` | text | The jurisdictionStateOrProvince elements of the Distinguished Name (OID: 1.3.6.1.4.1.311.60.2.1.2). |
| `web.cert.parsed.subject.surname` | text | The surname (SN) elements of the Distinguished Name (OID: 2.5.4.4). |
| `web.cert.parsed.subject.email_address` | text | The emailAddress (E) elements of the Distinguished Name (OID: 1.2.840.113549.1.9.1). |
| `web.cert.parsed.subject.jurisdiction_country` | text | The jurisdictionCountry elements of the Distinguished Name (OID: 1.3.6.1.4.1.311.60.2.1.3). |
| `web.cert.parsed.subject.organization_id` | text |  |
| `web.cert.parsed.subject.street_address` | text | The streetAddress (STREET) elements of the Distinguished Name (OID: 2.5.4.9). |
| `web.cert.parsed.subject.serial_number` | keyword | The serialNumber elements of the Distinguished Name (OID: 2.5.4.5). |
| `web.cert.parsed.subject.domain_component` | text | The domainComponent (DC) elements of the Distinguished Name (OID: 0.9.2342.19200300.100.1.25). |
| `web.cert.parsed.subject.jurisdiction_locality` | text | The jurisdictionLocality elements of the Distinguished Name (OID: 1.3.6.1.4.1.311.60.2.1.1). |
| `web.cert.parsed.subject.province` | text | The stateOrProvinceName (ST) elements of the Distinguished Name (OID: 2.5.4.8). |
| `web.cert.parsed.subject.common_name` | text | The commonName (CN) elements of the Distinguished Name (OID: 2.5.4.3). |
| `web.cert.parsed.subject.country` | text | The countryName (C) elements of the Distinguished Name (OID: 2.5.4.6). |
| `web.cert.parsed.subject.given_name` | text | The givenName (G) elements of the Distinguished Name (OID: 2.5.4.42). |
| `web.cert.parsed.subject.organization` | text | The organizationName (O) elements of the Distinguished Name (OID: 2.5.4.10). |
| `web.cert.parsed.subject.locality` | text | The localityName (L) elements of the Distinguished Name (OID: 2.5.4.7). |
| `web.cert.parsed.validity_period` | object | Information about the time for which the certificate is valid. |
| `web.cert.parsed.validity_period.length_seconds` | long | The duration of the certificate's validity period, in seconds. |
| `web.cert.parsed.validity_period.not_after` | date | An RFC-3339-formatted timestamp after which the certificate is no longer valid. |
| `web.cert.parsed.validity_period.not_before` | date | An RFC-3339-formatted timestamp before which the certificate is not valid. |
| `web.cert.parsed.issuer_dn` | text | Distinguished Name of the entity that has signed and issued the certificate. |
| `web.cert.parsed.ja4x` | text |  |
| `web.cert.parsed.serial_number` | text | Issuer-specific identifier of the certificate. |
| `web.cert.parsed.signature` | object |  |
| `web.cert.parsed.signature.self_signed` | boolean | Whether the certificate was signed by its own key. |
| `web.cert.parsed.signature.signature_algorithm` | object |  |
| `web.cert.parsed.signature.signature_algorithm.oid` | text |  |
| `web.cert.parsed.signature.signature_algorithm.name` | text | Name of public key type, such as RSA or ECDSA. Information specific to the key type is available in the named sub-record. |
| `web.cert.parsed.signature.valid` | boolean | Whether the signature is valid. |
| `web.cert.parsed.signature.value` | text | Contents of the signature. |
| `web.cert.parsed.issuer` | object | A record containing the parsed contents of the issuer_dn. |
| `web.cert.parsed.issuer.surname` | text | The surname (SN) elements of the Distinguished Name (OID: 2.5.4.4). |
| `web.cert.parsed.issuer.organization_id` | text |  |
| `web.cert.parsed.issuer.locality` | text | The localityName (L) elements of the Distinguished Name (OID: 2.5.4.7). |
| `web.cert.parsed.issuer.serial_number` | keyword | The serialNumber elements of the Distinguished Name (OID: 2.5.4.5). |
| `web.cert.parsed.issuer.country` | text | The countryName (C) elements of the Distinguished Name (OID: 2.5.4.6). |
| `web.cert.parsed.issuer.common_name` | text | The commonName (CN) elements of the Distinguished Name (OID: 2.5.4.3). |
| `web.cert.parsed.issuer.postal_code` | keyword | The postalCode elements of the Distinguished Name (OID: 2.5.4.17). |
| `web.cert.parsed.issuer.organization` | text | The organizationName (O) elements of the Distinguished Name (OID: 2.5.4.10). |
| `web.cert.parsed.issuer.email_address` | text | The emailAddress (E) elements of the Distinguished Name (OID: 1.2.840.113549.1.9.1). |
| `web.cert.parsed.issuer.given_name` | text | The givenName (G) elements of the Distinguished Name (OID: 2.5.4.42). |
| `web.cert.parsed.issuer.jurisdiction_locality` | text | The jurisdictionLocality elements of the Distinguished Name (OID: 1.3.6.1.4.1.311.60.2.1.1). |
| `web.cert.parsed.issuer.jurisdiction_country` | text | The jurisdictionCountry elements of the Distinguished Name (OID: 1.3.6.1.4.1.311.60.2.1.3). |
| `web.cert.parsed.issuer.organizational_unit` | text | The organizationalUnit (OU) elements of the Distinguished Name (OID: 2.5.4.11). |
| `web.cert.parsed.issuer.street_address` | text | The streetAddress (STREET) elements of the Distinguished Name (OID: 2.5.4.9). |
| `web.cert.parsed.issuer.province` | text | The stateOrProvinceName (ST) elements of the Distinguished Name (OID: 2.5.4.8). |
| `web.cert.parsed.issuer.domain_component` | text | The domainComponent (DC) elements of the Distinguished Name (OID: 0.9.2342.19200300.100.1.25). |
| `web.cert.parsed.issuer.jurisdiction_province` | text | The jurisdictionStateOrProvince elements of the Distinguished Name (OID: 1.3.6.1.4.1.311.60.2.1.2). |
| `web.cert.validation_level` | keyword | The extent to which the certificate's issuer validated the identity of the entity requesting the certificate. Options include Domain validated (DV), Organization Validated (OV), or Extended Validation (EV). |
| `web.cert.ever_seen_in_scan` | boolean | Whether the certificate has ever been presented by a service during a scan. |
| `web.cert.fingerprint_sha1` | text | The SHA-1 digest of the entire raw certificate. An identifier used by some systems. |
| `web.cert.spki_subject_fingerprint_sha256` | text | The SHA-256 digest of the certificate's DER-encoded SubjectPublicKeyInfo concatenated with its Subject. |
| `web.cert.fingerprint_md5` | text | The MD-5 digest of the entire raw certificate. An identifier used by some systems. |
| `web.cert.revocation` | object | A record containing revocation information, if the certificate has been revoked. |
| `web.cert.revocation.ocsp` | object |  |
| `web.cert.revocation.ocsp.revoked` | boolean | Whether the certificate has been revoked before its expiry date by the issuer. |
| `web.cert.revocation.ocsp.next_update` | date |  |
| `web.cert.revocation.ocsp.reason` | keyword | An enumerated value indicating the issuer-supplied reason for the revocation. |
| `web.cert.revocation.ocsp.revocation_time` | date | The issuer-supplied timestamp indicating when the certificate was revoked. |
| `web.cert.revocation.crl` | object |  |
| `web.cert.revocation.crl.reason` | keyword | An enumerated value indicating the issuer-supplied reason for the revocation. |
| `web.cert.revocation.crl.revocation_time` | date | The issuer-supplied timestamp indicating when the certificate was revoked. |
| `web.cert.revocation.crl.revoked` | boolean | Whether the certificate has been revoked before its expiry date by the issuer. |
| `web.cert.revocation.crl.next_update` | date |  |
| `web.exposures` | nested |  |
| `web.exposures.evidence` | nested |  |
| `web.exposures.evidence.negative` | boolean |  |
| `web.exposures.evidence.proprietary` | boolean |  |
| `web.exposures.evidence.regex` | text |  |
| `web.exposures.evidence.semver_expression` | text |  |
| `web.exposures.evidence.data_path` | text |  |
| `web.exposures.evidence.exists` | boolean |  |
| `web.exposures.evidence.found_value` | text |  |
| `web.exposures.evidence.literal_match` | text |  |
| `web.exposures.id` | text |  |
| `web.exposures.metrics` | object |  |
| `web.exposures.metrics.cvss_v30` | object |  |
| `web.exposures.metrics.cvss_v30.components` | object | These metrics contribute to how a CVE is scored. |
| `web.exposures.metrics.cvss_v30.components.availability` | keyword | If an attack renders information unavailable, such as when a system crashes or through a DDoS attack, availability is negatively impacted. Availability has three possible values: None (N) – There is no loss of availability, Low (L) – Availability might be intermittently limited, or performance might be negatively impacted, as a result of a successful attack, High (H) – There is a complete loss of availability of the impacted system or information. |
| `web.exposures.metrics.cvss_v30.components.confidentiality` | keyword | Refers to the disclosure of sensitive information to authorized and unauthorized users, with the goal being that only authorized users are able to access the target data. Confidentiality has three potential values: High (H) – The attacker has full access to all resources in the impacted system, including highly sensitive information such as encryption keys, Low (L) – The attacker has partial access to information, with no control over what, specifically, they are able to access, None (N) – No data is accessible to unauthorized users as a result of the exploit. |
| `web.exposures.metrics.cvss_v30.components.integrity` | keyword | Refers to whether the protected information has been tampered with or changed in any way. If there is no way for an attacker to alter the accuracy or completeness of the information, integrity has been maintained. Integrity has three values: None (N) – There is no loss of the integrity of any information, Low (L) – A limited amount of information might be tampered with or modified, but there is no serious impact on the protected system, High (H) – The attacker can modify any/all information on the target system, resulting in a complete loss of integrity. |
| `web.exposures.metrics.cvss_v30.components.privileges_required` | keyword | Describes the level of privileges or access an attacker must have before successful exploitation. There are three possible values: None (N) – There is no privilege or special access required to conduct the attack, Low (L) – The attacker requires basic, “user” level privileges to leverage the exploit, High (H) – Administrative or similar access privileges are required for successful attack. |
| `web.exposures.metrics.cvss_v30.components.scope` | keyword | Determines whether a vulnerability in one system or component can impact another system or component. If a vulnerability in a vulnerable component can affect a component which is in a different security scope than the vulnerable component, a scope change occurs. Scope has two possible ratings: Changed (C) – An exploited vulnerability can have a carry over impact on another system, Unchanged (U) – The exploited vulnerability is limited in damage to only the local security authority. |
| `web.exposures.metrics.cvss_v30.components.user_interaction` | keyword | Describes whether a user, other than the attacker, is required to do anything or participate in exploitation of the vulnerability. User interaction has two possible values: None (N) – No user interaction is required, Required (R) – A user must complete some steps for the exploit to succeed. For example, a user might be required to install some software. |
| `web.exposures.metrics.cvss_v30.components.attack_complexity` | keyword | Indicates conditions beyond the attacker’s control that must exist in order to exploit the vulnerability. The Attack Complexity metric is scored as either Low or High. There are two possible values: Low (L) – There are no specific pre-conditions required for exploitation, High (H) – The attacker must complete some number of preparatory steps in order to get access. |
| `web.exposures.metrics.cvss_v30.components.attack_vector` | keyword | Indicates the level of access required for an attacker to exploit the vulnerability. The Attack Vector metric is scored in one of four levels: Network (N) – Vulnerabilities with this rating are remotely exploitable, from one or more hops away, up to, and including, remote exploitation over the Internet, Adjacent (A) – A vulnerability with this rating requires network adjacency for exploitation. The attack must be launched from the same physical or logical network, Local (L) – Vulnerabilities with this rating are not exploitable over a network, Physical (P) – An attacker must physically interact with the target system. |
| `web.exposures.metrics.cvss_v30.score` | double | Score of the vulnerability; 0.1 is the lowest, 10 is the maximum |
| `web.exposures.metrics.cvss_v30.vector` | text | The path, method, or scenario used to exploit the vulnerability. Each section represents components that contribute to the overall CVSS score. |
| `web.exposures.metrics.cvss_v31` | object |  |
| `web.exposures.metrics.cvss_v31.vector` | text | The path, method, or scenario used to exploit the vulnerability. Each section represents components that contribute to the overall CVSS score. |
| `web.exposures.metrics.cvss_v31.components` | object | These metrics contribute to how a CVE is scored. |
| `web.exposures.metrics.cvss_v31.components.confidentiality` | keyword | Refers to the disclosure of sensitive information to authorized and unauthorized users, with the goal being that only authorized users are able to access the target data. Confidentiality has three potential values: High (H) – The attacker has full access to all resources in the impacted system, including highly sensitive information such as encryption keys, Low (L) – The attacker has partial access to information, with no control over what, specifically, they are able to access, None (N) – No data is accessible to unauthorized users as a result of the exploit. |
| `web.exposures.metrics.cvss_v31.components.integrity` | keyword | Refers to whether the protected information has been tampered with or changed in any way. If there is no way for an attacker to alter the accuracy or completeness of the information, integrity has been maintained. Integrity has three values: None (N) – There is no loss of the integrity of any information, Low (L) – A limited amount of information might be tampered with or modified, but there is no serious impact on the protected system, High (H) – The attacker can modify any/all information on the target system, resulting in a complete loss of integrity. |
| `web.exposures.metrics.cvss_v31.components.privileges_required` | keyword | Describes the level of privileges or access an attacker must have before successful exploitation. There are three possible values: None (N) – There is no privilege or special access required to conduct the attack, Low (L) – The attacker requires basic, “user” level privileges to leverage the exploit, High (H) – Administrative or similar access privileges are required for successful attack. |
| `web.exposures.metrics.cvss_v31.components.scope` | keyword | Determines whether a vulnerability in one system or component can impact another system or component. If a vulnerability in a vulnerable component can affect a component which is in a different security scope than the vulnerable component, a scope change occurs. Scope has two possible ratings: Changed (C) – An exploited vulnerability can have a carry over impact on another system, Unchanged (U) – The exploited vulnerability is limited in damage to only the local security authority. |
| `web.exposures.metrics.cvss_v31.components.user_interaction` | keyword | Describes whether a user, other than the attacker, is required to do anything or participate in exploitation of the vulnerability. User interaction has two possible values: None (N) – No user interaction is required, Required (R) – A user must complete some steps for the exploit to succeed. For example, a user might be required to install some software. |
| `web.exposures.metrics.cvss_v31.components.attack_complexity` | keyword | Indicates conditions beyond the attacker’s control that must exist in order to exploit the vulnerability. The Attack Complexity metric is scored as either Low or High. There are two possible values: Low (L) – There are no specific pre-conditions required for exploitation, High (H) – The attacker must complete some number of preparatory steps in order to get access. |
| `web.exposures.metrics.cvss_v31.components.attack_vector` | keyword | Indicates the level of access required for an attacker to exploit the vulnerability. The Attack Vector metric is scored in one of four levels: Network (N) – Vulnerabilities with this rating are remotely exploitable, from one or more hops away, up to, and including, remote exploitation over the Internet, Adjacent (A) – A vulnerability with this rating requires network adjacency for exploitation. The attack must be launched from the same physical or logical network, Local (L) – Vulnerabilities with this rating are not exploitable over a network, Physical (P) – An attacker must physically interact with the target system. |
| `web.exposures.metrics.cvss_v31.components.availability` | keyword | If an attack renders information unavailable, such as when a system crashes or through a DDoS attack, availability is negatively impacted. Availability has three possible values: None (N) – There is no loss of availability, Low (L) – Availability might be intermittently limited, or performance might be negatively impacted, as a result of a successful attack, High (H) – There is a complete loss of availability of the impacted system or information. |
| `web.exposures.metrics.cvss_v31.score` | double | Score of the vulnerability; 0.1 is the lowest, 10 is the maximum |
| `web.exposures.metrics.cvss_v40` | object |  |
| `web.exposures.metrics.cvss_v40.score` | double | Score of the vulnerability; 0.1 is the lowest, 10 is the maximum |
| `web.exposures.metrics.cvss_v40.vector` | text | The path, method, or scenario used to exploit the vulnerability. Each section represents components that contribute to the overall CVSS score. |
| `web.exposures.metrics.cvss_v40.components` | object | These metrics contribute to how a CVE is scored. |
| `web.exposures.metrics.cvss_v40.components.automatable` | keyword |  |
| `web.exposures.metrics.cvss_v40.components.confidentiality` | keyword | Refers to the disclosure of sensitive information to authorized and unauthorized users, with the goal being that only authorized users are able to access the target data. Confidentiality has three potential values: High (H) – The attacker has full access to all resources in the impacted system, including highly sensitive information such as encryption keys, Low (L) – The attacker has partial access to information, with no control over what, specifically, they are able to access, None (N) – No data is accessible to unauthorized users as a result of the exploit. |
| `web.exposures.metrics.cvss_v40.components.provider_urgency` | keyword |  |
| `web.exposures.metrics.cvss_v40.components.availability` | keyword | If an attack renders information unavailable, such as when a system crashes or through a DDoS attack, availability is negatively impacted. Availability has three possible values: None (N) – There is no loss of availability, Low (L) – Availability might be intermittently limited, or performance might be negatively impacted, as a result of a successful attack, High (H) – There is a complete loss of availability of the impacted system or information. |
| `web.exposures.metrics.cvss_v40.components.attack_complexity` | keyword | Indicates conditions beyond the attacker’s control that must exist in order to exploit the vulnerability. The Attack Complexity metric is scored as either Low or High. There are two possible values: Low (L) – There are no specific pre-conditions required for exploitation, High (H) – The attacker must complete some number of preparatory steps in order to get access. |
| `web.exposures.metrics.cvss_v40.components.attack_requirements` | keyword |  |
| `web.exposures.metrics.cvss_v40.components.attack_vector` | keyword | Indicates the level of access required for an attacker to exploit the vulnerability. The Attack Vector metric is scored in one of four levels: Network (N) – Vulnerabilities with this rating are remotely exploitable, from one or more hops away, up to, and including, remote exploitation over the Internet, Adjacent (A) – A vulnerability with this rating requires network adjacency for exploitation. The attack must be launched from the same physical or logical network, Local (L) – Vulnerabilities with this rating are not exploitable over a network, Physical (P) – An attacker must physically interact with the target system. |
| `web.exposures.metrics.cvss_v40.components.recovery` | keyword |  |
| `web.exposures.metrics.cvss_v40.components.safety` | keyword |  |
| `web.exposures.metrics.cvss_v40.components.value_density` | keyword |  |
| `web.exposures.metrics.cvss_v40.components.vulnerability_response_effort` | keyword |  |
| `web.exposures.metrics.cvss_v40.components.integrity` | keyword | Refers to whether the protected information has been tampered with or changed in any way. If there is no way for an attacker to alter the accuracy or completeness of the information, integrity has been maintained. Integrity has three values: None (N) – There is no loss of the integrity of any information, Low (L) – A limited amount of information might be tampered with or modified, but there is no serious impact on the protected system, High (H) – The attacker can modify any/all information on the target system, resulting in a complete loss of integrity. |
| `web.exposures.metrics.cvss_v40.components.privileges_required` | keyword | Describes the level of privileges or access an attacker must have before successful exploitation. There are three possible values: None (N) – There is no privilege or special access required to conduct the attack, Low (L) – The attacker requires basic, “user” level privileges to leverage the exploit, High (H) – Administrative or similar access privileges are required for successful attack. |
| `web.exposures.metrics.cvss_v40.components.user_interaction` | keyword | Describes whether a user, other than the attacker, is required to do anything or participate in exploitation of the vulnerability. User interaction has two possible values: None (N) – No user interaction is required, Required (R) – A user must complete some steps for the exploit to succeed. For example, a user might be required to install some software. |
| `web.exposures.metrics.epss` | object |  |
| `web.exposures.metrics.epss.score` | double |  |
| `web.exposures.metrics.epss.percentile` | double |  |
| `web.exposures.risk_source` | keyword |  |
| `web.exposures.source` | keyword |  |
| `web.exposures.confidence` | double |  |
| `web.exposures.severity` | keyword |  |
| `web.exposures.year` | unsigned_long |  |
| `web.exposures.name` | text |  |
| `web.exposures.type` | text |  |
| `web.exposures.cvss` | object |  |
| `web.exposures.cvss.score` | double | Score of the vulnerability; 0.1 is the lowest, 10 is the maximum |
| `web.exposures.cvss.vector` | text | The path, method, or scenario used to exploit the vulnerability. Each section represents components that contribute to the overall CVSS score. |
| `web.exposures.cvss.components` | object | These metrics contribute to how a CVE is scored. |
| `web.exposures.cvss.components.attack_vector` | keyword | Indicates the level of access required for an attacker to exploit the vulnerability. The Attack Vector metric is scored in one of four levels: Network (N) – Vulnerabilities with this rating are remotely exploitable, from one or more hops away, up to, and including, remote exploitation over the Internet, Adjacent (A) – A vulnerability with this rating requires network adjacency for exploitation. The attack must be launched from the same physical or logical network, Local (L) – Vulnerabilities with this rating are not exploitable over a network, Physical (P) – An attacker must physically interact with the target system. |
| `web.exposures.cvss.components.availability` | keyword | If an attack renders information unavailable, such as when a system crashes or through a DDoS attack, availability is negatively impacted. Availability has three possible values: None (N) – There is no loss of availability, Low (L) – Availability might be intermittently limited, or performance might be negatively impacted, as a result of a successful attack, High (H) – There is a complete loss of availability of the impacted system or information. |
| `web.exposures.cvss.components.confidentiality` | keyword | Refers to the disclosure of sensitive information to authorized and unauthorized users, with the goal being that only authorized users are able to access the target data. Confidentiality has three potential values: High (H) – The attacker has full access to all resources in the impacted system, including highly sensitive information such as encryption keys, Low (L) – The attacker has partial access to information, with no control over what, specifically, they are able to access, None (N) – No data is accessible to unauthorized users as a result of the exploit. |
| `web.exposures.cvss.components.integrity` | keyword | Refers to whether the protected information has been tampered with or changed in any way. If there is no way for an attacker to alter the accuracy or completeness of the information, integrity has been maintained. Integrity has three values: None (N) – There is no loss of the integrity of any information, Low (L) – A limited amount of information might be tampered with or modified, but there is no serious impact on the protected system, High (H) – The attacker can modify any/all information on the target system, resulting in a complete loss of integrity. |
| `web.exposures.cvss.components.privileges_required` | keyword | Describes the level of privileges or access an attacker must have before successful exploitation. There are three possible values: None (N) – There is no privilege or special access required to conduct the attack, Low (L) – The attacker requires basic, “user” level privileges to leverage the exploit, High (H) – Administrative or similar access privileges are required for successful attack. |
| `web.exposures.cvss.components.scope` | keyword | Determines whether a vulnerability in one system or component can impact another system or component. If a vulnerability in a vulnerable component can affect a component which is in a different security scope than the vulnerable component, a scope change occurs. Scope has two possible ratings: Changed (C) – An exploited vulnerability can have a carry over impact on another system, Unchanged (U) – The exploited vulnerability is limited in damage to only the local security authority. |
| `web.exposures.cvss.components.user_interaction` | keyword | Describes whether a user, other than the attacker, is required to do anything or participate in exploitation of the vulnerability. User interaction has two possible values: None (N) – No user interaction is required, Required (R) – A user must complete some steps for the exploit to succeed. For example, a user might be required to install some software. |
| `web.exposures.cvss.components.attack_complexity` | keyword | Indicates conditions beyond the attacker’s control that must exist in order to exploit the vulnerability. The Attack Complexity metric is scored as either Low or High. There are two possible values: Low (L) – There are no specific pre-conditions required for exploitation, High (H) – The attacker must complete some number of preparatory steps in order to get access. |
| `web.misconfigs` | nested |  |
| `web.misconfigs.type` | text |  |
| `web.misconfigs.name` | text |  |
| `web.misconfigs.evidence` | nested |  |
| `web.misconfigs.evidence.regex` | text |  |
| `web.misconfigs.evidence.semver_expression` | text |  |
| `web.misconfigs.evidence.data_path` | text |  |
| `web.misconfigs.evidence.exists` | boolean |  |
| `web.misconfigs.evidence.found_value` | text |  |
| `web.misconfigs.evidence.literal_match` | text |  |
| `web.misconfigs.evidence.negative` | boolean |  |
| `web.misconfigs.evidence.proprietary` | boolean |  |
| `web.misconfigs.cvss` | object |  |
| `web.misconfigs.cvss.components` | object | These metrics contribute to how a CVE is scored. |
| `web.misconfigs.cvss.components.attack_vector` | keyword | Indicates the level of access required for an attacker to exploit the vulnerability. The Attack Vector metric is scored in one of four levels: Network (N) – Vulnerabilities with this rating are remotely exploitable, from one or more hops away, up to, and including, remote exploitation over the Internet, Adjacent (A) – A vulnerability with this rating requires network adjacency for exploitation. The attack must be launched from the same physical or logical network, Local (L) – Vulnerabilities with this rating are not exploitable over a network, Physical (P) – An attacker must physically interact with the target system. |
| `web.misconfigs.cvss.components.availability` | keyword | If an attack renders information unavailable, such as when a system crashes or through a DDoS attack, availability is negatively impacted. Availability has three possible values: None (N) – There is no loss of availability, Low (L) – Availability might be intermittently limited, or performance might be negatively impacted, as a result of a successful attack, High (H) – There is a complete loss of availability of the impacted system or information. |
| `web.misconfigs.cvss.components.confidentiality` | keyword | Refers to the disclosure of sensitive information to authorized and unauthorized users, with the goal being that only authorized users are able to access the target data. Confidentiality has three potential values: High (H) – The attacker has full access to all resources in the impacted system, including highly sensitive information such as encryption keys, Low (L) – The attacker has partial access to information, with no control over what, specifically, they are able to access, None (N) – No data is accessible to unauthorized users as a result of the exploit. |
| `web.misconfigs.cvss.components.integrity` | keyword | Refers to whether the protected information has been tampered with or changed in any way. If there is no way for an attacker to alter the accuracy or completeness of the information, integrity has been maintained. Integrity has three values: None (N) – There is no loss of the integrity of any information, Low (L) – A limited amount of information might be tampered with or modified, but there is no serious impact on the protected system, High (H) – The attacker can modify any/all information on the target system, resulting in a complete loss of integrity. |
| `web.misconfigs.cvss.components.privileges_required` | keyword | Describes the level of privileges or access an attacker must have before successful exploitation. There are three possible values: None (N) – There is no privilege or special access required to conduct the attack, Low (L) – The attacker requires basic, “user” level privileges to leverage the exploit, High (H) – Administrative or similar access privileges are required for successful attack. |
| `web.misconfigs.cvss.components.scope` | keyword | Determines whether a vulnerability in one system or component can impact another system or component. If a vulnerability in a vulnerable component can affect a component which is in a different security scope than the vulnerable component, a scope change occurs. Scope has two possible ratings: Changed (C) – An exploited vulnerability can have a carry over impact on another system, Unchanged (U) – The exploited vulnerability is limited in damage to only the local security authority. |
| `web.misconfigs.cvss.components.user_interaction` | keyword | Describes whether a user, other than the attacker, is required to do anything or participate in exploitation of the vulnerability. User interaction has two possible values: None (N) – No user interaction is required, Required (R) – A user must complete some steps for the exploit to succeed. For example, a user might be required to install some software. |
| `web.misconfigs.cvss.components.attack_complexity` | keyword | Indicates conditions beyond the attacker’s control that must exist in order to exploit the vulnerability. The Attack Complexity metric is scored as either Low or High. There are two possible values: Low (L) – There are no specific pre-conditions required for exploitation, High (H) – The attacker must complete some number of preparatory steps in order to get access. |
| `web.misconfigs.cvss.score` | double | Score of the vulnerability; 0.1 is the lowest, 10 is the maximum |
| `web.misconfigs.cvss.vector` | text | The path, method, or scenario used to exploit the vulnerability. Each section represents components that contribute to the overall CVSS score. |
| `web.misconfigs.risk_source` | keyword |  |
| `web.misconfigs.severity` | keyword |  |
| `web.misconfigs.source` | keyword |  |
| `web.misconfigs.confidence` | double |  |
| `web.misconfigs.year` | unsigned_long |  |
| `web.misconfigs.id` | text |  |
| `web.misconfigs.metrics` | object |  |
| `web.misconfigs.metrics.cvss_v30` | object |  |
| `web.misconfigs.metrics.cvss_v30.score` | double | Score of the vulnerability; 0.1 is the lowest, 10 is the maximum |
| `web.misconfigs.metrics.cvss_v30.vector` | text | The path, method, or scenario used to exploit the vulnerability. Each section represents components that contribute to the overall CVSS score. |
| `web.misconfigs.metrics.cvss_v30.components` | object | These metrics contribute to how a CVE is scored. |
| `web.misconfigs.metrics.cvss_v30.components.attack_vector` | keyword | Indicates the level of access required for an attacker to exploit the vulnerability. The Attack Vector metric is scored in one of four levels: Network (N) – Vulnerabilities with this rating are remotely exploitable, from one or more hops away, up to, and including, remote exploitation over the Internet, Adjacent (A) – A vulnerability with this rating requires network adjacency for exploitation. The attack must be launched from the same physical or logical network, Local (L) – Vulnerabilities with this rating are not exploitable over a network, Physical (P) – An attacker must physically interact with the target system. |
| `web.misconfigs.metrics.cvss_v30.components.availability` | keyword | If an attack renders information unavailable, such as when a system crashes or through a DDoS attack, availability is negatively impacted. Availability has three possible values: None (N) – There is no loss of availability, Low (L) – Availability might be intermittently limited, or performance might be negatively impacted, as a result of a successful attack, High (H) – There is a complete loss of availability of the impacted system or information. |
| `web.misconfigs.metrics.cvss_v30.components.confidentiality` | keyword | Refers to the disclosure of sensitive information to authorized and unauthorized users, with the goal being that only authorized users are able to access the target data. Confidentiality has three potential values: High (H) – The attacker has full access to all resources in the impacted system, including highly sensitive information such as encryption keys, Low (L) – The attacker has partial access to information, with no control over what, specifically, they are able to access, None (N) – No data is accessible to unauthorized users as a result of the exploit. |
| `web.misconfigs.metrics.cvss_v30.components.integrity` | keyword | Refers to whether the protected information has been tampered with or changed in any way. If there is no way for an attacker to alter the accuracy or completeness of the information, integrity has been maintained. Integrity has three values: None (N) – There is no loss of the integrity of any information, Low (L) – A limited amount of information might be tampered with or modified, but there is no serious impact on the protected system, High (H) – The attacker can modify any/all information on the target system, resulting in a complete loss of integrity. |
| `web.misconfigs.metrics.cvss_v30.components.privileges_required` | keyword | Describes the level of privileges or access an attacker must have before successful exploitation. There are three possible values: None (N) – There is no privilege or special access required to conduct the attack, Low (L) – The attacker requires basic, “user” level privileges to leverage the exploit, High (H) – Administrative or similar access privileges are required for successful attack. |
| `web.misconfigs.metrics.cvss_v30.components.scope` | keyword | Determines whether a vulnerability in one system or component can impact another system or component. If a vulnerability in a vulnerable component can affect a component which is in a different security scope than the vulnerable component, a scope change occurs. Scope has two possible ratings: Changed (C) – An exploited vulnerability can have a carry over impact on another system, Unchanged (U) – The exploited vulnerability is limited in damage to only the local security authority. |
| `web.misconfigs.metrics.cvss_v30.components.user_interaction` | keyword | Describes whether a user, other than the attacker, is required to do anything or participate in exploitation of the vulnerability. User interaction has two possible values: None (N) – No user interaction is required, Required (R) – A user must complete some steps for the exploit to succeed. For example, a user might be required to install some software. |
| `web.misconfigs.metrics.cvss_v30.components.attack_complexity` | keyword | Indicates conditions beyond the attacker’s control that must exist in order to exploit the vulnerability. The Attack Complexity metric is scored as either Low or High. There are two possible values: Low (L) – There are no specific pre-conditions required for exploitation, High (H) – The attacker must complete some number of preparatory steps in order to get access. |
| `web.misconfigs.metrics.cvss_v31` | object |  |
| `web.misconfigs.metrics.cvss_v31.vector` | text | The path, method, or scenario used to exploit the vulnerability. Each section represents components that contribute to the overall CVSS score. |
| `web.misconfigs.metrics.cvss_v31.components` | object | These metrics contribute to how a CVE is scored. |
| `web.misconfigs.metrics.cvss_v31.components.integrity` | keyword | Refers to whether the protected information has been tampered with or changed in any way. If there is no way for an attacker to alter the accuracy or completeness of the information, integrity has been maintained. Integrity has three values: None (N) – There is no loss of the integrity of any information, Low (L) – A limited amount of information might be tampered with or modified, but there is no serious impact on the protected system, High (H) – The attacker can modify any/all information on the target system, resulting in a complete loss of integrity. |
| `web.misconfigs.metrics.cvss_v31.components.privileges_required` | keyword | Describes the level of privileges or access an attacker must have before successful exploitation. There are three possible values: None (N) – There is no privilege or special access required to conduct the attack, Low (L) – The attacker requires basic, “user” level privileges to leverage the exploit, High (H) – Administrative or similar access privileges are required for successful attack. |
| `web.misconfigs.metrics.cvss_v31.components.scope` | keyword | Determines whether a vulnerability in one system or component can impact another system or component. If a vulnerability in a vulnerable component can affect a component which is in a different security scope than the vulnerable component, a scope change occurs. Scope has two possible ratings: Changed (C) – An exploited vulnerability can have a carry over impact on another system, Unchanged (U) – The exploited vulnerability is limited in damage to only the local security authority. |
| `web.misconfigs.metrics.cvss_v31.components.user_interaction` | keyword | Describes whether a user, other than the attacker, is required to do anything or participate in exploitation of the vulnerability. User interaction has two possible values: None (N) – No user interaction is required, Required (R) – A user must complete some steps for the exploit to succeed. For example, a user might be required to install some software. |
| `web.misconfigs.metrics.cvss_v31.components.attack_complexity` | keyword | Indicates conditions beyond the attacker’s control that must exist in order to exploit the vulnerability. The Attack Complexity metric is scored as either Low or High. There are two possible values: Low (L) – There are no specific pre-conditions required for exploitation, High (H) – The attacker must complete some number of preparatory steps in order to get access. |
| `web.misconfigs.metrics.cvss_v31.components.attack_vector` | keyword | Indicates the level of access required for an attacker to exploit the vulnerability. The Attack Vector metric is scored in one of four levels: Network (N) – Vulnerabilities with this rating are remotely exploitable, from one or more hops away, up to, and including, remote exploitation over the Internet, Adjacent (A) – A vulnerability with this rating requires network adjacency for exploitation. The attack must be launched from the same physical or logical network, Local (L) – Vulnerabilities with this rating are not exploitable over a network, Physical (P) – An attacker must physically interact with the target system. |
| `web.misconfigs.metrics.cvss_v31.components.availability` | keyword | If an attack renders information unavailable, such as when a system crashes or through a DDoS attack, availability is negatively impacted. Availability has three possible values: None (N) – There is no loss of availability, Low (L) – Availability might be intermittently limited, or performance might be negatively impacted, as a result of a successful attack, High (H) – There is a complete loss of availability of the impacted system or information. |
| `web.misconfigs.metrics.cvss_v31.components.confidentiality` | keyword | Refers to the disclosure of sensitive information to authorized and unauthorized users, with the goal being that only authorized users are able to access the target data. Confidentiality has three potential values: High (H) – The attacker has full access to all resources in the impacted system, including highly sensitive information such as encryption keys, Low (L) – The attacker has partial access to information, with no control over what, specifically, they are able to access, None (N) – No data is accessible to unauthorized users as a result of the exploit. |
| `web.misconfigs.metrics.cvss_v31.score` | double | Score of the vulnerability; 0.1 is the lowest, 10 is the maximum |
| `web.misconfigs.metrics.cvss_v40` | object |  |
| `web.misconfigs.metrics.cvss_v40.components` | object | These metrics contribute to how a CVE is scored. |
| `web.misconfigs.metrics.cvss_v40.components.attack_requirements` | keyword |  |
| `web.misconfigs.metrics.cvss_v40.components.recovery` | keyword |  |
| `web.misconfigs.metrics.cvss_v40.components.privileges_required` | keyword | Describes the level of privileges or access an attacker must have before successful exploitation. There are three possible values: None (N) – There is no privilege or special access required to conduct the attack, Low (L) – The attacker requires basic, “user” level privileges to leverage the exploit, High (H) – Administrative or similar access privileges are required for successful attack. |
| `web.misconfigs.metrics.cvss_v40.components.safety` | keyword |  |
| `web.misconfigs.metrics.cvss_v40.components.availability` | keyword | If an attack renders information unavailable, such as when a system crashes or through a DDoS attack, availability is negatively impacted. Availability has three possible values: None (N) – There is no loss of availability, Low (L) – Availability might be intermittently limited, or performance might be negatively impacted, as a result of a successful attack, High (H) – There is a complete loss of availability of the impacted system or information. |
| `web.misconfigs.metrics.cvss_v40.components.value_density` | keyword |  |
| `web.misconfigs.metrics.cvss_v40.components.attack_complexity` | keyword | Indicates conditions beyond the attacker’s control that must exist in order to exploit the vulnerability. The Attack Complexity metric is scored as either Low or High. There are two possible values: Low (L) – There are no specific pre-conditions required for exploitation, High (H) – The attacker must complete some number of preparatory steps in order to get access. |
| `web.misconfigs.metrics.cvss_v40.components.attack_vector` | keyword | Indicates the level of access required for an attacker to exploit the vulnerability. The Attack Vector metric is scored in one of four levels: Network (N) – Vulnerabilities with this rating are remotely exploitable, from one or more hops away, up to, and including, remote exploitation over the Internet, Adjacent (A) – A vulnerability with this rating requires network adjacency for exploitation. The attack must be launched from the same physical or logical network, Local (L) – Vulnerabilities with this rating are not exploitable over a network, Physical (P) – An attacker must physically interact with the target system. |
| `web.misconfigs.metrics.cvss_v40.components.user_interaction` | keyword | Describes whether a user, other than the attacker, is required to do anything or participate in exploitation of the vulnerability. User interaction has two possible values: None (N) – No user interaction is required, Required (R) – A user must complete some steps for the exploit to succeed. For example, a user might be required to install some software. |
| `web.misconfigs.metrics.cvss_v40.components.vulnerability_response_effort` | keyword |  |
| `web.misconfigs.metrics.cvss_v40.components.automatable` | keyword |  |
| `web.misconfigs.metrics.cvss_v40.components.confidentiality` | keyword | Refers to the disclosure of sensitive information to authorized and unauthorized users, with the goal being that only authorized users are able to access the target data. Confidentiality has three potential values: High (H) – The attacker has full access to all resources in the impacted system, including highly sensitive information such as encryption keys, Low (L) – The attacker has partial access to information, with no control over what, specifically, they are able to access, None (N) – No data is accessible to unauthorized users as a result of the exploit. |
| `web.misconfigs.metrics.cvss_v40.components.integrity` | keyword | Refers to whether the protected information has been tampered with or changed in any way. If there is no way for an attacker to alter the accuracy or completeness of the information, integrity has been maintained. Integrity has three values: None (N) – There is no loss of the integrity of any information, Low (L) – A limited amount of information might be tampered with or modified, but there is no serious impact on the protected system, High (H) – The attacker can modify any/all information on the target system, resulting in a complete loss of integrity. |
| `web.misconfigs.metrics.cvss_v40.components.provider_urgency` | keyword |  |
| `web.misconfigs.metrics.cvss_v40.score` | double | Score of the vulnerability; 0.1 is the lowest, 10 is the maximum |
| `web.misconfigs.metrics.cvss_v40.vector` | text | The path, method, or scenario used to exploit the vulnerability. Each section represents components that contribute to the overall CVSS score. |
| `web.misconfigs.metrics.epss` | object |  |
| `web.misconfigs.metrics.epss.percentile` | double |  |
| `web.misconfigs.metrics.epss.score` | double |  |
| `web.vulns` | nested |  |
| `web.vulns.type` | text |  |
| `web.vulns.year` | unsigned_long |  |
| `web.vulns.severity` | keyword |  |
| `web.vulns.confidence` | double |  |
| `web.vulns.cwes` | object |  |
| `web.vulns.cwes.entry` | text | A unique identifier associated with a class of a software or hardware weakness. |
| `web.vulns.evidence` | nested |  |
| `web.vulns.evidence.literal_match` | text |  |
| `web.vulns.evidence.negative` | boolean |  |
| `web.vulns.evidence.proprietary` | boolean |  |
| `web.vulns.evidence.regex` | text |  |
| `web.vulns.evidence.semver_expression` | text |  |
| `web.vulns.evidence.data_path` | text |  |
| `web.vulns.evidence.exists` | boolean |  |
| `web.vulns.evidence.found_value` | text |  |
| `web.vulns.kev` | object |  |
| `web.vulns.kev.date_added` | date | The date the vulnerability was added to the KEV catalog. |
| `web.vulns.kev.date_due` | date | Per CISA’s Binding Operation Directive 22-01, the date all federal civilian executive branch (FCEB) agencies are required to remediate vulnerabilities in the KEV catalog. |
| `web.vulns.kev.source` | keyword | The source checked to determine whether the CVE is in the KEV catalog. |
| `web.vulns.metrics` | object |  |
| `web.vulns.metrics.epss` | object |  |
| `web.vulns.metrics.epss.score` | double |  |
| `web.vulns.metrics.epss.percentile` | double |  |
| `web.vulns.metrics.cvss_v30` | object |  |
| `web.vulns.metrics.cvss_v30.components` | object | These metrics contribute to how a CVE is scored. |
| `web.vulns.metrics.cvss_v30.components.user_interaction` | keyword | Describes whether a user, other than the attacker, is required to do anything or participate in exploitation of the vulnerability. User interaction has two possible values: None (N) – No user interaction is required, Required (R) – A user must complete some steps for the exploit to succeed. For example, a user might be required to install some software. |
| `web.vulns.metrics.cvss_v30.components.attack_complexity` | keyword | Indicates conditions beyond the attacker’s control that must exist in order to exploit the vulnerability. The Attack Complexity metric is scored as either Low or High. There are two possible values: Low (L) – There are no specific pre-conditions required for exploitation, High (H) – The attacker must complete some number of preparatory steps in order to get access. |
| `web.vulns.metrics.cvss_v30.components.attack_vector` | keyword | Indicates the level of access required for an attacker to exploit the vulnerability. The Attack Vector metric is scored in one of four levels: Network (N) – Vulnerabilities with this rating are remotely exploitable, from one or more hops away, up to, and including, remote exploitation over the Internet, Adjacent (A) – A vulnerability with this rating requires network adjacency for exploitation. The attack must be launched from the same physical or logical network, Local (L) – Vulnerabilities with this rating are not exploitable over a network, Physical (P) – An attacker must physically interact with the target system. |
| `web.vulns.metrics.cvss_v30.components.availability` | keyword | If an attack renders information unavailable, such as when a system crashes or through a DDoS attack, availability is negatively impacted. Availability has three possible values: None (N) – There is no loss of availability, Low (L) – Availability might be intermittently limited, or performance might be negatively impacted, as a result of a successful attack, High (H) – There is a complete loss of availability of the impacted system or information. |
| `web.vulns.metrics.cvss_v30.components.confidentiality` | keyword | Refers to the disclosure of sensitive information to authorized and unauthorized users, with the goal being that only authorized users are able to access the target data. Confidentiality has three potential values: High (H) – The attacker has full access to all resources in the impacted system, including highly sensitive information such as encryption keys, Low (L) – The attacker has partial access to information, with no control over what, specifically, they are able to access, None (N) – No data is accessible to unauthorized users as a result of the exploit. |
| `web.vulns.metrics.cvss_v30.components.integrity` | keyword | Refers to whether the protected information has been tampered with or changed in any way. If there is no way for an attacker to alter the accuracy or completeness of the information, integrity has been maintained. Integrity has three values: None (N) – There is no loss of the integrity of any information, Low (L) – A limited amount of information might be tampered with or modified, but there is no serious impact on the protected system, High (H) – The attacker can modify any/all information on the target system, resulting in a complete loss of integrity. |
| `web.vulns.metrics.cvss_v30.components.privileges_required` | keyword | Describes the level of privileges or access an attacker must have before successful exploitation. There are three possible values: None (N) – There is no privilege or special access required to conduct the attack, Low (L) – The attacker requires basic, “user” level privileges to leverage the exploit, High (H) – Administrative or similar access privileges are required for successful attack. |
| `web.vulns.metrics.cvss_v30.components.scope` | keyword | Determines whether a vulnerability in one system or component can impact another system or component. If a vulnerability in a vulnerable component can affect a component which is in a different security scope than the vulnerable component, a scope change occurs. Scope has two possible ratings: Changed (C) – An exploited vulnerability can have a carry over impact on another system, Unchanged (U) – The exploited vulnerability is limited in damage to only the local security authority. |
| `web.vulns.metrics.cvss_v30.score` | double | Score of the vulnerability; 0.1 is the lowest, 10 is the maximum |
| `web.vulns.metrics.cvss_v30.vector` | text | The path, method, or scenario used to exploit the vulnerability. Each section represents components that contribute to the overall CVSS score. |
| `web.vulns.metrics.cvss_v31` | object |  |
| `web.vulns.metrics.cvss_v31.score` | double | Score of the vulnerability; 0.1 is the lowest, 10 is the maximum |
| `web.vulns.metrics.cvss_v31.vector` | text | The path, method, or scenario used to exploit the vulnerability. Each section represents components that contribute to the overall CVSS score. |
| `web.vulns.metrics.cvss_v31.components` | object | These metrics contribute to how a CVE is scored. |
| `web.vulns.metrics.cvss_v31.components.scope` | keyword | Determines whether a vulnerability in one system or component can impact another system or component. If a vulnerability in a vulnerable component can affect a component which is in a different security scope than the vulnerable component, a scope change occurs. Scope has two possible ratings: Changed (C) – An exploited vulnerability can have a carry over impact on another system, Unchanged (U) – The exploited vulnerability is limited in damage to only the local security authority. |
| `web.vulns.metrics.cvss_v31.components.user_interaction` | keyword | Describes whether a user, other than the attacker, is required to do anything or participate in exploitation of the vulnerability. User interaction has two possible values: None (N) – No user interaction is required, Required (R) – A user must complete some steps for the exploit to succeed. For example, a user might be required to install some software. |
| `web.vulns.metrics.cvss_v31.components.attack_complexity` | keyword | Indicates conditions beyond the attacker’s control that must exist in order to exploit the vulnerability. The Attack Complexity metric is scored as either Low or High. There are two possible values: Low (L) – There are no specific pre-conditions required for exploitation, High (H) – The attacker must complete some number of preparatory steps in order to get access. |
| `web.vulns.metrics.cvss_v31.components.attack_vector` | keyword | Indicates the level of access required for an attacker to exploit the vulnerability. The Attack Vector metric is scored in one of four levels: Network (N) – Vulnerabilities with this rating are remotely exploitable, from one or more hops away, up to, and including, remote exploitation over the Internet, Adjacent (A) – A vulnerability with this rating requires network adjacency for exploitation. The attack must be launched from the same physical or logical network, Local (L) – Vulnerabilities with this rating are not exploitable over a network, Physical (P) – An attacker must physically interact with the target system. |
| `web.vulns.metrics.cvss_v31.components.availability` | keyword | If an attack renders information unavailable, such as when a system crashes or through a DDoS attack, availability is negatively impacted. Availability has three possible values: None (N) – There is no loss of availability, Low (L) – Availability might be intermittently limited, or performance might be negatively impacted, as a result of a successful attack, High (H) – There is a complete loss of availability of the impacted system or information. |
| `web.vulns.metrics.cvss_v31.components.confidentiality` | keyword | Refers to the disclosure of sensitive information to authorized and unauthorized users, with the goal being that only authorized users are able to access the target data. Confidentiality has three potential values: High (H) – The attacker has full access to all resources in the impacted system, including highly sensitive information such as encryption keys, Low (L) – The attacker has partial access to information, with no control over what, specifically, they are able to access, None (N) – No data is accessible to unauthorized users as a result of the exploit. |
| `web.vulns.metrics.cvss_v31.components.integrity` | keyword | Refers to whether the protected information has been tampered with or changed in any way. If there is no way for an attacker to alter the accuracy or completeness of the information, integrity has been maintained. Integrity has three values: None (N) – There is no loss of the integrity of any information, Low (L) – A limited amount of information might be tampered with or modified, but there is no serious impact on the protected system, High (H) – The attacker can modify any/all information on the target system, resulting in a complete loss of integrity. |
| `web.vulns.metrics.cvss_v31.components.privileges_required` | keyword | Describes the level of privileges or access an attacker must have before successful exploitation. There are three possible values: None (N) – There is no privilege or special access required to conduct the attack, Low (L) – The attacker requires basic, “user” level privileges to leverage the exploit, High (H) – Administrative or similar access privileges are required for successful attack. |
| `web.vulns.metrics.cvss_v40` | object |  |
| `web.vulns.metrics.cvss_v40.vector` | text | The path, method, or scenario used to exploit the vulnerability. Each section represents components that contribute to the overall CVSS score. |
| `web.vulns.metrics.cvss_v40.components` | object | These metrics contribute to how a CVE is scored. |
| `web.vulns.metrics.cvss_v40.components.safety` | keyword |  |
| `web.vulns.metrics.cvss_v40.components.user_interaction` | keyword | Describes whether a user, other than the attacker, is required to do anything or participate in exploitation of the vulnerability. User interaction has two possible values: None (N) – No user interaction is required, Required (R) – A user must complete some steps for the exploit to succeed. For example, a user might be required to install some software. |
| `web.vulns.metrics.cvss_v40.components.attack_vector` | keyword | Indicates the level of access required for an attacker to exploit the vulnerability. The Attack Vector metric is scored in one of four levels: Network (N) – Vulnerabilities with this rating are remotely exploitable, from one or more hops away, up to, and including, remote exploitation over the Internet, Adjacent (A) – A vulnerability with this rating requires network adjacency for exploitation. The attack must be launched from the same physical or logical network, Local (L) – Vulnerabilities with this rating are not exploitable over a network, Physical (P) – An attacker must physically interact with the target system. |
| `web.vulns.metrics.cvss_v40.components.automatable` | keyword |  |
| `web.vulns.metrics.cvss_v40.components.availability` | keyword | If an attack renders information unavailable, such as when a system crashes or through a DDoS attack, availability is negatively impacted. Availability has three possible values: None (N) – There is no loss of availability, Low (L) – Availability might be intermittently limited, or performance might be negatively impacted, as a result of a successful attack, High (H) – There is a complete loss of availability of the impacted system or information. |
| `web.vulns.metrics.cvss_v40.components.confidentiality` | keyword | Refers to the disclosure of sensitive information to authorized and unauthorized users, with the goal being that only authorized users are able to access the target data. Confidentiality has three potential values: High (H) – The attacker has full access to all resources in the impacted system, including highly sensitive information such as encryption keys, Low (L) – The attacker has partial access to information, with no control over what, specifically, they are able to access, None (N) – No data is accessible to unauthorized users as a result of the exploit. |
| `web.vulns.metrics.cvss_v40.components.attack_requirements` | keyword |  |
| `web.vulns.metrics.cvss_v40.components.provider_urgency` | keyword |  |
| `web.vulns.metrics.cvss_v40.components.value_density` | keyword |  |
| `web.vulns.metrics.cvss_v40.components.vulnerability_response_effort` | keyword |  |
| `web.vulns.metrics.cvss_v40.components.privileges_required` | keyword | Describes the level of privileges or access an attacker must have before successful exploitation. There are three possible values: None (N) – There is no privilege or special access required to conduct the attack, Low (L) – The attacker requires basic, “user” level privileges to leverage the exploit, High (H) – Administrative or similar access privileges are required for successful attack. |
| `web.vulns.metrics.cvss_v40.components.recovery` | keyword |  |
| `web.vulns.metrics.cvss_v40.components.attack_complexity` | keyword | Indicates conditions beyond the attacker’s control that must exist in order to exploit the vulnerability. The Attack Complexity metric is scored as either Low or High. There are two possible values: Low (L) – There are no specific pre-conditions required for exploitation, High (H) – The attacker must complete some number of preparatory steps in order to get access. |
| `web.vulns.metrics.cvss_v40.components.integrity` | keyword | Refers to whether the protected information has been tampered with or changed in any way. If there is no way for an attacker to alter the accuracy or completeness of the information, integrity has been maintained. Integrity has three values: None (N) – There is no loss of the integrity of any information, Low (L) – A limited amount of information might be tampered with or modified, but there is no serious impact on the protected system, High (H) – The attacker can modify any/all information on the target system, resulting in a complete loss of integrity. |
| `web.vulns.metrics.cvss_v40.score` | double | Score of the vulnerability; 0.1 is the lowest, 10 is the maximum |
| `web.vulns.source` | keyword |  |
| `web.vulns.risk_source` | keyword |  |
| `web.vulns.id` | text |  |
| `web.vulns.name` | text |  |
| `web.endpoints.kubernetes` | object |  |
| `web.endpoints.kubernetes.kubernetes_dashboard_found` | boolean | True if the dashboard is running and accessible |
| `web.endpoints.kubernetes.nodes` | object |  |
| `web.endpoints.kubernetes.nodes.operating_system` | text | The Operating System reported by the node. |
| `web.endpoints.kubernetes.nodes.architecture` | text | The Architecture reported by the node. |
| `web.endpoints.kubernetes.nodes.images` | text | List of container images on this node |
| `web.endpoints.kubernetes.nodes.kube_proxy_version` | text | KubeProxy Version reported by the node. |
| `web.endpoints.kubernetes.nodes.os_image` | text | OS Image reported by the node from /etc/os-release (e.g. Debian GNU/Linux 7 (wheezy)). |
| `web.endpoints.kubernetes.nodes.name` | text |  |
| `web.endpoints.kubernetes.nodes.container_runtime_version` | text | ContainerRuntime Version reported by the node through runtime remote API (e.g. docker://1.5.0). |
| `web.endpoints.kubernetes.nodes.kernel_version` | text | Kernel Version reported by the node from 'uname -r' (e.g. 3.16.0-0.bpo.4-amd64). |
| `web.endpoints.kubernetes.nodes.kubelet_version` | text | Kubelet Version reported by the node. |
| `web.endpoints.kubernetes.nodes.addresses` | object |  |
| `web.endpoints.kubernetes.nodes.addresses.address` | keyword | Node address, IP/URL. |
| `web.endpoints.kubernetes.nodes.addresses.address_type` | text | Node address type, one of Hostname, ExternalIP or InternalIP. |
| `web.endpoints.kubernetes.pod_names` | text |  |
| `web.endpoints.kubernetes.roles` | object |  |
| `web.endpoints.kubernetes.roles.rules` | object | Rules set for this role. |
| `web.endpoints.kubernetes.roles.rules.verbs` | text | Verbs is a list of Verbs that apply to ALL the ResourceKinds and AttributeRestrictions contained in this rule. VerbAll represents all kinds. |
| `web.endpoints.kubernetes.roles.rules.api_groups` | text | APIGroups is the name of the APIGroup that contains the resources. If multiple API groups are specified, any action requested against one of the enumerated resources in any API group will be allowed. |
| `web.endpoints.kubernetes.roles.rules.resources` | text | Resources is a list of resources this rule applies to. ResourceAll represents all resources |
| `web.endpoints.kubernetes.roles.name` | text |  |
| `web.endpoints.kubernetes.version_info` | object |  |
| `web.endpoints.kubernetes.version_info.major` | text | Kubernetes major version |
| `web.endpoints.kubernetes.version_info.git_tree_state` | text | State of the tree when built. |
| `web.endpoints.kubernetes.version_info.minor` | text | Kubernetes minor version |
| `web.endpoints.kubernetes.version_info.platform` | text | Platform compiled for |
| `web.endpoints.kubernetes.version_info.build_date` | text | Date version was built. |
| `web.endpoints.kubernetes.version_info.compiler` | text | Go Compiler used |
| `web.endpoints.kubernetes.version_info.git_commit` | text | Git commit version built from. |
| `web.endpoints.kubernetes.version_info.go_version` | text | Version of GO used to build version. |
| `web.endpoints.kubernetes.version_info.git_version` | text |  |
| `web.endpoints.kubernetes.endpoints` | object |  |
| `web.endpoints.kubernetes.endpoints.subsets` | object |  |
| `web.endpoints.kubernetes.endpoints.subsets.addresses` | object |  |
| `web.endpoints.kubernetes.endpoints.subsets.addresses.ip` | ip |  |
| `web.endpoints.kubernetes.endpoints.subsets.addresses.node_name` | text |  |
| `web.endpoints.kubernetes.endpoints.subsets.addresses.hostname` | text |  |
| `web.endpoints.kubernetes.endpoints.subsets.ports` | object |  |
| `web.endpoints.kubernetes.endpoints.subsets.ports.protocol` | text |  |
| `web.endpoints.kubernetes.endpoints.subsets.ports.name` | text |  |
| `web.endpoints.kubernetes.endpoints.subsets.ports.port` | unsigned_long |  |
| `web.endpoints.kubernetes.endpoints.name` | text |  |
| `web.endpoints.kubernetes.endpoints.self_link` | text |  |
| `web.endpoints.cobalt_strike` | object |  |
| `web.endpoints.cobalt_strike.x64` | object |  |
| `web.endpoints.cobalt_strike.x64.ssl` | boolean |  |
| `web.endpoints.cobalt_strike.x64.jitter` | unsigned_long |  |
| `web.endpoints.cobalt_strike.x64.host_header` | text |  |
| `web.endpoints.cobalt_strike.x64.dns` | boolean |  |
| `web.endpoints.cobalt_strike.x64.crypto_scheme` | unsigned_long |  |
| `web.endpoints.cobalt_strike.x64.killdate` | unsigned_long |  |
| `web.endpoints.cobalt_strike.x64.public_key` | text |  |
| `web.endpoints.cobalt_strike.x64.unknown_bytes` | object |  |
| `web.endpoints.cobalt_strike.x64.unknown_bytes.key` | unsigned_long |  |
| `web.endpoints.cobalt_strike.x64.unknown_bytes.value` | text |  |
| `web.endpoints.cobalt_strike.x64.watermark` | unsigned_long |  |
| `web.endpoints.cobalt_strike.x64.user_agent` | text |  |
| `web.endpoints.cobalt_strike.x64.http_post` | object |  |
| `web.endpoints.cobalt_strike.x64.http_post.verb` | text |  |
| `web.endpoints.cobalt_strike.x64.http_post.client` | text |  |
| `web.endpoints.cobalt_strike.x64.http_post.uri` | text |  |
| `web.endpoints.cobalt_strike.x64.post_ex` | object |  |
| `web.endpoints.cobalt_strike.x64.post_ex.x64` | text |  |
| `web.endpoints.cobalt_strike.x64.post_ex.x86` | text |  |
| `web.endpoints.cobalt_strike.x64.cookie_beacon` | unsigned_long |  |
| `web.endpoints.cobalt_strike.x64.http_get` | object |  |
| `web.endpoints.cobalt_strike.x64.http_get.client` | text |  |
| `web.endpoints.cobalt_strike.x64.http_get.uri` | text |  |
| `web.endpoints.cobalt_strike.x64.http_get.verb` | text |  |
| `web.endpoints.cobalt_strike.x64.sleep_time` | unsigned_long |  |
| `web.endpoints.cobalt_strike.x64.unknown_int` | object |  |
| `web.endpoints.cobalt_strike.x64.unknown_int.value` | unsigned_long |  |
| `web.endpoints.cobalt_strike.x64.unknown_int.key` | unsigned_long |  |
| `web.endpoints.cobalt_strike.x86` | object |  |
| `web.endpoints.cobalt_strike.x86.dns` | boolean |  |
| `web.endpoints.cobalt_strike.x86.unknown_int` | object |  |
| `web.endpoints.cobalt_strike.x86.unknown_int.key` | unsigned_long |  |
| `web.endpoints.cobalt_strike.x86.unknown_int.value` | unsigned_long |  |
| `web.endpoints.cobalt_strike.x86.killdate` | unsigned_long |  |
| `web.endpoints.cobalt_strike.x86.crypto_scheme` | unsigned_long |  |
| `web.endpoints.cobalt_strike.x86.http_get` | object |  |
| `web.endpoints.cobalt_strike.x86.http_get.verb` | text |  |
| `web.endpoints.cobalt_strike.x86.http_get.client` | text |  |
| `web.endpoints.cobalt_strike.x86.http_get.uri` | text |  |
| `web.endpoints.cobalt_strike.x86.ssl` | boolean |  |
| `web.endpoints.cobalt_strike.x86.user_agent` | text |  |
| `web.endpoints.cobalt_strike.x86.unknown_bytes` | object |  |
| `web.endpoints.cobalt_strike.x86.unknown_bytes.value` | text |  |
| `web.endpoints.cobalt_strike.x86.unknown_bytes.key` | unsigned_long |  |
| `web.endpoints.cobalt_strike.x86.cookie_beacon` | unsigned_long |  |
| `web.endpoints.cobalt_strike.x86.post_ex` | object |  |
| `web.endpoints.cobalt_strike.x86.post_ex.x64` | text |  |
| `web.endpoints.cobalt_strike.x86.post_ex.x86` | text |  |
| `web.endpoints.cobalt_strike.x86.host_header` | text |  |
| `web.endpoints.cobalt_strike.x86.watermark` | unsigned_long |  |
| `web.endpoints.cobalt_strike.x86.jitter` | unsigned_long |  |
| `web.endpoints.cobalt_strike.x86.public_key` | text |  |
| `web.endpoints.cobalt_strike.x86.http_post` | object |  |
| `web.endpoints.cobalt_strike.x86.http_post.client` | text |  |
| `web.endpoints.cobalt_strike.x86.http_post.uri` | text |  |
| `web.endpoints.cobalt_strike.x86.http_post.verb` | text |  |
| `web.endpoints.cobalt_strike.x86.sleep_time` | unsigned_long |  |
| `web.endpoints.prometheus` | object |  |
| `web.endpoints.prometheus.response` | object | Information Prometheus captured as well as build information. |
| `web.endpoints.prometheus.response.all_versions` | text | List of the versions of everything that Prometheus finds i.e., version of Prometheus, Go, Node, cAdvisor, etc. |
| `web.endpoints.prometheus.response.config_exposed` | boolean | True when the config endpoint is exposed. |
| `web.endpoints.prometheus.response.dropped_targets` | object | List of dropped targets. |
| `web.endpoints.prometheus.response.dropped_targets.metrics_path` | text | Path to metrics of target. |
| `web.endpoints.prometheus.response.dropped_targets.scheme` | text | URL scheme. |
| `web.endpoints.prometheus.response.dropped_targets.address` | text | Address of target. |
| `web.endpoints.prometheus.response.dropped_targets.job` | text | Job of target. |
| `web.endpoints.prometheus.response.go_versions` | text | List of the versions of Go. |
| `web.endpoints.prometheus.response.prometheus_versions` | object |  |
| `web.endpoints.prometheus.response.prometheus_versions.revision` | text | Revision of Prometheus. |
| `web.endpoints.prometheus.response.prometheus_versions.version` | text | Version of Prometheus. |
| `web.endpoints.prometheus.response.prometheus_versions.go_version` | text | Version of Go used to build Prometheus. |
| `web.endpoints.prometheus.response.active_targets` | object | List of active targets. |
| `web.endpoints.prometheus.response.active_targets.scrape_url` | text | URL that Prometheus scraped. |
| `web.endpoints.prometheus.response.active_targets.discovered_labels` | object |  |
| `web.endpoints.prometheus.response.active_targets.discovered_labels.metrics_path` | text | Path to metrics of target. |
| `web.endpoints.prometheus.response.active_targets.discovered_labels.scheme` | text | URL scheme. |
| `web.endpoints.prometheus.response.active_targets.discovered_labels.address` | text | Address of target. |
| `web.endpoints.prometheus.response.active_targets.discovered_labels.job` | text | Job of target. |
| `web.endpoints.prometheus.response.active_targets.health` | text | Whether target is up or down. |
| `web.endpoints.prometheus.response.active_targets.labels` | object |  |
| `web.endpoints.prometheus.response.active_targets.labels.instance` | text | Instance after relabelling has occurred. |
| `web.endpoints.prometheus.response.active_targets.labels.job` | text | Job of target after relabelling has occurred. |
| `web.endpoints.prometheus.response.active_targets.last_error` | text | Last error that occurred within target. |
| `web.endpoints.prometheus.response.active_targets.last_scrape` | text | Last time Prometheus scraped target. |
| `web.endpoints.elasticsearch` | object |  |
| `web.endpoints.elasticsearch.error_message` | object |  |
| `web.endpoints.elasticsearch.error_message.type` | text |  |
| `web.endpoints.elasticsearch.error_message.header` | text |  |
| `web.endpoints.elasticsearch.error_message.reason` | text |  |
| `web.endpoints.elasticsearch.results_node_info` | object |  |
| `web.endpoints.elasticsearch.results_node_info.cluster_combined_info` | object |  |
| `web.endpoints.elasticsearch.results_node_info.cluster_combined_info.status` | text |  |
| `web.endpoints.elasticsearch.results_node_info.cluster_combined_info.timestamp` | unsigned_long |  |
| `web.endpoints.elasticsearch.results_node_info.cluster_combined_info.uuid` | text |  |
| `web.endpoints.elasticsearch.results_node_info.cluster_combined_info.filesystem` | object |  |
| `web.endpoints.elasticsearch.results_node_info.cluster_combined_info.filesystem.available_in_bytes` | unsigned_long |  |
| `web.endpoints.elasticsearch.results_node_info.cluster_combined_info.filesystem.free` | text |  |
| `web.endpoints.elasticsearch.results_node_info.cluster_combined_info.filesystem.free_in_bytes` | unsigned_long |  |
| `web.endpoints.elasticsearch.results_node_info.cluster_combined_info.filesystem.total` | text |  |
| `web.endpoints.elasticsearch.results_node_info.cluster_combined_info.filesystem.total_in_bytes` | unsigned_long |  |
| `web.endpoints.elasticsearch.results_node_info.cluster_combined_info.filesystem.available` | text |  |
| `web.endpoints.elasticsearch.results_node_info.cluster_combined_info.indices` | object |  |
| `web.endpoints.elasticsearch.results_node_info.cluster_combined_info.indices.count` | unsigned_long |  |
| `web.endpoints.elasticsearch.results_node_info.cluster_combined_info.indices.docs` | object |  |
| `web.endpoints.elasticsearch.results_node_info.cluster_combined_info.indices.docs.deleted` | unsigned_long |  |
| `web.endpoints.elasticsearch.results_node_info.cluster_combined_info.indices.docs.count` | unsigned_long |  |
| `web.endpoints.elasticsearch.results_node_info.cluster_combined_info.indices.store` | object |  |
| `web.endpoints.elasticsearch.results_node_info.cluster_combined_info.indices.store.reserved_in_bytes` | unsigned_long |  |
| `web.endpoints.elasticsearch.results_node_info.cluster_combined_info.indices.store.size_in_bytes` | unsigned_long |  |
| `web.endpoints.elasticsearch.results_node_info.cluster_combined_info.name` | text |  |
| `web.endpoints.elasticsearch.results_node_info.node_info` | object |  |
| `web.endpoints.elasticsearch.results_node_info.node_info.node_name` | text |  |
| `web.endpoints.elasticsearch.results_node_info.node_info.node_data` | object |  |
| `web.endpoints.elasticsearch.results_node_info.node_info.node_data.jvm` | object |  |
| `web.endpoints.elasticsearch.results_node_info.node_info.node_data.jvm.start_time` | text |  |
| `web.endpoints.elasticsearch.results_node_info.node_info.node_data.jvm.start_time_ms` | unsigned_long |  |
| `web.endpoints.elasticsearch.results_node_info.node_info.node_data.jvm.vm_version` | text |  |
| `web.endpoints.elasticsearch.results_node_info.node_info.node_data.jvm.input_args` | text |  |
| `web.endpoints.elasticsearch.results_node_info.node_info.node_data.jvm.gc` | text |  |
| `web.endpoints.elasticsearch.results_node_info.node_info.node_data.jvm.version` | text |  |
| `web.endpoints.elasticsearch.results_node_info.node_info.node_data.jvm.vm_vendor` | text |  |
| `web.endpoints.elasticsearch.results_node_info.node_info.node_data.jvm.memory_pools` | text |  |
| `web.endpoints.elasticsearch.results_node_info.node_info.node_data.jvm.vm_name` | text |  |
| `web.endpoints.elasticsearch.results_node_info.node_info.node_data.build_flavor` | text |  |
| `web.endpoints.elasticsearch.results_node_info.node_info.node_data.total_indexing_buffer` | unsigned_long |  |
| `web.endpoints.elasticsearch.results_node_info.node_info.node_data.build_type` | text |  |
| `web.endpoints.elasticsearch.results_node_info.node_info.node_data.os` | object |  |
| `web.endpoints.elasticsearch.results_node_info.node_info.node_data.os.allocated_proc` | integer |  |
| `web.endpoints.elasticsearch.results_node_info.node_info.node_data.os.arch` | text |  |
| `web.endpoints.elasticsearch.results_node_info.node_info.node_data.os.available_proc` | integer |  |
| `web.endpoints.elasticsearch.results_node_info.node_info.node_data.os.name` | text |  |
| `web.endpoints.elasticsearch.results_node_info.node_info.node_data.os.pretty_name` | text |  |
| `web.endpoints.elasticsearch.results_node_info.node_info.node_data.os.refresh_interval_ms` | unsigned_long |  |
| `web.endpoints.elasticsearch.results_node_info.node_info.node_data.os.version` | text |  |
| `web.endpoints.elasticsearch.results_node_info.node_info.node_data.build_hash` | text |  |
| `web.endpoints.elasticsearch.results_node_info.node_info.node_data.roles` | text |  |
| `web.endpoints.elasticsearch.results_node_info.node_info.node_data.settings` | object |  |
| `web.endpoints.elasticsearch.results_node_info.node_info.node_data.settings.cluster_name` | text |  |
| `web.endpoints.elasticsearch.results_node_info.node_info.node_data.settings.node` | object |  |
| `web.endpoints.elasticsearch.results_node_info.node_info.node_data.settings.node.name` | text |  |
| `web.endpoints.elasticsearch.results_node_info.node_info.node_data.settings.node.attr` | object |  |
| `web.endpoints.elasticsearch.results_node_info.node_info.node_data.settings.node.attr.xpack_installed` | text |  |
| `web.endpoints.elasticsearch.results_node_info.node_info.node_data.settings.node.attr.ml` | object |  |
| `web.endpoints.elasticsearch.results_node_info.node_info.node_data.settings.node.attr.ml.max_open_jobs` | text |  |
| `web.endpoints.elasticsearch.results_node_info.node_info.node_data.settings.node.attr.ml.enabled` | text |  |
| `web.endpoints.elasticsearch.results_node_info.node_info.node_data.settings.node.attr.ml.machine_memory` | text |  |
| `web.endpoints.elasticsearch.results_node_info.node_info.node_data.ip` | text |  |
| `web.endpoints.elasticsearch.results_node_info.node_info.node_data.thread_pool_list` | object |  |
| `web.endpoints.elasticsearch.results_node_info.node_info.node_data.thread_pool_list.max` | integer |  |
| `web.endpoints.elasticsearch.results_node_info.node_info.node_data.thread_pool_list.min` | integer |  |
| `web.endpoints.elasticsearch.results_node_info.node_info.node_data.thread_pool_list.queue_size` | integer |  |
| `web.endpoints.elasticsearch.results_node_info.node_info.node_data.thread_pool_list.type` | text |  |
| `web.endpoints.elasticsearch.results_node_info.node_info.node_data.thread_pool_list.keep_alive` | text |  |
| `web.endpoints.elasticsearch.results_node_info.node_info.node_data.modules` | object |  |
| `web.endpoints.elasticsearch.results_node_info.node_info.node_data.modules.desc` | text |  |
| `web.endpoints.elasticsearch.results_node_info.node_info.node_data.modules.elastic_version` | text |  |
| `web.endpoints.elasticsearch.results_node_info.node_info.node_data.modules.ext_plugins` | text |  |
| `web.endpoints.elasticsearch.results_node_info.node_info.node_data.modules.has_native_ctrl` | boolean |  |
| `web.endpoints.elasticsearch.results_node_info.node_info.node_data.modules.java_version` | text |  |
| `web.endpoints.elasticsearch.results_node_info.node_info.node_data.modules.name` | text |  |
| `web.endpoints.elasticsearch.results_node_info.node_info.node_data.modules.version` | text |  |
| `web.endpoints.elasticsearch.results_node_info.node_info.node_data.modules.class_name` | text |  |
| `web.endpoints.elasticsearch.results_node_info.node_info.node_data.host` | text |  |
| `web.endpoints.elasticsearch.results_node_info.node_info.node_data.name` | text |  |
| `web.endpoints.elasticsearch.results_node_info.node_info.node_data.version` | text |  |
| `web.endpoints.elasticsearch.results_node_info.node_info.node_data.ingest_processors` | text |  |
| `web.endpoints.elasticsearch.results_node_info.node_info.node_data.ip_raw` | text |  |
| `web.endpoints.elasticsearch.system_info` | object |  |
| `web.endpoints.elasticsearch.system_info.name` | text |  |
| `web.endpoints.elasticsearch.system_info.tagline` | text |  |
| `web.endpoints.elasticsearch.system_info.version` | object |  |
| `web.endpoints.elasticsearch.system_info.version.min_wire_compat_ver` | text |  |
| `web.endpoints.elasticsearch.system_info.version.number` | text |  |
| `web.endpoints.elasticsearch.system_info.version.build_flavor` | text |  |
| `web.endpoints.elasticsearch.system_info.version.build_snapshot` | boolean |  |
| `web.endpoints.elasticsearch.system_info.version.build_type` | text |  |
| `web.endpoints.elasticsearch.system_info.version.min_idx_compat_ver` | text |  |
| `web.endpoints.elasticsearch.system_info.version.build_date` | text |  |
| `web.endpoints.elasticsearch.system_info.version.build_hash` | text |  |
| `web.endpoints.elasticsearch.system_info.version.lucene_version` | text |  |
| `web.endpoints.elasticsearch.system_info.cluster_uuid` | text |  |
| `web.endpoints.http` | object |  |
| `web.endpoints.http.status_reason` | text | A human-readable phrase describing the status code. |
| `web.endpoints.http.html_tags` | text | A list of the <title> and <meta> tags from services.http.response.body. |
| `web.endpoints.http.redirect_chain` | nested | If the scan redirects, the list of followup scans performed |
| `web.endpoints.http.redirect_chain.hostname` | text |  |
| `web.endpoints.http.redirect_chain.http_status` | object | The HTTP status code and reason of the redirecting response. |
| `web.endpoints.http.redirect_chain.http_status.code` | integer | A 3-digit integer result code indicating the result of the redirecting response. |
| `web.endpoints.http.redirect_chain.http_status.reason` | text | A human-readable phrase describing the status code. |
| `web.endpoints.http.redirect_chain.path` | text |  |
| `web.endpoints.http.redirect_chain.port` | unsigned_long |  |
| `web.endpoints.http.redirect_chain.reason` | text |  |
| `web.endpoints.http.redirect_chain.scheme` | text |  |
| `web.endpoints.http.redirect_chain.transport_protocol` | keyword |  |
| `web.endpoints.http.uri` | text | The full path used to make the request, which includes the scheme, host, port (when non-standard), and endpoint. |
| `web.endpoints.http.network_log` | object | List of all resources fetched when visiting this page as browser |
| `web.endpoints.http.network_log.har_handle` | text | Storage handle for the full HAR network log. |
| `web.endpoints.http.network_log.resources` | nested | Resources fetched during page load. |
| `web.endpoints.http.network_log.resources.scheme` | text | URL scheme (e.g., http, https). |
| `web.endpoints.http.network_log.resources.path` | text | Path from the URL. |
| `web.endpoints.http.network_log.resources.sha256` | text | SHA-256 hash of the resource content. |
| `web.endpoints.http.network_log.resources.url` | text | Full URL of the resource. |
| `web.endpoints.http.network_log.resources.mime_type` | text | MIME type of the resource. |
| `web.endpoints.http.network_log.resources.sha1` | text | SHA-1 hash of the resource content. |
| `web.endpoints.http.network_log.resources.host` | text | Hostname from the URL. |
| `web.endpoints.http.network_log.resources.md5` | text | MD5 hash of the resource content. |
| `web.endpoints.http.network_log.resources.port` | text | Port from the URL. |
| `web.endpoints.http.network_log.resources.size` | integer | Size of the resource in bytes. |
| `web.endpoints.http.status_code` | integer | A 3-digit integer result code indicating the result of the services.http.request. |
| `web.endpoints.http.headers` | nested | The key-value header pairs included in the response. |
| `web.endpoints.http.headers.value` | text | The values provided in the corresponding header. |
| `web.endpoints.http.headers.key` | text |  |
| `web.endpoints.http.body_hash_sha256` | text |  |
| `web.endpoints.http.html_title` | text | The title of the HTML page: the inner contents of the <title> tag in the response body, if present. |
| `web.endpoints.http.body_hash_sha1` | text |  |
| `web.endpoints.http.supported_versions` | text |  |
| `web.endpoints.http.body` | text | The body of the HTTP response. For hosts without a name, the first 64KB are available. For hosts with a name, only 6KB are available. |
| `web.endpoints.http.protocol` | text | The protocol field of the response, which includes the claimed HTTP version number. |
| `web.endpoints.http.body_size` | integer | The length, in bytes, of services.http.response.body; at most, 64KB. |
| `web.endpoints.http.body_hash_tlsh` | text |  |
| `web.endpoints.http.favicons` | object |  |
| `web.endpoints.http.favicons.hash_md5` | text |  |
| `web.endpoints.http.favicons.hash_phash` | text | A 64-bit 'perceptual' hash of the favicon |
| `web.endpoints.http.favicons.hash_sha256` | text |  |
| `web.endpoints.http.favicons.hash_shodan` | integer | A hash expressed as a signed decimal integer, provided for compatability with Shodan search. |
| `web.endpoints.http.favicons.name` | text | The URI used to retrieve the favicon, which most commonly use the http(s) or data schemes. URIs using the data scheme are truncated: the first 48 and last 24 characters are preserved. |
| `web.endpoints.http.favicons.size` | integer | The size of the favicon retrieved, in bytes. |
| `web.tls` | object |  |
| `web.tls.versions` | object |  |
| `web.tls.versions.ja4s` | text |  |
| `web.tls.versions.version` | keyword |  |
| `web.tls.versions.ja3s` | text |  |
| `web.tls.cipher_selected` | text | Cipher suite chosen for the exchange. |
| `web.tls.fingerprint_sha256` | text | The SHA-256 digest of the entire raw certificate. Its unique identifier, which Censys uses to index certificates records. |
| `web.tls.ja3s` | text | The JA3S fingerprint for this service. |
| `web.tls.ja4s` | text |  |
| `web.tls.presented_chain` | object | Certificate chain information. |
| `web.tls.presented_chain.subject_dn` | text | Distinguished name of the entity that the certificate belongs to. |
| `web.tls.presented_chain.fingerprint_sha256` | text | SHA 256 fingerprint of the certificate in the certificate chain. |
| `web.tls.presented_chain.issuer_dn` | text | Distinguished name of the entity that has signed and issued the certificate. |
| `web.tls.version_selected` | keyword | Certificate version v1(0), v2(1), v3(2). |
