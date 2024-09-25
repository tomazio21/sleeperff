import httputil

urls = {
    "get_league": "https://api.sleeper.app/v1/league/"
}

league_id = input('enter league id:\n')

response = httputil.get(urls['get_league']+league_id)
print(response)
