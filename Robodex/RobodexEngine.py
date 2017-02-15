import tkinter as tk
from PIL import ImageTk
from PIL import Image
from ScrollFrame import VerticalScrolledFrame
import csv
from Histogram import *

default_logo = 'first_logo.jpg'
default_image = 'kachow.gif'

''' Reads and creates the list of dictionaries of the teams info '''
inf = []
with open('CSVTest.csv') as csvfile:
    reader = csv.DictReader(csvfile, delimiter='/')
    for column in reader:
        file = {'Team':column['Team'], 'Name':column['Name'], 'Drive':column['Drive'],
                'Chassis':column['Chassis'], 'Mechs':column['Mechs'], 'MechD':column['MechD'],
                'Autonomous Gear':column['aGear'], 'Autonomous Gear Positon':column['aGearPos'],
                'Autonomous Position Start':column['aPosStart'], 'Autonomous Position End':column['aPosEnd'],
                'Gear Per Round':column['gPerRound'], 'Fuel Per Round Low':column['fPerRoundLo'],
                'Fuel Per Round High':column['fPerRoundHi'], 'Climb':column['climb'], 'Image':column['Image'], 'Logo':column['Logo']}
        inf.append(file)
        
    for rob in inf:
        rob['Mechs'] = rob['Mechs'].split(',')
        rob['MechD'] = rob['MechD'].split(',')
        
class RootApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        '''Custom Window'''
        self.columnconfigure(0, weight=1)

        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others

        container = tk.Frame(self)
        container.columnconfigure(0, weight=1)
        container.grid(sticky = (tk.N+tk.S+tk.E+tk.W))
        self.frames = {}
        for F in (Robodex, CompareTwo):
            page_name = F.__name__
            frame = F(parent=container, controller=self) 
            self.frames[page_name] = frame  

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row = 0,column=0, sticky = (tk.N+tk.S+tk.E+tk.W))

        self.show_frame("Robodex")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()

class Robot():
    ''' Creates a data class meant to house the displayed infomation '''
    def __init__(self, name="Robodex", team="First", drive="Python3.6", chassis="tkinter library using the pack module",
                 image=default_image, logo=default_logo, mechs=["Key Searcher", "Indexer"],
                 mechD=["Button in top left will cycle through available keys to be used in search.",
                        "Arrow buttons in top right will cycle through the robots that satisfy search parameter."]):

        self.name = name
        self.team = team
        self.drive = drive
        self.chassis = chassis
        self.mechs = mechs
        self.mechD = mechD
        self.image = image
        self.logo = logo
        self.right_img = Image.open('left_frame_img.jpg')
        self.right_img = self.right_img.resize((850, 1000), Image.ANTIALIAS)
        self.teams_found = []
        

        

    def makeSize(self, image, logo=False):
        '''Remakes Image.jpg or any into an image that is 250x250 pixels
        Do not take Portait photos with phone. Causes image to go sideways'''
        image_file = Image.open(image)
        if logo:
            image_resized = image_file.resize((100, 100), Image.ANTIALIAS)
        else:
            image_resized = image_file.resize((250, 250), Image.ANTIALIAS)
        return ImageTk.PhotoImage(image_resized)

class Robodex(tk.Frame):
    ''' Frame that shows the information about the robot searched for '''
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.pack()
        self.controller = controller
        self.create_widgets()
        

    def create_widgets(self):
        #Creating frame for top
        self.topFrame = tk.Frame(self, height=30, bg='gray')
        self.topFrame.pack(fill='x')
        
        #Creating widgets in top frame
        self.top_left_Label= tk.Label(self.topFrame, text="Search ",
                                 font=("courier", "13", "bold"),
                                 fg="#EEE3B9", bg= "gray")
        self.top_left_Label.grid(sticky=tk.W, row=0, column=0)

        self.key_button = tk.Button(self.topFrame, text="Team",
                                    command=lambda: self.key_change())
        self.key_button.grid(sticky=tk.W, row=0, column=1)

        self.top_right_Label = tk.Label(self.topFrame, text=": ",
                                        font=("courier", "13", "bold"),
                                        fg="#EEE3B9", bg= "gray")
        self.top_right_Label.grid(sticky=tk.W, row=0, column=3)

        self.search_entry = tk.Entry(self.topFrame, width=10)
        self.search_entry.grid(sticky=tk.W, row=0, column=4)

        self.search_button = tk.Button(self.topFrame, text="Search",
                                       command=lambda: self.search(self.key_button['text'],
                                                                   self.search_entry.get()))
        self.search_button.grid(sticky=tk.W, row=0, column=5)
        
        self.left_button = tk.Button(self.topFrame, text="<-",
                                      command=lambda: self.profile_change(-1))
        self.left_button.grid(sticky=tk.W, row=0, column=6)
        
        self.right_button = tk.Button(self.topFrame, text="->",
                                      command=lambda: self.profile_change(1))
        self.right_button.grid(sticky=tk.W, row=0, column=7)
        
        self.team_before_Label = tk.Label(self.topFrame, text="Teams found:",
                                          font=("courier", "13", "bold"),
                                          fg="#EEE3B9", bg= "gray")
        self.team_before_Label.grid(sticky=tk.W, row=1, column=0, columnspan=2)
        self.teams_found_Label = tk.Label(self.topFrame, text="Nothing",
                                          font=("courier", "13", "bold"),
                                          fg="#EEE3B9", bg= "gray")

        self.change_button = tk.Button(self.topFrame, text="change",
                                       command=lambda: self.controller.show_frame("CompareTwo"))
        self.change_button.grid(row=0, column=10)
        

        
        #Creating frame for left side
        self.leftFrame = tk.Frame(self, bg='#957156', width=250, height=300)
        self.leftFrame.pack(side='left', anchor=tk.NW)

        #Creating widgets in left side frame
        self.image = robot.makeSize(default_image)
        self.image_label = tk.Label(self.leftFrame, image = self.image, width=250, height=250)
        self.image_label.pack()
        
        #name & team -Need to fix problem with label growing frame becaues of more text
        self.name_label = tk.Label(self.leftFrame, text=("Robot:"),
                                   font=("courier", "15", "bold"),
                                   relief=tk.GROOVE, fg="#EEE3B9", bg="#7D4735")
        self.name_label.pack(pady=(10, 0))
        
        self.robotName_label = tk.Label(self.leftFrame, text=(robot.name),
                                    font=("courier", "15", "bold"),
                                    relief=tk.GROOVE, fg="#EEE3B9", bg="#7D4735")
        self.robotName_label.pack()

        self.t = tk.Frame(self.leftFrame, bg='#957156')
        self.t.pack(side='left', padx=(25, 0))
        self.team_label = tk.Label(self.t, text=("Team:"),
                                   font=("courier", "15", "bold"),
                                   relief=tk.GROOVE, fg="#EEE3B9", bg="#7D4735")
        self.team_label.pack()
        
        self.robotTeam_label = tk.Label(self.t, text=(robot.team),
                                    font=("courier", "15", "bold"),
                                    relief=tk.GROOVE, fg="#EEE3B9", bg="#7D4735")
        self.robotTeam_label.pack(padx=10)
        
        self.image_frame = tk.Frame(self.leftFrame)
        self.image_frame.pack(anchor=tk.E, padx=(10, 25), pady=10)
        self.logo_image = robot.makeSize(robot.logo, True)
        self.logo_label = tk.Label(self.image_frame, image=self.logo_image)
        self.logo_label.pack()
        

        #Magical things happend in VerticalScrolledFrame - bless the coding gods
        self.rightFrame = VerticalScrolledFrame(self)
        self.rightFrame.pack(expand=True, fill=tk.BOTH, anchor=tk.E)
        self.right_img = ImageTk.PhotoImage(robot.right_img)
        self.right_bg = tk.Label(self.rightFrame.interior, image=self.right_img)
        self.right_bg.place(x=0, y=0, relwidth=1, relheight=1)

        #Creating widgets in right side frame - create first instance of info to describe Robodex
        self.dFrame = tk.Frame(self.rightFrame.interior)
        self.dFrame.pack(pady=(10,10), anchor=tk.W)
        self.template_drive_label = tk.Label(self.dFrame, text=("Drive Train Type:"),
                                   font=("courier", "15"), bg='#7D4735', fg='#EEE3B9',
                                        relief=tk.RAISED)
        self.template_drive_label.pack(side="left")
        self.drive_label = tk.Label(self.dFrame, text=(robot.drive),
                                    font=("courier", "15"), bg='#7D4735', fg='#EEE3B9',
                                    relief=tk.RAISED)
        self.drive_label.pack(side="left")
        self.cFrame = tk.Frame(self.rightFrame.interior)
        self.cFrame.pack(pady=(10,10), anchor=tk.W)
        self.template_chassis_label = tk.Label(self.cFrame, text=("Chassis Type:"),
                                     font=("courier", "15"), bg= '#7D4735', fg='#EEE3B9',
                                     relief=tk.RAISED)
        self.template_chassis_label.pack(side="left")
        self.chassis_label = tk.Label(self.cFrame, text=(robot.chassis),
                                     font=("courier", "15"), bg= '#7D4735', fg='#EEE3B9',
                                     relief=tk.RAISED)
        self.chassis_label.pack(side="left")
        self.mechan_label = tk.Label(self.rightFrame.interior, text="Mechanisms",
                                   font=("courier", "15"), bg= '#7D4735', fg='#EEE3B9',
                                     relief=tk.RAISED)
        self.mechan_label.pack()

        #Initializing Lists For Robot Data
        self.mechs_list = []
        self.text_list = []
        self.keys = []
        self.profile = []
        self.teams_found = []
        self.compare = ['=', '<', '>']

        self.indexed = 0
        self.key_index = 0
        self.compare_index = 0
        self.key = ""
        self.isNum = False

        self.numCompare = tk.Button(self.topFrame, text="=",
                               command=lambda: self.compare_change())
        
        for key, value in inf[0].items():
                self.keys.append(key)
                
        for p in range(len(inf)):
            self.profile.append(p)
            
        self.create_robot_info()
            
    def create_robot_info(self):
        '''writes the information in the scrollable frame
           creates new labels and text boxes for mechs of found robot'''
        self.mechs_list = []
        self.text_list = []
        for mech in robot.mechs:
            self.mechs_list.append(robot.mechs[robot.mechs.index(mech)])
            self.text_list.append(robot.mechs[robot.mechs.index(mech)])
        print(self.mechs_list)
            
        for mech in robot.mechs:
            self.mechs_list[self.mechs_list.index(mech)] = tk.Label(self.rightFrame.interior, text=mech,
                                       bg="#7D4735", fg="#EEE3B9", font=("courier", "15"),
                                                                    relief=tk.RAISED)
            self.text_list[robot.mechs.index(mech)] = tk.Text(self.rightFrame.interior, height=2, width=70,
                                     wrap=tk.WORD, font=("courier", "13"),
                                     bg="#7D4735", fg="#EEE3B9")
            self.mechs_list[robot.mechs.index(mech)].pack(pady=(10, 0),ipadx=5, anchor=tk.W)
            self.text_list[robot.mechs.index(mech)].pack(padx=(45, 10), pady=(5, 10))
            self.text_list[robot.mechs.index(mech)].insert(tk.END, robot.mechD[robot.mechs.index(mech)])
            self.text_list[robot.mechs.index(mech)].config(state=tk.DISABLED)
            
        self.graph = Histogram(self.rightFrame.interior)
        self.graph.pack(anchor=tk.W)
            
        
    def compare_change(self):
        '''Makes the compare button's text index through [=,<,>].'''
        if self.compare_index > 2:
            self.compare_index = 0
        self.numCompare['text'] = self.compare[self.compare_index]
        self.compare_index += 1



    def key_change(self):
        '''Makes the key button's text index through all the keys in our dictionary.'''
        if self.key_index > len(self.keys) - 1:
            self.key_index = 0
        if inf[0][self.keys[self.key_index]][0] in ['1','2','3','4','5','6','7','8','9','0']:
            self.isNum = True
        else:
            self.isNum = False
            
        if self.isNum:
            self.numCompare.grid(column=2, row=0)
        else:
            self.numCompare.grid_forget()

        self.key_button['text'] = self.keys[self.key_index]
        self.key_index += 1

    def profile_change(self, value):
        '''Index thorugh the profiles in self.profile list'''
        self.indexed += value #Fixed issue with not indexing to multiple data displays
        if self.indexed > len(self.profile) - 1:
            self.indexed = 0
        if self.indexed < 0:
            self.indexed = len(self.profile) - 1
        print(self.indexed)
        self.change_text(self.profile[self.indexed])
        
    def search(self, key, wanted):
        '''Checks through the keys in our dictionary to see if that key holds the wanted variable'''
        self.search_button['text'] = "Searching..."
        self.key = key
        found = False
        result = []
        if self.isNum:
            wanted = int(wanted)
            if self.compare_index == 2:
                for i in range(len(inf)):
                    if wanted > int(inf[i][key]):
                        found = True
                        result.append(i)

            elif self.compare_index == 3:
                    for i in range(len(inf)):
                        if wanted < int(inf[i][key]):
                            found = True
                            result.append(i)
            else:
                for i in range(len(inf)):
                        if wanted == int(inf[i][key]):
                            found = True
                            result.append(i) 
        else:
            for i in range(len(inf)):
                if wanted in inf[i][key]:
                    found = True
                    result.append(i)

        if found:
            self.search_button['text'] = "Found!"
            self.profile = result #Asign profile list to result
            for index in self.profile:
                robot.teams_found.append(inf[index]['Team'])
            self.change_text(self.profile[0]) #Sets the text on screen to first item in profile list
        else:
            self.search_button['text'] = "Nothing Found"
            
    def change_text(self, index):
        '''Rewrites the labels & textboxes to hold information about searched team'''

        

        #Clear labels and data
        for mech in robot.mechs:
            self.mechs_list[robot.mechs.index(mech)].pack_forget()
            self.text_list[robot.mechs.index(mech)].pack_forget()
        self.graph.pack_forget()
        self.teams_found_Label['text'] = ""

        #Change robot class values
        robot.name = inf[index]['Name']
        robot.team = inf[index]['Team']
        robot.drive = inf[index]['Drive']
        robot.chassis = inf[index]['Chassis']
        robot.mechs = inf[index]['Mechs']
        robot.mechD = inf[index]['MechD']
        robot.image = robot.makeSize(inf[index]['Image'])
        robot.image = robot.makeSize(inf[index]['Image'])

        #Create new robot info
        self.create_robot_info()
        self.graph.pack(anchor=tk.W)
        self.image_label['image'] = robot.image
        self.logo = robot.makeSize(inf[index]['Logo'], logo=True)
        self.logo_label['image'] = self.logo
        self.robotName_label['text'] = robot.name
        self.robotTeam_label['text'] = robot.team
        self.drive_label['text'] = robot.drive
        self.chassis_label['text'] = robot.chassis
        self.teams_found_Label['text'] = robot.teams_found
        self.teams_found_Label.grid(sticky=tk.W, row=1, column=2, columnspan=10)

class CompareTwo(tk.Frame):
    '''shows info on two different robots'''
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.columnconfigure(0, weight=1)
        self.create_widgets()
    

    def create_widgets(self):
        '''method for widget placement'''
        #Creating frame for top
        self.topFrame = tk.Frame(self, height=30, bg='gray')
        self.topFrame.grid(sticky=tk.W+tk.E)

        self.initialise_button = tk.Button(self.topFrame, text="Initialise",
                                       command=lambda: self.initialise_text())
        self.initialise_button.grid(sticky=tk.NW, row=0, column=0)
        self.top_left_label1 = tk.Label(self.topFrame, text="Search ",
                                 font=("courier", "13", "bold"),
                                 fg="#EEE3B9", bg= "gray")
        self.top_left_label1.grid(sticky=tk.W, row=0, column=1, padx=(50, 0))

        #Left Frame Search Entry
        self.search_entry1 = tk.Entry(self.topFrame, width=10)
        self.search_entry1.grid(sticky=tk.W, row=0, column=2, padx=(0, 10))
        
        self.search_button1 = tk.Button(self.topFrame, text="Search",
                                       command=lambda: self.search(self.key_button['text'],
                                                                   self.search_entry.get()))
        self.search_button1.grid(sticky=tk.W, row=0, column=3, padx=(0, 20))
        
        titleLbl = tk.Label(self.topFrame, text="Two Robots Are Compared Here",
                                 font=("courier", "13", "bold"),
                                 fg="#EEE3B9", bg= "gray", relief=tk.RAISED)
        titleLbl.grid(row=0, column=4)

        self.top_left_label2 = tk.Label(self.topFrame, text="Search ",
                                 font=("courier", "13", "bold"),
                                 fg="#EEE3B9", bg= "gray")
        self.top_left_label2.grid(sticky=tk.W, row=0, column=5, padx=(20,0))
        
        #Right Frame Search Entry
        self.search_entry2 = tk.Entry(self.topFrame, width=10)
        self.search_entry2.grid(sticky=tk.W, row=0, column=6)

        self.search_button2 = tk.Button(self.topFrame, text="Search",
                                       command=lambda: self.search(self.key_button['text'],
                                                                   self.search_entry.get()))
        self.search_button2.grid(sticky=tk.W, row=0, column=7, padx=(10,0))
        
        self.change_button_r = tk.Button(self, text="change",
                                       command=lambda: self.controller.show_frame("Robodex"))
        self.change_button_r.grid()

        self.team_found_Label = tk.Label(self.topFrame, text="Teams found:",
                                          font=("courier", "13", "bold"),
                                          fg="#EEE3B9", bg= "gray")
        self.team_found_Label.grid(sticky=tk.W, row=1, column=0)
        self.teams_found_Label = tk.Label(self.topFrame, text="Nothing",
                                          font=("courier", "13", "bold"),
                                          fg="#EEE3B9", bg= "gray")
        self.teams_found_Label.grid(sticky=tk.W, row=1, column=1, columnspan=10)
        
        #Creating bottom frame
        self.botFrame = tk.Frame(self, width=800)
        self.botFrame.grid()
        
        #Create left frame
        self.leftCompareFrame = VerticalScrolledFrame(self.botFrame, width=500)
        self.leftCompareFrame.pack(expand=True, fill=tk.BOTH, anchor=tk.E, side='left')
        self.bg_left = ImageTk.PhotoImage(robot.right_img)
        self.leftBg = tk.Label(self.leftCompareFrame.interior, image=self.bg_left)
        self.leftBg.place(x=0, y=0, relwidth=1, relheight=1)

        self.leftCompare = tk.Frame(self.leftCompareFrame.interior)
        self.leftCompare.grid(row=0, column=0)
        self.leftRobotName = tk.Label(self.leftCompare, text=("Left Robot"), font=("courier", "20"), bg='#7D4735', fg='#EEE3B9',relief=tk.RAISED)
        self.leftRobotName.grid()
        self.leftRobotDrive = tk.Label(self.leftCompare, text=("Left Drive"), font=("courier", "15"), bg='#7D4735', fg='#EEE3B9',relief=tk.RAISED)
        self.leftRobotDrive.grid(sticky=tk.E+tk.W)
        self.leftRobotChassis = tk.Label(self.leftCompare, text=("Left Chassis"), font=("courier", "15"), bg='#7D4735', fg='#EEE3B9',relief=tk.RAISED)
        self.leftRobotChassis.grid(sticky=tk.E+tk.W)
        self.leftRobotMechan = tk.Label(self.leftCompare, text=("Left Mechanisms"), font=("courier", "15"), bg='#7D4735', fg='#EEE3B9',relief=tk.RAISED)
        self.leftRobotMechan.grid(sticky=tk.E+tk.W)

        #Create right frame
        self.rightCompareFrame = VerticalScrolledFrame(self.botFrame, width=500)
        self.rightCompareFrame.pack(expand=True, fill=tk.BOTH, anchor=tk.E, side='left')
        self.bg_right = ImageTk.PhotoImage(robot.right_img)
        self.rightBg = tk.Label(self.rightCompareFrame.interior, image=self.bg_left)
        self.rightBg.place(x=0, y=0, relwidth=1, relheight=1)

        self.rightCompare = tk.Frame(self.rightCompareFrame.interior)
        self.rightCompare.grid()
        self.rightRobotName = tk.Label(self.rightCompare, text=("Right Robot"), font=("courier", "20"), bg='#7D4735', fg='#EEE3B9',relief=tk.RAISED)
        self.rightRobotName.grid(sticky=tk.E+tk.W)
        self.rightRobotDrive = tk.Label(self.rightCompare, text=("Right Drive"), font=("courier", "15"), bg='#7D4735', fg='#EEE3B9',relief=tk.RAISED)
        self.rightRobotDrive.grid(sticky=tk.E+tk.W)
        self.rightRobotChassis = tk.Label(self.rightCompare, text=("Right Chassis"), font=("courier", "15"), bg='#7D4735', fg='#EEE3B9',relief=tk.RAISED)
        self.rightRobotChassis.grid(sticky=tk.E+tk.W)
        self.rightRobotMechan = tk.Label(self.rightCompare, text=("Right Mechanisms"), font=("courier", "15"), bg='#7D4735', fg='#EEE3B9',relief=tk.RAISED)
        self.rightRobotMechan.grid(sticky=tk.E+tk.W)

    def initialise_text(self):
        '''Rewrites the labels & textboxes to hold information about searched team'''

        self.teams_found_Label['text'] = robot.teams_found
        #self.image_label['image'] = robot.image
        #self.leftRobotTeam['text'] = robot.team
        self.leftRobotName['text'] = robot.name
        self.leftRobotDrive['text'] = robot.drive
        self.leftRobotChassis['text'] = robot.chassis
        


robot = Robot()
robot2 = Robot()
root = RootApp()
