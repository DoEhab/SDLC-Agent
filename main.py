from tools.filesystem import read_file, list_files, list_repo_files, read_repo_file

content = read_repo_file(
    "https://github.com/DoEhab/pay_service",
    "src/main/java/com/example/payment_service/service/PaymentService.java"
)

print(content)