from gevent.server import StreamServer
from job import Job
from gevent.queue import Queue
import threading

q = Queue()

def dispatch_cmd(f, sock):
    cmd_line = f.readline()
    e = cmd_line.split(' ')
    if not e or len(e) < 1:
        sock.sendall('Bad Command: %s' % cmd_line)
        sock.close()
    cmd = e[0]
    if cmd == 'put':
        job_size = int(e[4])
        data = f.read(job_size + 2)
        #print 'get data: %s' % data.__repr__()
        if data[-2:] != '\r\n':
            sock.sendall('EXPECTED_CRLF\r\n')
            return
        data = data[:-2]
        j = Job(data)
        q.put(j)
        sock.sendall('INSERTED %d\r\n' % j.id)
    elif cmd == 'reserve\r\n':
        j = q.get()
        sock.sendall('RESERVED %d %d\r\n%s\r\n' % (j.id, len(j.data), j.data))
    else:
        sock.sendall('Not Implemented yet:%s\r\n'% cmd)

def handle_conn(sock, addr):
    print threading.current_thread().name, '=>New connection:', sock
    f = sock.makefile('r')
    while True:
        dispatch_cmd(f, sock)

if __name__ == '__main__':
    sockaddr = ('0.0.0.0', 4201)
    server = StreamServer(sockaddr, handle_conn)
    print 'Server listening @%s' % str(sockaddr)
    server.serve_forever()

    

