from datetime import date

class Helper:

    def getFileExtension(filename):
        return filename.split(".")[1]

    def allowedFile(filename, allowed_extensions):
        ext = Helper.getFileExtension(filename)
        return ext in allowed_extensions
    
    def getFileName(ext):
        return str(date.today()) + '.' + ext
