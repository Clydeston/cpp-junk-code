import requests
import glob
import os
import re
import html
import random
import string

# TODO
# add args for both unicode / multi byte
# classes 
# loops variation
# string types
# add modulo back to var types
# add junk loops for outside of function decs

junk_code_macro = "JUNKCODE"
junk_class_macro = "JUNKCLASS"
minimum_created_code_lines = 33
maximum_created_code_lines = 67
ignore_loops = False

def randomNumber(length):
    letters = string.digits
    return random.randint(1, length)

def randomString(length):
    letters = string.ascii_letters
    return ( ''.join(random.choice(letters) for i in range(length)))

def generateLoop():
    type_array = ["int", "float", "short", "long"]
    incrementor_name = randomString(random.randint(10, 40))
    var_type = type_array[random.randint(0, (len(type_array)-1))]
    var_value = generateValueForJunkCodeType(var_type)

    signs = [">", "<"]
    finished_loop = f'\nfor({var_type} {incrementor_name} = {var_value};{incrementor_name} {signs[random.randint(0,1)]} 0; {incrementor_name}++)\n{{\ncontinue;\n}}\n'

    return finished_loop

def junkCodeRequest():
    type_array = ["string", "bool", "int", "float", "long", "short", "DWORD", "char"]    
    lines_amount = random.randint(minimum_created_code_lines,maximum_created_code_lines)

    random_code = ""    
    for line_number in range(lines_amount):
        loop_bool = random.randint(0, 1)
        var_name = randomString(random.randint(10, 40))
        var_type = type_array[random.randint(0, (len(type_array)-1))]
        var_value = generateValueForJunkCodeType(var_type)
        
        if(var_value == None or var_name == None or var_type == None):
            continue

        completed_var = f'\n{var_type} {var_name} = {var_value};'

        random_code += completed_var

        if(loop_bool == 1 and ignore_loops == False):
            random_code += generateLoop()

    
    with open(f"./parsed/testcode.cpp", 'w') as newfile:
        newfile.write(random_code)
    return random_code

def junkClassRequest():
    url = "https://junkcode.gehaxelt.in/"
    request = requests.get(url)
    if(request.status_code == 200):
        text = html.unescape(request.text)


        text = re.sub("</pre></code>", "", text)
        text = re.sub("<code><pre>#include <stdio.h>", "", text)
        text = re.sub("#include <iostream>", "", text)
        text = re.sub("#include <string>", "", text)
        text = re.sub("<br><br><code><pre>", "", text)
        

        return text
    else:
        return ""

def generateValueForJunkCodeType(type):
    signs = ["+", "-", "/"] 
    selection = random.randint(0, 1)
    if(type == "bool"):
        options = ["true", "false"]
        return options[random.randint(0, 1)]
    elif(type == "int"):              
        if(selection == 1):
            return f'{randomNumber(random.randint(1, 21474864))}'
        else:
            return f"{randomNumber(random.randint(1, 21474864))} {signs[random.randint(0, 1)]} {randomNumber(random.randint(1, 21474864))}"
    elif(type == "long"):              
        if(selection == 1):
            return f'{randomNumber(random.randint(1, 21474864))}'
        else:
            return f"{randomNumber(random.randint(1, 21474864))} {signs[random.randint(0, 1)]} {randomNumber(random.randint(1, 21474864))}"        
    elif(type == "short"):              
        if(selection == 1):
            return f'{randomNumber(random.randint(1, 32767))}'            
        else:
            return f"{randomNumber(random.randint(1, 32767))} {signs[random.randint(0, 1)]} {randomNumber(random.randint(1, 32767))}"        
    elif(type == "DWORD"):
        if(selection == 1):
            return f'{randomNumber(random.randint(1, 21474864))}'            
        else:
            return f"{randomNumber(random.randint(1, 2147486))} {signs[random.randint(0, 1)]} {randomNumber(random.randint(1, 2147486))}" 
    elif(type == "char"):
        return f'(char)"{randomString(1)}"'
    elif(type == "float"):
        if(selection == 1):
            return random.random()
        else:
            return f"{random.random()} {signs[random.randint(0, 2)]} { random.random()}"         
    elif(type == "string"):    
        return f'"{randomString(random.randint(20, 50))}"'
    
def findMacroOccurences(text, macro_type):
        try:
            # finding #define index
            define_index = text.index(f'{macro_type}')
            print(define_index)
            
            # finding all occorunes of macros
            indices_object = re.finditer(pattern=macro_type, string=text)
            indices = [index.start() for index in indices_object]
            
            for indice in indices:
                if(indice == define_index):
                    indices.remove(indice)

            return indices
        except:
            return None

def parseFile(fileName):

    with open(f"./{fileName}", 'r') as file:
        text = file.read()
    
    # finding instances of macros
    print(f"Parsing file {fileName}")
    class_macro_locations = findMacroOccurences(text, junk_class_macro)

    if(class_macro_locations == None):
        print(f"No macros found for {fileName}")
        return

    new_string = text
    for macro_index in range(len(class_macro_locations)): 
        if(macro_index != 0):
            code_macro_locations = findMacroOccurences(new_string, junk_class_macro)

        new_string_to_insert = junkClassRequest()
        
        new_string = new_string[:class_macro_locations[macro_index]] + new_string_to_insert  + new_string[class_macro_locations[macro_index]:] 

    code_macro_locations = findMacroOccurences(new_string, junk_code_macro)

    for macro_index in range(len(code_macro_locations)): 
        if(macro_index != 0):
            code_macro_locations = findMacroOccurences(new_string, junk_code_macro)

        new_string_to_insert = junkCodeRequest()
        
        new_string = new_string[:code_macro_locations[macro_index]] + new_string_to_insert  + new_string[code_macro_locations[macro_index]:] 

    #now replace remove all macro occorunces
    print(f"Inserted code")
    
    new_string = re.sub(f"#define {junk_class_macro}", "", new_string)
    new_string = re.sub(f"#define {junk_code_macro}", "", new_string)

    new_string = re.sub(f"{junk_class_macro}", "", new_string)
    new_string = re.sub(f"{junk_code_macro}", "", new_string)

    print(f"Removed macros")

    directory = "./parsed"
    if not os.path.exists(directory):
        os.makedirs(directory)

    with open(f"{directory}/{fileName}", 'w') as newfile:
        newfile.write(new_string)

    print(f"{fileName} completed")
    #print(new_string)


print("Parsing files")
for file in os.listdir("./"):
    if file.endswith(".cpp"):
        parseFile(file)
        #print(junkCodeRequest())
print("File parsing finished")
