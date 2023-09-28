import subprocess
import json

def get_vm_info(vm_name, resource_group):
    """
    This function uses the Azure CLI to get the information of a VM in Azure.
    """
    command = f"az vm show --name {vm_name} --resource-group {resource_group}"
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()

    if error:
        print(f"Error getting VM info: {error}")
        return None

    return json.loads(output)

def create_instance(oci_compartment_id, oci_subnet_id, vm_info):
    """
    This function uses the OCI CLI to create an instance in OCI with the same configuration as the Azure VM.
    """
    command = f"oci compute instance launch --compartment-id {oci_compartment_id} --subnet-id {oci_subnet_id} --shape {vm_info['hardwareProfile']['vmSize']} --display-name {vm_info['name']} --image-id {vm_info['storageProfile']['imageReference']['id']}"
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()

    if error:
        print(f"Error creating instance: {error}")
        return None

    return json.loads(output)

def migrate_vm(azure_vm_name, azure_resource_group, oci_compartment_id, oci_subnet_id):
    """
    This function migrates a VM from Azure to OCI.
    """
    vm_info = get_vm_info(azure_vm_name, azure_resource_group)
    if vm_info is None:
        print(f"Error: Could not get VM info for {azure_vm_name} in resource group {azure_resource_group}")
        return

    instance_info = create_instance(oci_compartment_id, oci_subnet_id, vm_info)
    if instance_info is None:
        print(f"Error: Could not create instance in OCI")
        return

    print(f"Successfully migrated {azure_vm_name} to OCI. New instance ID is {instance_info['id']}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 5:
        print("Usage: python migrate_vm.py <azure_vm_name> <azure_resource_group> <oci_compartment_id> <oci_subnet_id>")
        sys.exit(1)

    azure_vm_name = sys.argv[1]
    azure_resource_group = sys.argv[2]
    oci_compartment_id = sys.argv[3]
    oci_subnet_id = sys.argv[4]

    migrate_vm(azure_vm_name, azure_resource_group, oci_compartment_id, oci_subnet_id)
