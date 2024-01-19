input_string = "service1_"
services = input_string.split('_')
services = [service for service in services if service]
print(services)

