import platform
import os
from tqdm.auto import tqdm
import subprocess

# global variable for operating system detection
class GlobalDataFO:
    isOnWindows = False
    isOnLinux = True

# Checking weather the user is on windows or not
osUsing = platform.system()

if(osUsing == "Windows"):
    GlobalDataFO.isOnWindows = True
    GlobalDataFO.isOnLinux = False



class GlobalMethods:


    @classmethod
    # function to get the files list in folder passed
    def getSubFilesList(cls , root, files=True, dirs=False, hidden=False, relative=True, topdown=True):
        root = os.path.join(root, '')  # add slash if not there
        for parent, ldirs, lfiles in os.walk(root, topdown=topdown):
            if relative:
                parent = parent[len(root):]
            if dirs and parent:
                yield os.path.join(parent, '')
            if not hidden:
                lfiles   = [nm for nm in lfiles if not nm.startswith('.')]
                ldirs[:] = [nm for nm in ldirs  if not nm.startswith('.')]  # in place
            if files:
                lfiles.sort()
                for nm in lfiles:
                    nm = os.path.join(parent, nm)
                    yield nm

    

    @classmethod
    # function to get the folders to be generated
    def getFolderNameToBeGenerated(cls , pathToFile):
        
        if(GlobalDataFO.isOnLinux):
            new = pathToFile.split("/")
            lenNew = len(new)

            folderPath = ""
            for j in range(lenNew-1):
                folderPath = folderPath + new[j] + "/"


        else:
            new = pathToFile.split("\\")
            lenNew = len(new)

            folderPath = ""
            for j in range(lenNew-1):
                folderPath = folderPath + new[j] + "\\"
            
        return folderPath


class EasyCopy:


    # cls variables
    __workWithHiddenFilesValue = False
    errorList = []



    # function to set the hidden files mode to ON
    @classmethod
    def workWithHiddenFiles(cls):
        cls.__workWithHiddenFilesValue = True



    # function to set the hidden files mode to OFF
    @classmethod
    def dontWorkWithHiddenFiles(cls):
        cls.__workWithHiddenFilesValue = False



    @classmethod
    def copyDir_withoutLoading(cls , source , dest , showCopy = False , returnStatus = False):

        cls.errorList.clear()

        for i in GlobalMethods.getSubFilesList(source , hidden=cls.__workWithHiddenFilesValue):

            if(GlobalDataFO.isOnLinux):
                newSource = source + "/" + i
                folderToBeGenerated = dest + "/" + GlobalMethods.getFolderNameToBeGenerated(i)
            else:
                newSource = source + "\\" + i
                folderToBeGenerated = dest + "\\" + GlobalMethods.getFolderNameToBeGenerated(i)

            try:
                os.makedirs(folderToBeGenerated)
            except FileExistsError:
                pass

            done = cls.copy(newSource , folderToBeGenerated , returnStatus)

            if(not(returnStatus)):
                if(done == False):
                    toAppend = "failed to copy    " + newSource + "    to    " + folderToBeGenerated + "    with exception =    " + done
                    cls.errorList.append(toAppend)

                if(showCopy):
                    try:
                        yield "copying    {}    to    {}".format(newSource , folderToBeGenerated)
                    except Exception:
                        yield "copying    {}    to    {}".format(newSource , folderToBeGenerated)
                else:
                    yield

            else:
                if(done == False):
                    yield "error"
                else:
                    yield str(done)




    @classmethod
    def copyDir_withLoading(cls , source , dest , animationChar = "#" , showFile = False , showSpaceBtw = True):

        filesCount = 0

        for i in GlobalMethods.getSubFilesList(source , hidden=cls.__workWithHiddenFilesValue):
            filesCount += 1
            print("\rFinding files to copy || found till now = {}".format(filesCount) , end="")

        if(showSpaceBtw):
            print("\n")
        else:
            print()

        loop = tqdm(total=filesCount , position=0 , leave=False)

        if(showFile):
            for i in cls.copyDir_withoutLoading(source , dest):
                loop.set_description(i)
                loop.update(1)
            loop.close()

        else:
            for i in cls.copyDir_withoutLoading(source , dest):
                loop.set_description("copying...        ")
                loop.update(1)
            loop.close()



    @classmethod
    def copy(cls , source , destination , returnStatus = False):

        
        # for linux
        if(GlobalDataFO.isOnLinux):

            newSource = source
            newDest = destination
            
            # if the path is pre correct
            yes = False
            for i in source:
                if(i == "\\"):
                    yes = True
                    break


            # if the path is not correctly passed like projects/hello boi/ is actaully projects/hello\ boi/ 
            if(not(yes)):

                # converting the source
                tempList = []
                newString = ""
                tempList = source.split("/")

                for i in tempList:
                    space = False
                    string = ""
                    for j in i:
                        if(j == " "):
                            space = True
                            break

                    if(space):
                        tempList2 = []
                        tempList2 = i.split(" ")
                        for i in tempList2:
                            string = string + i + "\\" + " "
                        
                        string = string[:-2]
                    
                    else:
                        string = i
                    
                    newString = newString + string + "/"

                newSource = newString[:-1]


                # converting the destination
                tempList.clear()
                newString = ""
                tempList = destination.split("/")

                for i in tempList:
                    space = False
                    string = ""
                    for j in i:
                        if(j == " "):
                            space = True
                            break

                    if(space):
                        tempList2 = []
                        tempList2 = i.split(" ")
                        for i in tempList2:
                            string = string + i + "\\" + " "
                        
                        string = string[:-2]
                    
                    else:
                        string = i
                    
                    newString = newString + string + "/"

                newDest = newString[:-1]


            # making the command
            toExe = "cp " + str(newSource) + " " + str(newDest)

        # for windows
        else:

            newSource = source
            newDest = destination

            # if the path is pre correct
            yes = False
            for i in source:
                if(i == '"'):
                    yes = True
                    break

            
            if(not(yes)):

                # converting the source
                tempList = []
                newString = ""
                tempList = source.split("\\")

                for i in tempList:
                    space = False
                    string = ""
                    for j in i:
                        if(j == " "):
                            space = True
                            break

                    if(space):
                        string = '"' + i + '"'
                    
                    else:
                        string = i
                    
                    newString = newString + string + "\\"

                newSource = newString[:-1]


                # converting the destination

                tempList.clear()
                newString = ""
                tempList = destination.split("\\")

                for i in tempList:
                    space = False
                    string = ""
                    for j in i:
                        if(j == " "):
                            space = True
                            break

                    if(space):
                        string = '"' + i + '"'
                    
                    else:
                        string = i
                    
                    newString = newString + string + "\\"

                newDest = newString[:-1]


            # making the command
            toExe = "copy " + str(newSource) + " " + str(newDest)
        

        # executing the command
        # will return True if succesfull or Return exception in form of string if the process fails if the returnStatus is False which is by default
        # will return output message generated the system call if succesfull else return False if the returnStatus is set to True
        try:
            status = subprocess.check_output(toExe, shell=True , stderr=subprocess.STDOUT)
            if(returnStatus):
                return status.decode("utf-8") 
            else:
                return True

        except Exception as e:
            if(returnStatus):
                return False
            else:
                return str(e)




# for testing purpose
if __name__ == "__main__":

    # file1 = r"C:\Users\harsh\Desktop\hello.txt"
    # file1dir = r"C:\Users\harsh\Desktop\Quick launch\hello.txt"

    # file2 = r"C:\Users\harsh\Desktop\MY_files\my softwares\instagram bot - find unfollowing\.git\objects\2a\9c1042772519e56e45c8f078a5ab4a1a223dd3"
    # file2dir = r"C:\Users\harsh\Desktop\9c1042772519e56e45c8f078a5ab4a1a223dd3"

    # status = EasyCopy.copy(file2 , file2dir , True)

    source = r"Z:\docx"
    dest = r"C:\Users\harsh\Desktop\New folder"

    count = 0

    EasyCopy.workWithHiddenFiles()

    EasyCopy.copyDir_withLoading(source , dest)


    # for i in EasyCopy.copyDir_withoutLoading(source , dest , returnStatus=True):
    #     print(i)

    print(EasyCopy.errorList)
    pass