To achieve this, we will need to create a Python script that uses the Azure CLI and OCI CLI to migrate VMs from Azure to OCI. The script will take as input the VM name from Azure, its resource group, the compartment_id to be migrated to OCI, and the subnet_id from OCI.

Here is the Python script:

migrate_vm.py
