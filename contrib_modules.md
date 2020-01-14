
# Pangea Contrib Modules

Contrib modules are sub-programs designed to add optional, non-core, functionality to pangea. Their source code exists in a separate folder in the repositories.

## Example Contrib Modules

These are some examples of what contrib modules could be used for
 - a blogging extension
 - an API that searches taxonomic profiles from metagenomes for specific species
 - an API that 'aliases' a request to another bioinformatics service
 - a pipeline specific scheduler, like the luigi scheduler
 - a jupyter notebook server


## Basic Rules for Contrib Modules

Most of these rules are soft rules which won't be enforced in code

 - Contrib modules should be optional and configurable at deploy
 - Contrib modules will define a `module_name`
 - Contrib modules can make SQL tables and have rwx for tables they create
 - Contrib modules have r-- priveleges for core pangea tables
 - Contrib modules have no privileges for other contrib module tables (maybe?)
 - Contrib modules may define API endpoints under a `<url>/api/contrib/<module_name>` prefix
