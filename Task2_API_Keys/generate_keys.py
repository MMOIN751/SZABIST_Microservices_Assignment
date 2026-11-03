import secrets

print("Create these three keys for three separate testers.")
print("Copy them into the API_KEYS environment variable; do not commit them.")
for number in range(1, 4):
    print(f"TESTER_{number}_KEY={secrets.token_urlsafe(32)}")
