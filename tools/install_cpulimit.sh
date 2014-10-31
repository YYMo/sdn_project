//Install cpulimit in ubuntu
sudo apt-get install cpulimit

//Synopsis
cpulimit TARGET [OPTIONS...]

//Description::TARGET must be exactly one of these:

-p, --pid=N pid of the process

-e, --exe=FILE name of the executable program file

-P, --path=PATH absolute path name of the executable program file

//OPTIONS

-l, --limit=N percentage of CPU allowed from 0 to 100 (mandatory)

-v, --verbose show control statistics

-z, --lazy exit if there is no suitable target process, or if it dies

-h, --help display this help and exit

//examples
# cpulimit -p 1234 -l 50
# cpulimit -P /usr/bin/foo -l 50
# cpulimit -e foo -l 50
