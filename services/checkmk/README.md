# CheckMK Automation Playbooks

## A project to simplify the deployment of CheckMK


- Install ChecMK Server 2.4.0b1 into Alma Linux 9.4 (Seafoam Ocelot) you can set this in site_vars.yml file but make sure the package is available (if custom repository is used) so that Ansible can pull from.
- Install Agent on target server, register target nodes with CheckMK server.
- Create service account for Grafana (used in datasource plugin) and operator account (view only)
- Create folder, adding target nodes to folder, running service discovery, active changes on web.


## Dependencies

 - [ansible.posix](https://github.com/ansible-collections/ansible.posix)
 - [ansible.utils](https://github.com/ansible-collections/ansible.utils)
 - [community.general](https://github.com/ansible-collections/community.general)

## Setup

 Authentication information stored in Ansible host.
 - /home/ansible/variables/vars_file.yml
 The file should contain these information for both Grafana and CheckMK since they related to each other:
 ---

# Example:

customer_name: STM
site: TST
cmk_user: cmkadmin
cmk_secret: abcabc
cmk_automation_user: grafana_svc
cmk_automation_user_secret: passwdpasswd
grafana_user: admin
grafana_secret: adminadmin
grafana_viewer_user: oper
grafana_viewer_secret: operpasswd
cmk_ops_user: oper
cmk_ops_user_secret: passwdpasswd

 Another file contains information about version of CheckMK Server, packages URL is imported per customer
 The exammple location of file is:
 To let ansible load this file from different location when deploy for different customer set a var called "customer_name" and "site" inside /home/ansible/variables/vars_file.yml 
 ../../envs/NA/CM/DRC/playbooks/CMK/site_vars.yml


## Structure:

```bash
├── 1-checkmk-folder-creation.yml          # Create folders in CheckMK
├── 2-checkmk-add-host-to-folder.yml       # Add a host into a CheckMK folder
├── 3.1-checkmk-agent-install-linux.yml    # Install CheckMK agent on Linux
├── 3.2-checkmk-agent-install-windows.yml  # Install CheckMK agent on Windows
├── 4-checkmk-service-discovery.yml        # Run service discovery on target servers after agent installation
├── 5-checkmk-site-activation.yml          # Activate the changes on CheckMK site
├── checkmk-add-host-to-monitor.yml        # Master playbook chaining 1-5
├── checkmk-install.yml                    # Install CheckMK itself (server-side)
├── checkmk-csv-check.yml                  # Pushing custom check that create .csv files for Grafana
├── checkmk-custom-check-push.yml          # Pushing localcheck used to montior custom metric
├── checkmk-remove-host-from-folder.yml    # Remove a host from CheckMK
├── README.md                              # Description / how-to
```

## Usage:

```bash


# Each site (PDC,DRC or TST) will have its own varible about site name, IP of nodes,... stored in site_vars.yml file so please modify it before run.
# With customer who has local repository deployed, packages should be retrieved from there to shorten download time and ensure exact version is installed.
# Playbook will be call in form of bash script file.
# For example this bash script is going to install CheckMK for NA PDC site.
cd system-automation/envs/NA/CM/PDC
bash NA-PDC-CMK.sh

