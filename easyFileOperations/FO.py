
# global variable for operating system detection
isOnWindows = False
isOnLinux = True

import platform

# Checking weather the user is on windows or not
osUsing = platform.system()

if(osUsing == "Windows"):
    isOnWindows = True
    isOnLinux = False




import subprocess



class easyCopy:

    @classmethod
    def copy(cls , source , destination , returnStatus = False):

        if(isOnLinux):
            toExe = "cp " + str(source) + " " + str(destination)

        else:

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

                if(space):
                    string = '"' + i + '"'
                
                else:
                    string = i
                
                newString = newString + string + "\\"

            newDest = newString[:-1]


            # making the command
            toExe = "copy " + str(newSource) + " " + str(newDest)
        
        # executing the command
        try:
            status = subprocess.check_output(toExe, shell=True)
            if(returnStatus):
                return status.decode("utf-8") 
            else:
                return True

        except Exception as e:
            if(returnStatus):
                return False
            else:
                return str(e)




if __name__ == "__main__":

    file1 = r"C:\Users\harsh\Desktop\hello.txt"
    file1dir = r"C:\Users\harsh\Desktop\Quick launch\hello.txt"

    file2 = r"C:\Users\harsh\Desktop\MY_files\my softwares\instagram bot - find unfollowing\.git\objects\2a\9c1042772519e56e45c8f078a5ab4a1a223dd3"
    file2dir = r"C:\Users\harsh\Desktop\9c1042772519e56e45c8f078a5ab4a1a223dd3"

    status = easyCopy.copy(file2 , file2dir , True)


