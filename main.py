#!/usr/bin/python3
from colors import bcolors
import cmd
import os
from room import get_blocks
from player import get_player

class Game(cmd.Cmd):
    def Splash():
        os.system('cls' if os.name=='nt' else 'clear')
        print ("welcome")
    intro = Splash()
    #print (blocks)
    prompt  = "Action >>"
    def __init__(self):
        cmd.Cmd.__init__(self)
        self.player = get_player()
        self.blocks = get_blocks()
        self.getRoom("F1")
        
    def getRoom(self,room):
        for x in self.blocks:
            if x.id == room:
                self.loc = x
        self.player.SetRoom(self.loc.id)
    def move(self,dir):
        newroom = self.loc._neighbour(dir)
        #check to see if newroom is in the neighbour list if not
        #tell the user it is not a valid move and do nothing
        if newroom is None:
            self.printScreen("You can not go that way")
        else:
            if newroom["keyrequired"] == "No":
                self.getRoom(newroom["id"])
                self.player.SetRoom(self.loc.id)
                self.printScreen(self.loc.name)
            else:
                if self.player._item(newroom["key"]):
                    self.getRoom(newroom["id"])
                    self.player.SetRoom(self.loc.id)
                    self.printScreen(self.loc.name)
                else:
                    self.printScreen("a key is required")

    def printScreen(self,text):
        #call this function each time you want to print
        os.system('cls' if os.name=='nt' else 'clear')
        if self.player.isDead():

            os.system('cls' if os.name=='nt' else 'clear')
            print ("you are dead")
            raise SystemExit 
            #self.do_quit("q")
        else:
            if os.name == 'nt':
                print ("HEALTH " , 
                    str(self.player.getHP()), "/",
                    str(self.player.getMaxHP()),
                    "     ", self.player.name,
                    "     LEVEL ",self.player.level,
                    "     POINTS ",self.player.points,
                    "\n")
            else:
                print (bcolors.HEADER,bcolors.BACKGROUND,"HEALTH " , 
                    str(self.player.getHP()), "/",
                    str(self.player.getMaxHP()),
                    "     ", self.player.name,
                    "     LEVEL ",self.player.level,
                    "     POINTS ",self.player.points,
                    bcolors.ENDC,bcolors.ENDC,"\n")
            print (text) 
   
    def default(self,line):
       self.printScreen("command no recognized")
    def do_pickup(self,args):
        #make an update incase they enter more then one word
        item = self.loc._item(args)
        if item == None:
            self.printScreen("item not there")
        else:
            self.player.updatePoints(item[1])
            self.player.addItem(item[0])
            self.loc.removeItem(args)
            self.printScreen("you picked up a %s"%args)
    def do_look(self,args):
        text = self.loc.description
        if len(self.loc.returnItems())>0:
            text = text + "\nThese items look interesting:\n"
            for item in self.loc.returnItems():
                text = text + item + "\n"

        self.printScreen(text)
    def do_name(self,name):

        '''makes the ability to change your name\
        \nType name followed by your wanted name\
        \nExample name player'''
        self.player.name = name
        self.prompt = str(name)+ ">>"
        self.printScreen("")   

    def do_n(self,args):
        """Go North"""
        self.move("n")
    def do_e(self,args):
        """Go East"""
        self.move("e")
    def do_w(self,args):
        """Go West"""
        self.move("w")
    def do_s(self,args):
        """Go South"""
        self.move("s")
    def do_quit(self, args):
        """leaves the game"""

        self.printScreen("Thank you for playing")
        return True



if __name__=="__main__":
    #Try to set width and height of screen 
    #os.popen("stty cols 80").read()
    #os.popen("stty rows 34").read()

    g=Game()
    g.cmdloop()
