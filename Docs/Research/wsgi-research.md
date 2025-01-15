# WSGI

Web Server Gateway Interface is a specification that describes how web servers and python web applications communicate and 
how web applications can be chained together to process one request.
It is described in full in PEP 3333

WSGI itself is ONLY a specification that defines how server and application communicate.

In a broad sense WSGI server only receives the request from a client, passes it on to the application and then sends the response created by the application back to the client.

### Server interface

The Server must provide two things:
- An ```environ``` dictionary. It contains CGI like variables
- A ```start_response``` callable that takes as arguments the HTTP status string (e.g 200 OK) and ```response_headers``` containing a list of standard HTTP response headers
### Application interface

The WSGI application interface is implemented as a callable.
A callable can be a function, method, class or an instance that has a ```__call__()``` method.
The callable must take ```environ``` and ```start_response``` as arguments

### Middleware
WSGI compliant application can be stacked, called middleware.
Middleware must implement both the server and application interfaces plus a few other small details.
They should also be as transparent as possible.

## Benefits

One of the main benefits that was envisioned with the creation and adoption of WSGI was the decoupling of big monolithic frameworks into libraries to be used as WSGI middleware allowing developers to choose the best components for their needs.
It also removed the factor of selecting a framework based on what servers it can run on, as now most python web frameworks implement WSGI.

# [Gunicorn](https://docs.gunicorn.org/en/latest/design.html)
Gunicorn is a WSGI HTTP server.
It is based on the pre-fork worker model.
## Pre-fork worker model

The pre-fork Worker model is a concurrency model used to handle multiple client requests efficiently.
It works by forking worker processes from a main process **before** handling new requests.
 The master has no information about the individual clients, requests and responses are handled completely by worker processes.
These are the different types of worker processes.


## Master
The master listens to various signals and acts accordingly.
For example CHLD indicates that a child process has terminated and so the master restarts it.

## Sync worker
The default worker type.
Handles a single request at a time and, as such, errors should affect one request only.
Does not support persistent connections.

## Async worker
An implmentation of cooperative multi-threading, based on Greenlets.
Applications generally will not need to implement changes to their code to use these workers.
In the event a application wants to use full Greenlets, some code changes may be required

## GThread worker
A threaded worker.
Connections are accepted in the main loop and added to a thread pool as connection jobs.
Compatible with keepalive connections, they are put back into the pool waiting for an event until the keepalive timeout.
Using threads is also a good way of reducing memory usage as application code is shared by all threads.

## Tornado worker
Can be used to write applications with the tornado framework, capable of serving WSGI applications, altought this is not recommended.


## Choosing the worker

The default synchronous worker is not the best choice as blocking calls are made to the ProxmoxVE and GNS3 APIs, as well as tests done with nornir.
As such Async worker will be our choice as no changes to code are predicted.

## How many workers

To figure out the optimal amount of workers, testing is required.
As a starting point the formula (2 * #number_of_cores) + 1 is given as a rule of thumb, with load testing recommended to fine tune this value.

# Web server
It is generally recommended to use a WSGI server behind an HTTP proxy server when exposed to the internet.
The reasons are that WSGI are not typically optimized for static file handling, cannot handle HTTPS and SSL/TLS connections among a few other features that are typically implemented among HTTP servers, like NGINX or apache