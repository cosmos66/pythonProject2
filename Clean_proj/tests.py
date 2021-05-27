from configparser import ConfigParser
# config_object = ConfigParser()
# config_object["USERINFO"] = {
#     "admin": "Chankey Pathak",
#     "loginid": "chankeypathak",
#     "password": "tutswiki"
# }
# with open('config.ini', 'w') as conf:
#     config_object.write(conf)

config_object = ConfigParser()
config_object.read("config.ini")

#Get the password
userinfo = config_object["USERINFO"]
print("admin is {}".format(userinfo["admin"]))
print("Password is {}".format(userinfo["password"]))
config_object["USERINFO"]["password"]="new_bal"
with open('config.ini', 'w') as conf:
    config_object.write(conf)