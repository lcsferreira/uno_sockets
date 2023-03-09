import time

def progress_bar(done):
    print("\rProgress: [{0:50s}] {1:.1f}%".format('#' * int(done * 50), done * 100),end='')

def test():
    for n in range(101):
        print(n)
        print(n/100)
        progress_bar(n/100)
        time.sleep(1)
        
test()