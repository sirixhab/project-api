import requests

def convert(amount, curr_from, curr_to):
    r = requests.get('https://api.frankfurter.app/latest', params={'from':curr_from, 'to':curr_to})  
    
    r.raise_for_status()

    data = r.json()
    rate = data['rates'][curr_to]

    return amount * rate

print(convert(1000, 'INR' , 'USD'))
print(convert(1000, 'KRW' , 'MXN'))
print(convert(1000, 'NZD' , 'PHP'))
print(convert(1000, 'ZAR' , 'TRY'))


# chaining data, real-world JSON structures

