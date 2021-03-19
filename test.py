def func0():
    print("Ran function 0")

def func1():
    print("Ran function 1")

def func2():
    print("Ran function 2")

# Current implementation:
# selected = input("Select function: ")

# if selected == "func0":
#     func0()
# elif selected == "func1":
#     func1()
# elif selected == "func2":
#     func2()

# Wanted implementation:
options = {"func0": func0, "func1": func1, "func2": func2}

func = None
while func is None:
    func = options.get(input("Select function: "), None)
    if func is None:
        print("Invalid function!")

func()