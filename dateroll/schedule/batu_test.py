import importlib


if __name__=='__main__':
    ddh = importlib.import_module("dateroll.ddh.ddh")
    import code
    code.interact(local=dict(globals(),**locals()))