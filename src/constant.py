version = '0.4'

help_info = '\
optional arguments:\n\
help                               get help for ruyibuild command\n\
version                            print the program version\n\
init -d <dir> [-f <yaml_dir>]      initialize an ruyibuild working directory\n\
update                             pull docker image, download package source code and download build script\n\
generate [<name>]                  if there is no <name>, run and enter a docker container, or run a docker container, then build and packaging in container, package name is <name>\n\
destroy                            destroy docker container\n\
'