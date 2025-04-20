def find_prices(file):
    prices = []
    for car in file:
        prices.append(car['price'])

    new_price = []
    for price in prices:
        clean_price = int(price.replace(' ', '').replace('€', ''))
        new_price.append(clean_price)

    min_price = min(new_price)
    max_price = max(new_price)
    average_price = round(sum(new_price) / len(new_price))

    return {
        'min_price': min_price,
        'max_price': max_price,
        'average_price': average_price,
    }
