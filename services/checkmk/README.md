# CheckMK Automation Playbooks

## A project to simplify the deployment of CheckMK

- Install CheckMK Server into AlmaLinux (RHEL-based); the package URL is set in `site_vars.yml`, so make sure it's reachable (a local/custom repo can be used to shorten download time).
- Install the Agent on target servers and register them with the CheckMK server.
- Create the automation user consumed by Grafana's datasource plugin and a read-only operator account.
- Create folders, add target nodes to folders, run service discovery, activate changes.
- Optional: HTTPS enforcement, custom/built-in agent plugins, custom check scripts (e.g. iLO health via Redfish, VMware snapshot summary), LDAP/AD integration, and process/systemd service monitoring rules.

## Dependencies

 - [ansible.posix](https://github.com/ansible-collections/ansible.posix)
 - [ansible.utils](https://github.com/ansible-collections/ansible.utils)
 - [community.general](https://github.com/ansible-collections/community.general)
 - [checkmk.general](https://github.com/Checkmk/ansible-collection-checkmk.general)
 - [ansible.windows](https://github.com/ansible-collections/ansible.windows) and [community.windows](https://github.com/ansible-collections/community.windows) (for `3.2-checkmk-agent-install-windows.yml`; the target Windows hosts must already be reachable over WinRM)

## Setup

Credentials are stored outside this repository on the Ansible control node, at:
```
/home/ansible/variables/vars_file.yml
```
See `sample_vars_files.yml` at the repo root for the full list of required keys. Every playbook validates its
required secrets via `commons/validate-vault-keys.yml` before doing anything else, and stops if one is missing.

Non-secret, per-site configuration (CheckMK URL, package URLs, folders, monitored hosts, etc.) lives in:
```
sites/{{ customer_name }}/CM/{{ site }}/playbooks/CMK/site_vars.yml
```
`customer_name` and `site` are set in the vault file above so Ansible knows which `site_vars.yml` to load.

## Structure:

```bash
├── 1-checkmk-folder-creation.yml               # Create folders in CheckMK
├── 2-checkmk-add-host-to-folder.yml            # Add a host into a CheckMK folder
├── 3.1-checkmk-agent-install-linux.yml         # Install/register CheckMK agent on Linux hosts
├── 3.2-checkmk-agent-install-windows.yml       # Install/register CheckMK agent on Windows hosts
├── 4-checkmk-service-discovery.yml             # Run service discovery on target servers after agent installation
├── 5-checkmk-site-activation.yml               # Activate the changes on the CheckMK site
├── checkmk-add-host-to-monitor.yml             # Convenience wrapper chaining 1-5
├── checkmk-install.yml                         # Install CheckMK itself (server-side) and create service users
├── checkmk-install-custom-plugins.yml          # Import custom check plugins (server-plugins/) into the CheckMK site
├── checkmk-remove-host-from-folder.yml         # Remove a host from CheckMK
├── checkmk-https-setup.yml                     # Enforce HTTPS on the CheckMK server via httpd
├── checkmk-client-install-built-in-plugin.yml  # Download a built-in agent plugin from the CheckMK server to a client
├── checkmk-client-install-custom-plugin.yml    # Push a custom agent plugin (client-plugins/) to a client
├── checkmk-custom-check-deploy.yml             # Deploy templated custom checks (iLO health, vCenter snapshots, csv export)
├── checkmk-ad-integration.yml                  # Configure LDAP/AD user connections in CheckMK
├── checkmk-process-monitor.yml                 # Create/update process (ps) monitoring rules from cmk_process_checks
├── checkmk-systemd-service-rule.yml            # Create/update systemd service monitoring rules from cmk_systemd_checks
├── checkmk-csv-check.yml                       # Simple push of static .csv check scripts from filecheck/
├── checkmk-custom-check-push.yml               # Simple push of static local-check scripts from localcheck/
├── server-plugins/                             # Example server-side check plugins (checkmk-install-custom-plugins.yml)
├── client-plugins/                              # Example client-side agent plugins (checkmk-client-install-custom-plugin.yml)
├── j2-template/                                # Jinja2 templates used by the optional playbooks above
├── filecheck/, localcheck/                     # Static scripts used by checkmk-csv-check.yml / checkmk-custom-check-push.yml
├── README.md                                    # Description / how-to
```

## Usage:

```bash
# Each site will have its own site_vars.yml with site name, package URLs and monitored hosts,
# so modify it before running. With a local package repository, point the *_package_url vars
# at it to shorten download time and pin an exact version.
cd sites/CORP1/CM/DEV
bash DEV-MONITORING.sh
```

## Process / systemd service monitoring rules

Instead of clicking through the CheckMK UI, define the rules as data in `site_vars.yml` and let
`checkmk-process-monitor.yml` / `checkmk-systemd-service-rule.yml` create or update them via the API.
Each entry's `description` is treated as the rule's unique identity, so re-running the playbook updates
the existing rule instead of creating a duplicate. See `cmk_process_checks` / `cmk_systemd_checks` in
`site_vars.yml` for the expected shape.
