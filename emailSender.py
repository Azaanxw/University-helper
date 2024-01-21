# Imports
from customtkinter import CTk, CTkLabel, CTkEntry, CTkButton, CTkTextbox
from CTkMessagebox import CTkMessagebox
import customtkinter
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

icon_path = "Images\\email icon.ico"  # Icon path for the email window

class EmailSender(CTk):
    def __init__(self,main_page, fg_color=None, **kwargs):
        super().__init__(fg_color, **kwargs)
        self.title("Email Sender")
        self.geometry("400x500")
        self.resizable(False, False)
        self.main_page = main_page
        self.iconbitmap(icon_path)  # Icon that will be displayed for the email window

        # Initialize instance attributes for entry widgets
        self.email_entry = None
        self.app_key_entry = None
        self.receiver_entry = None
        self.subject_entry = None

        # Components for email sender
        self.create_entry_frame("Your Email:")
        self.create_entry_frame("Your App Key:")
        self.create_entry_frame("Receiver's Email:")
        self.create_entry_frame("Subject:")

        # Message entry frame
        message_frame = customtkinter.CTkFrame(self)
        message_frame.pack(pady=10)

        message_label = CTkLabel(message_frame, text="Message:")
        message_label.pack(pady=5)

        # Uses CTkTextbox for message input
        self.message_entry = CTkTextbox(message_frame, width=190, height=80)
        self.message_entry.pack(pady=5)

        send_button = CTkButton(self, text="Send", command=self.send_email)
        send_button.pack(pady=20)

    def create_entry_frame(self, label_text): # Creates the frame for the inputs to be fit inside 
        entry_frame = customtkinter.CTkFrame(self)
        entry_frame.pack(pady=5)

        label = CTkLabel(entry_frame, text=label_text)
        label.pack(side=customtkinter.LEFT)

        # Use instance attributes
        entry_widget = CTkEntry(entry_frame)
        entry_widget.pack(side=customtkinter.LEFT, padx=5)

        # Assign instance attributes
        if label_text == "Your Email:":
            self.email_entry = entry_widget
        elif label_text == "Your App Key:":
            self.app_key_entry = entry_widget
        elif label_text == "Receiver's Email:":
            self.receiver_entry = entry_widget
        elif label_text == "Subject:":
            self.subject_entry = entry_widget

    def send_email(self):
        # Get values from entry widgets
        your_email = self.email_entry.get()
        app_key = self.app_key_entry.get()
        receiver_email = self.receiver_entry.get()
        subject = self.subject_entry.get()
        message = self.message_entry.get("1.0", "end-1c")  # Get the message from the CTkTextbox

        # Basic validation
        if not all([your_email, app_key, receiver_email, subject, message]):
            CTkMessagebox(title="Error", message="Please fill in all details!", icon="cancel")
            return

        # Email configuration (for Gmail)
        smtp_server = "smtp.gmail.com"
        smtp_port = 587
        smtp_username = your_email
        smtp_password = app_key

        # Create message
        email_message = MIMEMultipart()
        email_message['From'] = your_email
        email_message['To'] = receiver_email
        email_message['Subject'] = subject
        email_message.attach(MIMEText(message, 'plain'))

        try:
            # Connect to the server
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()

            # Login to the email account
            server.login(smtp_username, smtp_password)

            # Send the email
            server.sendmail(your_email, receiver_email, email_message.as_string())

            # Close the connection
            server.quit()

            # Provide feedback to the user
            CTkMessagebox(message="Email sent successfully!",
                  icon="check",option_1="Ok")

            # Close the EmailSender window after sending the email
            self.withdraw()

        except Exception as e:
            CTkMessagebox(title="Error", message=f"An error occurred: {str(e)}", icon="cancel")

    def turn_on(self):
        self.deiconify()
        self.mainloop()

    def turn_off(self):
         self.withdraw()
         self.main_page.mainloop()