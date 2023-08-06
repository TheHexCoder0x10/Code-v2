import JsonHandler
import socket


class WiFi:
    def __init__(self):
        self.Run = JsonHandler.getdata('/Assets/Settings.json')['online']
        self.s = socket.socket()
        self.s.bind(('127.0.0.1', 1234))
        self.s.listen()


    def Send(self, filename):
        with open(filename, "rb") as f:
            while True:
                bytes_read = f.read(4096)  # read the bytes from the file
                if not bytes_read: break  # file transmitting is done
                self.s.sendall(bytes_read)  # we use sendall to assure transmission in busy networks
                print(len(bytes_read))  # update the progress bar
        self.s.close()  # close the socket


    def Receive(self): pass

    def Connect(self): pass


    def Disconnect(self): pass


if __name__ == '__main__': WiFi.Send('C:/Code4Games/Pixel Code/Code/Assets/MEMES134.png')