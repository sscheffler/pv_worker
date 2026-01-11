#!/bin/bash

auto_yes=false
if [[ "$1" == "-y" ]]; then
    auto_yes=true
fi

commands=(
    "uv run ruff check --fix"
    "uv run pytest"
    "uv run ruff format"
    "uv run mypy"
)

for cmd in "${commands[@]}"; do
    echo "Command: '$cmd'"
    if [[ "$auto_yes" == true ]]; then
        echo "Executing command automatically (due to -y parameter)..."
        eval "$cmd"
        echo "Command completed."
    else
        read -n 1 -p "Do you want to execute this command? (Press ENTER to execute, n to skip): " choice
        echo
        if [[ -z "$choice" ]]; then
            eval "$cmd"
            echo "Command completed."
        elif [[ "$choice" =~ ^[Nn]$ ]]; then
            echo "Command skipped."
        else
            echo "Invalid input. Command skipped."
        fi
    fi
    echo
done
echo "All commands processed."
