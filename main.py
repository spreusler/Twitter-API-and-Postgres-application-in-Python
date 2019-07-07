import utils


def main():
    keywords = utils.create_object_list()

    for obj in keywords:
        obj.insert_database()


main()
