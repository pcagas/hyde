# Design and Implementation of Hyde

Hyde is a web (browser) based UX for Gkeyll. Although Hyde can be run
on local machines, its key goal is to allow global access to the code
via the WWW.

Hyde depends on the following packages:

- Gkeyll 2.0
- postgkyl
- flask
- zeromq
- redis
- Vue (https://vuejs.org)

Vue.js will be used to build the web client-side code.

## Data storage policy

All persistent data (except simulation output) is stored in redis. No
data that must persist and is shared shall be stored in an object, but
only in Redis. Python objects will provide methods to CRUD (Create,
Retrive, Update Delete) these data. This indirection allows
maintaining a consistent state for each object.

Simulation output will be stored on-disk in the usual way.

## Communication with Gkeyll

There will be two types of communiation with G2. First, a in-memory G2
instance will be created for each connection. This will allow user to
run code in an interactive way. The second will be a batch mode in
which the input file is run throught G2, potentially in parallel on a
remote machine (different than the server).

The communication will be performed with ZeroMQ and Redis pub/sub.

## User object

The User object stores all information about a user. Guest users are
allowed, although there is no data persistence for guest user. (That
is, once a guest user closes the browser, all server-side data is
deleted).

Each User has the following data stored for it:

- User group (allowing previledge access to features/machies)
- List of examples (User can add/remove from this list)
- List of user specific templates
- List of simulations performed
- List of currently running simulations
