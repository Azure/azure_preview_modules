from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = """
    lookup: azure_keyvault_secret
    author:
        - Hai Cao <t-haicao@microsoft.com>
        - Daryl Banttari <dbanttari@gmail.com>
    version_added: 2.9
    requirements:
        - azure
        - msrest
        - msrestazure
        - azure-keyvault
    short_description: Reads secrets from Azure Key Vault.
    description:
        - This lookup fetches secrets from Azure Key Vault.
    options:
        _terms:
            description: Secret name or list of secret names. Secret version can be included like secret_name/secret_version.
            required: True
        vault_url:
            description: URL of your Azure Key Vault.
            required: True
    notes:
        - If a version is not provided, this plugin will return the latest version of the secret.
        - See Azure authentication guidance at https://docs.ansible.com/ansible/latest/scenario_guides/guide_azure.html#providing-credentials-to-azure-modules
"""

EXAMPLE = """
- name: Show secret using creds provided via either environment vars or `az login`.
  debug:
    msg: "the value of this secret is {{ lookup('azure_keyvault_secret', 'testSecret/version', vault_url='https://yourvault.vault.azure.net') }}"

- name: Show secret using explicitly-passed Service Principal creds
  vars:
    url: 'https://yourvault.vault.azure.net'
    secretname: 'testSecret/version'
    client_id: '123456789'
    secret: 'abcdefg'
    tenant: 'uvwxyz'
  debug:
    msg: "the value of this secret is {{ lookup('azure_keyvault_secret', secretname, vault_url=url, client_id=client_id, secret=secret, tenant=tenant) }}"

# Example below creates an Azure Virtual Machine with SSH public key from Key Vault
# using creds provided via either environment vars or `az login`.
- name: Create Azure VM
  hosts: localhost
  connection: local
  no_log: True
  vars:
    resource_group: myResourceGroup
    vm_name: testvm
    location: eastus
    ssh_key: "{{ lookup('azure_keyvault_secret','myssh_key') }}"
  - name: Create VM
    azure_rm_virtualmachine:
      resource_group: "{{ resource_group }}"
      name: "{{ vm_name }}"
      vm_size: Standard_DS1_v2
      admin_username: azureuser
      ssh_password_enabled: false
      ssh_public_keys:
        - path: /home/azureuser/.ssh/authorized_keys
          key_data: "{{ ssh_key }}"
      network_interfaces: "{{ vm_name }}"
      image:
        offer: UbuntuServer
        publisher: Canonical
        sku: 16.04-LTS
        version: latest
"""

RETURN = """
  _raw:
    description: secret content string
"""

from ansible.errors import AnsibleError
from ansible.plugins.lookup import LookupBase
from ansible.module_utils.azure_rm_common import AzureRMAuth
from azure.keyvault import KeyVaultClient
from azure.cli.core.adal_authentication import AdalAuthentication
from azure.common.credentials import get_azure_cli_credentials

KEYVAULT_RESOURCE_ID="https://vault.azure.net"

class LookupModule(LookupBase):

    def run(self, terms, inject=None, variables=None, **kwargs):

        vault_url = kwargs.pop('vault_url', None)
        if vault_url is None:
            raise AnsibleError("You must provide your Key Vault's url.")

        credentials = AzureRMAuth(**kwargs).azure_credentials
        # if doing`az login` auth (which returns an AdalAuthentication
        # object), we can't use the access token that AzureRMAuth fetches,
        # because that token doesn't support access to non-default `resource`
        # types (in this case "https://vault.azure.net"), so we need to
        # replace the gathered creds with resource-appropriate creds
        if isinstance(credentials, AdalAuthentication):
            credentials, subscription_id = get_azure_cli_credentials(resource=KEYVAULT_RESOURCE_ID)

        client = KeyVaultClient(credentials)

        ret = []
        for term in terms:
            try:
                ret.append(client.get_secret(vault_url, term, '').value)
            except Exception as e:
                raise AnsibleError('Failed to fetch secret {}: {}'.format(term, str(e)))
        return ret
