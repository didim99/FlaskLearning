
cpdef int inversem(int a, int m):
    if a == 0:
        return 1
    cdef int x1 = 0
    cdef int x2 = 1
    cdef int y1 = 1
    cdef int y2 = 0
    cdef int m0 = m
    cdef int q, r, x, y

    while a > 0:
        q = m // a
        r = m - a * q
        x = x2 - q * x1
        y = y2 - q * y1
        m = a
        a = r
        x2 = x1
        y2 = y1
        x1 = x
        y1 = y

    if y2 < 0:
        y2 += m0
    return y2


cpdef int powm(int a, int b, int m):
    cdef int t
    if b == 0:
        return 1
    if b % 2 == 0:
        t = powm(a, b // 2, m)
        return mulm(t, t, m) % m
    else:
        return mulm(powm(a, b - 1, m), a, m) % m


cpdef mulm(int a, int b, int m):
    cdef int t
    if b == 1:
        return a
    if b % 2 == 0:
        t = mulm(a, b // 2, m)
        return (2 * t) % m
    else:
        return (mulm(a, b - 1, m) + a) % m
