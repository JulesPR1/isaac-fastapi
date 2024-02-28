if [ ! -d "app/db/json" ]; then
    mkdir -p app/db/json
    echo "Created app/db/json folder"
fi

if [ ! -d "app/storage/characters" ]; then
    mkdir -p app/storage/characters
    echo "Created app/storage/characters folder"
fi

if [ ! -d "app/storage/items" ]; then
    mkdir -p app/storage/items
    echo "Created app/storage/items folder"
fi
