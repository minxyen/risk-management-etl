import win32com.client as win32
# from log import config_logger
# logger = config_logger()

def send_outlook_email(email_recipients, subject, body, logger):
    try:
        outlook = win32.Dispatch('Outlook.Application')
        mail = outlook.CreateItem(0)  # 0: olMailItem

        email_recipients = email_recipients.split(',')
        recipients_str = ";".join(email_recipients)
        mail.To = recipients_str
        mail.Subject = subject
        mail.Body = body

        # Uncomment the following line if you want to send the email immediately without displaying the email window
        mail.Send()
        logger.info(f"Email sent to recipients: {recipients_str}, Subject: {subject}")

        # mail.Display()  # Display the email window for manual review before sending

    except Exception as ex:
        # Log the error and exception details
        logger.error(f"An error occurred while sending the email: {ex}")

# send_outlook_email(EMAIL_RECIPIENTS, 'test', 'test', logger)