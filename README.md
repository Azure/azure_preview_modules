Azure.azure_preview_modules
=========

This role is the most complete and includes all the latest Azure modules. The update and bug fix are done in a more timely manner than official Ansible release.

If you use Ansible for Azure resource provisioning purpose, you're strongly encouraged to install this role. 

Prerequisite
------------

The usage of this role assumes that you've already setup an Ansible environment for Azure. For details, please refer to Ansible tutorial [Getting Started with Azure](http://docs.ansible.com/ansible/latest/guide_azure.html)


Installation
------------

1. Install the role

  ``` bash
  $ ansible-galaxy install Azure.azure_preview_modules
  ```

2. Install Azure Python SDK Dependencies

    Note: Instructions below apply to Ansible version 2.4 or earlier. If version of your Ansible is 2.5.0 or later, you shouldn't need to install any additional dependencies.

    Several reasons for installing Python SDKs are listed here.

    - New module is added to the role and this module is for one new Azure service, which is not part of existing Ansible release yet. Corresponding SDK of this new service needs to be installed.

    - Newer versions of SDKs introduce breaking API change. One specific working version should be installed here.

    The required SDKs are listed in the *[~/files/requirements-azure.txt](files/requirements-azure.txt)* file. The tricky part is the installation location, which has to be the same as where existing Azure Python SKDs are installed.

    Taking Ubuntu for example, the existing SDKs may be located in folders like
    `/home/your-user-name/.local/lib/python2.7/site-packages` or `/usr/local/lib/python2.7/dist-packages`. The former is an user folder and the later is a system folder, which requires sudo access. This depends on how you have installed `ansible`. In short, you should install the SDKs the same way as you installed `ansible` so that the SDKs are in the same `site-packages` folder.

    On macOS, the path of `site-packages` folder can be like `/Users/your-user-name/Library/Python/2.7/lib/python/site-packages` or `/Library/Python/2.7/site-packages`. Similar to Ubuntu, the former is an user folder and the later is a system folder.

    One way to figure out the correct `site-packages` path is to check the details of existing packages, say `azure-mgmt-storage` by running below command.

      ``` bash
      $ pip show azure-mgmt-storage
      ```

    The output can be like below. 

    ``` bash
    your-user-name@ansible:~$ pip show azure-mgmt-storage
    Name: azure-mgmt-storage
    Version: 1.5.0
    Summary: Microsoft Azure Storage Management Client Library for Python
    Home-page: https://github.com/Azure/azure-sdk-for-python
    Author: Microsoft Corporation
    Author-email: azpysdkhelp@microsoft.com
    License: MIT License
    Location: /home/your-user-name/.local/lib/python2.7/site-packages
    Requires: azure-common, azure-mgmt-nspkg, msrestazure
    ```

    From the information above you can learn that the SDKs are installed in *user* `site-packages` folder and use below command to install the listed packages. The `requirements-azure.txt` file can be found in the installed role folder, which is usually at `~\.ansible\roles` folder.

    ``` bash
    pip install --user -r files/requirements-azure.txt
    ```

Role Variables
--------------

No.

Dependencies
------------

No dependencies on other roles.

Example Playbook
----------------

    - hosts: localhost
      roles:
        - { role: Azure.azure_preview_modules }
      tasks:
      - name: create storage account
        azure_rm_storageaccount:
          resource_group: resourcegroupname
          name: storagename
          account_type: Standard_LRS

License
-------
MIT
