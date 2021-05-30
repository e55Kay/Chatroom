from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter as tk
from tkinter import ttk
import tkinter.messagebox

LARGEFONT =("Verdana", 15)

#class for the tkinter GUI application

class tkinterApp(tk.Tk):
     
    def __init__(self, *args, **kwargs):
         
        tk.Tk.__init__(self, *args, **kwargs)
         
        # creating a container
        container = tk.Frame(self) 
        container.pack(side = "top", fill = "both", expand = True)
  
        container.grid_rowconfigure(0, weight = 1)
        container.grid_columnconfigure(0, weight = 1)
  
        # initializing frames to an empty array
        self.frames = {} 
  
        frame = StartPage(container)
        frame.grid(row = 0, column = 0, sticky ="nsew")
        frame.tkraise()
  
# connection window frame startpage
  
class StartPage(tk.Frame):

    #function to connect to server

    def connect(self, flag = 0):
        global HOST, PORT, con_flag

        if (flag == 0):
            HOST = self.serv_host.get()
            p = self.serv_port.get()
            PORT = int(p)

        con_flag = 1

        frame = Page1(self.control)

        frame.grid(row = 0, column = 0, sticky ="nsew")
        frame.tkraise()
        
    #Start window structure
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)

        self.control = parent
        
        label = ttk.Label(self, text ="CHATROOM", font = LARGEFONT)
         
        label.grid(row = 0, column = 2, padx = 10, pady = 10)

        host_label = ttk.Label(self, text = "Enter Host")
        host_label.grid(row = 2, column = 1, padx = 10, pady = 10)

        port_label = ttk.Label(self, text = "Enter Port")
        port_label.grid(row = 3, column = 1, padx = 10, pady = 10)
        
        self.serv_host = tk.StringVar() 
        self.serv_host.set("")

        self.serv_port = tk.StringVar() 
        self.serv_port.set("")

        #entry fields
        
        host_entry = tk.Entry(self, textvariable=self.serv_host)
        
        host_entry.grid(row = 2, column = 2, padx = 10, pady = 10)

        port_entry = tk.Entry(self, textvariable=self.serv_port)
        port_entry.bind("<Return>", self.connect)
        port_entry.grid(row = 3, column = 2, padx = 10, pady = 10)

        #buttons on start page
        
        button1 = ttk.Button(self, text ="Connect",
        command = self.connect)
        
        button1.grid(row = 4, column = 1, padx = 5, pady = 5)
  
        button2 = ttk.Button(self, text ="Connect to Local",
        command = lambda : self.connect(1))
     
        button2.grid(row = 4, column = 3, padx = 10, pady = 10)

  
# Main window frame
class Page1(tk.Frame):

    #recieves messages from the server
    def receive(self):
        global quit_state
        while True:
            try:
                msg = self.client_socket.recv(BUFSIZ).decode("utf8")
                self.msg_list.insert(tk.END, msg)
                if msg == "!quit":
                    print("quit")
                    quit_state = 1
                    self.client_socket.close()
                    app.destroy()
                elif msg == "!discon":
                    self.client_socket.close()
                    tk.Frame.destroy(self)
            except OSError: 
                break

    #sends messages to the server
    def send(self,event=None):
        try:
            msg = self.my_msg.get()
            self.my_msg.set("")  
            self.client_socket.send(bytes(msg, "utf8"))
           
        except Exception as e:
            print("Lost connection to the chatroom")
            tk.Frame.destroy(self)


    #for disconnecting from the sever
    def disconnect(self, event=None):
        self.my_msg.set("!discon")
        self.send()

    #function called when application closed using close window button
    def on_closing(self,event=None):
        if tk.messagebox.askokcancel("Warning", "Are you sure to close the application"):
            global quit_state
            if (quit_state ==0):
                self.my_msg.set("!quit")
                self.send()
            else:
                tk.Frame.destroy(self)

    #Main window structure
    def __init__(self, parent):
         
        tk.Frame.__init__(self, parent)
        self.control = parent
        
        messages_frame = tk.Frame(self)
        self.my_msg = tk.StringVar() 
        self.my_msg.set("")
        self.scrollbar = tk.Scrollbar(messages_frame)

        self.msg_list = tk.Listbox(messages_frame, height=15, width=50, yscrollcommand=self.scrollbar.set)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.msg_list.pack(side=tk.LEFT, fill=tk.BOTH)
        self.msg_list.pack()
        self.scrollbar.config(command = self.msg_list.yview)
        
        messages_frame.pack()

        entry_field = tk.Entry(self, textvariable=self.my_msg)
        entry_field.bind("<Return>", self.send)
        entry_field.pack()
        
        send_button = tk.Button(self, text="Send", command=self.send)
        send_button.pack()
        
        disconnect_button = tk.Button(self, text="Disconnect", command=self.disconnect)
        disconnect_button.pack()

        app.protocol("WM_DELETE_WINDOW", self.on_closing)

        global con_flag

        #print(con_flag)

        #creating socket
        if  (con_flag == 1):
            ADDR = (HOST, PORT)

            try:
                self.client_socket = socket(AF_INET, SOCK_STREAM)
                self.client_socket.connect(ADDR)

            except Exception as e:
                tk.messagebox.showerror("ERROR", "Unable to connect")
                #app.destroy()
                
            #creating threads for multiple incoming messages
            receive_thread = Thread(target=self.receive)
            receive_thread.start()


#global variables

BUFSIZ = 1024
quit_state = 0

con_flag = 0

HOST = '127.0.0.1'
PORT = 33000

#executing the application
app = tkinterApp()
app.mainloop()
