# Censys Platform Queryable Fields

Parsed from `Certificate Censys Data Definitions.html` (in-app data definitions, <https://platform.censys.io/home/definitions>).

**Total fields: 427**

| Dataset | Field count |
| --- | --- |
| `cert` | 427 |

## cert (427 fields)

| Field | Type | Description |
| --- | --- | --- |
| `cert` | object |  |
| `cert.parsed` | object | A record containing all of the data parsed from the certificate. |
| `cert.parsed.extensions` | object | A record containing parsed X.509 extensions that provide additional identification information or additional cryptographic capabilities. |
| `cert.parsed.extensions.ct_poison` | boolean | Whether the certificate possesses the pre-certificate "poison" extension (OID: 1.3.6.1.4.1.11129.2.4.3). |
| `cert.parsed.subject_key_info` | object | Information about the certificate's public key. |
| `cert.parsed.subject_key_info.fingerprint_sha256` | text | The SHA-256 digest of the certificate's DER-encoded SubjectPublicKeyInfo. |
| `cert.parsed.subject_key_info.key_algorithm` | object | A record containing information about the type of subject key algorithm and any relevant parameters. |
| `cert.parsed.subject_key_info.key_algorithm.name` | text | Name of public key type, such as RSA or ECDSA. Information specific to the key type is available in the named sub-record. |
| `cert.parsed.subject_key_info.key_algorithm.oid` | text |  |
| `cert.parsed.subject_key_info.rsa` | object | A record containing the public portion of an RSA asymmetric key. |
| `cert.parsed.subject_key_info.rsa.exponent` | long | The RSA key's public exponent (e). |
| `cert.parsed.subject_key_info.rsa.length` | long | Bit-length of the RSA modulus. |
| `cert.parsed.subject_key_info.rsa.modulus` | text | The RSA key's modulus (n) in big-endian encoding. |
| `cert.parsed.subject_key_info.unrecognized` | object | A record containing known information about an unrecognized key type. |
| `cert.parsed.subject_key_info.unrecognized.raw` | text |  |
| `cert.parsed.subject_key_info.dsa` | object | A record containing the public portion of a DSA asymmetric key. |
| `cert.parsed.subject_key_info.dsa.q` | text |  |
| `cert.parsed.subject_key_info.dsa.y` | text |  |
| `cert.parsed.subject_key_info.dsa.g` | text |  |
| `cert.parsed.subject_key_info.dsa.p` | text |  |
| `cert.parsed.subject_key_info.ecdsa` | object | A record containing the public portion of an ECDSA asymmetric key. |
| `cert.parsed.subject_key_info.ecdsa.p` | text |  |
| `cert.parsed.subject_key_info.ecdsa.y` | text |  |
| `cert.parsed.subject_key_info.ecdsa.x` | text |  |
| `cert.parsed.subject_key_info.ecdsa.b` | text |  |
| `cert.parsed.subject_key_info.ecdsa.n` | text |  |
| `cert.parsed.subject_key_info.ecdsa.curve` | text |  |
| `cert.parsed.subject_key_info.ecdsa.gx` | text |  |
| `cert.parsed.subject_key_info.ecdsa.gy` | text |  |
| `cert.parsed.subject_key_info.ecdsa.pub` | text |  |
| `cert.parsed.subject_key_info.ecdsa.length` | long |  |
| `cert.validation` | object | A record containing information from the maintainers of major root certificate stores related to their trust assessment. |
| `cert.revocation` | object | A record containing revocation information, if the certificate has been revoked. |
| `cert.ct` | object |  |
| `cert.names` | text | All the names contained in the certificate from various fields. |
| `cert.tags` | object |  |
| `cert.tags.id` | keyword |  |
| `cert.tags.name` | keyword |  |
| `cert.parsed.serial_number` | text | Issuer-specific identifier of the certificate. |
| `cert.parsed.issuer_dn` | text | Distinguished Name of the entity that has signed and issued the certificate. |
| `cert.fingerprint_md5` | text | The MD-5 digest of the entire raw certificate. An identifier used by some systems. |
| `cert.tbs_fingerprint_sha256` | text | The SHA-256 digest of the unsigned certificate's contents. |
| `cert.tbs_no_ct_fingerprint_sha256` | text | The SHA-256 digest of the unsigned certificate with the CT Poison extension removed, if present. This represents the shared contents of a certificate and its corresponding pre-certificate. |
| `cert.fingerprint_sha1` | text | The SHA-1 digest of the entire raw certificate. An identifier used by some systems. |
| `cert.fingerprint_sha256` | text | The SHA-256 digest of the entire raw certificate. Its unique identifier, which Censys uses to index certificates records. |
| `cert.parsed.ja4x` | text |  |
| `cert.modified_at` | date | When the certificate record was last modified. |
| `cert.added_at` | date | When the certificate was added to the Censys dataset. |
| `cert.labels` | text |  |
| `cert.parse_status` | text |  |
| `cert.parsed.validity_period` | object | Information about the time for which the certificate is valid. |
| `cert.parsed.validity_period.not_after` | date | An RFC-3339-formatted timestamp after which the certificate is no longer valid. |
| `cert.parsed.validity_period.not_before` | date | An RFC-3339-formatted timestamp before which the certificate is not valid. |
| `cert.parsed.validity_period.length_seconds` | long | The duration of the certificate's validity period, in seconds. |
| `cert.parsed.serial_number_hex` | text | Issuer-specific identifier of the certificate, represented as hexadecimal. |
| `cert.parsed.subject_dn` | text | Distinguished Name of the entity associated with the public key. |
| `cert.validated_at` | date | When the certificate record's trust was last checked. |
| `cert.parsed.issuer` | object | A record containing the parsed contents of the issuer_dn. |
| `cert.parsed.issuer.jurisdiction_province` | text | The jurisdictionStateOrProvince elements of the Distinguished Name (OID: 1.3.6.1.4.1.311.60.2.1.2). |
| `cert.parsed.issuer.province` | text | The stateOrProvinceName (ST) elements of the Distinguished Name (OID: 2.5.4.8). |
| `cert.parsed.issuer.jurisdiction_locality` | text | The jurisdictionLocality elements of the Distinguished Name (OID: 1.3.6.1.4.1.311.60.2.1.1). |
| `cert.parsed.issuer.country` | text | The countryName (C) elements of the Distinguished Name (OID: 2.5.4.6). |
| `cert.parsed.issuer.locality` | text | The localityName (L) elements of the Distinguished Name (OID: 2.5.4.7). |
| `cert.parsed.issuer.serial_number` | keyword | The serialNumber elements of the Distinguished Name (OID: 2.5.4.5). |
| `cert.parsed.issuer.domain_component` | text | The domainComponent (DC) elements of the Distinguished Name (OID: 0.9.2342.19200300.100.1.25). |
| `cert.parsed.issuer.organization` | text | The organizationName (O) elements of the Distinguished Name (OID: 2.5.4.10). |
| `cert.parsed.issuer.email_address` | text | The emailAddress (E) elements of the Distinguished Name (OID: 1.2.840.113549.1.9.1). |
| `cert.parsed.issuer.organization_id` | text |  |
| `cert.parsed.issuer.street_address` | text | The streetAddress (STREET) elements of the Distinguished Name (OID: 2.5.4.9). |
| `cert.parsed.issuer.common_name` | text | The commonName (CN) elements of the Distinguished Name (OID: 2.5.4.3). |
| `cert.parsed.issuer.postal_code` | keyword | The postalCode elements of the Distinguished Name (OID: 2.5.4.17). |
| `cert.parsed.issuer.jurisdiction_country` | text | The jurisdictionCountry elements of the Distinguished Name (OID: 1.3.6.1.4.1.311.60.2.1.3). |
| `cert.parsed.issuer.surname` | text | The surname (SN) elements of the Distinguished Name (OID: 2.5.4.4). |
| `cert.parsed.issuer.given_name` | text | The givenName (G) elements of the Distinguished Name (OID: 2.5.4.42). |
| `cert.parsed.issuer.organizational_unit` | text | The organizationalUnit (OU) elements of the Distinguished Name (OID: 2.5.4.11). |
| `cert.parsed.signature` | object |  |
| `cert.parsed.signature.value` | text | Contents of the signature. |
| `cert.parsed.signature.self_signed` | boolean | Whether the certificate was signed by its own key. |
| `cert.parsed.signature.signature_algorithm` | object |  |
| `cert.parsed.signature.signature_algorithm.name` | text | Name of public key type, such as RSA or ECDSA. Information specific to the key type is available in the named sub-record. |
| `cert.parsed.signature.signature_algorithm.oid` | text |  |
| `cert.parsed.signature.valid` | boolean | Whether the signature is valid. |
| `cert.parsed.subject` | object | A record containing the parsed contents of the subject_dn. |
| `cert.parsed.subject.given_name` | text | The givenName (G) elements of the Distinguished Name (OID: 2.5.4.42). |
| `cert.parsed.subject.organization_id` | text |  |
| `cert.parsed.subject.common_name` | text | The commonName (CN) elements of the Distinguished Name (OID: 2.5.4.3). |
| `cert.parsed.subject.jurisdiction_country` | text | The jurisdictionCountry elements of the Distinguished Name (OID: 1.3.6.1.4.1.311.60.2.1.3). |
| `cert.parsed.subject.province` | text | The stateOrProvinceName (ST) elements of the Distinguished Name (OID: 2.5.4.8). |
| `cert.parsed.subject.organizational_unit` | text | The organizationalUnit (OU) elements of the Distinguished Name (OID: 2.5.4.11). |
| `cert.parsed.subject.serial_number` | keyword | The serialNumber elements of the Distinguished Name (OID: 2.5.4.5). |
| `cert.parsed.subject.jurisdiction_province` | text | The jurisdictionStateOrProvince elements of the Distinguished Name (OID: 1.3.6.1.4.1.311.60.2.1.2). |
| `cert.parsed.subject.postal_code` | keyword | The postalCode elements of the Distinguished Name (OID: 2.5.4.17). |
| `cert.parsed.subject.country` | text | The countryName (C) elements of the Distinguished Name (OID: 2.5.4.6). |
| `cert.parsed.subject.email_address` | text | The emailAddress (E) elements of the Distinguished Name (OID: 1.2.840.113549.1.9.1). |
| `cert.parsed.subject.street_address` | text | The streetAddress (STREET) elements of the Distinguished Name (OID: 2.5.4.9). |
| `cert.parsed.subject.jurisdiction_locality` | text | The jurisdictionLocality elements of the Distinguished Name (OID: 1.3.6.1.4.1.311.60.2.1.1). |
| `cert.parsed.subject.organization` | text | The organizationName (O) elements of the Distinguished Name (OID: 2.5.4.10). |
| `cert.parsed.subject.locality` | text | The localityName (L) elements of the Distinguished Name (OID: 2.5.4.7). |
| `cert.parsed.subject.domain_component` | text | The domainComponent (DC) elements of the Distinguished Name (OID: 0.9.2342.19200300.100.1.25). |
| `cert.parsed.subject.surname` | text | The surname (SN) elements of the Distinguished Name (OID: 2.5.4.4). |
| `cert.parsed.unknown_extensions` | nested |  |
| `cert.parsed.unknown_extensions.critical` | boolean |  |
| `cert.parsed.unknown_extensions.id` | text |  |
| `cert.parsed.unknown_extensions.value` | text |  |
| `cert.parsed.extensions.name_constraints` | object | The parsed id-ce-nameConstraints extension (OID: 2.5.29.30). Specifies a name space within which all child certificates' subject names MUST be located. |
| `cert.parsed.extensions.name_constraints.permitted_registered_ids` | text | A record providing permitted names of the type registeredID in leaf certificates whose trust path includes this certificate. |
| `cert.parsed.extensions.name_constraints.permitted_edi_party_names` | nested | A record providing permitted names of the type ediPartyName in leaf certificates whose trust path includes this certificate. |
| `cert.parsed.extensions.name_constraints.permitted_edi_party_names.name_assigner` | text |  |
| `cert.parsed.extensions.name_constraints.permitted_edi_party_names.party_name` | text |  |
| `cert.parsed.extensions.name_constraints.permitted_ip_addresses` | nested | A record providing a range of permitted names of the type iPAddress in leaf certificates whose trust path includes this certificate. |
| `cert.parsed.extensions.name_constraints.permitted_ip_addresses.mask` | text | The subnet mask of the CIDR. |
| `cert.parsed.extensions.name_constraints.permitted_ip_addresses.begin` | text | The first IP address in the range. |
| `cert.parsed.extensions.name_constraints.permitted_ip_addresses.cidr` | text | The CIDR specifying the subtree. |
| `cert.parsed.extensions.name_constraints.permitted_ip_addresses.end` | text | The last IP address in the range. |
| `cert.parsed.extensions.name_constraints.permitted_email_addresses` | text | A record providing a range of permitted names of the type rfc822Name in leaf certificates whose trust path includes this certificate. |
| `cert.parsed.extensions.name_constraints.critical` | boolean |  |
| `cert.parsed.extensions.name_constraints.excluded_ip_addresses` | nested | A record providing a range of excluded names of the type iPAddress in leaf certificates whose trust path includes this certificate. |
| `cert.parsed.extensions.name_constraints.excluded_ip_addresses.begin` | text | The first IP address in the range. |
| `cert.parsed.extensions.name_constraints.excluded_ip_addresses.cidr` | text | The CIDR specifying the subtree. |
| `cert.parsed.extensions.name_constraints.excluded_ip_addresses.end` | text | The last IP address in the range. |
| `cert.parsed.extensions.name_constraints.excluded_ip_addresses.mask` | text | The subnet mask of the CIDR. |
| `cert.parsed.extensions.name_constraints.permitted_uris` | text | A record providing a range of permitted uniform resource identifiers in leaf certificates whose trust path includes this certificate. |
| `cert.parsed.extensions.name_constraints.excluded_directory_names` | nested | A record providing excluded names of the type directoryName in leaf certificates whose trust path includes this certificate. |
| `cert.parsed.extensions.name_constraints.excluded_directory_names.email_address` | text | The emailAddress (E) elements of the Distinguished Name (OID: 1.2.840.113549.1.9.1). |
| `cert.parsed.extensions.name_constraints.excluded_directory_names.province` | text | The stateOrProvinceName (ST) elements of the Distinguished Name (OID: 2.5.4.8). |
| `cert.parsed.extensions.name_constraints.excluded_directory_names.jurisdiction_locality` | text | The jurisdictionLocality elements of the Distinguished Name (OID: 1.3.6.1.4.1.311.60.2.1.1). |
| `cert.parsed.extensions.name_constraints.excluded_directory_names.jurisdiction_province` | text | The jurisdictionStateOrProvince elements of the Distinguished Name (OID: 1.3.6.1.4.1.311.60.2.1.2). |
| `cert.parsed.extensions.name_constraints.excluded_directory_names.surname` | text | The surname (SN) elements of the Distinguished Name (OID: 2.5.4.4). |
| `cert.parsed.extensions.name_constraints.excluded_directory_names.serial_number` | keyword | The serialNumber elements of the Distinguished Name (OID: 2.5.4.5). |
| `cert.parsed.extensions.name_constraints.excluded_directory_names.organization_id` | text |  |
| `cert.parsed.extensions.name_constraints.excluded_directory_names.common_name` | text | The commonName (CN) elements of the Distinguished Name (OID: 2.5.4.3). |
| `cert.parsed.extensions.name_constraints.excluded_directory_names.jurisdiction_country` | text | The jurisdictionCountry elements of the Distinguished Name (OID: 1.3.6.1.4.1.311.60.2.1.3). |
| `cert.parsed.extensions.name_constraints.excluded_directory_names.organization` | text | The organizationName (O) elements of the Distinguished Name (OID: 2.5.4.10). |
| `cert.parsed.extensions.name_constraints.excluded_directory_names.organizational_unit` | text | The organizationalUnit (OU) elements of the Distinguished Name (OID: 2.5.4.11). |
| `cert.parsed.extensions.name_constraints.excluded_directory_names.given_name` | text | The givenName (G) elements of the Distinguished Name (OID: 2.5.4.42). |
| `cert.parsed.extensions.name_constraints.excluded_directory_names.domain_component` | text | The domainComponent (DC) elements of the Distinguished Name (OID: 0.9.2342.19200300.100.1.25). |
| `cert.parsed.extensions.name_constraints.excluded_directory_names.locality` | text | The localityName (L) elements of the Distinguished Name (OID: 2.5.4.7). |
| `cert.parsed.extensions.name_constraints.excluded_directory_names.country` | text | The countryName (C) elements of the Distinguished Name (OID: 2.5.4.6). |
| `cert.parsed.extensions.name_constraints.excluded_directory_names.street_address` | text | The streetAddress (STREET) elements of the Distinguished Name (OID: 2.5.4.9). |
| `cert.parsed.extensions.name_constraints.excluded_directory_names.postal_code` | keyword | The postalCode elements of the Distinguished Name (OID: 2.5.4.17). |
| `cert.parsed.extensions.name_constraints.permitted_directory_names` | nested | A record providing permitted names of the type directoryName in leaf certificates whose trust path includes this certificate. |
| `cert.parsed.extensions.name_constraints.permitted_directory_names.common_name` | text | The commonName (CN) elements of the Distinguished Name (OID: 2.5.4.3). |
| `cert.parsed.extensions.name_constraints.permitted_directory_names.organizational_unit` | text | The organizationalUnit (OU) elements of the Distinguished Name (OID: 2.5.4.11). |
| `cert.parsed.extensions.name_constraints.permitted_directory_names.locality` | text | The localityName (L) elements of the Distinguished Name (OID: 2.5.4.7). |
| `cert.parsed.extensions.name_constraints.permitted_directory_names.postal_code` | keyword | The postalCode elements of the Distinguished Name (OID: 2.5.4.17). |
| `cert.parsed.extensions.name_constraints.permitted_directory_names.jurisdiction_province` | text | The jurisdictionStateOrProvince elements of the Distinguished Name (OID: 1.3.6.1.4.1.311.60.2.1.2). |
| `cert.parsed.extensions.name_constraints.permitted_directory_names.surname` | text | The surname (SN) elements of the Distinguished Name (OID: 2.5.4.4). |
| `cert.parsed.extensions.name_constraints.permitted_directory_names.email_address` | text | The emailAddress (E) elements of the Distinguished Name (OID: 1.2.840.113549.1.9.1). |
| `cert.parsed.extensions.name_constraints.permitted_directory_names.domain_component` | text | The domainComponent (DC) elements of the Distinguished Name (OID: 0.9.2342.19200300.100.1.25). |
| `cert.parsed.extensions.name_constraints.permitted_directory_names.organization_id` | text |  |
| `cert.parsed.extensions.name_constraints.permitted_directory_names.organization` | text | The organizationName (O) elements of the Distinguished Name (OID: 2.5.4.10). |
| `cert.parsed.extensions.name_constraints.permitted_directory_names.jurisdiction_country` | text | The jurisdictionCountry elements of the Distinguished Name (OID: 1.3.6.1.4.1.311.60.2.1.3). |
| `cert.parsed.extensions.name_constraints.permitted_directory_names.jurisdiction_locality` | text | The jurisdictionLocality elements of the Distinguished Name (OID: 1.3.6.1.4.1.311.60.2.1.1). |
| `cert.parsed.extensions.name_constraints.permitted_directory_names.street_address` | text | The streetAddress (STREET) elements of the Distinguished Name (OID: 2.5.4.9). |
| `cert.parsed.extensions.name_constraints.permitted_directory_names.country` | text | The countryName (C) elements of the Distinguished Name (OID: 2.5.4.6). |
| `cert.parsed.extensions.name_constraints.permitted_directory_names.province` | text | The stateOrProvinceName (ST) elements of the Distinguished Name (OID: 2.5.4.8). |
| `cert.parsed.extensions.name_constraints.permitted_directory_names.serial_number` | keyword | The serialNumber elements of the Distinguished Name (OID: 2.5.4.5). |
| `cert.parsed.extensions.name_constraints.permitted_directory_names.given_name` | text | The givenName (G) elements of the Distinguished Name (OID: 2.5.4.42). |
| `cert.parsed.extensions.name_constraints.excluded_names` | text | A record providing a range of excluded names of the type dNSName in leaf certificates whose trust path includes this certificate. |
| `cert.parsed.extensions.name_constraints.excluded_email_addresses` | text | A record providing a range of excluded names of the type rfc822Name in leaf certificates whose trust path includes this certificate. |
| `cert.parsed.extensions.name_constraints.permitted_names` | text | A record providing a range of permitted names of the type dNSName in leaf certificates whose trust path includes this certificate. |
| `cert.parsed.extensions.name_constraints.excluded_edi_party_names` | nested | A record providing excluded names of the type ediPartyName in leaf certificates whose trust path includes this certificate. |
| `cert.parsed.extensions.name_constraints.excluded_edi_party_names.name_assigner` | text |  |
| `cert.parsed.extensions.name_constraints.excluded_edi_party_names.party_name` | text |  |
| `cert.parsed.extensions.name_constraints.excluded_registered_ids` | text | A record providing excluded names of the type registeredID in leaf certificates whose trust path includes this certificate. |
| `cert.parsed.extensions.name_constraints.excluded_uris` | text | A record providing a range of excluded uniform resource identifiers in leaf certificates whose trust path includes this certificate. |
| `cert.parsed.extensions.extended_key_usage` | object | The parsed id-ce-extKeyUsage extension (OID: 2.5.29.37). |
| `cert.parsed.extensions.extended_key_usage.apple_software_update_signing` | boolean |  |
| `cert.parsed.extensions.extended_key_usage.microsoft_nt5_crypto` | boolean |  |
| `cert.parsed.extensions.extended_key_usage.client_auth` | boolean |  |
| `cert.parsed.extensions.extended_key_usage.microsoft_system_health` | boolean |  |
| `cert.parsed.extensions.extended_key_usage.apple_ichat_encryption` | boolean |  |
| `cert.parsed.extensions.extended_key_usage.server_auth` | boolean |  |
| `cert.parsed.extensions.extended_key_usage.sbgp_cert_aa_service_auth` | boolean |  |
| `cert.parsed.extensions.extended_key_usage.ipsec_user` | boolean |  |
| `cert.parsed.extensions.extended_key_usage.ipsec_end_system` | boolean |  |
| `cert.parsed.extensions.extended_key_usage.microsoft_system_health_loophole` | boolean |  |
| `cert.parsed.extensions.extended_key_usage.apple_crypto_production_env` | boolean |  |
| `cert.parsed.extensions.extended_key_usage.microsoft_licenses` | boolean |  |
| `cert.parsed.extensions.extended_key_usage.microsoft_enrollment_agent` | boolean |  |
| `cert.parsed.extensions.extended_key_usage.code_signing` | boolean |  |
| `cert.parsed.extensions.extended_key_usage.microsoft_cert_trust_list_signing` | boolean |  |
| `cert.parsed.extensions.extended_key_usage.microsoft_oem_whql_crypto` | boolean |  |
| `cert.parsed.extensions.extended_key_usage.microsoft_qualified_subordinate` | boolean |  |
| `cert.parsed.extensions.extended_key_usage.microsoft_server_gated_crypto` | boolean |  |
| `cert.parsed.extensions.extended_key_usage.apple_crypto_maintenance_env` | boolean |  |
| `cert.parsed.extensions.extended_key_usage.microsoft_embedded_nt_crypto` | boolean |  |
| `cert.parsed.extensions.extended_key_usage.apple_crypto_qos` | boolean |  |
| `cert.parsed.extensions.extended_key_usage.microsoft_whql_crypto` | boolean |  |
| `cert.parsed.extensions.extended_key_usage.apple_crypto_tier0_qos` | boolean |  |
| `cert.parsed.extensions.extended_key_usage.time_stamping` | boolean |  |
| `cert.parsed.extensions.extended_key_usage.apple_crypto_tier1_qos` | boolean |  |
| `cert.parsed.extensions.extended_key_usage.microsoft_drm` | boolean |  |
| `cert.parsed.extensions.extended_key_usage.apple_ichat_signing` | boolean |  |
| `cert.parsed.extensions.extended_key_usage.apple_resource_signing` | boolean |  |
| `cert.parsed.extensions.extended_key_usage.any` | boolean |  |
| `cert.parsed.extensions.extended_key_usage.dvcs` | boolean |  |
| `cert.parsed.extensions.extended_key_usage.microsoft_mobile_device_software` | boolean |  |
| `cert.parsed.extensions.extended_key_usage.microsoft_key_recovery_21` | boolean |  |
| `cert.parsed.extensions.extended_key_usage.microsoft_kernel_mode_code_signing` | boolean |  |
| `cert.parsed.extensions.extended_key_usage.microsoft_ca_exchange` | boolean |  |
| `cert.parsed.extensions.extended_key_usage.microsoft_smartcard_logon` | boolean |  |
| `cert.parsed.extensions.extended_key_usage.microsoft_lifetime_signing` | boolean |  |
| `cert.parsed.extensions.extended_key_usage.microsoft_drm_individualization` | boolean |  |
| `cert.parsed.extensions.extended_key_usage.microsoft_efs_recovery` | boolean |  |
| `cert.parsed.extensions.extended_key_usage.apple_crypto_test_env` | boolean |  |
| `cert.parsed.extensions.extended_key_usage.apple_code_signing_third_party` | boolean |  |
| `cert.parsed.extensions.extended_key_usage.microsoft_sgc_serialized` | boolean |  |
| `cert.parsed.extensions.extended_key_usage.apple_crypto_tier3_qos` | boolean |  |
| `cert.parsed.extensions.extended_key_usage.microsoft_root_list_signer` | boolean |  |
| `cert.parsed.extensions.extended_key_usage.apple_system_identity` | boolean |  |
| `cert.parsed.extensions.extended_key_usage.apple_crypto_tier2_qos` | boolean |  |
| `cert.parsed.extensions.extended_key_usage.ocsp_signing` | boolean |  |
| `cert.parsed.extensions.extended_key_usage.email_protection` | boolean |  |
| `cert.parsed.extensions.extended_key_usage.ipsec_tunnel` | boolean |  |
| `cert.parsed.extensions.extended_key_usage.microsoft_smart_display` | boolean |  |
| `cert.parsed.extensions.extended_key_usage.eap_over_lan` | boolean |  |
| `cert.parsed.extensions.extended_key_usage.microsoft_csp_signature` | boolean |  |
| `cert.parsed.extensions.extended_key_usage.microsoft_document_signing` | boolean |  |
| `cert.parsed.extensions.extended_key_usage.apple_code_signing` | boolean |  |
| `cert.parsed.extensions.extended_key_usage.microsoft_key_recovery_3` | boolean |  |
| `cert.parsed.extensions.extended_key_usage.netscape_server_gated_crypto` | boolean |  |
| `cert.parsed.extensions.extended_key_usage.eap_over_ppp` | boolean |  |
| `cert.parsed.extensions.extended_key_usage.unknown` | text |  |
| `cert.parsed.extensions.extended_key_usage.apple_crypto_env` | boolean |  |
| `cert.parsed.extensions.extended_key_usage.apple_crypto_development_env` | boolean |  |
| `cert.parsed.extensions.extended_key_usage.microsoft_encrypted_file_system` | boolean |  |
| `cert.parsed.extensions.extended_key_usage.microsoft_timestamp_signing` | boolean |  |
| `cert.parsed.extensions.extended_key_usage.ipsec_intermediate_system_usage` | boolean |  |
| `cert.parsed.extensions.extended_key_usage.apple_code_signing_development` | boolean |  |
| `cert.parsed.extensions.extended_key_usage.microsoft_license_server` | boolean |  |
| `cert.parsed.extensions.tor_service_descriptors` | nested |  |
| `cert.parsed.extensions.tor_service_descriptors.algorithm_name` | text |  |
| `cert.parsed.extensions.tor_service_descriptors.hash` | text |  |
| `cert.parsed.extensions.tor_service_descriptors.hash_bits` | integer |  |
| `cert.parsed.extensions.tor_service_descriptors.onion` | text |  |
| `cert.parsed.extensions.crl_distribution_points` | text | The parsed id-ce-cRLDistributionPoints extension (OID: 2.5.29.31). Contents are a list of distributionPoint URLs; other distributionPoint types are omitted). |
| `cert.parsed.extensions.signed_certificate_timestamps` | nested |  |
| `cert.parsed.extensions.signed_certificate_timestamps.signature` | object |  |
| `cert.parsed.extensions.signed_certificate_timestamps.signature.signature` | text |  |
| `cert.parsed.extensions.signed_certificate_timestamps.signature.signature_algorithm` | text |  |
| `cert.parsed.extensions.signed_certificate_timestamps.signature.hash_algorithm` | text |  |
| `cert.parsed.extensions.signed_certificate_timestamps.timestamp` | date |  |
| `cert.parsed.extensions.signed_certificate_timestamps.version` | integer |  |
| `cert.parsed.extensions.signed_certificate_timestamps.log_id` | text |  |
| `cert.parsed.extensions.key_usage.certificate_sign` | boolean | Whether the keyCertSign bit is set. |
| `cert.parsed.extensions.key_usage` | object | The parsed id-ce-keyUsage extension (OID: 2.5.29.15). |
| `cert.parsed.extensions.key_usage.encipher_only` | boolean | Whether the encipherOnly bit is set. |
| `cert.parsed.extensions.key_usage.key_encipherment` | boolean | Whether the keyEncipherment bit is set. |
| `cert.parsed.extensions.key_usage.decipher_only` | boolean | Whether the decipherOnly bit is set. |
| `cert.parsed.extensions.key_usage.crl_sign` | boolean | Whether the cRLSign bit is set. |
| `cert.parsed.extensions.key_usage.data_encipherment` | boolean | Whether the dataEncipherment bit is set. |
| `cert.parsed.extensions.key_usage.value` | unsigned_long | The integer value of the bitmask in the extension. |
| `cert.parsed.extensions.key_usage.key_agreement` | boolean | Whether the keyAgreement bit is set. |
| `cert.parsed.extensions.key_usage.content_commitment` | boolean | Whether the contentCommitment (formerly called nonRepudiation) bit is set. |
| `cert.parsed.extensions.key_usage.digital_signature` | boolean | Whether the digitalSignature bit is set. |
| `cert.parsed.extensions.cabf_organization_id` | object | CA/Browser Forum organization ID extensions (OID: 2.23.140.3.1). |
| `cert.parsed.extensions.cabf_organization_id.country` | text |  |
| `cert.parsed.extensions.cabf_organization_id.reference` | text |  |
| `cert.parsed.extensions.cabf_organization_id.scheme` | text |  |
| `cert.parsed.extensions.cabf_organization_id.state` | text |  |
| `cert.parsed.extensions.basic_constraints` | object | The parsed id-ce-basicConstraints extension (OID: 2.5.29.19). |
| `cert.parsed.extensions.basic_constraints.is_ca` | boolean | Whether the certificate is permitted to sign other certificates. |
| `cert.parsed.extensions.basic_constraints.max_path_len` | integer | When present, provides the maximum number of intermediate certificates that may follow this certificate in a trusted certification path. |
| `cert.parsed.extensions.qc_statements` | object |  |
| `cert.parsed.extensions.qc_statements.ids` | text |  |
| `cert.parsed.extensions.qc_statements.parsed` | object |  |
| `cert.parsed.extensions.qc_statements.parsed.limit` | nested |  |
| `cert.parsed.extensions.qc_statements.parsed.limit.currency_number` | long |  |
| `cert.parsed.extensions.qc_statements.parsed.limit.exponent` | long |  |
| `cert.parsed.extensions.qc_statements.parsed.limit.amount` | long |  |
| `cert.parsed.extensions.qc_statements.parsed.limit.currency` | text |  |
| `cert.parsed.extensions.qc_statements.parsed.pds_locations` | nested |  |
| `cert.parsed.extensions.qc_statements.parsed.pds_locations.language` | text |  |
| `cert.parsed.extensions.qc_statements.parsed.pds_locations.url` | text |  |
| `cert.parsed.extensions.qc_statements.parsed.retention_period` | long |  |
| `cert.parsed.extensions.qc_statements.parsed.sscd` | boolean |  |
| `cert.parsed.extensions.qc_statements.parsed.types` | nested |  |
| `cert.parsed.extensions.qc_statements.parsed.types.ids` | text |  |
| `cert.parsed.extensions.qc_statements.parsed.etsi_compliance` | boolean |  |
| `cert.parsed.extensions.qc_statements.parsed.legislation` | nested |  |
| `cert.parsed.extensions.qc_statements.parsed.legislation.country_codes` | text |  |
| `cert.parsed.extensions.issuer_alt_name` | object | The parsed id-ce-issuerAltName extension (OID: 2.5.29.18). |
| `cert.parsed.extensions.issuer_alt_name.other_names` | nested | The parsed otherName entries in the GeneralName. An arbitrary binary value identified by an OID. |
| `cert.parsed.extensions.issuer_alt_name.other_names.id` | text | The OID identifying the syntax of the otherName value. |
| `cert.parsed.extensions.issuer_alt_name.other_names.value` | text | The raw otherName value. |
| `cert.parsed.extensions.issuer_alt_name.registered_ids` | text | The parsed registeredID entries in the GeneralName. Stored in dotted-decimal format. |
| `cert.parsed.extensions.issuer_alt_name.uniform_resource_identifiers` | text | The parsed uniformResourceIdentifier entries in the GeneralName. |
| `cert.parsed.extensions.issuer_alt_name.directory_names` | nested | The parsed directoryName entries in the GeneralName. |
| `cert.parsed.extensions.issuer_alt_name.directory_names.given_name` | text | The givenName (G) elements of the Distinguished Name (OID: 2.5.4.42). |
| `cert.parsed.extensions.issuer_alt_name.directory_names.country` | text | The countryName (C) elements of the Distinguished Name (OID: 2.5.4.6). |
| `cert.parsed.extensions.issuer_alt_name.directory_names.common_name` | text | The commonName (CN) elements of the Distinguished Name (OID: 2.5.4.3). |
| `cert.parsed.extensions.issuer_alt_name.directory_names.organization_id` | text |  |
| `cert.parsed.extensions.issuer_alt_name.directory_names.province` | text | The stateOrProvinceName (ST) elements of the Distinguished Name (OID: 2.5.4.8). |
| `cert.parsed.extensions.issuer_alt_name.directory_names.jurisdiction_province` | text | The jurisdictionStateOrProvince elements of the Distinguished Name (OID: 1.3.6.1.4.1.311.60.2.1.2). |
| `cert.parsed.extensions.issuer_alt_name.directory_names.domain_component` | text | The domainComponent (DC) elements of the Distinguished Name (OID: 0.9.2342.19200300.100.1.25). |
| `cert.parsed.extensions.issuer_alt_name.directory_names.street_address` | text | The streetAddress (STREET) elements of the Distinguished Name (OID: 2.5.4.9). |
| `cert.parsed.extensions.issuer_alt_name.directory_names.locality` | text | The localityName (L) elements of the Distinguished Name (OID: 2.5.4.7). |
| `cert.parsed.extensions.issuer_alt_name.directory_names.organizational_unit` | text | The organizationalUnit (OU) elements of the Distinguished Name (OID: 2.5.4.11). |
| `cert.parsed.extensions.issuer_alt_name.directory_names.organization` | text | The organizationName (O) elements of the Distinguished Name (OID: 2.5.4.10). |
| `cert.parsed.extensions.issuer_alt_name.directory_names.surname` | text | The surname (SN) elements of the Distinguished Name (OID: 2.5.4.4). |
| `cert.parsed.extensions.issuer_alt_name.directory_names.email_address` | text | The emailAddress (E) elements of the Distinguished Name (OID: 1.2.840.113549.1.9.1). |
| `cert.parsed.extensions.issuer_alt_name.directory_names.postal_code` | keyword | The postalCode elements of the Distinguished Name (OID: 2.5.4.17). |
| `cert.parsed.extensions.issuer_alt_name.directory_names.serial_number` | keyword | The serialNumber elements of the Distinguished Name (OID: 2.5.4.5). |
| `cert.parsed.extensions.issuer_alt_name.directory_names.jurisdiction_country` | text | The jurisdictionCountry elements of the Distinguished Name (OID: 1.3.6.1.4.1.311.60.2.1.3). |
| `cert.parsed.extensions.issuer_alt_name.directory_names.jurisdiction_locality` | text | The jurisdictionLocality elements of the Distinguished Name (OID: 1.3.6.1.4.1.311.60.2.1.1). |
| `cert.parsed.extensions.issuer_alt_name.dns_names` | text | The parsed dNSName entries in the GeneralName. |
| `cert.parsed.extensions.issuer_alt_name.edi_party_names` | nested | The parsed eDIPartyName entries in the GeneralName. |
| `cert.parsed.extensions.issuer_alt_name.edi_party_names.name_assigner` | text |  |
| `cert.parsed.extensions.issuer_alt_name.edi_party_names.party_name` | text |  |
| `cert.parsed.extensions.issuer_alt_name.email_addresses` | text | The parsed rfc822Name entries in the GeneralName. |
| `cert.parsed.extensions.issuer_alt_name.ip_addresses` | text | The parsed ipAddress entries in the GeneralName. |
| `cert.parsed.extensions.authority_key_id` | text | A key identifier, usually a digest of the DER-encoded SubjectPublicKeyInfo. |
| `cert.parsed.extensions.authority_info_access` | object | The parsed id-pe-authorityInfoAccess extension (OID: 1.3.6.1.5.7.1.1). Only id-ad-caIssuers and id-ad-ocsp accessMethods are supported; others are omitted. |
| `cert.parsed.extensions.authority_info_access.issuer_urls` | text |  |
| `cert.parsed.extensions.authority_info_access.ocsp_urls` | text |  |
| `cert.parsed.extensions.certificate_policies` | nested | The parsed id-ce-certificatePolicies extension (OID: 2.5.29.32). |
| `cert.parsed.extensions.certificate_policies.id` | text |  |
| `cert.parsed.extensions.certificate_policies.user_notice` | nested |  |
| `cert.parsed.extensions.certificate_policies.user_notice.explicit_text` | text |  |
| `cert.parsed.extensions.certificate_policies.user_notice.notice_reference` | object |  |
| `cert.parsed.extensions.certificate_policies.user_notice.notice_reference.notice_numbers` | integer |  |
| `cert.parsed.extensions.certificate_policies.user_notice.notice_reference.organization` | text |  |
| `cert.parsed.extensions.certificate_policies.cps` | text |  |
| `cert.parsed.extensions.subject_key_id` | text | A key identifier, usually a digest of the DER-encoded SubjectPublicKeyInfo.. |
| `cert.parsed.extensions.subject_alt_name` | object | The parsed id-ce-subjectAltName extension (OID: 2.5.29.17). |
| `cert.parsed.extensions.subject_alt_name.other_names` | nested | The parsed otherName entries in the GeneralName. An arbitrary binary value identified by an OID. |
| `cert.parsed.extensions.subject_alt_name.other_names.value` | text | The raw otherName value. |
| `cert.parsed.extensions.subject_alt_name.other_names.id` | text | The OID identifying the syntax of the otherName value. |
| `cert.parsed.extensions.subject_alt_name.registered_ids` | text | The parsed registeredID entries in the GeneralName. Stored in dotted-decimal format. |
| `cert.parsed.extensions.subject_alt_name.uniform_resource_identifiers` | text | The parsed uniformResourceIdentifier entries in the GeneralName. |
| `cert.parsed.extensions.subject_alt_name.directory_names` | nested | The parsed directoryName entries in the GeneralName. |
| `cert.parsed.extensions.subject_alt_name.directory_names.given_name` | text | The givenName (G) elements of the Distinguished Name (OID: 2.5.4.42). |
| `cert.parsed.extensions.subject_alt_name.directory_names.street_address` | text | The streetAddress (STREET) elements of the Distinguished Name (OID: 2.5.4.9). |
| `cert.parsed.extensions.subject_alt_name.directory_names.jurisdiction_country` | text | The jurisdictionCountry elements of the Distinguished Name (OID: 1.3.6.1.4.1.311.60.2.1.3). |
| `cert.parsed.extensions.subject_alt_name.directory_names.locality` | text | The localityName (L) elements of the Distinguished Name (OID: 2.5.4.7). |
| `cert.parsed.extensions.subject_alt_name.directory_names.jurisdiction_locality` | text | The jurisdictionLocality elements of the Distinguished Name (OID: 1.3.6.1.4.1.311.60.2.1.1). |
| `cert.parsed.extensions.subject_alt_name.directory_names.serial_number` | keyword | The serialNumber elements of the Distinguished Name (OID: 2.5.4.5). |
| `cert.parsed.extensions.subject_alt_name.directory_names.email_address` | text | The emailAddress (E) elements of the Distinguished Name (OID: 1.2.840.113549.1.9.1). |
| `cert.parsed.extensions.subject_alt_name.directory_names.jurisdiction_province` | text | The jurisdictionStateOrProvince elements of the Distinguished Name (OID: 1.3.6.1.4.1.311.60.2.1.2). |
| `cert.parsed.extensions.subject_alt_name.directory_names.postal_code` | keyword | The postalCode elements of the Distinguished Name (OID: 2.5.4.17). |
| `cert.parsed.extensions.subject_alt_name.directory_names.surname` | text | The surname (SN) elements of the Distinguished Name (OID: 2.5.4.4). |
| `cert.parsed.extensions.subject_alt_name.directory_names.domain_component` | text | The domainComponent (DC) elements of the Distinguished Name (OID: 0.9.2342.19200300.100.1.25). |
| `cert.parsed.extensions.subject_alt_name.directory_names.organization` | text | The organizationName (O) elements of the Distinguished Name (OID: 2.5.4.10). |
| `cert.parsed.extensions.subject_alt_name.directory_names.country` | text | The countryName (C) elements of the Distinguished Name (OID: 2.5.4.6). |
| `cert.parsed.extensions.subject_alt_name.directory_names.province` | text | The stateOrProvinceName (ST) elements of the Distinguished Name (OID: 2.5.4.8). |
| `cert.parsed.extensions.subject_alt_name.directory_names.common_name` | text | The commonName (CN) elements of the Distinguished Name (OID: 2.5.4.3). |
| `cert.parsed.extensions.subject_alt_name.directory_names.organization_id` | text |  |
| `cert.parsed.extensions.subject_alt_name.directory_names.organizational_unit` | text | The organizationalUnit (OU) elements of the Distinguished Name (OID: 2.5.4.11). |
| `cert.parsed.extensions.subject_alt_name.dns_names` | text | The parsed dNSName entries in the GeneralName. |
| `cert.parsed.extensions.subject_alt_name.edi_party_names` | nested | The parsed eDIPartyName entries in the GeneralName. |
| `cert.parsed.extensions.subject_alt_name.edi_party_names.name_assigner` | text |  |
| `cert.parsed.extensions.subject_alt_name.edi_party_names.party_name` | text |  |
| `cert.parsed.extensions.subject_alt_name.email_addresses` | text | The parsed rfc822Name entries in the GeneralName. |
| `cert.parsed.extensions.subject_alt_name.ip_addresses` | text | The parsed ipAddress entries in the GeneralName. |
| `cert.parsed.redacted` | boolean |  |
| `cert.parsed.version` | integer |  |
| `cert.validation_level` | text | The extent to which the certificate's issuer validated the identity of the entity requesting the certificate. Options include Domain validated (DV), Organization Validated (OV), or Extended Validation (EV). |
| `cert.ever_seen_in_scan` | boolean |  |
| `cert.spki_subject_fingerprint_sha256` | text | The SHA-256 digest of the certificate's DER-encoded SubjectPublicKeyInfo concatenated with its Subject. |
| `cert.precert` | boolean | Whether the X.509 "poison" extension (OID: 1.3.6.1.4.1.11129.2.4.3) is marked critical, which prohibits the pre-certificate from being trusted. |
| `cert.parent_spki_subject_fingerprint_sha256` | text | The SHA-256 digest of the parent certificate's DER-encoded SubjectPublicKeyInfo concatenated with its Subject. |
| `cert.ct.entries` | nested |  |
| `cert.ct.entries.value` | object |  |
| `cert.ct.entries.value.index` | long | Numerical marker of the certificate's place in the CT log. |
| `cert.ct.entries.value.added_to_ct_at` | date | An RFC-3339-formatted timestamp indicating when the certificate was entered into the CT log. |
| `cert.ct.entries.value.ct_to_censys_at` | date | An RFC-3339-formated timestamp indicating when the certificate was ingested from the CT log into the Censys dataset. |
| `cert.ct.entries.key` | text |  |
| `cert.revocation.ocsp` | object |  |
| `cert.revocation.ocsp.reason` | text | An enumerated value indicating the issuer-supplied reason for the revocation. |
| `cert.revocation.ocsp.revocation_time` | date | The issuer-supplied timestamp indicating when the certificate was revoked. |
| `cert.revocation.ocsp.revoked` | boolean | Whether the certificate has been revoked before its expiry date by the issuer. |
| `cert.revocation.ocsp.next_update` | date |  |
| `cert.revoked` | boolean | Whether the certificate has been revoked before its expiry date by the issuer. |
| `cert.revocation.crl` | object |  |
| `cert.revocation.crl.next_update` | date |  |
| `cert.revocation.crl.reason` | text | An enumerated value indicating the issuer-supplied reason for the revocation. |
| `cert.revocation.crl.revocation_time` | date | The issuer-supplied timestamp indicating when the certificate was revoked. |
| `cert.revocation.crl.revoked` | boolean | Whether the certificate has been revoked before its expiry date by the issuer. |
| `cert.validation.nss` | object | A record containing validation information about the certificate from the Mozilla NSS root store. |
| `cert.validation.nss.chains` | nested | A path of trusted signing certificates up to a root certificate present in a root store, represented as an ordered list of SHA-256 fingerprints. |
| `cert.validation.nss.chains.sha256fp` | text |  |
| `cert.validation.nss.ever_valid` | boolean | Whether the certificate has ever been considered valid by the root store. |
| `cert.validation.nss.had_trusted_path` | boolean | Whether there ever existed a trusted path of signing certificates from a certificate present in the root certificate store. |
| `cert.validation.nss.has_trusted_path` | boolean | Whether there currently exists a trusted path of signing certificates from a certificate present in the root certificate store. |
| `cert.validation.nss.in_revocation_set` | boolean | Whether the certificate is in the revocation set (e.g. OneCRL) associated with the root store. |
| `cert.validation.nss.is_valid` | boolean | Whether the certificate is currently considered valid by the root store: a summary of the trust path, revoked, blocklisted/allowlisted, and expired fields. |
| `cert.validation.nss.parents` | text | The SHA-256 fingerprints of the certificate's immediate parents in its trust path(s). |
| `cert.validation.nss.type` | text | The certificate's type. Options include root, intermediate, or leaf. |
| `cert.validation.apple` | object | A record containing validation information about the certificate from the Apple root store. |
| `cert.validation.apple.had_trusted_path` | boolean | Whether there ever existed a trusted path of signing certificates from a certificate present in the root certificate store. |
| `cert.validation.apple.has_trusted_path` | boolean | Whether there currently exists a trusted path of signing certificates from a certificate present in the root certificate store. |
| `cert.validation.apple.in_revocation_set` | boolean | Whether the certificate is in the revocation set (e.g. OneCRL) associated with the root store. |
| `cert.validation.apple.is_valid` | boolean | Whether the certificate is currently considered valid by the root store: a summary of the trust path, revoked, blocklisted/allowlisted, and expired fields. |
| `cert.validation.apple.parents` | text | The SHA-256 fingerprints of the certificate's immediate parents in its trust path(s). |
| `cert.validation.apple.type` | text | The certificate's type. Options include root, intermediate, or leaf. |
| `cert.validation.apple.chains` | nested | A path of trusted signing certificates up to a root certificate present in a root store, represented as an ordered list of SHA-256 fingerprints. |
| `cert.validation.apple.chains.sha256fp` | text |  |
| `cert.validation.apple.ever_valid` | boolean | Whether the certificate has ever been considered valid by the root store. |
| `cert.validation.chrome` | object | A record containing validation information about the certificate from the Chrome root store. |
| `cert.validation.chrome.ever_valid` | boolean | Whether the certificate has ever been considered valid by the root store. |
| `cert.validation.chrome.had_trusted_path` | boolean | Whether there ever existed a trusted path of signing certificates from a certificate present in the root certificate store. |
| `cert.validation.chrome.has_trusted_path` | boolean | Whether there currently exists a trusted path of signing certificates from a certificate present in the root certificate store. |
| `cert.validation.chrome.in_revocation_set` | boolean | Whether the certificate is in the revocation set (e.g. OneCRL) associated with the root store. |
| `cert.validation.chrome.is_valid` | boolean | Whether the certificate is currently considered valid by the root store: a summary of the trust path, revoked, blocklisted/allowlisted, and expired fields. |
| `cert.validation.chrome.parents` | text | The SHA-256 fingerprints of the certificate's immediate parents in its trust path(s). |
| `cert.validation.chrome.type` | text | The certificate's type. Options include root, intermediate, or leaf. |
| `cert.validation.chrome.chains` | nested | A path of trusted signing certificates up to a root certificate present in a root store, represented as an ordered list of SHA-256 fingerprints. |
| `cert.validation.chrome.chains.sha256fp` | text |  |
| `cert.validation.microsoft` | object | A record containing validation information about the certificate from the Microsoft root store. |
| `cert.validation.microsoft.ever_valid` | boolean | Whether the certificate has ever been considered valid by the root store. |
| `cert.validation.microsoft.had_trusted_path` | boolean | Whether there ever existed a trusted path of signing certificates from a certificate present in the root certificate store. |
| `cert.validation.microsoft.has_trusted_path` | boolean | Whether there currently exists a trusted path of signing certificates from a certificate present in the root certificate store. |
| `cert.validation.microsoft.in_revocation_set` | boolean | Whether the certificate is in the revocation set (e.g. OneCRL) associated with the root store. |
| `cert.validation.microsoft.is_valid` | boolean | Whether the certificate is currently considered valid by the root store: a summary of the trust path, revoked, blocklisted/allowlisted, and expired fields. |
| `cert.validation.microsoft.parents` | text | The SHA-256 fingerprints of the certificate's immediate parents in its trust path(s). |
| `cert.validation.microsoft.type` | text | The certificate's type. Options include root, intermediate, or leaf. |
| `cert.validation.microsoft.chains` | nested | A path of trusted signing certificates up to a root certificate present in a root store, represented as an ordered list of SHA-256 fingerprints. |
| `cert.validation.microsoft.chains.sha256fp` | text |  |
| `cert.zlint` | object | A record containing the results of linting the certificate for conformance to the X.509 standard using Zlint. |
| `cert.zlint.failed_lints` | text | A list of lint names which failed, if applicable. |
| `cert.zlint.fatals_present` | boolean | Whether the certificate's attributes triggered any fatal lints for non-conformance to the X.509 standard. |
| `cert.zlint.notices_present` | boolean | Whether the certificate's attributes triggered any notice lints for non-conformance to the X.509 standard. |
| `cert.zlint.timestamp` | date | An RFC-3339-formated timestamp indicating when the certificate was linted. |
| `cert.zlint.version` | long | The version of Zlint used to lint the certificate. |
| `cert.zlint.warnings_present` | boolean | Whether the certificate's attributes triggered any warning lints for non-conformance to the X.509 standard. |
| `cert.zlint.errors_present` | boolean | Whether the certificate's attributes triggered any error lints for non-conformance to the X.509 standard. |
