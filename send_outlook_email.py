import win32com.client as win32


def send_outlook_email(recipients, subject, body):
    outlook = win32.Dispatch('Outlook.Application')
    mail = outlook.CreateItem(0)  # 0: olMailItem

    mail.To = recipients
    mail.Subject = subject
    mail.Body = body

    # Uncomment the following line if you want to send the email immediately without displaying the email window
    mail.Send()

# mail.Display()  # Display the email window for manual review before sending