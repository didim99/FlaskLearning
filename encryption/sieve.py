# Sieve of Eratosthenes
# Code by David Eppstein, UC Irvine, 28 Feb 2002
# http://code.activestate.com/recipes/117119/


class SieveEratosthenes(object):
    # Maps composites to primes witnessing their compositeness.
    # This is memory efficient, as the sieve is not "run forward"
    # indefinitely, but only as long as required by the current
    # number being tested.
    #
    D = {}
    primes = []

    def get(self, index: int):
        return self.primes[index]

    def get_size(self):
        return len(self.primes)

    def get_last(self):
        if len(self.primes) == 0:
            return 0
        return self.primes[len(self.primes) - 1]

    def fill(self, max_value):
        gen = self.gen_primes()
        while self.get_last() < max_value:
            self.primes.append(next(gen))

    def gen_primes(self):
        """ Generate an infinite sequence of prime numbers.
        """

        # The running integer that's checked for primeness
        q = 2

        while True:
            if q not in self.D:
                # q is a new prime.
                # Yield it and mark its first multiple that isn't
                # already marked in previous iterations
                #
                yield q
                self.D[q * q] = [q]
            else:
                # q is composite. D[q] is the list of primes that
                # divide it. Since we've reached q, we no longer
                # need it in the map, but we'll mark the next
                # multiples of its witnesses to prepare for larger
                # numbers
                #
                for p in self.D[q]:
                    self.D.setdefault(p + q, []).append(p)
                del self.D[q]

            q += 1
