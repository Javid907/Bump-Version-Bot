import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def merge_notification(email_of_author, http_mr_url, email_server, email,
                       email_password, branch_name, project_name, new_version):
    notification_message = """
    My friend your branch was merged.
    Congratulation !!!

    Branch: {}
    Merge Request: {}
    Project Name: {}
    Version: {}

    I said you can do it.
    """.format(branch_name, http_mr_url, project_name, new_version)

    subject = 'Congratulation from Bump BOT'

    send_notification(email_of_author, email_server, email, email_password, notification_message, subject)


def merge_error_notification(email_of_author, http_mr_url, email_server, email, email_password):
    notification_message = """
    Got an error in time merge your branch and reassigned it back to you.
    Please check again.
    {}

    Problem: I can't do merge please check your merge request

    Don't forget You are the best.
    """.format(http_mr_url)

    subject = 'Error while merge to master from Bump BOT'

    send_notification(email_of_author, email_server, email, email_password, notification_message, subject)


def changelog_from_description_migration_error(email_of_author, http_mr_url, email_server, email, email_password):
    notification_message = """
    Got an error in time merge your branch and reassigned it back to you.
    Please check again.
    {}

    Problem: You did not mark tag under Tags checkbox DB Migration

    Don't forget You are the best.
    """.format(http_mr_url)

    subject = 'Error while merge to master from Bump BOT'

    send_notification(email_of_author, email_server, email, email_password, notification_message, subject)


def branch_type_error_notification(email_of_author, http_mr_url, email_server, email, email_password):
    notification_message = """
    Got an error in time merge your branch and reassigned it back to you.
    Please check again.
    {}

    Problem: Your branch type is not right.

    Don't forget You are the best.
    """.format(http_mr_url)

    subject = 'Error while merge to master from Bump BOT'

    send_notification(email_of_author, email_server, email, email_password, notification_message, subject)


def changelog_error_notification(email_of_author, http_mr_url, email_server, email, email_password):
    notification_message = """
    Got an error in time merge your branch and reassigned it back to you.
    Please check again.
    {}

    Problem: You should add changelog in MR description.

    Don't forget You are the best.
    """.format(http_mr_url)

    subject = 'Error while merge to master from Bump BOT'

    send_notification(email_of_author, email_server, email, email_password, notification_message, subject)


def thread_error_notification(email_of_author, http_mr_url, email_server, email, email_password):
    notification_message = """
    Got an error in time merge your branch and reassigned it back to you.
    Please check again.
    {}

    Problem: You should fix all threads in your MR.

    Don't forget You are the best.
    """.format(http_mr_url)

    subject = 'Error while merge to master from Bump BOT'

    send_notification(email_of_author, email_server, email, email_password, notification_message, subject)


def rebase_error_notification(email_of_author, http_mr_url, email_server, email, email_password):
    notification_message = """
    Got an error in time merge your branch and reassigned it back to you.
    Please check again.
    {}

    Problem: You should do rebase your branch.

    Believe me I tried do rebase, but I am stupid and I couldn't do it((((((.
    But you can do it.

    Don't forget You are the best.
    """.format(http_mr_url)

    subject = 'Error while merge to master from Bump BOT'

    send_notification(email_of_author, email_server, email, email_password, notification_message, subject)


def approve_error_notification(email_of_author, http_mr_url, email_server, email, email_password):
    notification_message = """
    Got an error in time merge your branch and reassigned it back to you.
    Please check again.
    {}

    Problem: You don't have enough approves.

    Don't forget You are the best and You can do it.
    """.format(http_mr_url)

    subject = 'Error while merge to master from Bump BOT'

    send_notification(email_of_author, email_server, email, email_password, notification_message, subject)


def pipeline_error_notification(email_of_author, http_mr_url, email_server, email, email_password):
    notification_message = """
    Got an error in time merge your branch and reassigned it back to you.
    Please check again.
    {}

    Problem: Pipeline of your merge request failed.

    Don't forget You are the best and You can do it.
    """.format(http_mr_url)

    subject = 'Error while merge to master from Bump BOT'

    send_notification(email_of_author, email_server, email, email_password, notification_message, subject)


def approved_error_notification(email_of_author, http_mr_url, email_server, email, email_password):
    notification_message = """
    Got an error in time merge your branch and reassigned it back to you.
    Please check again.
    {}

    Problem: You can not approve your own branch.

    Please ask someone make it for you.

    Don't forget You are the best and You can do it.
    """.format(http_mr_url)

    subject = 'Error while merge to master from Bump BOT'

    send_notification(email_of_author, email_server, email, email_password, notification_message, subject)


def send_notification(email_of_author, email_server, email, email_password, notification_message, subject):
    rec_list = [email_of_author]

    msg = MIMEMultipart()
    msg['From'] = "Bump BOT <{}>".format(email)
    msg['To'] = email_of_author
    msg['Subject'] = subject
    msg.attach(MIMEText(notification_message))

    mailserver = smtplib.SMTP(email_server, 587)
    mailserver.ehlo()
    mailserver.starttls()
    mailserver.ehlo()
    mailserver.login(email, email_password)
    mailserver.sendmail(email, rec_list, msg.as_string())
    mailserver.quit()


def merge_approved_notification(http_mr_url, email_server, email, email_password, branch_name, project_name, new_version, email_list):
    notification_message = """
    My friend branch that you gave your approuve was merged.

    Branch: {}
    Merge Request: {}
    Project Name: {}
    Version: {}
    """.format(branch_name, http_mr_url, project_name, new_version)

    subject = 'Congratulation from Bump BOT'

    send_approved_notification(email_server, email, email_password, notification_message, subject, email_list)


def send_approved_notification(email_server, email, email_password, notification_message, subject, email_list):
    msg = MIMEMultipart()
    msg['From'] = "Bump BOT <{}>".format(email)
    msg['To'] = ' '.join(email_list)
    msg['Subject'] = subject
    msg.attach(MIMEText(notification_message))

    mailserver = smtplib.SMTP(email_server, 587)
    mailserver.ehlo()
    mailserver.starttls()
    mailserver.ehlo()
    mailserver.login(email, email_password)
    mailserver.sendmail(email, (email_list), msg.as_string())
    mailserver.quit()
