
str_main_header = "\n\n\n\n -- ANN Lab1 --\n---------------------"


class ANN:
    filename = str
    layers = list()
    results = list()


training_set = list()
verification_set = list()
test_set = list()

ann = ANN()


def ANN_run():
    # after running
    print("Do you want to save the results?")
    if user_confirmation():
        # save results
        return 1
    else:
        # discard results
        return 1


def ANN_train():
    # train ANN
    # save results
    return 1


def ANN_save():
    # print ANN files already saved
    # input file name to save ANN in
    return 1


def ANN_new():
    # randomize weights
    # clear results
    return 1


def ANN_load():
    # if files exist: choose a file
    # check that ANN could be loaded
    return 1


def ANN_results():
    # if results exists: print them
    if False:
        # print results
        return 1
    else:
        print("No results were found\n\npress ENTER to continue")
        input()

        main_menu()


def ANN_exit():
    print("Are you sure you want to exit?")
    if user_confirmation():
        print("exiting...")
        return -1
    else:
        return 0


def user_confirmation():
    usr_input = input("[y/N]\n ").lower()  # get first character and make it lowercase

    if usr_input in {"y", "yes"}:
        return 1
    else:
        return 0


def invalid_func():
    print("Switcher: Invalid function")
    return -1


switcher_options = {
    "train": ANN_train,
    "run": ANN_run,
    "results": ANN_results,
    "save": ANN_save,
    "load": ANN_load,
    "new": ANN_new,
    "exit": ANN_exit
}


def switcher(available_choices):
    print("Choose one of the following:", sep="\n")
    for string in available_choices:
        print("* " + string[0].upper() + string[1:])

    usr_input = input("Enter your choice:\n   ").lower()
    while usr_input not in available_choices:
        usr_input = input("Try again:\n   ").lower()

    func = switcher_options.get(usr_input, lambda: "invalid_func")
    return func()


def main_menu():
    retval = None

    available_choices = {"new", "load", "exit"}
    while retval != 1:
        print(str_main_header)
        retval = switcher(available_choices)
        if retval == -1:
            return -1
    # [print ANN file name]

    while retval != -1:
        available_choices = {
            "train",
            "run",
            "results",
            "save",
            "load",
            "new",
            "exit"
        }
        print(str_main_header)
        retval = switcher(available_choices)

    return


main_menu()

