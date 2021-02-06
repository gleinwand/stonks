import finnhub

# Setup client
finnhub_client = finnhub.Client(api_key="c0fgiif48v6snribasr0")

print(len(finnhub_client.stock_symbols('US')))
