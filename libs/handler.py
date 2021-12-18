from datetime import datetime

class Generate:
    
    def Date():
        now = datetime.now()
        return str(now.day) + "|" + str(now.month) + "|" + str(now.year) + "|" + str(now.hour) + "|" + str(now.minute)
    
    def NewData(args, write):

        string = ''
        
        for j in range(len(args)):
            string += "'" + args[j] + "'" + write[j]
        
        return string.encode("utf-8")
    
    def ConvertData(string):
        string = string.split(":")
        string = list(filter(None, string))

        data = [

            [string[x] for x in range(len(string)) if not x % 2 != 0],
            [string[x] for x in range(len(string)) if not x % 2 == 0]
            
        ]

        return data

class Read:
    
    def Data(string):

        string = string.split("'")
        string = list(filter(None, string))

        data = [

            [string[x] for x in range(len(string)) if not x % 2 != 0],
            [string[x] for x in range(len(string)) if not x % 2 == 0]
            
            ]

        return data[0], data[1]

    def AllData(string):

        data = string.split("\n")
        data = list(filter(None, data))

        return data
    
    def Date(array):
        
        date = list(
            map(
                str,
                array[0].split("|")
                )
            )
        
        info = date[0] + "-" + date[1] + "-" + date[2]
        time = date[3] + ":" + date[4]
        return info, time
    
    def ListData(string):
        return Read.AllData(string)

    def StringNumberByTag(list, tag, string):
        
        for x in range(len(list)):
            tags, strings = Read.Data(list[x])
            
            for j in range(0, (len(tags) + len(strings)) // 2):
                if tags[j] == tag and strings[j] == string:
                    return x