# Modules

Bundled with the project, you will find already implemented tests.

To use modules, call the respective constructor, passing the already built nornir configuration file for that specific machine/project followed by calling the "command" function, giving it the necessary arguments, as these may vary.

## Implementing a new module

To implement a module you may create a new class that inherits the methods in the ```CommandLibrary``` class found in "modules/module.py"

Then you must provide your own implementation of the following methods:

- ```_command_router```
- ```_command_switch```
- ```_command_vpcs```
- ```_command_linux```
- ```interpret_cisco_response```
- ```interpret_linux_response```
- ```interpret_vpcs_response```

For the "_command*" family of methods, you may look in "PingLibrary" to obtain a skeleton, replacing the command string with your own.

For the "interpret*" family of methods, you have to implement code that, given the output of the command ran on the machine, can identify if the result is what is expected or not.

You may also implement a module from scratch, if you see fit.

## Ping

### Arguments

``` command(source, destination) ```

- source: Name of the host to run the command on
- destination: IP Address of the host to ping

Will return true if packet loss is higher than ( 100 - TOLERANCE ) 
TOLERANCE is defined in constants.py

## Traceroute

### NOT FINISHED