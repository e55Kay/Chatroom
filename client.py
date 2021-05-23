from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter as tk
from tkinter import ttk

LARGEFONT =("Verdana", 15)
####burh 

class tkinterApp(tk.Tk):
     
    # __init__ function for class tkinterApp
    def __init__(self, *args, **kwargs):
         
        # __init__ function for class Tk
        tk.Tk.__init__(self, *args, **kwargs)
         
        # creating a container
        container = tk.Frame(self) 
        container.pack(side = "top", fill = "both", expand = True)
  
        container.grid_rowconfigure(0, weight = 1)
        container.grid_columnconfigure(0, weight = 1)
  
        # initializing frames to an empty array
        self.frames = {} 
  
        # iterating through a tuple consisting
        # of the different page layouts
        '''for F in (StartPage, Page1):
  
            frame = F(container, self)
  
            # initializing frame of that object from
            # startpage, page1, page2 respectively with
            # for loop
            self.frames[F] = frame
  
            frame.grid(row = 0, column = 0, sticky ="nsew")
  
        self.show_frame(StartPage)'''
        frame = StartPage(container)
        frame.grid(row = 0, column = 0, sticky ="nsew")
        frame.tkraise()
  
    # to display the current frame passed as
    # parameter
    '''def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()'''
  
# first window frame startpage
  
class StartPage(tk.Frame):
    def lol(self):
        print("lol")

    def connect(self, flag = 0):
        global HOST, PORT, con_flag

        if (flag == 0):
            HOST = self.serv_host.get()
            p = self.serv_port.get()
            PORT = int(p)

        con_flag = 1

        frame = Page1(self.control)

        #self.control.show_frame(Page1)
        frame.grid(row = 0, column = 0, sticky ="nsew")
        frame.tkraise()
        
    
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)

        self.control = parent
        # label of frame Layout 2
        label = ttk.Label(self, text ="CHATROOM", font = LARGEFONT)
         
        # putting the grid in its place by using
        # grid
        label.grid(row = 0, column = 2, padx = 10, pady = 10)

        host_label = ttk.Label(self, text = "Enter Host")
        host_label.grid(row = 2, column = 1, padx = 10, pady = 10)

        port_label = ttk.Label(self, text = "Enter Port")
        port_label.grid(row = 3, column = 1, padx = 10, pady = 10)

        #message_frame = tk.Frame(self)
        
        self.serv_host = tk.StringVar() 
        self.serv_host.set("")

        self.serv_port = tk.StringVar() 
        self.serv_port.set("")

        host_entry = tk.Entry(self, textvariable=self.serv_host)
        #entry_field.bind("<Return>", self.send)
        host_entry.grid(row = 2, column = 2, padx = 10, pady = 10)

        port_entry = tk.Entry(self, textvariable=self.serv_port)
        port_entry.bind("<Return>", self.connect)
        port_entry.grid(row = 3, column = 2, padx = 10, pady = 10)
  
        button1 = ttk.Button(self, text ="Connect",
        command = self.connect)
        #lambda : controller.show_frame(Page1))
     
        # putting the button in its place by
        # using grid
        button1.grid(row = 4, column = 1, padx = 5, pady = 5)
  
        ## button to show frame 2 with text layout2
        button2 = ttk.Button(self, text ="Connect to Local",
        command = lambda : self.connect(1))
     
        # putting the button in its place by
        # using grid
        button2.grid(row = 4, column = 3, padx = 10, pady = 10)
  
          
  
  
# second window frame page1
class Page1(tk.Frame):
    def receive(self):
        global quit_state
        while True:
            try:
                msg = self.client_socket.recv(BUFSIZ).decode("utf8")
                self.msg_list.insert(tk.END, msg)
                if msg == "!quit":
                    print("quit")
                    quit_state = 1
                    #print(quit_state)
                    self.client_socket.close()
                    #tk.Frame.destroy(self)
                    #self.control.destroy()
                    app.destroy()
                elif msg == "!discon":
                    self.client_socket.close()
                    tk.Frame.destroy(self)
            except OSError: 
                break
        '''while True:
            try:
                msg = self.client_socket.recv(BUFSIZ).decode("utf8")
                self.msg_list.insert(tk.END, msg)
            except OSError: 
                break'''

    def send(self,event=None):
        try:
            msg = self.my_msg.get()
            self.my_msg.set("")  
            self.client_socket.send(bytes(msg, "utf8"))
            #self.scrollbar.set(0.5,1)
            t,b = self.scrollbar.get()
            print(t,b)
            self.scrollbar.set(1,1)
            print(self.scrollbar.get())
            '''if msg == "{quit}":
            self.client_socket.close()
            #top.quit()'''
        except Exception as e:
            print("Lost connection to the chatroom")

    def disconnect(self, event=None):
        #self.client_socket.close()
        
        frame = StartPage(self.control)
        frame.grid(row = 0, column = 0, sticky ="nsew")
        frame.tkraise()
        #close connection

    def on_closing(self,event=None):
        global quit_state
        if (quit_state ==0):
            self.my_msg.set("{quit}")
            self.send()
        else:
            #print(quit_state)
            tk.Frame.destroy(self)
     
    def __init__(self, parent):
         
        tk.Frame.__init__(self, parent)
        self.control = parent
        #label = ttk.Label(self, text ="Page 1", font = LARGEFONT)
        #label.grid(row = 0, column = 4, padx = 10, pady = 10)
  
        # button to show frame 2 with text
        # layout2
        #button1 = ttk.Button(self, text ="StartPage",command = lambda : controller.show_frame(StartPage))
     
        # putting the button in its place
        # by using grid
        #button1.grid(row = 1, column = 1, padx = 10, pady = 10)
  
        # button to show frame 2 with text
        # layout2
        #button2 = ttk.Button(self, text ="Page 2",command = lambda : controller.show_frame(Page2))
     
        # putting the button in its place by
        # using grid
        #button2.grid(row = 2, column = 1, padx = 10, pady = 10)
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

        #print(scrollbar.get())
        
        disconnect_button = tk.Button(self, text="Disconnect", command=self.disconnect)
        disconnect_button.pack()

        global con_flag

        print(con_flag)
        
        if  (con_flag == 1):
            ADDR = (HOST, PORT)

            self.client_socket = socket(AF_INET, SOCK_STREAM)
            self.client_socket.connect(ADDR)

            receive_thread = Thread(target=self.receive)
            receive_thread.start()


'''top = tk.Tk()
top.title("Chatter")

messages_frame = tk.Frame(top)
my_msg = tk.StringVar() 
my_msg.set("Type here.")
scrollbar = tk.Scrollbar(messages_frame)

msg_list = tk.Listbox(messages_frame, height=15, width=50, yscrollcommand=scrollbar.set)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
msg_list.pack(side=tk.LEFT, fill=tk.BOTH)
msg_list.pack()
messages_frame.pack()

entry_field = tk.Entry(top, textvariable=my_msg)
entry_field.bind("<Return>", send)
entry_field.pack()
send_button = tk.Button(top, text="Send", command=send)
send_button.pack()

top.protocol("WM_DELETE_WINDOW", on_closing)
'''
BUFSIZ = 1024
quit_state = 0
'''HOST = input('Enter host: ')
PORT = input('Enter port: ')

if not PORT:
    PORT = 33000
else:
    PORT = int(PORT)'''
con_flag = 0

HOST = '127.0.0.1'
PORT = 33000

#tk.mainloop()
app = tkinterApp()
app.mainloop()
