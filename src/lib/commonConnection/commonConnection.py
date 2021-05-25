from lib.constants import Constants


class CommonConnection:

    def sendACK(socket, host, port, mode, filename, lastBytesReceived):
        addr = (host, port)
        message = 'A'+mode+filename+';'+str(lastBytesReceived)
        try:
            socket.sendto(message.encode(), addr)
        except socket.error:
            return
        return

    def sendError(socket, filename, host, port):
        addr = (host, port)
        msg = 'F'+filename
        try:
            socket.sendto(msg.encode(), addr)
        except socket.error:
            return
        return msg

    def sendEndFile(socket, host, port, filename, bytesAlreadyReceived):
        addr = (host, port)
        message = 'E'+filename
        try:
            socket.sendto(message.encode(), addr)
        except socket.error:
            return
        return message

    def sendMessage(socket, host, port, filename, message, bytesReceived):
        addr = (host, port)
        data = Constants.fileTransferProtocol() + filename + ";"
        data += str(bytesReceived) + ";"
        data = data.encode() + message
        try:
            socket.sendto(data, addr)
        except socket.error:
            return
        return data.decode()

    def receiveMessageFromServer(socket, addr, recvsMsg):
        data, addr = socket.recvfrom(Constants.bytesChunk())
        message = data.decode()
        recvsMsg[message + '-' + str(addr[0]) + '-' + str(addr[1])] = True
        return message
