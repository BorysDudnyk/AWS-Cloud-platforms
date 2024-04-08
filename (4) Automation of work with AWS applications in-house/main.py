import key_pair
import instance
import bucket

def main_menu():
    print("1. Створення пари ключів")
    print("2. Створення інстансу")
    print("3. Запуск інстансу")
    print("4. Зупинити інстанс")
    print("5. Видалити інстанс")
    print("6. Створити бакет")
    print("7. Видалити бакет")
    print("8. Вихід")

def main():
    while True:
        main_menu()
        choice = input("Виберіть опцію: ")

        if choice == '1':
            key_pair.create_key_pair()
        elif choice == '2':
            instance.create_instance()
        elif choice == '3':
            instance.start_instance()
        elif choice == '4':
            instance.stop_instance()
        elif choice == '5':
            instance.delete_instance()
        elif choice == '6':
            bucket.create_bucket()
        elif choice == '7':
            bucket.delete_bucket()
        elif choice == '8':
            break
        else:
            print("Недійсний вибір. Спробуйте ще раз.")

if __name__ == "__main__":
    main()
