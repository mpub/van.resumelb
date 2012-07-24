from zc.resumelb.lb import Pool as _Pool

class Pool:
    """A Pool which groups workers up by version

    This pool requires that the classifier return a tuple of (version, class).
    It will return workers only if the class matches.

    Load balancing on the workers within a specific version uses the normal
    algorithm.
    """

    def __init__(self, **pool_settings):
        self._pool_settings = pool_settings
        self._updated_settings = pool_settings
        self._pools = {}

    @property
    def backlog(self):
        return sum([p.backlog for p in self._pools.values()])

    def _new_pool(self, version):
        assert version not in self._pools
        p = _Pool(**self._pool_settings)
        p.update_settings(self._updated_settings)
        self._pools[version] = p
        return p

    def new_resume(self, worker, resume):
        pool = self._pools.get(worker.version)
        if pool is None:
            pool = self._new_pool(worker.version)
        pool.new_resume(worker, resume)

    def get(self, rclass, timeout=None):
        version = None
        try:
            version, rclass = rclass
        except ValueError:
            assert isinstance(rclass, basestring)
        pool = self._pools.get(version)
        if pool is None:
            pool = self._new_pool(version)
        worker = pool.get(rclass, timeout)
        assert worker is None or worker.version == version
        return worker

    def update_settings(self, settings):
        self._updated_settings = settings
        for pool in self._pools.values():
            pool.update_settings(settings)

    def __repr__(self):
        out = ['Versioned Pool']
        out.append('  sub-pools: %s' % len(self._pools))
        out.append('  backlog: %s' % self.backlog)
        for version, pool in sorted(self._pools.items()):
            out.append('Sub-Pool: %s' % (version, ))
            for l in repr(pool).splitlines():
                out.append('  %s' % l)
        if not out:
            return 'Emtpy VersionedPool'
        return '\n'.join(out)

    def remove(self, worker):
        pool = self._pools.get(worker.version)
        pool.remove(worker)

    def put(self, worker):
        pool = self._pools.get(worker.version)
        pool.put(worker)

    def status(self):
        pools = {}
        result = dict(backlog=self.backlog, sub_pools=pools)
        for name, p in self._pools.items():
            # Use status if ever committed here
            pools[name] = dict(
                    backlog=p.backlog,
                    mean_backlog=p.mbacklog,
                    workers = [
                        dict(name=worker.__name__,
                            backlog=worker.backlog,
                            mbacklog=worker.mbacklog,
                            oldest_time=(int(worker.oldest_time)
                                            if worker.oldest_time else None),
                            version=worker.version
                            )
                        for worker in sorted(
                            p.workers, key=lambda w: w.__name__)
                        ])
        return result
