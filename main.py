import csv
import tkinter as tk
import sys
from os.path import exists
from tkinter import ttk, messagebox, simpledialog
from tkinter import *
from datetime import datetime



# Define a class to represent a ticket
class Ticket:
    # Initialize the ticket with a description, priority, and an empty list of work notes
    def __init__(self, ticketNumber, name, status, service, email, description):
        self.description = description
        self.ticketNumber = ticketNumber
        self.name = name  # need to be implemented
        self.email = email  # needs to be implemented
        self.service = service  # needs to be implemented
        self.status = status
        self.work_notes = []

    # Define a method to print the ticket
    def __str__(self):
        return f"Ticket: {self.ticketNumber}, {self.name}, {self.status}, {self.email}, {self.service} {self.description}, Work Notes: {self.work_notes}"

    # Define a method to add a work note to the ticket
    def add_work_note(self, text):
        # Get the current time and date
        if self.status == "NEW" and text != "Ticket Opened":
            self.status = "ACTIVE"
        now = datetime.now()
        timestring = now.strftime("%d/%m/%Y %H:%M:%S")
        fullticket = str(timestring + " -----> " + text)
        # Add the work note and the current time and date to the list of work notes
        self.work_notes.append(fullticket)

    def add_work_note_no_time(self, text):
        # Get the current time and date
        # Add the work note and the current time and date to the list of work notes
        self.work_notes.append(text)

class TicketWindow(Frame):
    def __init__(self, ticket, master=None):
        Frame.__init__(self, master)
        self.master = master
        self.ticket = None


    def view_ticket(self):
        # self.title(ticket.ticketNumber)
        # self.resizable(False, False)

        # Create a label with the ticket number
        for widget in self.winfo_children():
            widget.destroy()
        number_label = tk.Label(self, text=f"Ticket Number: {self.ticket.ticketNumber}")

        # Create a label with the ticket priority
        name_label = tk.Label(self, text=f"Customer Name: {self.ticket.name}")

        email_label = tk.Label(self, text=f"Customer email: {self.ticket.email}")

        service_label = tk.Label(self, text=f"Customer service: {self.ticket.service}")

        # Create a label with the ticket description
        description_label = tk.Label(self, text=f"Description: {self.ticket.description}")

        # Create a label with the ticket status
        self.status_label = tk.Label(self, text=f"Status: {self.ticket.status}")

        # Create a text area for displaying the work notes
        self.work_notes_text = tk.Text(self)


        # Add the work notes to the text area
        for work_note in self.ticket.work_notes:
            self.work_notes_text.insert('end', work_note + "\n")

        self.work_notes_text['state'] = 'disabled'

        # Create a button for updating the ticket status
        self.status_button = tk.Button(self, text="Update Status", command=self.update_status)

        # Create a button for adding a work note
        self.work_note_button = tk.Button(self, text="Add Work Note", command=self.add_work_note)

        self.close_ticket_button = tk.Button(self, text="Close Ticket", command=self.close_ticket)

        number_label.grid(row=0, column=0)
        name_label.grid(row=1, column=0)
        service_label.grid(row=0, column=1)
        email_label.grid(row=2, column=0)
        description_label.grid(row=2, column=1)
        self.status_label.grid(row=1, column=1)
        self.close_ticket_button.grid(row=3,column=1)
        self.work_notes_text.grid(row=4, column=0, columnspan=2)
        self.status_button.grid(row=3, column=0)
        self.work_note_button.grid(row=5, column=0, columnspan=2)
        gui.Save_CSV()


    def update_status(self):
        # Update the ticket status
        status_text = tk.simpledialog.askstring("Update Ticket Status", "What would you like to change the ticket status to?")
        self.ticket.status = status_text
        self.ticket.add_work_note(f"Ticket Status Changed to {status_text}")
        self.view_ticket()


    def close_ticket(self):
        self.ticket.status = "CLOSED"
        self.ticket.add_work_note("Ticket Closed")
        self.view_ticket()

    def add_work_note(self):
        # Get the current time and date
        now = datetime.now()
        timestring = now.strftime("%d/%m/%Y %H:%M:%S")

        # Get the work note text from the user
        work_note_text = tk.simpledialog.askstring("Add Work Note", "Enter the work note:")

        # Add the work note to the ticket
        self.ticket.add_work_note(work_note_text)

        # Add the work note to the text area
        self.view_ticket()

class ListBox(tk.Tk):
    def __init__(self, ticket_system, open_only):
        super().__init__()
        self.geometry('300x200')
        self.ticket_system = ticket_system
        self.lb = tk.Listbox(
            self,
            height=6,
            selectmode=tk.SINGLE)
        if open_only:
            self.title("Open Tickets")
            for ticket in ticket_system.tickets:
                if(ticket.status != "CLOSED"):
                    self.lb.insert(ticket.ticketNumber, f'{ticket.ticketNumber} | {ticket.name} | {ticket.status}')
        else:
            self.title("All Tickets")
            for ticket in ticket_system.tickets:
                self.lb.insert(ticket.ticketNumber, f'{ticket.ticketNumber} | {ticket.name} | {ticket.status}')
        self.lb.pack(expand=True, fill=tk.BOTH, side=tk.LEFT)

        scrollbar = ttk.Scrollbar(
            self,
            orient=tk.VERTICAL,
            command=self.lb.yview
        )

        self.lb['yscrollcommand'] = scrollbar.set

        scrollbar.pack(side=tk.LEFT, expand=True, fill=tk.Y)

        self.open = ttk.Button(self, text="Open Ticket", command=self.ticketinfo)
        self.open.pack()
        self.exit = ttk.Button(self,text="Exit",command=self.destroy)
        self.exit.pack()

    def ticketinfo(self):
        # Get the selected item in the listbox
        item = self.lb.curselection()
        item = self.lb.get(item)
        item= int(item[:7])
        # print(item)

        # Check if the selected item is a valid key in the ticket_system.ticket_map dictionary
        if item in self.ticket_system.ticket_map:
            # If the item variable is a valid key, get the corresponding ticket object
            ticket = self.ticket_system.ticket_map[item]

            # Open the ticket window for the ticket object
            gui.Frame2.ticket=ticket
            gui.Frame2.view_ticket()
            self.destroy()
        else:
            # If the item variable is not a valid key, display an error message to the user
            messagebox.showerror("Error", "Invalid ticket number")


# Define a class to represent the ticketing system
class TicketSystem:
    # Initialize the system with an empty list of tickets
    def __init__(self):
        self.tickets = []
        self.nextTicketNumber = 100001
        self.savefile = "TicketLog.csv"
        self.ticket_map = {}  # Add a mapping of ticket numbers to Ticket objects

    # Define a method to add a ticket to the system
    def add_ticket(self, name, service, email, description):
        # Create a new ticket and add it to the list of tickets
        new_ticket = Ticket(self.nextTicketNumber, name, "NEW", service, email, description)
        new_ticket.add_work_note("Ticket Opened")
        self.nextTicketNumber += 1
        self.tickets.append(new_ticket)
        self.ticket_map[new_ticket.ticketNumber] = new_ticket  # Add the ticket to the map
        self.save_tickets()

    # Define a method to view all tickets in the system
    def view_all_tickets(self):
        # Print all tickets in the system
        lb = ListBox(self, False)
        lb.mainloop()


    def view_open_tickets(self):
        # Print all tickets in the system
        lb = ListBox(self, True)
        lb.mainloop()


    def check_last_ticket(self):
        for ticket in self.tickets:
            # print(ticket.ticketNumber)
            number = int(float(ticket.ticketNumber))
            if self.nextTicketNumber <= number:
                self.nextTicketNumber = number + 1



    def open_save(self):
        # Open the file for reading
        if not exists(self.savefile):
            self.save_tickets()
        with open(self.savefile, "r", newline="") as file:
            # Create a CSV reader
            reader = csv.reader(file)

            # Loop over the rows in the file
            for row in reader:
                ticketCheck = row[0]
                if ticketCheck != "Ticket Number":
                    # Get the ticket data from the row  Ticket Number", "Name", "Status", "Service", "E-mail", "Description"
                    ticketNumber = int(row[0])
                    name = row[1]
                    status = row[2]
                    service = row[3]
                    email = row[4]
                    description=row[5]
                    work_notes = row[6:]

                    # Create a new ticket and add it to the list of tickets
                    if self.nextTicketNumber <= ticketNumber:
                        self.nextTicketNumber = ticketNumber + 1

                    ticket = Ticket(ticketNumber, name, status, service, email, description)
                    self.tickets.append(ticket)
                    self.ticket_map[ticket.ticketNumber] = ticket  # Add the ticket to the map

                    # Add the work notes to the ticket
                    for work_note in work_notes:
                        ticket.add_work_note_no_time(str(work_note))

    # Define a method to save the tickets to a CSV file
    def save_tickets(self):
        # Open the file for writing
        with open(self.savefile, "w", newline="") as file:
            # Create a CSV writer
            writer = csv.writer(file)

            # Write each ticket to the file ticketNumber, name, status, service, email, description
            writer.writerow(["Ticket Number", "Name", "Status", "Service", "E-mail", "Description", "Notes"])
            for ticket in self.tickets:
                # Create a list with the ticket data
                ticket_data = [ticket.ticketNumber, ticket.name,
                               ticket.status, ticket.service, ticket.email,
                               ticket.description]

                # Add the work notes and their timestamps to the list
                for work_note in ticket.work_notes:
                    ticket_data.append(work_note)

                # Write the ticket data to the file
                writer.writerow(ticket_data)

    def change_status(self, ticket, change):
        ticket.status = change
        ticket.add_work_note("Ticket status changed to " + change)

    def close_ticket(self, ticket):
        ticket.add_work_note("Ticket Closed")
        ticket.status = "CLOSED"

class NewTicket(tk.Tk):
    def __init__(self, ticket_system):
        super().__init__()
        self.title("New Ticket")
        self.ticket_system = ticket_system

        self.name_label = ttk.Label(self, text="Customer Name:")
        self.name_entry = ttk.Entry(self)

        self.service_label = ttk.Label(self, text="Service Requested:")
        self.service_entry = ttk.Entry(self)

        self.email_label = ttk.Label(self, text="Customer Email:")
        self.email_entry = ttk.Entry(self)

        self.description_label = ttk.Label(self, text="Enter the ticket description:")
        self.description_entry = ttk.Entry(self)

        self.submit_button = ttk.Button(self, text="Submit", command=self.New_Ticket_Submit)

        self.name_label.grid(row=0,column=0)
        self.service_label.grid(row=1,column=0)
        self.email_label.grid(row=2,column=0)
        self.description_label.grid(row=3,column=0)

        self.name_entry.grid(row=0,column=1)
        self.service_entry.grid(row=1,column=1)
        self.email_entry.grid(row=2,column=1)
        self.description_entry.grid(row=3,column=1)
        self.submit_button.grid(row=4, column=1)



    def New_Ticket_Submit(self):
        description = self.description_entry.get()
        name = self.name_entry.get()
        service = self.service_entry.get()
        email = self.email_entry.get()



        self.ticket_system.add_ticket(name, service, email, description)
        self.destroy()

class GUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.ticket_system = TicketSystem()
        self.ticket_system.open_save()
        self.description_var = tk.StringVar()
        self.priority_var = tk.StringVar()
        self.Frame1=Frame(self,)
        self.Frame1.grid(row=0, column=0)
        self.Frame2=TicketWindow(None, self)
        if exists('icon2.ico'):
            self.iconbitmap(default="icon2.ico")
        self.Frame2.grid(row=0, column=1,rowspan=6)
        self.protocol('WM_DELETE_WINDOW', self.close_program)

        # Window properties
        self.title('Ticket System')
        self.geometry('780x520')


        tk.Label(self.Frame1, text="Menu").grid(row=0,column=0)

        ttk.Button(self.Frame1, text="View All Tickets", command=self.view_all_tickets,width=20).grid(row=1,column=0)
        ttk.Button(self.Frame1, text="View Open Tickets", command=self.view_open_tickets,width=20).grid(row=2,column=0)
        ttk.Button(self.Frame1, text="New Ticket", command=self.new_ticket,width=20).grid(row=3,column=0)
        ttk.Button(self.Frame1, text="Exit Application", command=self.close_program,width=20).grid(row=4,column=0)

        print("Application Loading Complete")



    def close_program(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.Save_CSV()
            sys.exit()

    def new_ticket(self):
        newticket = NewTicket(self.ticket_system)
        newticket.mainloop()

    def view_all_tickets(self):
        self.ticket_system.view_all_tickets()


    def view_open_tickets(self):
        self.ticket_system.view_open_tickets()


    



    def Add_Work_Note(self):
        index = input("Enter the Ticket Number of the ticket to add the work note to: ")
        index = int(index)
        self.ticket_system.tickets = []
        self.ticket_system.open_save()
        for ticket in self.ticket_system.tickets:
            if index == ticket.ticketNumber:
                work_note = input("Enter the work note: ")
                ticket.add_work_note(work_note)
                self.ticket_system.save_tickets()


    def Save_CSV(self):
        self.ticket_system.save_tickets()
        # print("File saved at ", self.ticket_system.savefile, "\n")
        self.ticket_system.tickets = []
        self.ticket_system.open_save()


    def Change_Ticket_Status(self):
        index = int(input("Enter Ticket Number"))
        self.ticket_system.tickets = []
        self.ticket_system.open_save()
        for ticket in self.ticket_system.tickets:
            if index == ticket.ticketNumber:
                status = input("What would you like to change the ticket status to? (PLEASE USE ALL CAPS)")
                confirm = input("Are you sure? (Y/N)")
                print("")
                if confirm == "Y" or "y":
                    self.ticket_system.change_status(ticket, status)
                    print(ticket)
                    print("\nTicket ", index, " changed to ", status)
                    self.ticket_system.save_tickets()
                    self.ticket_system.tickets = []
                    self.ticket_system.open_save()
                else:
                    self.ticket_system.tickets = []
                    self.ticket_system.open_save()







# mainloop
if __name__ == "__main__":
    print("Loading Program")
    gui = GUI()
    gui.mainloop()


def on_closing():
    gui.Save_CSV()
