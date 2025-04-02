import os
CONFIG_FILE = "./config.yaml"
# modify host file from config json object
def updated_inventory_host(filename):
    destination_folder = os.path.join( os.getenv("PYTHONPATH","../..") , "inventory")
    path = os.path.join(destination_folder, filename)
    inventory = {
            "plugin": "SimpleInventory",
            "options": {
                "host_file": path,
                "group_file": os.path.join(destination_folder, "groups.yaml"),
                "defaults_file": os.path.join(destination_folder, "defaults.yaml")
            }
        }
    
    runner={
        "plugin": "threaded",
        "options": {
            "num_workers": 2
        }
    }
    return inventory, runner