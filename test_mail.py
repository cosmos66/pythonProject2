from datetime import datetime
path=r'C:\Users\sdemyanosov\Desktop\'test.txt'
with open(path, "w") as file:
    file.write(datetime.now().strftime("%H:%M:%S"))

import win32com.client as win32
outlook = win32.Dispatch('outlook.application')
mail = outlook.CreateItem(0)
mail.To = 'sdemyanosov@ves-media.com'
mail.Subject = 'Good_try '+datetime.now().strftime("%H:%M:%S")
mail.Body = 'Добрый день, \n Это ежедневный отчет\n за сегодня -' +datetime.now().strftime("%d.%m.%y")
# mail.HTMLBody = '<h2>HTML Message body</h2>' #this field is optional

# To attach a file to the email (optional):
attachment= path
mail.Attachments.Add(attachment)

mail.Send()

