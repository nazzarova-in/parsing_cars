def find_prices(file):
    prices = []

    for car in file:
        clean_price = int(car['price'].replace(' ', '').replace('€', ''))
        prices.append({
            'price': clean_price,
            'link': car['link']
        })

    print(prices)

    min_price_item = min(prices, key=lambda x: x['price'])
    max_price_item = max(prices, key=lambda x: x['price'])
    average_price = round(sum(p['price'] for p in prices) / len(prices))

    return {
        'min_price': min_price_item['price'],
        'min_link': min_price_item['link'],
        'max_price': max_price_item['price'],
        'max_link': max_price_item['link'],
        'average_price': average_price,
    }

