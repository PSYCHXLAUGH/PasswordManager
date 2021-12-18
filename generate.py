import argparse
import shutil
import sys
import os

from cryptography.fernet import Fernet

from libs.console import ConsoleLog
from libs.handler import Generate
from libs.const import FOLDERNAME

def generate(console, key, file):

    key_data = Fernet.generate_key()
    cipher = Fernet(key_data)

    message = console.ok("generate new key: " + str(key_data))
    print(message)
    
    with open(FOLDERNAME + "\\" + key, 'wb') as f:
        f.write(key_data)
        f.close()
    
    message = console.ok("generate new file key: '" + key + "'")
    print(message)
    
    info = Generate.Date()

    with open(FOLDERNAME + "\\" + file, 'wb') as f:
        f.write(cipher.encrypt(Generate.NewData(
            ["info"],
            [info]
        )))
        f.close()
        
    message = console.ok("generate new file: '" + file + "'")
    print(message)

if __name__ == "__main__":

    console = ConsoleLog()
    parser = argparse.ArgumentParser()
    parser.add_argument("--key", "-k", type = str, help = "Key file name", default = "key")
    parser.add_argument("--file", "-f", type = str, help = "File name", default = "passwords")
    parser.add_argument("--rewrite", "-r", action = 'store_const', help = "rewriting mode", const = True)
    parser.add_argument("--clean", "-c", action = 'store_const', help = "clean mode", const = True) # поменять store на store_true
    
    args = parser.parse_args()

    if os.path.exists(FOLDERNAME) == True and args.clean == True:
        
        shutil.rmtree(FOLDERNAME)
        
        message = console.ok("the folder '" + FOLDERNAME + "' was cleaned up successfully")
        print(message)
        
        os.mkdir(FOLDERNAME)
        
        message = console.ok("created folder '" + FOLDERNAME + "'")
        print(message)
        
        generate(
            console,
            args.key, 
            args.file
        )

    elif os.path.exists(FOLDERNAME) == False:
        os.mkdir(FOLDERNAME)
        
        if args.clean == True:
            message = console.warning("folder '" + FOLDERNAME + "' does not exist")
            print(message)
        
        message = console.ok("created folder '" + FOLDERNAME + "'")
        print(message)
        
        generate(
            console,
            args.key,
            args.file
        )

    else:

        if os.path.exists(FOLDERNAME + "\\" + args.key) or os.path.exists(FOLDERNAME + "\\" + args.file):
            
            if args.rewrite == None:
                message = console.question("are you sure you want to overwrite the data in the folder '" + FOLDERNAME + "'? y/n >> ")
                print(message, end = '')
                
                yn = input()
            
                if yn.lower() == "y":       
                    generate(
                        console,
                        args.key,
                        args.file
                    )

                elif yn.lower() == "n" or yn == '':
                    sys.exit(0)
            else:
                generate(
                    console,
                    args.key,
                    args.file
                )

        else:
            generate(console,
                     args.key,
                     args.file
            )