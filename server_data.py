def init_server_ruleset(mongo_client, server_id):
    print("Init server ruleset: " + str(server_id))
    db = mongo_client["filter"]
    server_data = db["server_data"]
    find_server = server_data.find_one({"server_id": str(server_id)})
    if not find_server:
        server_data.insert_one({"server_id": str(server_id),
            "ruleset": "CONTEXT START: You are the moderator of a Discord server.\nRULES:"})


def set_server_ruleset(mongo_client, server_id, ruleset):
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
    db = mongo_client["filter"]
    server_data = db["server_data"]
    server = server_data.find_one({"server_id": str(server_id)})
    if not server:
        return False
    return server.get("ruleset")
