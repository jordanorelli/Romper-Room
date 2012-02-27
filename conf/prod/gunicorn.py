import multiprocessing

bind = 'unix:/var/tmp/romper.sock'
pidfile = '/var/tmp/romper.pid'

workers = multiprocessing.cpu_count() + 1
