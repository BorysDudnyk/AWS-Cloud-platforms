#!/bin/bash

check_pip() {
    if command -v pip >/dev/null 2>&1; then
        echo "pip вже встановлено."
    else
        echo "pip не встановлено. Встановлюю pip…"
        curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
        python get-pip.py
        rm get-pip.py
    fi
}

clone_repo() {
    local repo_url=$1
    local clone_dir=$2
    echo "Клоную репозиторій $repo_url"
    git clone "$repo_url" "$clone_dir"
}

install_dependencies() {
    local clone_dir=$1
    echo "Встановлюю залежності..."
    if [ -f "$clone_dir/requirements.txt" ]; then
        pip install -r "$clone_dir/requirements.txt"
    else
        echo "Помилка: Файл вимог не знайдено у $clone_dir/requirements.txt"
    fi
}

main() {
    read -p "Введіть URL-репозиторія: " repo_url
    read -p "Введіть директорію для клонування: " clone_dir
    
    echo "Починаю виконання скрипту..."
    
    check_pip
    
    clone_repo "$repo_url" "$clone_dir"
    
    install_dependencies "$clone_dir"
    
    echo "Скрипт виконаний..."
}

main
