from client_mqtt import run_mqtt
from api.server  import server_run
import threading

if __name__ == '__main__':
    thread1 = threading.Thread(target=server_run)
    thread2 = threading.Thread(target=run_mqtt)

    thread2.start()
    thread1.start()

    thread2.join()
    thread1.join()