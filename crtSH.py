import requests, time, random, sys


def is_valid_subdomain(entry, target_domain):
    new_all_domain = []
    for i in entry:
        e = i.strip()
        if '@' in e or ' ' in e:
            continue
        elif e == target_domain or e.endswith('.' + target_domain):
            new_all_domain.append(e)
        
    return new_all_domain 

def enumerate_subdomains(target_domain):
    url = f'https://crt.sh/?q={target_domain}&output=json'
    response = requests.get(url)
    print(response.status_code)
    for i in range(10):
        if response.status_code == 200:
            data = response.json()
            break
        time.sleep(random.uniform(5, 10))
        response = requests.get(url)
        print(response.status_code)
    else:
        print("Failed to retrieve data after 10 attempts. crt.sh may be down")
        sys.exit(1)

    all_domains = set()
    for i in range(len(data)):
        domain_x = data[i]['name_value']
        domain = domain_x.split('\n')
        all_domains.update(domain)
    for d in all_domains:
        if ']' in d or '[' in d:
            print(repr(d))

    new_all_domain = is_valid_subdomain(all_domains, target_domain)
    return new_all_domain

domain = input("Enter a domain to enumerate: ")
results = enumerate_subdomains(domain)
print(results)
