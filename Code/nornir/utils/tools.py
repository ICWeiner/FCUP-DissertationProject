CONFIG_FILE = "./config.yaml"
# modify host file from config json object
def updated_inventory_host(filename):
    path = "inventory/" + filename
    inventory = {
            "plugin": "SimpleInventory",
            "options": {
                "host_file": path,
                "group_file": "inventory/groups.yaml",
                "defaults_file": "inventory/defaults.yaml"
            }
        }
    
    runner={
        "plugin": "threaded",
        "options": {
            "num_workers": 2
        }
    }
    return inventory, runner