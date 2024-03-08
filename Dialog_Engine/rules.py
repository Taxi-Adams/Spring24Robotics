def main():
    txt = open("TangoChat.txt", "r")
    line = txt.readline().strip()
    variables = dict()
    while line:
        # Rules

        # Skip comments
        if line[0] == "#":
            pass
        
        # Creates the dict of variables
        elif line[0] == "~":
            end_string = line.index(":")
            var_name = line[1:end_string]   # Gets the variable name
            variables[var_name] = []

            # Gets the list of variables
            first_bracket = line.index("[")
            last_bracket = line.index("]")
            var_list = line[first_bracket + 1: last_bracket]

            # Checks for quotes (multi-word sayings)
            try:
                while True:
                    # Finds whats enclosed in quotes
                    first_quote = var_list.index('"') + 1
                    second_quote = var_list[first_quote:].index('"')

                    # Adds the word to the dict
                    quoted_word = var_list[first_quote: first_quote+second_quote]
                    variables[var_name].append(quoted_word)
                    
                    # Removes the word from the list
                    var_list = (var_list[:first_quote - 1] + var_list[first_quote + second_quote + 1:])
            except:
                pass
            
            # Adds the rest of the variables
            variables[var_name].extend(i for i in var_list.split())
        
        else:
            print(line.strip())
        
        line = txt.readline().strip()

main()