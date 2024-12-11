from application import init_app
import sys

sys.path.append("..")#Necessary to import nornir_lib and proxmox folders in other parts of the app

app = init_app()

if __name__ == "__main__":
    app.run(host='0.0.0.0')