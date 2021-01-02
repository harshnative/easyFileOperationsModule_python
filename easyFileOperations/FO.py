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

    # function to check for secific file extensions and then chech whether to keep both files if the file already exist in the destination folder 
    @classmethod
    def keepBothFiles(cls , source , destPath , keepVideo = True , keepMusic = True , keepImg = True , customList = None , sizeMatter = True):
        
        toReturnAtLast = destPath

        # list of video formats to check 
        videoFormatList = [
            'mp4' , 
            'm4v' , 
            'mov' , 
            'wmv' , 
            'flv' , 
            'avi' , 
            'mkv' ,
        ]

        # list of music format to check 
        musicFormatList = [
            'm4a' , 
            'flac' , 
            'mp3' , 
            'mp4' , 
            'wav' , 
            'wma' , 
            'aac' , 
        ]

        # list of img format to check 
        imgFileFormat = [
            'jpeg' , 
            'jpg' , 
            'gif' , 
            'png' , 
            'svg' , 
            'eps' , 
            'heif' , 
            'bmp' , 
            'webp' , 
            'psd' , 
            'ai' , 
            'indd' ,
        ]

        # extracting the file format of file 
        fileFormat = ""

        for i in destPath[::-1]:
            if(i == "."):
                break
            if(GlobalDataFO.isOnLinux):
                if(i == '/'):
                    break
            elif(GlobalDataFO.isOnWindows):
                if(i == "\\"):
                    break
            
            fileFormat = fileFormat + i

        fileFormat = fileFormat[::-1]

        # if the dest path is not passed with file name then file format path will be zero 
        if(len(fileFormat) == 0):
            
            # then getting the file name from the source path 
            tempFileName = ""

            for i in source[::-1]:
                if(GlobalDataFO.isOnLinux):
                    if(i == '/'):
                        break
                elif(GlobalDataFO.isOnWindows):
                    if(i == "\\"):
                        break

                tempFileName = tempFileName + i

            tempFileName = tempFileName[::-1]
            
            # adding the file name to destination path 
            if(GlobalDataFO.isOnLinux):
                if(destPath[-1] != "/"):
                    destPath = destPath + "/" + tempFileName
                else:
                    destPath = destPath + tempFileName

            elif(GlobalDataFO.isOnWindows):
                if(destPath[-1] != "\\"):
                    destPath = destPath + "\\" + tempFileName
                else:
                    destPath = destPath + tempFileName


            # now the dest path is normal so we can again extract the file format 
            fileFormat = ""

            for i in destPath[::-1]:
                if(i == "."):
                    break
                if(GlobalDataFO.isOnLinux):
                    if(i == '/'):
                        break
                elif(GlobalDataFO.isOnWindows):
                    if(i == "\\"):
                        break
                
                fileFormat = fileFormat + i

            fileFormat = fileFormat[::-1]

        tempFileFormat = fileFormat
        fileFormat = fileFormat.upper()

        # file name without extension
        fileNameWithoutExt = destPath[:len(destPath) - len(fileFormat) - 1]


        # if the file does not already exist then just return destpath
        if(not(os.path.isfile(destPath))):
            return destPath
        
        
        # checking the size of source and dest file
        # if the size is same then we just replace it
        sizeSource = os.stat(source).st_size
        sizeDest = os.stat(destPath).st_size

        if(sizeMatter and (sizeSource == sizeDest)):
            return destPath
        

        # checking if the file is video or not
        if(keepVideo):
            for i in videoFormatList:
                i = i.upper()
                
                # if the file is video then we need to rename
                if(i == fileFormat):
                    count = 0
                    while(True):
                        newDestPath = fileNameWithoutExt + " (" + str(count) + ")." + tempFileFormat
                        
                        if(not(os.path.isfile(newDestPath))):
                            return newDestPath
                        
                        count += 1

        if(keepMusic):
            for i in musicFormatList:
                i = i.upper()
                
                # if the file is music then we need to rename
                if(i == fileFormat):
                    count = 0
                    while(True):
                        newDestPath = fileNameWithoutExt + " (" + str(count) + ")." + tempFileFormat
                        
                        if(not(os.path.isfile(newDestPath))):
                            return newDestPath
                        
                        count += 1

        if(keepImg):
            for i in imgFileFormat:
                i = i.upper()
                
                # if the file is img then we need to rename
                if(i == fileFormat):
                    count = 0
                    while(True):
                        newDestPath = fileNameWithoutExt + " (" + str(count) + ")." + tempFileFormat
                        
                        if(not(os.path.isfile(newDestPath))):
                            return newDestPath
                        
                        count += 1

            
        if(customList != None):
            try:
                for i in customList:
                    i = i.upper()
                    
                    # if the file matches the format in custom list then we need to rename
                    if(i == fileFormat):
                        count = 0
                        while(True):
                            newDestPath = fileNameWithoutExt + " (" + str(count) + ")." + tempFileFormat
                            
                            if(not(os.path.isfile(newDestPath))):
                                return newDestPath
                            
                            count += 1

            except Exception as e:
                raise Exception("function returned this error - " + str(e) + "      May be file extensions are passed wrongly")

        return toReturnAtLast


            


    @classmethod
    def isDrive(cls , path = None):
        count = 0
        if(path == None):
            return None
        else:
            for i in path:
                if((i == '\\') or (i == "/")):
                    count += 1
        
        if(count <= 2):
            return True
        else:
            return False






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
    keepVideoForCopy = True 
    keepMusicForCopy = True
    keepImgForCopy = True
    customListForCopy = None 
    sizeMatterForCopy = True
    



    # function to set the hidden files mode to ON
    @classmethod
    def workWithHiddenFiles(cls):
        cls.__workWithHiddenFilesValue = True

    # function to set the paramerters to deal with same file name while copying
    @classmethod
    def setParmsForCopyFile(cls ,  keepVideo=True , keepMusic= True, keepImg=True , customList=None, sizeMatter=True):
        cls.keepVideoForCopy = keepVideo
        cls.keepMusicForCopy = keepMusic
        cls.keepImgForCopy = keepImg
        cls.customListForCopy = customList
        cls.sizeMatterForCopy = sizeMatter



    # function to set the hidden files mode to OFF
    @classmethod
    def dontWorkWithHiddenFiles(cls):
        cls.__workWithHiddenFilesValue = False


    # function to copy the entire dir recursively without any loading animation 
    # slighty faster as animation code does not have to be runned
    # pass the source dir , dest dir
    # if the show copy is True then program will return a string containing deatils about which files are been copied currently
    # if the return Status is True , then it will return the output generated by the shell during the operation
    @classmethod
    def copyDir_withoutLoading(cls , source , dest , showCopy = False , returnStatus = False):

        cls.errorList.clear()

        # getting which file as to be copied
        for i in GlobalMethods.getSubFilesList(source , hidden=cls.__workWithHiddenFilesValue):

            # generating the folder for the file 
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
            except PermissionError as e:
                cls.errorList.append(str(e))
                
            # copying the file
            done = cls.copy(newSource , folderToBeGenerated , returnStatus)

            # returning the desired output 
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



    # function to copy the entire dir recursively with a built in loading animation
    # if show file is true program will also display which files to currently copied
    # if showSpaceBtw is True then their will be a gap btw files found animation and file copy animation
    @classmethod
    def copyDir_withLoading(cls , source , dest , showFile = False , showSpaceBtw = False):

        # getting the number of files to be copied
        filesCount = 0

        for i in GlobalMethods.getSubFilesList(source , hidden=cls.__workWithHiddenFilesValue):
            filesCount += 1
            print("\rFinding files to copy || found till now = {}".format(filesCount) , end="")

        if(showSpaceBtw):
            print("\n")

        # using the tqdm module for animation
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



    # function to copy a single file
    @classmethod
    def copy(cls , source , destination , returnStatus = False):

        
        # for linux
        if(GlobalDataFO.isOnLinux):

            newDest = GlobalMethods.keepBothFiles(source , destination , keepVideo=cls.keepVideoForCopy , keepMusic=cls.keepMusicForCopy , keepImg=cls.keepImgForCopy , customList=cls.customListForCopy , sizeMatter=cls.sizeMatterForCopy)

            newSource = source
            
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
                tempList = newDest.split("/")

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

            # method called to check if we want to keep both files with similar names
            newDest = GlobalMethods.keepBothFiles(source , destination , keepVideo=cls.keepVideoForCopy , keepMusic=cls.keepMusicForCopy , keepImg=cls.keepImgForCopy , customList=cls.customListForCopy , sizeMatter=cls.sizeMatterForCopy)
            newSource = source

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
                tempList = newDest.split("\\")

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

    file1 = r"C:\Users\harsh\Desktop\101916125.png"
    file1dir = r"C:\Users\harsh\Desktop\Quick launch\101916125.png"

    # # file2 = r"C:\Users\harsh\Desktop\MY_files\my softwares\instagram bot - find unfollowing\.git\objects\2a\9c1042772519e56e45c8f078a5ab4a1a223dd3"
    # # file2dir = r"C:\Users\harsh\Desktop\9c1042772519e56e45c8f078a5ab4a1a223dd3"

    status = EasyCopy.copy(file1 , file1dir , True)

    # source = r"C:\Users\harsh\Desktop\hello"
    # dest = r"C:\Users\harsh\Desktop\hello1"

    # count = 0

    # EasyCopy.workWithHiddenFiles()

    # EasyCopy.copyDir_withLoading(source , dest)


    # for i in EasyCopy.copyDir_withoutLoading(source , dest , returnStatus=False):
    #     print(i)

    # print(EasyCopy.errorList)

    # for i in GlobalMethods.getSubFilesList(r"Z:\docx" , hidden=True):
    #     print(i)
    # pass