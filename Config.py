import configparser

# CREATE OBJECT
config_file = configparser.ConfigParser()

# ADD SECTION
config_file.add_section("Version&Branch")
# ADD SETTINGS TO SECTION
config_file.set("Version&Branch", "OB版本", "release")
config_file.set("Version&Branch", "OB+1版本", "dev")
config_file.set("Version&Branch", "OB热更1", "master")

# SAVE CONFIG FILE
with open(r"configurations.ini", 'w') as configfileObj:
    config_file.write(configfileObj)
    configfileObj.flush()
    configfileObj.close()

print("Config file 'configurations.ini' created")

# PRINT FILE CONTENT
read_file = open("configurations.ini", "r")
content = read_file.read()
print("Content of the config file are:\n")
print(content)
read_file.flush()
read_file.close()