import random
import string

is_pre = lambda n: '0' + str(n) if n < 10 else str(n)

rb64 = lambda : ''.join(random.choice(string.ascii_letters + string.digits) for i in range (764)) + "=="

rint= lambda : random.randint(1, 6)

rn = lambda min, max: is_pre(random.randint(min, max)) 

rd = lambda: '{y}-{m}-{d}T{h}:{mi}:{s}.{ms}Z'.format(y=rn(2019, 2020), m=rn(1,12), d=rn(1, 28), h=rn(1, 12), mi=rn(0,59), s=rn(0, 59), ms=rn(0, 999))

rb = lambda : random.choice([True, False])

rip = lambda : '.'.join([str(random.randint(0, 255)) for i in range(4)])

rh = lambda h: ''.join(random.choice(string.hexdigits[:-6]) for l in range(h))

rw = lambda n:''.join(random.choice(string.ascii_lowercase) for l in range(n))

rs = lambda : random.choice(['pending', 'accepted', 'rejected'])

ri = lambda: random.choice(['raspbian', 'arch', 'debian', 'ubuntu'])

rt = lambda : '-'.join([rh(8), rh(4), rh(4), rh(4), rh(12)]) 

r_mac = lambda: ':'.join([rh(2) for i in range(6)])

rf = lambda: ':'.join([rh(2) for i in range(16)])

r_name = lambda: '-'.join([rh(2) for i in range(6)])

