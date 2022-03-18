from requests import get, post, delete

print(get("http://localhost:8080/api/v2/users").json())
print(get("http://localhost:8080/api/v2/users/2").json())
print(get("http://localhost:8080/api/v2/users/169").json())  # Нет такого

print(post("http://localhost:8080/api/v2/users").json())  # Нет такого в словаре
print(post("http://localhost:8080/api/v2/users", json={"name": "Миша"}).json())  # Не все поля
print(post("http://localhost:8080/api/v2/users", json={"name": "Миша", "surname": "Пупкин", 'age': 12,
                                                       'position': "captain", 'speciality': "research engineer",
                                                       'address': "module_1", 'email': "scot_chief@mars.org",
                                                       'hashed_password': "lfkfdknlfkl",
                                                       'modified_date': "2022-02-26 15:12:03.417262"}).json())
print(delete("http://localhost:8080/api/v2/users/89322").json())  # Нет такого
print(delete("http://localhost:8080/api/v2/users/2").json())
