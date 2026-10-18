import argparse

from app.db import SessionLocal, create_tables
from app.services.importer import clean_catalog, read_catalog, save_catalog


def main():
    parser = argparse.ArgumentParser(description="Импорт каталога ароматов из CSV")
    parser.add_argument("path", help="путь к CSV-файлу Fragrantica")
    parser.add_argument("--min-votes", type=int, default=1000,
                        help="минимальное число голосов на Fragrantica (по умолчанию 1000)")
    args = parser.parse_args()

    create_tables()
    df, stats = clean_catalog(read_catalog(args.path), args.min_votes)

    with SessionLocal() as db:
        stats.update(save_catalog(db, df))

    print("Статистика импорта:")
    for name, value in stats.items():
        print(f"  {name}: {value}")


if __name__ == "__main__":
    main()
