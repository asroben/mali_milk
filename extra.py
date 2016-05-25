def saveRecording(path):
    #remove file:// if present
    #a lot of %00 stuff to remove
    path =  path.replace("\00","")
    path = re.sub(r"(file:\/\/)?(.*)",r"\2",path)
    dest = findFreshFilePath(config.recordingsPath+ "recording.wav")
    #convert to format that is good for vxml as well as web interface
    subprocess.call(['/usr/bin/sox',path,'-r','8k','-c','1','-e','signed-integer',dest])
    #shutil.copy(path,dest)
    return dest

def findFreshFilePath(preferredPath):
    addition = 1
    path = re.sub(r"(.*\/)(\w*)(\.\w{3})",r"\1\2" + "_" + str(addition) + r"\3",preferredPath)
    while os.path.isfile(path):
        addition = addition + 1
        path = re.sub(r"(.*\/)(\w*)(\.\w{3})",r"\1\2" + "_" + str(addition) + r"\3",preferredPath)
    return path