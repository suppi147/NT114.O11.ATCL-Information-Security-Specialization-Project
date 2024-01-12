input_string = "service1_service2_serviceASS_serviceSFX_"
services = input_string.split('_')
services = [service for service in services if service]
print(services)

