# project-2-project2-20
project-2-project2-20 created by GitHub Classroom

## Background
We are creating a RESTful API to hold a registry of trustworthy modules.

## Tools
We used the Django REST framework as the framework for the actual API, and Python for the new metric.

## Endpoints
**/packages** 
GET a list of all packages

**/reset**
DELETE all packages and all users except for the default user

**/package/<int:id>**
GET, PUT, DELETE packages by their ID (and PUT only if the new package is ingestible

**/package** 
POST a new package

**/package/<int:id>/rate**
GET rating for a package with a particular ID

**/authenticate**
returns HTTP 501, but we still have authentication through a login and Django User Permissions

**/package/byName/<str:name>**
GET or DELETE packages with the name specified

**/users**
GET a list of all users or POST a new user. (Only allowed for people with admin privileges).

