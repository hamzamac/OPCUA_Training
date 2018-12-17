import os
path = 'C:\\Users\\Makame\\Documents\\Projects\\Python\\OPCUA\\'

def delete_local_file(path:str, filename:str):
    with os.scandir(path) as it:
        for entry in it:
            if entry.name.startswith(filename) and entry.is_file():
                os.remove(entry.path)


delete_local_file(path, 'node1')