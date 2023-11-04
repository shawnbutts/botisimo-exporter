#!/usr/bin/env python3
import sys
import csv
import os
import json

from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport

csvFile = "viewers.csv"
rawFile = "viewers.jsonl"


def GatherData(APIkey, csvfile, rawfile):
    headers = {
        "Client-ID": APIkey,
        "Content-Type": "application/json",
        "user-agent": "exporter/0.0.1",
        "Accept": "*/*",
    }
    transport = AIOHTTPTransport(url="https://botisimo.com/graphql", headers=headers)
    client = Client(transport=transport, fetch_schema_from_transport=False)
    limit = 100

    with open(csvfile, "w", newline="") as c:
        fieldnames = ["user", "points"]
        cvswriter = csv.DictWriter(c, fieldnames=fieldnames)
        cvswriter.writeheader()

        with open(rawfile, "w") as r:
            query = gql(
                """
                query ($limit: Int!, $curpage: Int!) {
                  globalUsers(pagination: { limit:$limit, page:$curpage }) {
                    pageInfo {
                      limit
                      page
                      hasNextPage
                      total
                    }
                    edges {
                      node {
                        id
                        currency
                        level
                        xp
                        createdAt
                        updatedAt
                        accountId
                        twitchUserId
                        twitchUser {
                          id
                          createdAt
                          updatedAt
                          name
                        }
                        youtubeUserId
                        youtubeUser {
                          id
                        }
                        discordUserId
                        discordUser {
                          id
                          createdAt
                          updatedAt
                          name
                        }
                      }
                    }
                  }
                }
            """
            )

            try:
                hasnext = True
                i = 0
                while hasnext:
                    variables = {"limit": limit, "curpage": i + 1}
                    data = client.execute(query, variable_values=variables)

                    print("Processing page:", i + 1)

                    r.write(json.dumps(data) + "\n")
                    users = data["globalUsers"]["edges"]
                    for u in users:
                        if u["node"]["twitchUser"] is not None:
                            user = u["node"]["twitchUser"]["name"]
                            points = u["node"]["currency"]
                            if user is not None and points > 0:
                                cvswriter.writerow({"user": user, "points": points})

                    i += 1
                    hasnext = data["globalUsers"]["pageInfo"]["hasNextPage"]

                print("Processing complete")
            except Exception as e:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                print(exc_type, fname, exc_tb.tb_lineno)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Error: Must provide API Client Key")
    else:
        apikey = sys.argv[1]

    GatherData(apikey, csvFile, rawFile)
