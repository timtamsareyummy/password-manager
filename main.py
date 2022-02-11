import os
import json
import io
from hashlib import sha256
import pyAesCrypt


def hashstr(hashed):
    return sha256(hashed.encode('utf-8')).hexdigest()


if os.path.isfile('./hashedMasterPassword.txt'):
    while 1:
        masterPassword = str(input('Master password: '))
        hashedMasterPassword = str(open('hashedMasterPassword.txt','r').readlines())
        if hashstr(masterPassword) == hashedMasterPassword.strip("[']"):
            print('Success!')
            break
        else:
            print('Try again')
else:
    masterPassword = str(input('No master password detected, please specify one now: '))
    hashedMasterFile = open("./hashedMasterPassword.txt", "w")

    hashedMasterFile.write(hashstr(masterPassword))
    hashedMasterFile.close()

if os.path.isfile('PassList.json'):
    print('FATAL ERROR: UNENCRYPTED PASS LIST DETECTED, PLEASE ONLY EXIT USING THE PROVIDED OPTION')
    input("By pressing enter, you agree that terminating the program both jeopardizes your security and also stops the "
          "program from saving correctly: ")

if os.path.isfile('EncryptedPassList.aes'):

    infile = "EncryptedPassList.aes"
    with open(infile, "rb") as fCiph:

        fDec = io.BytesIO()
        inputFileSize = os.stat(infile).st_size
        pyAesCrypt.decryptStream(fCiph, fDec, masterPassword, 64 * 1024, inputFileSize)

        fDec.seek(0)
        passList = json.loads(fDec.read())
else:
    passList = {}
    print('No password file found, creating now...')


def savepass():
    passListOutput = json.dumps(passList)
    with open("EncryptedPassList.aes", "wb") as fOut:
        fIn = io.BytesIO(bytes(passListOutput, 'utf-8'))
        fIn.seek(0)
        pyAesCrypt.encryptStream(fIn, fOut, masterPassword, 64 * 1024)


while 1:
    print('')
    print('Please select one the following:')
    print('1: Create/Overwrite password')
    print('2: Delete existing password')
    print('3: Read existing password')
    print('4: List all services')
    print('5: Exit')
    print('')

    operation = str(input())
    match operation:
        case '1':
            print('')
            serviceToSave = str(input('Service: '))
            passToSave = str(input('Password: '))
            passList[serviceToSave] = passToSave
            print('Saved!')
            savepass()
            print('')
            input("Press Enter to continue...")
        case '2':
            print('')
            serviceToDelete = str(input('Service to delete: '))
            if serviceToDelete in passList:
                passList.pop(serviceToDelete)
                savepass()
                print('success!')
                print('')
                input("Press Enter to continue...")
            else:
                print(serviceToDelete + " doesn't exist! Please retry")
                print('')
                input("Press Enter to continue...")
        case '3':
            print('')
            serviceToCheck = str(input('Service: '))
            if serviceToCheck in passList:
                print("Password: " + passList[serviceToCheck])
            else:
                print(serviceToCheck + " Doesn't Exist!")
            print('')
            input("Press Enter to continue...")
        case '4':
            print('')
            if str(list(passList.keys())) != '[]':
                print(list(passList.keys()))
            else:
                print('No services or passwords exist!')
            input("Press Enter to continue...")
        case '5':
            break

savepass()