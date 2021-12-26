import yaml

with open("/etc/version-bump/config.yaml", "r") as config:
    try:
        config_file = yaml.safe_load(config)
    except yaml.YAMLError as exc:
        print(exc)

with open("/etc/version-bump/template.yaml", "r") as template:
    try:
        template_file = yaml.safe_load(template)
    except yaml.YAMLError as exc:
        print(exc)


def get_config(my_config):
    try:
        return config_file[my_config]
    except:
        return str("None")


def get_version_setting(programming_language):
    try:
        return template_file[programming_language]
    except:
        return False
