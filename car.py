from tkinter import *
from tkinter import messagebox, colorchooser
from logging import basicConfig, warning, info, error, DEBUG
from os import getcwd, path, mkdir
from time import strftime, time, localtime
from json import dump, load
from re import findall, search
from hmac import new, compare_digest
from hashlib import sha224, sha512
from secrets import choice
from string import ascii_letters
from requests import get
from smtplib import SMTP, SMTPRecipientsRefused
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class Vigenere:
      def __init__(self):
            self.letter_list = 'A B C D E F G H I J K L M N O P Q R S T U V W X Y Z'.split(' ')
            self.number_list = list(range(26))

      def encipher(self, msg, secret_key):
            self.pattern_list = findall(r'[\s]|[0123456789]|[~`!@#\$%\^&\*()_\+\-={}|\[\]\\:";\'\<\>\?,./", ]', msg)
            msg = msg.upper()
            for x in self.pattern_list:
                  msg = msg.replace(x, '')

            self.secret_key = secret_key.upper()
            while True:
                  if len(self.secret_key) < len(msg):
                        self.secret_key *= 2
                  else:
                        self.secret_key = self.secret_key[:len(msg)].upper()
                        break

            self.encipher_text_list1 = [x for x in list(msg)]
            self.encipher_text_list2 = [x for x in list(self.secret_key)]
            self.encipher_text_list = []
            for x in range(len(msg)):
                  self.encipher_text_list += [[self.encipher_text_list1[x], self.encipher_text_list2[x]]]

            self.output_list = []
            for x in range(len(msg)):
                  self.num_msg = self.number_list[self.letter_list.index(self.encipher_text_list[x][0])]
                  self.num_key = self.number_list[self.letter_list.index(self.encipher_text_list[x][1])]
                  self.new_letter_list = self.letter_list[self.number_list[self.num_msg]:] + list(self.letter_list[0:self.number_list[self.num_msg]])
                  self.output_list += self.new_letter_list[self.num_key]

            self.output = ''
            for x in self.output_list:
                  self.output += x
            return self.output

      def decipher(self, msg, secret_key):
            self.pattern_list = findall(r'[\s]|[0123456789]|[~`!@#\$%\^&\*()_\+\-={}|\[\]\\:";\'\<\>\?,./", ]', msg)
            msg = msg.upper()
            for x in self.pattern_list:
                  msg = msg.replace(x, '')

            self.secret_key = secret_key.upper()
            while True:
                  if len(self.secret_key) < len(msg):
                        self.secret_key *= 2
                  else:
                        self.secret_key = self.secret_key[:len(msg)].upper()
                        break
            
            self.decipher_text_list1 = [x for x in list(msg)]
            self.decipher_text_list2 = [x for x in list(self.secret_key)]
            self.decipher_text_list = []
            for x in range(len(msg)):
                  self.decipher_text_list += [[self.decipher_text_list1[x], self.decipher_text_list2[x]]]

            self.output_list = []
            self.msg_list = list(msg)
            for x in range(len(msg)):
                  self.num_msg = self.number_list[self.letter_list.index(self.decipher_text_list[x][0])]
                  self.num_key = self.number_list[self.letter_list.index(self.decipher_text_list[x][1])]
                  self.new_letter_list = self.letter_list[self.number_list[self.num_key]:] + list(self.letter_list[0:self.number_list[self.num_key]])
                  self.output_list += self.letter_list[self.new_letter_list.index(self.msg_list[x])]

            self.output = ''
            for x in self.output_list:
                  self.output += x
            return self.output

class GUI():
    def __init__(self):
        CreateLogFile()
        try:
            self.newcolor = Config('color.json').loadfile()
        except FileNotFoundError:
            self.newcolor = None
            Config('color.json').createfile(self.newcolor)

        self.root = Tk()
        self.root.title('Car Game')
        self.root.resizable(0, 0)
        
        try:
              open('.\\.image\\car.ico')
              self.root.iconbitmap('.\\.image\\car.ico')
        except FileNotFoundError:
              CreateFolder('.image')
              with open('.\\.image\\car.ico', 'wb') as code:
                    code.write(get('https://www.easyicon.net/download/ico/1284184/128/').content)

        self.rstr = StringVar()
        self.rint = IntVar()
        
        self.screenwidth = self.root.winfo_screenwidth()
        self.screenheight = self.root.winfo_screenheight()
        alignstr = f'750x600+{(self.screenwidth - 750) // 2}+{(self.screenheight - 600) // 2 - 50}'
        self.root.geometry(alignstr)

        self.lable = Label(self.root, height = 600, width = 750, bd = 0, \
                           bg = self.newcolor, highlightthickness = 0)
        self.lable.pack()

        self.check_account = Label(self.root, height = 200, width = 200, bd = 0, \
                           bg = self.newcolor, highlightthickness = 0, text = 'l').pack(anchor = 'nw')
        #self.check_account.pack(anchor = 'nw')
        
        self.menu = Menu(self.root, bd = 0, tearoff = False)
        self.file = Menu(self.menu, tearoff = False)
        self.menu.add_cascade(label = 'File', menu = self.file)
        self.file.add_command(label = 'Edit Color', command = self.color)
        self.file.add_separator()
        self.file.add_command(label = 'Exit', command = self.rquit)

        self.rmenu = Menu(self.root, tearoff = False)
        self.rmenu.add_command(label = 'Exit', command = self.rquit)
        self.lable.bind('<Button-3>', self.popup)
        
        self.createcar = Menu(self.menu, tearoff = False)
        self.menu.add_cascade(label = 'Cars', menu = self.createcar)
        self.createcar.add_command(label = 'Create New Car', \
                                   command = self.create_car_gui)

        self.account = Menu(self.menu, tearoff = False)
        self.menu.add_cascade(label = 'Account Manage', menu = self.account)
        self.account.add_command(label = 'Login', command = self.login)
        self.account.add_command(label = 'Register', command = self.register)
        self.root.config(menu = self.menu)
        
        self.root.mainloop()

    def register(self):
        self.registertop = Toplevel(bg = self.newcolor)
        self.registertop.title('Register')
        self.registertop.resizable(0, 0)
        alignstr = f'250x200+{(self.screenwidth - 750) // 2}+{(self.screenheight - 600) // 2 - 50}'
        self.registertop.geometry(alignstr)
        self.registertop.iconbitmap('.\\.image\\car.ico')

        label1 = Label(self.registertop, text = 'User Name', bg = self.newcolor).place(relx = .025, rely = .03)
        self.username = Entry(self.registertop, bg = self.newcolor)
        self.username.place(relx = .45, rely = .04)

        label2 = Label(self.registertop, text = 'Email', bg = self.newcolor).place(relx = .025, rely = .14)
        self.emailname = Entry(self.registertop, bg = self.newcolor)
        self.emailname.place(relx = .45, rely = .15)
        
        label3 = Label(self.registertop, text = 'Password', bg = self.newcolor).place(relx = .025, rely = .25)
        self.password = Entry(self.registertop, bg = self.newcolor, show = '*')
        self.password.place(relx = .45, rely = .26)
        
        label4 = Label(self.registertop, text = 'Confirm Password', bg = self.newcolor).place(relx = .025, rely = .36)
        self.conpassword = Entry(self.registertop, bg = self.newcolor, show = '*')
        self.conpassword.place(relx = .45, rely = .37)
        
        button = Button(self.registertop, text = 'Create Account', \
                        command = self.registervalid, bg = self.newcolor).place(relx = .5, \
                                                                             rely = .8, anchor = 'center')

    def registervalid(self):
        self.user = self.username.get()
        self.em = self.emailname.get()
        self.word = self.password.get()
        self.cword = self.conpassword.get()
        self.valid1 = self.valid2 = self.valid3 = self.valid4 = self.valid5 = True
        if not self.user.split():
            warninput = messagebox.showwarning('Warning', 'No input of username')
            warning('No input of username.')
            self.valid1 = False

        if not self.em.split():
            warninput = messagebox.showwarning('Warning', 'No input of email')
            warning('No input of email.')
            self.valid2 = False

        if not self.word.split():
            warninput = messagebox.showwarning('Warning', 'No input of password')
            warning('No input of password.')
            self.valid3 = False

        if self.word != self.cword:
            errorinput = messagebox.showerror('Error', 'Passwords are not the same')
            error('Passwords are not the same.')
            self.valid4 = False

        if not self.valid1 or not self.valid2 or not self.valid3 or not self.valid4:
            self.register()
            
        else:
            self.send_email()
            
    def send_email(self):
        msg = MIMEMultipart()
        msg.attach(MIMEText(f'Dear {self.user}: \n\tYour Password is {self.word}.', 'plain', 'utf-8'))
        
        sender = 'GGJamesQQ@yeah.net'
        password = 'APYDOSTDPDUOEEHQ'
        receiver = self.em
        receiver = 'GGJamesQQ@yeah.net' #HUHuh
            
        msg['From'] = sender
        msg['To'] = receiver
        msg['Subject'] = 'Confirm Password'

        with open(getcwd() + '\\.config\\color.json', 'rb') as send_file:
            att = MIMEText(send_file.read(), 'base64', 'utf-8')
            att['Content-Type'] = 'application/octet-stream'
            att['Content-Disposition'] = 'attachment;filename="color.json"'

        msg.attach(att)
        
        smtp_server = 'smtp.yeah.net'
        
        server = SMTP(smtp_server, 25)
        server.ehlo()
        server.starttls()
        server.login(sender, password)
        server.set_debuglevel(False)
        try:
            server.sendmail(sender, receiver, msg.as_string())
        except SMTPRecipientsRefused:
            self.valid5 = False
            msg['To'] = 'trashjames@sohu.com'
            server.sendmail(sender, 'trashjames@sohu.com', msg.as_string())
            
        server.quit()
        if self.valid5:
            messagebox.showinfo('Successful', f'Successfuly create account {self.user}')
            info(f'Successfuly create account \'{self.user}\'.')
            self.encrypt_register(self.word)

        else:
            messagebox.showerror('Error', f'Email \'{self.em}\' is uncorrect')
            error(f'Email \'{self.em}\' is uncorrect.')
            self.register()

    def encrypt_register(self, password):
        encrypted_password = Vigenere().encipher(password, 'fdfskfg')
        
        onepass = sha512(b'2erer3asdfwerxdf34sdfsdfs90')
        onepass.update(encrypted_password.encode())
        import hashlib
        signp = b'GQnIdFUUAUDlcepuaDVGJpnmfRektPLT'
        sign = new(signp, onepass.hexdigest().encode('utf-8'), \
                   digestmod = sha224).hexdigest()
        
        Account(f'{self.user}.json').createfile([onepass.hexdigest(), 'fdfskfg', sign])

    def login(self):
        self.logintop = Toplevel(bg = self.newcolor)
        self.logintop.title('Login')
        self.logintop.resizable(0, 0)
        alignstr = f'250x200+{(self.screenwidth - 750) // 2}+{(self.screenheight - 600) // 2 - 50}'
        self.logintop.geometry(alignstr)
        self.logintop.iconbitmap('.\\.image\\car.ico')
        self.loginuser = None

    def decrypt_login(self, password):
        loadaccount = Account(f'{self.loginuser}.json').loadfile()
        dsign = new(signp, loadaccount[0].encode('utf-8'), digestmod = sha224).hexdigest()
        print(compare_digest(sign, dsign))

    def popup(self, event):
        self.rmenu.post(event.x_root, event.y_root)
    
    def color(self):
        self.newcolor = colorchooser.askcolor(self.newcolor, title = 'Choose a color')[1]
        if self.newcolor:
            Config('color.json').createfile(self.newcolor)
            info(f'Edited color config: {self.newcolor}.')
            self.root.destroy()
            self.__init__()

    def create_car(self):
        self.get_manufacturer = self.manufacturer.get()
        self.get_name = self.name.get()
        self.get_year = self.year.get()
        if self.rint.get():
            self.new_car = ElectricCar(self.get_manufacturer, self.get_name, \
                                       self.get_year)
            self.new_car_name = self.new_car.get_descriptive_name()
        else:
            self.new_car = Car(self.get_manufacturer, self.get_name, self.get_year)
            self.new_car_name = self.new_car.get_descriptive_name()
        
        self.valid1 = False
        self.valid2 = False
        self.valid3 = False
        if self.get_manufacturer:
            try:
                self.get_manufacturer = int(self.get_manufacturer)
            except:
                pass
            if isinstance(self.get_manufacturer, str):
                self.valid1 = True
            else:
                warntype = messagebox.showerror('Error', f'Invalid Type \'{type(self.get_manufacturer).__name__}\' of manufacturer')
                error(f'Invalid Type \'{type(self.get_manufacturer).__name__}\' of manufacturer.')
        else:
            warninput = messagebox.showwarning('Warning', 'No input of manufacturer')
            warning('No input of manufacturer.')

        if self.get_name:
            try:
                self.get_name = int(self.get_name)
            except:
                pass
            if isinstance(self.get_name, str):
                self.valid2 = True
            else:
                warntype = messagebox.showerror('Error', f'Invalid Type \'{type(self.get_name).__name__}\' of name')
                error(f'Invalid Type \'{type(self.get_name).__name__}\' of name.')
        else:
            warninput = messagebox.showwarning('Warning', 'No input of name')
            warning('No input of name.')

        if self.get_year:
            try:
                self.get_year = int(self.get_year)
            except:
                warntype = messagebox.showerror('Error', f'Invalid Type \'{type(self.get_year).__name__}\' of year')
                error(f'Invalid Type \'{type(self.get_year).__name__}\' of year.')
                
            if isinstance(self.get_year, int):
                self.valid3 = True
        else:
            warninput = messagebox.showwarning('Warning', 'No input of year')
            warning('No input of year.')

        ele = 'eletric car' if self.rint.get() else 'car'
        if self.valid1 and self.valid2 and self.valid3:
            self.confirm = messagebox.askyesno('Confirm', f'Create new {ele}: \n{self.new_car_name}')
            if self.confirm:
                Config('cars.json').createfile({'Name': self.new_car_name, \
                                                'Type': ele.title()}, True)
                messagebox.showinfo('Successful', f'Successfuly create {ele} \'{self.new_car_name}\'')
                info(f'Successfuly create {ele} \'{self.new_car_name}\'.')
            else:
                self.create_car_gui()

    def set_battery_gui(self):
        self.batterytop = Toplevel(bg = self.newcolor)
        self.batterytop.title('Set Battery -kWh')
        self.batterytop.resizable(0, 0)
        alignstr = f'250x100+{(self.screenwidth - 750) // 2}+{(self.screenheight - 600) // 2 - 50}'
        self.batterytop.geometry(alignstr)
        self.batterytop.iconbitmap('.\\.image\\car.ico')
        
        self.battery_button1 = Radiobutton(self.cartop, text = '60 -kWh', \
                                           variable = self.rint, bg = self.newcolor, \
                                        value = 0, indicatoron = False).pack()
        
    def create_car_gui(self):
        self.cartop = Toplevel(bg = self.newcolor)
        self.cartop.title('Create Car')
        self.cartop.resizable(0, 0)
        alignstr = f'250x200+{(self.screenwidth - 750) // 2}+{(self.screenheight - 600) // 2 - 50}'
        self.cartop.geometry(alignstr)
        self.cartop.iconbitmap('.\\.image\\car.ico')

        self.radiobutton1 = Radiobutton(self.cartop, text = 'Car', variable = self.rint, \
                                        bg = self.newcolor, value = 0).pack()

        self.radiobutton2 = Radiobutton(self.cartop, text = 'Eletric Car', variable = self.rint, \
                                        bg = self.newcolor, value = 1).pack()

        label1 = Label(self.cartop, text = 'Car Manufacturer: (Str)', \
                       bg = self.newcolor).pack()
        self.manufacturer = Entry(self.cartop, bg = self.newcolor)
        self.manufacturer.pack()

        label2 = Label(self.cartop, text = 'Car Name: (Str)', \
                       bg = self.newcolor).pack()
        self.name = Entry(self.cartop, bg = self.newcolor)
        self.name.pack()

        label3 = Label(self.cartop, text = 'Year: (Int)', \
                       bg = self.newcolor).pack()
        self.year = Spinbox(self.cartop, from_ = localtime()[0] - 15, \
                            to = localtime()[0] + 1, bg = self.newcolor)
        self.year.pack()

        button = Button(self.cartop, text = 'Create', command = self.create_car, \
                        bg = self.newcolor).pack()

    def rquit(self):
        self.root.destroy()

def CreateFolder(pathcwd):
    if not path.exists(getcwd() + '\\%s' % pathcwd):
        mkdir(getcwd() + '\\%s' % pathcwd)

def CreateLogFile():
    CreateFolder('.log')
    basicConfig(format = '%(asctime)s %(levelname)s: %(message)s', \
                datefmt = '%Y-%m-%d %H:%M:%S', filename = getcwd() + \
                '\\.log\\logs.log', filemode = 'a', level = DEBUG)

class Config():
    def __init__(self, filename):
        CreateFolder('.config')
        self.filename = filename

    def createfile(self, msg, ifadd = False):
        configfolder = getcwd() + '\\.config\\%s' % self.filename
        if ifadd:
            with open(configfolder, mode = 'a') as file:
                dump(msg, file)
            return
        
        with open(configfolder, mode = 'w+') as file:
                dump(msg, file)
        return

    def loadfile(self):
        configfolder = getcwd() + '\\.config\\%s' % self.filename
        with open(configfolder, mode = 'r') as file:
            self.fileinfo = load(file)
        return self.fileinfo

class Account():
    def __init__(self, filename):
        CreateFolder('.account')
        self.filename = filename

    def createfile(self, msg):
        configfolder = getcwd() + '\\.account\\%s' % self.filename
        with open(configfolder, mode = 'w+') as file:
                dump(msg, file)
        return

    def loadfile(self):
        configfolder = getcwd() + '\\.account\\%s' % self.filename
        with open(configfolder, mode = 'r') as file:
            self.fileinfo = load(file)
        return self.fileinfo

class Car():
    def __init__(self, make, model, year):
        CreateLogFile()
        self.make = make
        self.model = model
        self.year = year
        self.odometer_reading = 0

    def get_descriptive_name(self):
        self.descriptive = f'{str(self.year)} {self.make} {self.model}'.title()
        info(f'Getting car name: {self.descriptive}')
        return self.descriptive

    def descriptive_name(self):
        return f'{str(self.year)} {self.make} {self.model}'.title()

    def update_odometer(self, mileage):
        if mileage >= self.odometer_reading:
            self.odometer_reading = mileage
        else:
            warning('Rolling back an odometer.')

    def read_odometer(self):
        return f'This car has {str(self.odometer_reading)} miles on it.'

    def get_odometer(self):
        info(f'Getting odometer: {self.odometer_reading}')
        return self.odometer_reading

    def increment_odometer(self, miles):
        self.odometer_reading += miles

class ElectricCar(Car):
    def __init__(self, make, model, year):
        super().__init__(make, model, year)
        self.battery = Battery(85)

class Battery():
    def __init__(self, battery_size = 60):
        self.battery_size = battery_size

    def describe_battery(self):
        return f'This car has a {str(self.battery_size)} -kWh battery.'
        
    def get_range(self):
        if self.battery_size == 60:
            range = 340
            
        elif self.battery_size == 85:
            range = 685
        
        return f'This car can go approximately {str(range)} miles on a full charge.'

class Mainloop():
    CreateLogFile()
    info('Opened GUI application.')
    GUI()
    
Audi_Q5 = Car('Audi', 'Q5', 2018)
print(Audi_Q5.get_descriptive_name())
Audi_Q5.update_odometer(7884)
print(Audi_Q5.read_odometer())
print()

Tesla_Model3 = ElectricCar('Tesla', 'Model 3', 2020)
print(Tesla_Model3.get_descriptive_name())
Tesla_Model3.update_odometer(397)
print(Tesla_Model3.read_odometer())
print(Tesla_Model3.battery.describe_battery())
print(Tesla_Model3.battery.get_range())


descriptive_dict = {'Name': Audi_Q5.descriptive_name(), \
                    'Odometer': Audi_Q5.get_odometer()}
print(descriptive_dict)

Config('test.json').createfile(descriptive_dict)

Mainloop()
