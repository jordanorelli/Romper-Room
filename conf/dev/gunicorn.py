import multiprocessing

bind = 'unix:/var/tmp/romper-room.sock'
pidfile = '/var/tmp/romper-room.pid'

worker = multiprocessing.cpu_count() + 1
