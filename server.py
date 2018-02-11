import sys, asyncio

################
# Server class #
################

class Server:
    default_server_address = '127.0.0.1'
    default_server_port = 8888

    # NOTE: you can modify __init__
    def __init__(self,server_address=default_server_address,server_port=default_server_port):
        self.address = server_address
        self.port = server_port
        self.all_clients = set([])
        self.currentClients = []
    
    def check_usernames(self, new_username):  #Checks if the username is already in the list.
        usernamelist = get_registered_usernames_list(self)
        length = len(usernamelist)
        for i in range (0, length - 1):
            if usernameList[i] == new_username:
               return(True);
        pass
    
    # NOTE: the following method must be implemented for some of our grading tests to work. I you don't implement this method correctly, you will lose some marks!
    # method for registering usernames 
    def set_username(self,new_username):
        if check_usernames(new_username):
            print ("Client already in use")
        else:
            self.currentClients.add(new_username)
            userName = new_username
        return(userName)
        pass
    
    # NOTE: this method must be implemented for some of our grading tests to work. If you don't implement this method correctly, you will lose some markethod that the registered usernames as a list

    
    def get_registered_usernames_list(self):
        return self.currentClients
        pass

    # NOTE: you can modify the implementation of handle_connection (but not its signature)
    @asyncio.coroutine
    def handle_connection(self, reader, writer):
        self.all_clients.add(writer)
        client_addr = writer.get_extra_info('peername')
        print('New client {}'.format(client_addr))
        while True:
            data = yield from reader.read(100)
            if data == None or len(data) == 0:
                break
            
            message = data.decode()
            print("Received {} from {}".format(message, client_addr))
            
            for other_writer in self.all_clients:
                if message[:16] == '@server set_name':
                    string = message[17:len(message)-1]
                    print(string)
                    self.set_username(string)
                    print(self.currentClients)
                if other_writer != writer:
                    new_message = '{}: {}'.format(client_addr,data)
                    other_writer.write(new_message.encode())
                    yield from other_writer.drain()        
        print("Closing connection with client {}".format(client_addr))
        writer.close()
        self.all_clients.remove(writer)

    # NOTE: do not modify run
    def run(self):
        loop = asyncio.get_event_loop()
        coro = asyncio.start_server(self.handle_connection,self.address,
                                                    self.port,loop=loop)
        server = loop.run_until_complete(coro)

        print('Serving on {}'.format(server.sockets[0].getsockname()))
        try:
            loop.run_forever()
        except KeyboardInterrupt:
            print('\nGot keyboard interrupt, shutting down',file=sys.stderr)
        
        for task in asyncio.Task.all_tasks():
            task.cancel()
        server.close()
        loop.run_until_complete(server.wait_closed())
        loop.close()    


# NOTE: do not modify the following two lines
if __name__ == '__main__':
    Server().run()

