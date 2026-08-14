# Install CheckMK Server
ansible-playbook playbooks/DEV-MONITORING.yml -i CORP1-inventory.yml --limit CORP1_CMK

# Install CheckMK Agent + client plugins (delegate_to model: run once against the CMK/controller
# host, the play delegates to every host listed in cmk_monitored_hosts, so no host-group --limit
# is needed here anymore)
# ansible-playbook playbooks/DEV-MONITORING.yml -i CORP1-inventory.yml --limit CORP1_CMK
