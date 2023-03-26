This script will do the following:
- [x] get version from branch name
    - the name will be like: `feature/ALL-899-upgrade-goerli-prysm-to-v3.2.2`
- [x] verify the image exist in dockerhub
    - let's start with this, sometimes we weill have to build the image from binary
- [x] update image, push, get commit hash

- ref: https://github.com/hashicorp/nomad/pull/12591

- [x] get node in eu by hitting nomad api
- [x] add `!=` constraint for the node
- [x] scale down in eu (run the nomad job spec)

- [] take snapshot in that node (will have to ssh into the node and run the command)

- [] create new canary group in the nomad job spec with the new upgraded image
- [] add constraint for `==` node we used earlier
- [] scale up in eu (run the nomad job spec) with canary group

- [] verify the node is in sync, and healthchecks pass and all green
  - [] we might need to consult with Consul API

- [] if all is well
  - [] repeat this for one node in US
  - [] if all green, raise PR
  - [] once approved rollout deploy
  - [] either nomad job run
  - [] or tf apply
- [] else:
    - [] rollback to previous image in that node
