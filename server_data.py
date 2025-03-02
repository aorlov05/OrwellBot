def init_server_ruleset(mongo_client, server_id):
    """
    Initializes a new server's database with the default ruleset.

    Parameters:
    mongo_client: the MongoClient object used to interact with the database
    server_id: the unique id for each Discord server

    Returns:
    None
    """
    print("Init server ruleset: " + str(server_id))
    db = mongo_client["filter"]
    server_data = db["server_data"]
    find_server = server_data.find_one({"server_id": str(server_id)})
    if not find_server:
        server_data.insert_one({"server_id": str(server_id),
            "ruleset": "CONTEXT START: You are the moderator of a Discord server.\nRULES:"})


def set_server_ruleset(mongo_client, server_id, ruleset):
    """
    Sets the ruleset for a Discord server.

    Parameters:
    mongo_client: the MongoClient object used to interact with the database
    server_id: the unique id for each Discord server
    ruleset: the provided ruleset string

    Returns:
    None
    """
    print(ruleset)
    db = mongo_client["filter"]
    server_data = db["server_data"]
    server = server_data.find_one({"server_id": str(server_id)})
    if server:
        server_data.update_one(
            {"server_id": str(server_id)},
            {"$set": {"ruleset": ruleset}},
            upsert=True
        )
        print("Done")

def get_server_ruleset(mongo_client, server_id):
    """
    Gets the ruleset for a Discord server.

    Parameters:
    mongo_client: the MongoClient object used to interact with the database
    server_id: the unique id for each Discord server

    Returns:
    The requested server's ruleset
    """
    db = mongo_client["filter"]
    server_data = db["server_data"]
    server = server_data.find_one({"server_id": str(server_id)})
    if not server:
        return False
    return server.get("ruleset")

def add_server_ruleset(mongo_client, server_id, ruleset):
    """
    Adds to the end of a server's ruleset

    Parameters:
    mongo_client: the MongoClient object used to interact with the database
    server_id: the unique id for each Discord server
    ruleset: the provided ruleset string

    Returns:
    None
    """
    db = mongo_client["filter"]
    server_data = db["server_data"]
    server = server_data.find_one({"server_id": str(server_id)})
    newruleset=server.get("ruleset")+ruleset
    if server:
        server_data.update_one(
            {"server_id": str(server_id)},
            {"$set": {"ruleset": newruleset}},
            upsert=True
        )
        print("Done")
