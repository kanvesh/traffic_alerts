import os

def send_email(recipient='akollu@quotient.com',subject='test',body='test'):
    print('echo "'+body+'" | mail -s "'+subject+'" '+recipient)
    os.system('echo "'+body+'" | mail -s "'+subject+'" '+recipient)

