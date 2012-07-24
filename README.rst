Pool for zc.resumelb to divide workers by version
=================================================

This module contains a pool class which uses the classifier to route
requests to multiple sub-pools of workers. Each sub-pool works like a
normal zc.resumelb pool but only on workers of a single version.

The classifier will decide which of the sub-pools will serve the request
by returning a tuple (version, classifier). This request will be served
by a sub-pool containing only workers of a matching version.

Usage
=====

At the current time, the only way is to monkey patch the zc.resumelb.lb.Pool class
Like this:

      >>> from van.resumelb import Pool
      >>> import zc.resumelb.lb
      >>> zc.resumelb.lb.Pool = Pool

WARNING: you must pass --single-version to the loadbalancer startup
script.  If you do not, all the workers will have a version of None.

In the future it should be possible to set the Pool class on the command
line. The code to enable command-line overriding of the pool is awaiting
merging at:

    http://zope3.pov.lt/trac/browser/zc.resumelb/branches/jinty-external-pool/
