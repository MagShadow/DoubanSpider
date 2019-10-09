import sys
from utilities import *
from user_spider import dig_user
from status_spider import collect_status

# import getopt


def main(argv):
    """
    -h: Show Help;
    -s: Generate Personal Status;
    -i: Collect User Info;
    -c: Compare 2 User and Generate Report;
    -p: Generate Personal Report

    -s [user_id] [-t day]
    -i [user_id]
    """
    # print(argv)
    l = len(argv)
    try:
        opt = argv[0][1].lower()
        assert opt in {"h", "s", "i", "c", "p"}
        if opt == "h":
            print(main.__doc__)
        try:
            se = login(os.path.join("src", "config.json"))
        except:
            print("Login Error!")
            exit(2)
        try:
            f = open(os.path.join("src", "config.json"), "r")
            user_json = json.load(f)
        except:
            print("Need config.json!")
            exit(2)

        if opt == "s":
            if l == 1:
                filename = os.path.join(
                    user_json["user"], user_json["user"]+"_status.html")
                collect_status(user_json["user"], se,
                               time_window=86400*1, filename=filename)
                return

            if argv[1].lower() == "-t":
                filename = os.path.join(
                    user_json["user"], user_json["user"]+"_status.html")
                time_window = float(argv[2])*86400
                collect_status(user_json["user"], se,
                               time_window=time_window, filename=filename)
                return
            else:
                tar_user_id = argv[1]
                filename = os.path.join(
                    tar_user_id, tar_user_id+"_status.html")
                time_window = 86400
                if l >= 4 and argv[2].lower() == "-t":
                    time_window = float(argv[3])*86400
                collect_status(tar_user_id, se,
                               time_window=time_window, filename=filename)
                return

        if opt == "i":
            try:
                if l == 1:
                    dig_user(user_json["user"], se, recursive=False)
                    return
                dig_user(argv[1], se, recursive=False)
                return
            except Exception as e:
                print(e)
                print("User_id is wrong!")
                exit(2)

        if opt == "c":
            print("Function not complete. Please wait for updates.")
            return
        if opt == "p":
            print("Function not complete. Please wait for updates.")
            return
    except Exception as e:
        print(e)
        print(main.__doc__)
        exit(2)


if __name__ == "__main__":
    main(sys.argv[1:])
