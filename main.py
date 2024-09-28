from http_server import run_http_server
from socket_server import run_socket_server
from multiprocessing import Process

if __name__ == "__main__":
    socket_server_process = Process(target=run_socket_server)
    socket_server_process.start()
    
    http_server_process = Process(target=run_http_server)
    http_server_process.start()
    
    http_server_process.join()
    socket_server_process.join()
