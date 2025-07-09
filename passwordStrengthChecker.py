import tkinter as tk
import PicturesBase64

class PasswordStrengthChecker:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Password Strength Checker")
        self.root.geometry("600x700")
        self.root.resizable(0, 0)
        self.root.config(bg="#E1F7F5")
        self.window = tk.Frame(self.root, bg="#E1F7F5")
        self.window.pack(pady=20)
        self.bulbPicture = tk.PhotoImage(data=PicturesBase64.bulbPicture)
        self.errorPicture = tk.PhotoImage(data=PicturesBase64.errorPicture)
        self.iconPicture = tk.PhotoImage(data=PicturesBase64.iconPicture)
        self.passwordLabel = tk.Label(self.window, text="Password", font=("Arial", 12, "bold"), bg="#E1F7F5")
        self.passwordLabel.pack(pady=1)
        self.passwordEntry = tk.Entry(self.window, font=("Helvetica",15), show="*", width=40)
        self.passwordEntry.pack(pady=10)
        self.passwordEntry.config(highlightcolor="black", highlightthickness=2)
        self.passwordEntry.event_generate("<<Copy>>")
        self.passwordEntry.event_generate("<<Paste>>")
        self.choiceNum = tk.IntVar()
        self.hidePassword = tk.Checkbutton(self.window,text="Show password", onvalue=1,offvalue=0,bg="#E1F7F5",variable=self.choiceNum,command=self.showOrHideEntry,activebackground="#E1F7F5")
        self.hidePassword.pack(pady=2)
        self.submitButton = tk.Button(self.window,text="Check your password strength",command=self.checkPasswordStrength, font=("Helvetica",15),bg="blue",fg="white",activebackground="black",activeforeground="white",padx=9)
        self.submitButton.pack(pady=8)
        self.passwordStrength = tk.Label(self.window, font=("Arial", 15), bg="#E1F7F5")
        self.passwordStrength.pack(pady=7)
        self.frame1 = tk.Frame(self.window, bg="#E1F7F5")
        self.frame1.pack()
        self.root.iconphoto(True, self.iconPicture)
        self.window.mainloop()

    def checkPasswordStrength(self):
        userPassword = self.passwordEntry.get()
        strength = ["Weak password","Moderate password","Strong password","Very strong password"]
        symbolsList = ["!","'",",",".","\"","+","-","/","\\","(",")","*","=","_","&","^","%","$","#","@","|","[","]","{","}","<",">","~","`"]
        commonWeakPasswords = ["password","qwerty","qwertyui","123","123456","xyz","abc","abcdef","admin","1111","000","password123",
                           "password1","123321","monkey","football","hello","iloveyou","dragon","letmein","baseball","flower",
                           "superman","princess","passw0rd","master","root","welcome","starwars","sunshine","777","555","google",
                           "qwert","qwer","qwe","computer","laptop","soccer","222","333","444","666","888","999","apple",
                           "internet","angel","lion","pokemon","ccc","www","zzz","gotham","batman","spiderman","ball","happy",
                           "princes","prince","family","beatles","school","meme","cool","music","dance","man","secret","college",
                           "cat","dog","sweet","disney","house","home","thankyou","software","date"]
        status = 3
        issuesInPassword = []
        ideasToUser = []
        if len(userPassword)<8:
            issuesInPassword.append("Password length very small")
            status = 0
        elif userPassword.isspace():
            issuesInPassword.append("Only white spaces is present")
            status = 0
        hasUpperCase = hasLowerCase = hasDigit = hasSymbol = hasWhiteSpace = False
        countWhiteSpace = sameCharacterRepetition = 0
        for ptr in range(len(userPassword)):
            if ptr>0 and userPassword[ptr]==userPassword[ptr-1]:
                sameCharacterRepetition += 1
            character = userPassword[ptr]
            if character==" ":
                hasWhiteSpace = True
                countWhiteSpace += 1
            elif character.isdecimal():
                hasDigit = True
            elif character.isalpha()==True:
                if character.islower():
                    hasLowerCase = True
                elif character.isupper():
                    hasUpperCase = True
            elif character in symbolsList:
                hasSymbol = True
        if sameCharacterRepetition>0:
            issuesInPassword.append("Characters repeating continuously")
        if countWhiteSpace>1:
            issuesInPassword.append("Too many white spaces")
        if hasDigit==False:
            issuesInPassword.append("No numbers present")
        if hasLowerCase==False and hasUpperCase==False:
            issuesInPassword.append("No alphabets present")
        elif hasLowerCase==False and hasUpperCase==True:
            issuesInPassword.append("No letters in lowercase")
        elif hasUpperCase==False and hasLowerCase==True:
            issuesInPassword.append("No letters in uppercase")
        if hasSymbol==False:
            issuesInPassword.append("No symbols")
        if hasLowerCase==True and hasUpperCase==True and hasDigit==True and hasSymbol==True:
            if len(userPassword)>=8 and len(userPassword)<=10:
                ideasToUser.append("Make password longer")
                status = 1
            elif len(userPassword)>=11 and len(userPassword)<=14:
                ideasToUser.append("Make the password a little longer")
                status = 2
            elif len(userPassword)>=15:
                status = 3
                if len(userPassword)>30:
                    ideasToUser.append("Password very long. Use password manager to store your password!")
            if sameCharacterRepetition>0 or countWhiteSpace>1:
                status = 1
        else:
            status = 0
        hasRepeatedPattern = self.checkForPatternRepeating()
        if hasRepeatedPattern==True:
            issuesInPassword.append("Repeating patterns in password")
            status = 0
        userPasswordInLower = userPassword.lower()
        for commonWord in commonWeakPasswords:
            if userPasswordInLower.find(commonWord) >= 0:
                status = 0
                issuesInPassword.append("Commonly used words found")
                break
        if status==0:
            self.passwordStrength.config(text=strength[status],fg="red")
        elif status==1:
            self.passwordStrength.config(text=strength[status],fg="brown")
        elif status==2:
            self.passwordStrength.config(text=strength[status],fg="purple")
        elif status==3:
            self.passwordStrength.config(text=strength[status],fg="green")
        for widgets in self.frame1.winfo_children():
            widgets.destroy()
        for currentIndex in range(len(issuesInPassword)):
            self.issue = tk.Label(self.frame1,text=issuesInPassword[currentIndex],font=("Arial",13),anchor=tk.NW,image=self.errorPicture,compound=tk.LEFT,bg="#E1F7F5")
            self.issue.pack()
        for currentIndex in range(len(ideasToUser)):
            self.ideas = tk.Label(self.frame1,text=ideasToUser[currentIndex],image=self.bulbPicture,compound=tk.LEFT,font=("Arial",12),bg="#E1F7F5")
            self.ideas.pack()

    def checkForPatternRepeating(self):
        userPassword = self.passwordEntry.get()
        patternMap = {}
        countOfRepeatedPattern = 0
        for ptr in range(len(userPassword)):
            if (ptr+2)<len(userPassword):
                pattern = userPassword[ptr:ptr+3]
                if pattern not in patternMap:
                    patternMap.update({pattern:1})
                else:
                    patternMap.update({pattern:patternMap.get(pattern)+1})
        for patternCount in patternMap.values():
            if patternCount>1:
                countOfRepeatedPattern += 1
        if countOfRepeatedPattern == 1:
            if len(userPassword) <= 10:
                return True
            else:
                return False
        elif countOfRepeatedPattern > 1:
            return True
        return False

    def showOrHideEntry(self):
        if self.choiceNum.get()==1:
            self.passwordEntry.config(show="")
        else:
            self.passwordEntry.config(show="*")

PasswordStrengthChecker()
