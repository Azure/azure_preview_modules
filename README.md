This `integration` branch is for internal usage only. The purpose is to automate the workflow of merging Azure module related changes from Ansible repository to this repository. 

The Travis CI has been setup to run the automation once every week. The CI can also be triggered manually in the Travis portal. 

Steps to trigger the automation:

- Go to travis [link](https://travis-ci.org/Azure/azure_preview_modules/branches) for `azure_preview_modules`.
- Find `integration` branch and click latest build.
- There is a `Restart Build` in the build detail page. 

If there are new changes from Ansible repository, a new pull request will be created against `master` branch in `azure_preview_modules` repository. And the PR will trigger CI for testing. No changes, no PR.

Repository owner can decide the next step, given the CI result of the new PR.
