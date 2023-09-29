# Documentation.
This guide defines how any contributors is expected to interact with this project

## Setting up Work Space
For anyone that has been added as a contributor to this project

- Clone Repository
The easiest way to clone this repo to ease contribution is to do so with your access token

``` 
git clone https://<access-token>@github.com/Idris01/AirBnB_clone_v3.git

```
To generate an access token [here](https://github.com/settings/tokens)

- WorkFlow
  - You can only contribute using a featured branch, and you should create it by checking out
from the `development` branch as follows;
```
git checkout development
git checkout -b <feature-branch-name>
```
Note: The `feature-branch-name` must be unique to you for all you contributions.

  - All pull requests must be made to the development branch, (not the master branch).
    - Always request for a review
  - The `master` branch is only updated through the development branch, when requirements are met based on the milestones.

  - Always update your local environemnt using the development branch

```
git checkout development
git pull
git checkout <feature-branch-name>
git merge development
```
