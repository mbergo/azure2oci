python3 -m venv venv
source venv/bin/activate
pip install azure-cli oci-cli

python migrate_vm.py example_vm_name example_resource_group example_compartment_id example_subnet_id
