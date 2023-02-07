import requests
headers = {
"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
}
url = "https://www.trading-logic.com/index.html"
response = requests.get(url, headers=headers).text
response = response.split("<script type=\"application/json\" data-for=\"river\">")[1]
response = response.split("</script>")[0]
response = response.split("\"data\":")[1]
response = response.split("}]")[0]
print(response)