# search_files_and_add_corresponding_statements program 
'''
Difference from normal script: In SPs, the DROP statement should be added before the 'SET NOCOUNT OFF' statement
'''

import os
import pathlib
import re

# Use forward slashes in path (windows default in backslash)
# base_path = "C:/ZZ_mine/my_projects/temp_files/testing_search_files_add_corresponding_statements"   # for testing
base_path = "C:/ZZ_mine/Work/TestingScripts/HITT/04.StoredProcedures/OD"

comment_before_drop_statements = "--Dropping all created temp tables\n"
list_ignore_chars_after_these_special_chars = ['(', ')', ';', '"', '\'', ',', '.', '-', ']', '[' ]

def main():
    for path, subdirs, files in os.walk(base_path):
        for name in files:
            # print(pathlib.PurePath(path, name))
            file_path = pathlib.PurePath(path, name) 

            # print(file_path)

            set_of_temp_tables = set()     # Using set to avoid duplicates
            set_of_tables_lower_cased = set()
            new_contents=""
            is_stored_procedure = 0
            is_file_to_be_modified = 1 # file is marked true for modification

            with open(file_path, mode="r+") as file:
                for line in file:
                    # print(line)
                    if line.lstrip() == comment_before_drop_statements:  #ie; program has already been run on this file before
                        is_file_to_be_modified = 0
                        break;

                    for word in line.split():
                        # print(word)
                        modified_word = strip_chars_after_special_chars(word)
                        modified_word_lower_cased = modified_word.lower()
                        if word.startswith('#') and modified_word != '#' and modified_word_lower_cased != '#icr' and modified_word.strip('#').isnumeric() == False:
                            if modified_word_lower_cased not in set_of_tables_lower_cased:
                                set_of_temp_tables.add(modified_word)
                                set_of_tables_lower_cased.add(modified_word_lower_cased)
                    
                    # checking if file is stored procedure
                    if re.match(r"^createprocedure.*", lowercase_and_remove_spaces_and_strip(line)):
                        is_stored_procedure = 1

                    # adding DROP table statements before "SET NOCOUNT OFF" statement. Else using the line itself
                    if re.match(r"^set.*", line.strip().lower()): #performing an easier comparison before doing an expensive comparison for performance reasons 
                        if re.match(r"^setnocountoff;?$", lowercase_and_remove_spaces_and_strip(line)):         # regex for line starting with "setnocountoff" and can or cannot have 1 occurrence of semicolon and line ends after this statement
                            no_of_leading_spaces = len(line) - len(line.lstrip(' '))
                            no_of_leading_tabs = len(line) - len(line.lstrip('\t'))
                            leading_space_string = " " * no_of_leading_spaces + "\t" * no_of_leading_tabs
                            
                            if len(set_of_temp_tables) > 0:
                                new_contents = new_contents + write_drop_statements('', set_of_temp_tables, leading_space_string, comment_before_drop_statements)
                            new_contents = new_contents + (f"{leading_space_string}SET NOCOUNT OFF\n")
                        else:
                            new_contents = new_contents + (line)
                    else:
                        new_contents = new_contents + (line)

                if is_file_to_be_modified == 0:  # Avoids files that have already been editted in the past
                    continue; # skips this file
                else:
                    if is_stored_procedure == 1:
                        file.seek(0) # go to beginning of file                
                        file.writelines(new_contents)   #write the contents of `new_contents` to the file (removes the previous file content)
            
            # outside the context of opening of the file
            if is_file_to_be_modified == 1 and is_stored_procedure == 0:
                new_contents='' #setting it as empty
                with open(file_path, mode="a") as file: # append mode
                    if len(set_of_temp_tables) > 0:
                        file.write(write_drop_statements(new_contents, set_of_temp_tables, '', comment_before_drop_statements))

def strip_chars_after_special_chars(a_string):
    for char in list_ignore_chars_after_these_special_chars:
        a_string = a_string.split(char,1)[0]        # splits a_string at first occurence of `char` into 2 parts (inferred from '1' cuz index starts at 0) and return the first part (inferred from '0')
    return a_string

def lowercase_and_remove_spaces_and_strip(a_string):
    return a_string.strip().replace(' ','').replace('\n','').lower()

def write_drop_statements(new_contents, set_of_temp_tables, leading_space_string, comment_before_drop_statements):
    new_contents = new_contents + (f"\n\n{leading_space_string}{comment_before_drop_statements}")
    for temp_table in sorted(set_of_temp_tables,key=len):
        new_contents = new_contents + (f"{leading_space_string}DROP TABLE IF EXISTS {temp_table};\n")
    new_contents = new_contents + (f"\n\n")
    return new_contents

if __name__ == "__main__":	
    main()