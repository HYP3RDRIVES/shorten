# Shorten
A quick URL shortener

to use: simply just fill in .env_starter - rename to .env and then send POST requests to the /shorten endpoint - send the full original URL after /shorten (ex: /shorten/https://example.com/) and send Authorizaion token in a header with the same name. It will return the shortened URL, which the /<url> endpoint handles automatically.
