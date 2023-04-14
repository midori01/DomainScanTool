import socket
import select
import time
import os
import threading
import sys
import platform

max_thread = 1
timeout = 3
socket.setdefaulttimeout(timeout)
sleep_time = 1

def clear():
    sysy = platform.system()
    if sysy == "Windows":
        os.system('cls')
    elif sysy == "Linux":
        os.system('clear')
        
def get_top_level_domain_name_suffix():
    top_level_domain_name_suffix_list = list()
    with open('top_level_domain_name_suffix','r') as f:
        for line in f:
            if not line.startswith('//'):
                top_level_domain_name_suffix_list.append(line)
    return top_level_domain_name_suffix_list

def whois_query(domain_name, domain_name_server, domain_name_whois_server):
    retry = 3
    domain = domain_name + '.' + domain_name_server
    infomation = ''
    while(not infomation and retry > 0):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((domain_name_whois_server, 43))
            
            s.send(f'{domain} \r\n'.encode())
            
            while True:   
                res = s.recv(1024)  
                if not len(res):  
                    break    
                infomation += str(res)
            s.close()
            
            retry -= 1
            time.sleep(sleep_time)
        except:
            pass
    return infomation
    
def get_reginfomation(domain_name, domain_name_suffix_infomation):
    infomation = whois_query(domain_name, domain_name_suffix_infomation[0], domain_name_suffix_infomation[1])
    
    reg = domain_name_suffix_infomation[2]
    if not infomation:
        with open(f'failure.txt','a') as f:
            f.write(f'{domain_name}.{domain_name_suffix_infomation[0]} Error\n')
        print(f'{domain_name}.{domain_name_suffix_infomation[0]} Error')
        return
    if infomation.find(reg) >= 0:
        with open(f'success.txt','a') as f:
            f.write(f'{domain_name}.{domain_name_suffix_infomation[0]}\n')
        print(f'{domain_name}.{domain_name_suffix_infomation[0]} Available')
    else:
        print(f'{domain_name}.{domain_name_suffix_infomation[0]} Taken')

def specify_suffix_and_dictionary():
    domain_name_suffix = input("TLD:")
    domain_dictionary = input("Dic name:")
    domain_name_length = int(input("Number of characters:"))
    
    domain_name_list = []
    with open(domain_dictionary,'r') as f:
       for line in f:
            if line:
                if (len(line) < domain_name_length):
                    domain_name_list.append(line.strip())
   
    top_level_domain_name_suffix_list = get_top_level_domain_name_suffix()[1:]
    top_level_domain_name_suffix_array = [x.split('=')[0] for x in top_level_domain_name_suffix_list]

    if domain_name_suffix not in top_level_domain_name_suffix_array:
        print(f'{domain_name_suffix} is not in top_level_domain_name_suffix')
        
    top_level_domain_name_suffix_index = top_level_domain_name_suffix_array.index(domain_name_suffix)
    top_level_domain_name_par_list = [x.split('=')[:-1] for x in top_level_domain_name_suffix_list]
    
    for domain_name in domain_name_list:
        while threading.active_count() > max_thread:
            pass
        t = threading.Thread(target=get_reginfomation, args=(domain_name,top_level_domain_name_par_list[top_level_domain_name_suffix_index],))
        t.start()
        time.sleep(sleep_time)
    
def specify_the_domain_name():
    domain_name = input("Domain:")
    top_level_domain_name_suffix_list = get_top_level_domain_name_suffix()
    top_level_domain_name_suffix_array = [x.split('=')[:-1] for x in top_level_domain_name_suffix_list][1:]
    for domain_name_suffix in top_level_domain_name_suffix_array:
        while threading.active_count() > max_thread:
            pass
        t = threading.Thread(target=get_reginfomation, args=(domain_name,domain_name_suffix,))
        t.start()
        time.sleep(sleep_time)

def specify_a_dictionary():
    domain_dictionary = input("Dic name:")
    domain_name_length = int(input("Number of characters:"))
    
    domain_dictionary_list = []
    with open(domain_dictionary,'r') as f:
       for line in f:
            if line:
                if (len(line) < domain_name_length):
                    domain_dictionary_list.append(line.strip())

    top_level_domain_name_suffix_list = get_top_level_domain_name_suffix()
    top_level_domain_name_suffix_array = [x.split('=')[:-1] for x in top_level_domain_name_suffix_list][1:]

    for domain_name_suffix in top_level_domain_name_suffix_array:
        for domain_name in domain_dictionary_list:
            while threading.active_count() > max_thread:
                pass
            t = threading.Thread(target=get_reginfomation, args=(domain_name,domain_name_suffix,))
            t.start()
            time.sleep(sleep_time)    
    
def exit():
    print("Quit")

def welcome():
    clear()
    print(4 * '=' + 'Menu' + 4 * '='
            + '\n\n'
            + '1. Specify Domain + All TLD\n'
            + '2. Specify Dic + All TLD\n'
            + '3. Specify Dic + Specify TLD\n'
            
            + 'Exit:0' + '\n'
            + 'Input:' , end=""
        )
        
    select = input()
    return select

if __name__ == '__main__':
    select = welcome()
    if (select == "0"):
        clear()
        exit()
    elif (select == "1"):
        clear()
        specify_the_domain_name()
    elif (select == "2"):
        clear()
        specify_a_dictionary()
    elif select == "3":
        clear()
        specify_suffix_and_dictionary()   
    else:
        clear()
        print("\nInput error\n ")
        exit()
    
