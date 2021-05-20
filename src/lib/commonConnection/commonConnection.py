
class CommonConnection:
    def sendACK(socket, host, port, mode, filename, lastBytesReceived):
        addr = (host, port)
        message = 'A'+mode+filename+';'+str(lastBytesReceived)
        try:
            socket.sendto(message.encode(), addr)
        except socket.error:
            return
        return

    def sendError(socket, host, port):
        addr = (host, port)
        try:
            socket.sendto('F'.encode(), addr)
        except socket.error:
            return
        return

    def sendEndFile(socket, host, port, filename, lastBytesReceived):
        addr = (host, port)
        message = 'E'+filename
        try:
            socket.sendto(message.encode(), addr)
        except socket.error:
            return
        return

    def sendMessage(socket, host, port, filename, message, lastBytesReceived):
        addr = (host, port)
        data = 'T'+filename+";"+str(lastBytesReceived)+";"+message
        try:
            socket.sendto(data.encode(), addr)
        except socket.error:
            return
        return
