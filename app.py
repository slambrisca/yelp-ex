import csv
import json
import os
import random
import sys
import tarfile
from datetime import datetime, timedelta


def main():
    check_arguments()
    tarfile_path = get_filepath()

    dir = os.path.dirname(tarfile_path)

    with tarfile.open(tarfile_path) as tar:
        user_ids = set()
        with tar.extractfile("user.json") as file:
            with open(f"{dir}/user.csv", "w") as user_file:
                sample_file_to_csv(file, user_file, 1, user_ids)

        with tar.extractfile("review.json") as file:
            with open(f"{dir}/review.csv", "w") as review_file:
                filter_reviews_by_user_id(file, review_file, user_ids)

        with open("review.csv") as sample_review_file:
            with open(f"{dir}/noreviewers.csv", "w") as recent_reviewers_file:
                ayearago = datetime.now() - timedelta(days=365)
                filter_users_with_recent_reviews(sample_review_file, recent_reviewers_file, ayearago, user_ids)


def filter_reviews_by_user_id(input_file, output_file, user_ids):
    csv_writer = csv.writer(output_file)
    count = 0
    total = 0

    for line in input_file:
        json_row = json.loads(line)
        if json_row["user_id"] in user_ids:
            if count == 0:
                csv_writer.writerow(json_row.keys())

            csv_writer.writerow(json_row.values())
            count += 1
        total += 1

    print(f"{count} rows written from a total of {total}. Keeping: %{round(count / total * 100, 2)} of data.")


def filter_users_with_recent_reviews(input_file, output_file, since, user_ids):
    csv_reader = csv.DictReader(input_file)
    csv_writer = csv.writer(output_file)
    count = 0

    for row in csv_reader:
        if datetime.strptime(row["date"], "%Y-%m-%d %H:%M:%S") >= since:
            user_id = row["user_id"]
            if user_id in user_ids:
                user_ids.remove(user_id)

    for user_id in user_ids:
        if count == 0:
            csv_writer.writerow(["user_id"])
        csv_writer.writerow([user_id])
        count += 1


def sample_file_to_csv(input_file, output_file, percent, ids_set):
    csv_writer = csv.writer(output_file)
    count = 0
    total = 0
    for line in input_file:
        if should_write(percent=percent):
            json_row = json.loads(line)
            ids_set.add(json_row["user_id"])
            if count == 0:
                csv_writer.writerow(json_row.keys())

            csv_writer.writerow(json_row.values())
            count += 1
        total += 1
    print(f"{count} rows written from a total of {total}. Keeping: %{round(count / total * 100, 2)} of data.")


def should_write(percent):
    rn = random.randint(0, 99)
    return rn < percent


def check_arguments():
    if len(sys.argv) < 2:
        print("ERROR: Expected tarfile path as argument")
        exit(1)


def get_filepath():
    return sys.argv[1]


if __name__ == "__main__":
    main()
