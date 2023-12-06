import csv
import os
import random

TOTAL_GENERATED_URLS = 575_738
TOTAL_ORIGINAL_URLS = 651_191
TOTAL_URLS = TOTAL_GENERATED_URLS + TOTAL_ORIGINAL_URLS


def split_dataset(original_urls: list, generated_urls: list) -> (list, list):
    # Make a copy
    original_urls = original_urls.copy()
    generated_urls = generated_urls.copy()
    # Shuffle the datasets
    random.shuffle(original_urls)
    random.shuffle(generated_urls)

    # Split the datasets, 80% for training and 20% for testing
    # Training dataset should have both non-generated and generated urls
    # Testing dataset should have only non-generated urls
    training_ds_list = []
    test_ds_list = []

    # Add the original urls to the training dataset
    for _ in range(int(len(original_urls)*0.8)):
        training_ds_list.append(original_urls.pop())

    # Add the generated urls to the training dataset
    for _ in range(int(len(generated_urls)*0.8)):
        training_ds_list.append(generated_urls.pop())

    # Add the original urls to the testing dataset
    for _ in range(len(original_urls)):
        test_ds_list.append(original_urls.pop())

    return training_ds_list, test_ds_list


def combine_datasets(original_urls: list, generated_urls: list):
    training_ds_list, test_ds_list = split_dataset(
        original_urls, generated_urls)

    # Create Directories if they don't exist
    if not os.path.exists("./datasets/combined"):
        os.makedirs("./datasets/combined")

    # Create two csv files, one for training and one for testing
    with open("./datasets/combined/training_dataset.csv", "w", encoding='UTF-8') as training_ds:
        training_writer = csv.writer(training_ds)
        training_writer.writerow(["url", "label"])

        for row in training_ds_list:
            training_writer.writerow([row["url"], row["label"]])

    with open("./datasets/combined/testing_dataset.csv", "w", encoding='UTF-8') as testing_ds:
        testing_writer = csv.writer(testing_ds)
        testing_writer.writerow(["url", "label"])

        for row in test_ds_list:
            testing_writer.writerow([row["url"], row["label"]])


def combine_datasets_malicious(original_urls, generated_urls):
    training_ds_list, test_ds_list = split_dataset(
        original_urls, generated_urls)

    # Create directories if they don't exist
    if not os.path.exists("./datasets/malicious"):
        os.makedirs("./datasets/malicious")

    # Remove all benign urls from the training dataset
    training_ds_list = [
        row for row in training_ds_list if row["label"] == "malware"]

    # Create two csv files, one for training and one for testing
    with open("./datasets/malicious/testing_dataset.csv", "w", encoding='UTF-8') as malicious_ds:
        malicious_writer = csv.writer(malicious_ds)
        malicious_writer.writerow(["url", "label"])

        for row in test_ds_list:
            malicious_writer.writerow([row["url"], row["label"]])

    with open("./datasets/malicious/training_dataset.csv", "w", encoding='UTF-8') as malicious_ds:
        malicious_writer = csv.writer(malicious_ds)
        malicious_writer.writerow(["url", "label"])

        for row in training_ds_list:
            malicious_writer.writerow([row["url"], row["label"]])


def combine_datasets_benign(original_urls, generated_urls):
    training_ds_list, test_ds_list = split_dataset(
        original_urls, generated_urls)

    # Create directories if they don't exist
    if not os.path.exists("./datasets/benign"):
        os.makedirs("./datasets/benign")

    # Remove all malicious urls from the training dataset
    training_ds_list = [
        row for row in training_ds_list if row["label"] == "benign"]

    # Create two csv files, one for training and one for testing
    with open("./datasets/benign/testing_dataset.csv", "w", encoding='UTF-8') as benign_ds:
        benign_writer = csv.writer(benign_ds)
        benign_writer.writerow(["url", "label"])

        for row in test_ds_list:
            benign_writer.writerow([row["url"], row["label"]])

    with open("./datasets/benign/training_dataset.csv", "w", encoding='UTF-8') as benign_ds:
        benign_writer = csv.writer(benign_ds)
        benign_writer.writerow(["url", "label"])

        for row in training_ds_list:
            benign_writer.writerow([row["url"], row["label"]])


def main():
    print("Reading the datasets...", end="")
    original_ds = open("./datasets/malicious_phish.csv", "r", encoding="utf8")
    generated_ds = open("./datasets/generated_urls.csv", "r", encoding="utf8")

    # Read the original dataset
    original_reader = csv.reader(original_ds)
    original_urls = []
    for row in original_reader:
        label = row[1]
        if label != "benign":
            label = "malware"
        original_urls.append({"url": row[0], "label": label})

    # Read the generated dataset
    generated_reader = csv.reader(generated_ds)
    generated_urls = []
    for row in generated_reader:
        generated_urls.append({"url": row[0].strip(), "label": row[1].strip()})
    print("Done")
    # Combine the datasets
    print("Combining the datasets...", end="")
    combine_datasets(original_urls, generated_urls)
    print("Done")
    # Add all generated malicious urls to the original dataset
    print("Adding generated malicious urls to the original dataset...", end="")
    combine_datasets_malicious(original_urls, generated_urls)
    print("Done")
    # Add all benign urls to the original dataset
    print("Adding benign urls to the original dataset...", end="")
    combine_datasets_benign(original_urls, generated_urls)
    print("Done")
    # Close the files
    original_ds.close()
    generated_ds.close()


if __name__ == "__main__":
    main()
