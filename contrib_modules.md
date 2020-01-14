
# Pangea Extension Modules

Extension modules are sub-programs designed to add optional, non-core, functionality to pangea. Their source code exists in a separate folder in the repositories.

## Example Extension Modules

These are some examples of what extension modules could be used for
 - a blogging extension
 - an API that searches taxonomic profiles from metagenomes for specific species
 - an API that 'aliases' a request to another bioinformatics service
 - a pipeline specific scheduler, like the luigi scheduler
 - a jupyter notebook server


## Basic Rules for Extension Modules

Most of these rules are soft rules which won't be enforced in code

 - Extension modules should be optional and configurable at deploy
 - Extension modules will define a `module_name`
 - Extension modules can make SQL tables and have rwx for tables they create
 - Extension modules have r-- priveleges for core pangea tables
 - Extension modules have no privileges for other Extension module tables (maybe?)
 - Extension modules may define API endpoints under a `<url>/api/ext/<module_name>` prefix

## Extension Modules on the Server

The server will define a core api endpoint listing the currently enabled extension modules.

## Extension Modules on the Client

Extension modules may define React components. These components may reference (link to) other components within the same extension module and core components but may not link to other extension modules. Analagously extansion modules should only call the core Pangea API or their corresponding extension API on the backend.

Each extension module should define one entry point screen which will be listed by the core app if the extension is enabled. All other screens in the extension module should be reachable from this screen.


