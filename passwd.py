import argparse
import sys
from platform import system

import pyperclip
from cryptography.fernet import Fernet

from libs.console import ConsoleLog
from libs.const import VERSION
from libs.handler import Read, Generate

def ReadEncryptData(cipher, file):
    with open(file, "rb") as f:
        encrypt_data = f.read()
    f.close()

    decrypt_data = cipher.decrypt(encrypt_data).decode("utf-8")

    return decrypt_data

def WriteEncryptData(cipher, file, data):
    with open(file, "wb") as f:
        string = ''
        
        for x in range(len(data)):
            if (x + 1) > len(data):
                string += data[x]
            string += data[x] + "\n"
            
        f.write(cipher.encrypt(string.encode("utf-8")))
    f.close()

    return True

if __name__ == "__main__":

    console = ConsoleLog()
    parser = argparse.ArgumentParser()

    parser.add_argument("--key", "-k", type = str, required = True, help = "Decryption key")
    parser.add_argument("--file", "-f", type = str, required = True, help = "Path to file")
    parser.add_argument("--read", "-r", type = str, default = "all", help = "read data from encrypted file")
    parser.add_argument("--write", "-w", type = str, help = "write encrypted data")
    parser.add_argument("--remove", "-R", type = str, help = "remove encrypted data")
    parser.add_argument("--rewrite", "-rw", type = str, help = "rewrite encrypted data")
    
    args = parser.parse_args()
    
    with open(args.key, "rb") as f:
        key = f.read()
        f.close()

    cipher = Fernet(key)
    
    data = ReadEncryptData(cipher, args.file)
    file_data = Read.ListData(data)
    info, time = Read.Date(file_data)

    if args.read == "all" and args.write is None and args.remove is None and args.rewrite is None:
        date = console.date(info, time, VERSION)
        print(date)
        if len(file_data) == 1:
            message = console.warning("file is empty.")
            print(message)
        for x in range(1, len(file_data)):
            passsword = console.password(Read.Data(file_data[x]))
            print(passsword)

    else:

        if args.write:
            data = args.write
            tags, data = Generate.ConvertData(data)
            generate_data = Generate.NewData(tags, data)
            file_data.append(generate_data.decode("utf-8"))
            file_data[0] = Generate.Date()
            if WriteEncryptData(cipher, args.file, file_data):
                message = console.ok("data entered successfully.")
                print(message)

        elif args.read != "all" and args.write is None and args.remove is None:
            date = console.date(info, time, VERSION)
            print(date)
            tag, string = args.read.split(":")
            element = Read.StringNumberByTag(file_data, tag, string)

            if element is not None:
                password = console.password(Read.Data(file_data[element]))
                print(password)
                tag_copy, string_copy = Read.Data(file_data[element])
                clip = ''

                for x in range((len(tag_copy) + len(string_copy)) // 2):
                    if (x + 1) >= ((len(tag_copy) + len(string_copy)) // 2):
                        clip += tag_copy[x] + ":" + string_copy[x]
                    else:
                        clip += tag_copy[x] + ":" + string_copy[x] + "\n"
                        
                if system() == "Windows":
                    pyperclip.copy(clip)
                    message = console.ok("data copied to clipboard.")
                    print(message)
                    
                else:
                    message = console.warning("On this operating system, the program does not support the functions of the clipboard.")
                    print(message)
                    
            else:
                message = console.error("data was not found.")
                print(message)

        elif args.remove:
            if args.remove == "all":
                
                if len(file_data) != 1:
            
                    message = console.question("Do you really want to delete all '" + str(len(file_data) - 1) + "' data from the file? ")
                    print(message, end = '')
                    yn = input("y/n >> ")
                    if yn.lower() == "y":
                        log = console.info(str(len(file_data) - 1) + " data has been deleted." )
                        file_data.clear()
                        file_data.append(Generate.Date())
                        if WriteEncryptData(cipher, args.file, file_data):
                            print(log)
                    else:
                        sys.exit(0)
                        
                else:
                    message = console.warning("file is empty.")
                    print(message)
            else:
                tag, string = args.remove.split(":")
                element = Read.StringNumberByTag(file_data, tag, string)

                if element is not None:
                    file_data.remove(file_data[element])
                    file_data[0] = Generate.Date()
                    if WriteEncryptData(cipher, args.file, file_data):
                        message = console.ok("data deleted successfully.")
                        print(message)
                else:
                    message = console.error("data was not found.")
                    print(message)

        elif args.rewrite:
            tag, string = args.rewrite.split("-")[0].split(":")
            totag, tostring = args.rewrite.split("-")[1].split(":")
            element = Read.StringNumberByTag(file_data, tag, string)

            if element is not None:
                list = Read.Data(file_data[element])
                tag_content, str_content = list

                for x in range((len(tag_content) + len(str_content)) // 2):
                    if tag_content[x] == tag and str_content[x] == string:
                        tag_content[x] = totag
                        str_content[x] = tostring
                        
                        rewrite_string = Generate.NewData(tag_content, str_content).decode("utf-8")
                        file_data[element] = rewrite_string
                        file_data[0] = Generate.Date()
                        
                        if WriteEncryptData(cipher, args.file, file_data):
                            message = console.ok("data changed successfully.")
                            print(message)
            else:
                message = console.error("data was not found.")
                print(message)