Azure.azure_preview_modules
=========

The role includes the most compelete and latest Azure modules for Ansible users. The update and bug fix are done in a more timely mannaer than official Ansible release. 

If you use Ansible for Azure resource provisioning purpose, you're strongly encouraged to install this role. 

Prerequisite
------------

The usage of this role assumes that you've already setup an Ansible environemnt for Azure. For details, please reference Ansible tutorial [Getting Started with Azure](http://docs.ansible.com/ansible/latest/guide_azure.html)


Installation
------------

1. Install the role.

  ``` bash
  $ ansible-galaxy install Azure.azure_preview_modules
  ```

2. Install Azure Python SDKs.

    Several reasons for installing Python SKDs here.

    - New module is added to the role and this module is for one new Azure service, which is not part of existing Ansible release yet. Corresponding SDK of this new service needs to be installed.

    - Newer version of SDK introduces breaking API change. One specific working version should be installed here.

    The required SDKs are listed in the *[~/files/requirements-azure.txt](files/requirements-azure.txt)* file. The tricky part is the install location, which has to be the same as where existing Azure Python SKDs installed. 

    Taking Ubuntu for example, the existing SDKs can be in folders like
    `/home/your-user-name/.local/lib/python2.7/site-packages` or `/usr/local/lib/python2.7/dist-packages`. The former is a user folder and the later is a system folder, which requires sudo access. This depends on how you have installed `ansible`. In short, you should install the SDKs the same way as you're installing `ansible` so that the SDKs are in the same `site-packages` folder. 

    One trick to figure out the correct `site-packages` path is to check the info of existing package, say `azure-mgmt-storage` by running below command.

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

    So, you know that the SDKs are installed in *user* `site-packages` folder. Then, we can use below command to install the listed packages. You can find the `requirements-azure.txt` file in your installed role folder, which is usually at `~\.ansible\roles` folder.

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
