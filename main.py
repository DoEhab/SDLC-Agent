from tools.filesystem import read_file, list_files

files = list_files(
    "/home/dohaadmin/Desktop/VScodeProj/payment-service"
)

for file in files:
    print(file)

content = read_file(
    "/home/dohaadmin/Desktop/VScodeProj/payment-service/"
    "src/main/java/com/example/payment_service/service/PaymentService.java"
)

print(content)