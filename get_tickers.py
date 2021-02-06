import config
import finnhub

# Setup client
finnhub_client = finnhub.Client(api_key=config.api_key)

print(len(finnhub_client.stock_symbols('US')))
