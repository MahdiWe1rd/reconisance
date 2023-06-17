import dns.resolver
import requests
from bs4 import BeautifulSoup
import socket
import re
import whois




# subdomains and title and status code of each subdomain 


domain = input("enter domain : ")

ns = dns.resolver.query(domain, 'NS')



with open('mywordlist500.txt', 'r') as file:
    wordlist = file.read().splitlines()


printed_subdomains = set()



for server in ns:
    server = str(server)
    for word in wordlist:
        try:
            answers = dns.resolver.query(word + "." + domain, "A")
            for ip in answers:
                subdomain = word + "." + domain
                if subdomain in printed_subdomains:
                    continue

                url = f"http://{subdomain}"
                print("subdomain : " + word + "." + domain)
                print("*****************************")
                headers = {'User-Agent': 'Mozilla/5.0'}
                response = requests.get(url)
            

                soup = BeautifulSoup(response.content, 'html.parser')
                title = soup.title.text if soup.title else "No Title"
                print(f"{subdomain} - Title: {title}")

                if response.status_code == 200:
                    print(f"{subdomain} - status code : Success!")
                elif response.status_code == 301:
                    print(f"{subdomain} - status code :  Page moved permanently!")
                elif response.status_code == 302:
                    print(f"{subdomain} - status code :  Page found!")
                elif response.status_code == 400:
                    print(f"{subdomain} - status code :  Bad request!")
                elif response.status_code == 401:
                    print(f"{subdomain} - status code :  Unauthorized request!")
                elif response.status_code == 403:
                    print(f"{subdomain} - status code :  Forbidden request!")
                elif response.status_code == 404:
                    print(f"{subdomain} - status code :  Page not found!")
                elif response.status_code == 500:
                    print(f"{subdomain} - status code :  Internal server error!")
                else :
                    print("Unknown status code")
                
                print("*****************************")
                print("*****************************")
            
                
                
                
                printed_subdomains.add(subdomain)

        except:
            pass
        







# subdomains and their ips and open ports







printed_records = set()


common_ports = [21, 22, 23, 25, 53, 80, 110, 119, 123, 143, 161, 194, 443, 445, 993, 995]


for server in ns:
    server = str(server)
    for word in wordlist:
        try:
            answers = dns.resolver.query(word + "." + domain, "A")
            for ip in answers:
                subdomain = word + "." + domain
                ipaddress = socket.gethostbyname(subdomain)
                record = f"{subdomain} ---> IP address : {ipaddress}"
                if record not in printed_records:
                    printed_records.add(record)
                    print(record)
                    for port in common_ports:
                        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        sock.settimeout(1) 
                        result = sock.connect_ex((ipaddress, port))
                        if result == 0:
                             print("Port {} is open".format(port))
                        else:
                            print("Port {} is closed".format(port))
                            sock.close()

                   
        except:
            pass                                                                                              







# found emails and phone number 






printed_emails = set()

printed_phones = set()

cheked_subdomains = set()


for server in ns:
    server = str(server)
    for word in wordlist:
        try:
            answers = dns.resolver.query(word + "." + domain, "A")
            for ip in answers:
                subdomain = word + "." + domain
                if subdomain in cheked_subdomains:
                    continue
                cheked_subdomains.add(subdomain)

                url = f"http://{subdomain}"

                response = requests.get(url)
        
                html_content = response.text
                pattern_email = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
                pattern_phone = r"\b\d{3}[-.]?\d{3}[-.]?\d{4}\b"
                emails = re.findall(pattern_email, html_content)
                phones = re.findall(pattern_phone, html_content)
                for email in emails:
                    if email not in printed_emails:
                        printed_emails.add(email)
                        print(email)
                for phone in phones:
                    if phone not in printed_phones:
                        printed_phones.add(phone)
                        print(phone)
        except:
            pass                                                                                              







# whois look up to check domain information







w = whois.whois(domain)

print("Domain name:", w.domain_name)
print("Domain registrar:", w.registrar)
print("WHOIS server:", w.whois_server)
print("Domain creation date:", w.creation_date)
print("Domain expiration date:", w.expiration_date)
print("Domain last updated date:", w.updated_date)
print("Name servers:", w.name_servers)
print("Status:", w.status)
print("Registrant name:", w.name)
print("Registrant organization:", w.org)
print("Registrant email:", w.emails)
print("Registrant phone:", w.phones)
print("Registrant dnssec:", w.dnssec)
print("Registrant address:", w.address)
print("Registrant city:", w.city)
print("Registrant state:", w.state)
print("Registrant postal code:", w.registrant_postal_code)
print("Registrant country:", w.country)





# extract all urls on website






main_url = "https://www." + domain + "/"
 




response = requests.get(main_url)
soup = BeautifulSoup(response.content, "html.parser")
links = []
for link in soup.find_all("a"):
    href = link.get("href")
    if href is not None and href.startswith("https") and main_url in href:
         links.append(href)
         print(href)

for link in links:
     main_url = link
     response = requests.get(main_url)
     soup = BeautifulSoup(response.content, "html.parser")
     links2 = []
     for link in soup.find_all("a"):
        href = link.get("href")
        if href is not None and href.startswith("https") and main_url in href:
            links2.append(href)
            print(href)
            

