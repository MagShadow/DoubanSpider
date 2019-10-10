import sys
from utilities import *
from user_spider import dig_user
from status_spider import collect_status
from similarity import compare

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
    -c <user_id_1> <user_id_2> [-f]
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
            try:
                assert l >= 3
                user_id_1, user_id_2 = argv[1], argv[2]
                result = compare(se, user_id_1, user_id_2)
                print(f"Compare Result of {user_id_1} and {user_id_2}:")
                print()
                print("Number of Common Friends:", len(result["clist_friend"]))
                print("Number of Common Contacts:",
                      len(result["clist_contact"]))
                print("Number of Common Reverse Contacts:",
                      len(result["clist_rcontact"]))
                print()
                print("Number of Common Books:", len(result["clist_book"]))
                print("Number of Common Movies:", len(result["clist_movie"]))
                print("Number of Common Music:", len(result["clist_music"]))
                print("Number of Common Dramas:", len(result["clist_drama"]))
                print("Number of Common Games:", len(result["clist_game"]))
                print()
                print("Similarity of Ratings(percentage): %.1f" % (result["sim"]*100))
            except Exception as e:
                print(e)
                print(main.__doc__)
                exit(2)
        if opt == "p":
            print("Function not complete. Please wait for updates.")
            return
    except Exception as e:
        print(e)
        print(main.__doc__)
        exit(2)


if __name__ == "__main__":
    main(sys.argv[1:])
