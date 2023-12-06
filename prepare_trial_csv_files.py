import pandas as pd
import os


def load_dataframe(filepath):
    df = pd.read_csv(filepath)

    df.rename(columns={"type": "target", "label": "target"}, inplace=True)
    df["target"] = df["target"].map(
        lambda x: "malicious" if x != "benign" else "benign"
    )

    return df


def create_trial_df(original_df, generated_df, train_sizes):
    """Returns a train and test dataframe from the original and generated dataframes.
    The split is according to the train_sizes parameter.

    Args:
        original_df (pd.Dataframe): The original dataframe.
        generated_df (pd.Dataframe): The generated dataframe.
        train_sizes (tuple(int, int, int, int)): The number of samples to be used for training. (og_mal, og_ben, gen_mal, gen_ben)
    """
    # make copies of the original dataframes
    original_df = original_df.copy()
    generated_df = generated_df.copy()

    # split the original dataframes into malicious and benign urls
    original_malicious_urls = original_df[original_df["target"] == "malicious"]
    original_benign_urls = original_df[original_df["target"] == "benign"]

    generated_malicious_urls = generated_df[generated_df["target"] == "malicious"]
    generated_benign_urls = generated_df[generated_df["target"] == "benign"]

    # split the original accoriding to the train sizes
    train_original_malicious_urls = original_malicious_urls.sample(n=train_sizes[0])
    train_original_benign_urls = original_benign_urls.sample(n=train_sizes[1])

    # disable warnings
    pd.options.mode.chained_assignment = None

    # drops the rows that were sampled for training
    original_malicious_urls.drop(train_original_malicious_urls.index, inplace=True)
    original_benign_urls.drop(train_original_benign_urls.index, inplace=True)

    # enable warnings
    pd.options.mode.chained_assignment = "warn"

    # the remaining rows are used for testing
    test_original_malicious_urls = original_malicious_urls
    test_original_benign_urls = original_benign_urls

    train_df = pd.concat(
        [
            train_original_malicious_urls[["url", "target"]],
            train_original_benign_urls[["url", "target"]],
            generated_malicious_urls.sample(n=train_sizes[2])[["url", "target"]],
            generated_benign_urls.sample(n=train_sizes[3])[["url", "target"]],
        ]
    ).sample(frac=1)

    test_df = pd.concat(
        [
            test_original_malicious_urls[["url", "target"]],
            test_original_benign_urls[["url", "target"]],
        ]
    ).sample(frac=1)

    return train_df, test_df


# Original Dataset from Kaggle
original_df = load_dataframe("./datasets/malicious_phish.csv")

# Generated Dataset from RNN
generated_df = load_dataframe("./datasets/generated_urls_overnight.csv")

# Trial 1

trial1_train_df, trial1_test_df = create_trial_df(
    original_df, generated_df, (150000, 150000, 0, 0)
)
os.makedirs("./datasets/trial_1", exist_ok=True)
trial1_train_df.to_csv("./datasets/trial_1/train.csv", index=False)
trial1_test_df.to_csv("./datasets/trial_1/test.csv", index=False)

# Trial 2

trial2_train_df, trial2_test_df = create_trial_df(
    original_df, generated_df, (0, 0, 150000, 150000)
)
os.makedirs("./datasets/trial_2", exist_ok=True)
trial2_train_df.to_csv("./datasets/trial_2/train.csv", index=False)
trial2_test_df.to_csv("./datasets/trial_2/test.csv", index=False)

# Trial 3

trial3_train_df, trial3_test_df = create_trial_df(
    original_df, generated_df, (75000, 75000, 75000, 75000)
)
os.makedirs("./datasets/trial_3", exist_ok=True)
trial3_train_df.to_csv("./datasets/trial_3/train.csv", index=False)
trial3_test_df.to_csv("./datasets/trial_3/test.csv", index=False)

# Trial 4

trial4_train_df, trial4_test_df = create_trial_df(
    original_df, generated_df, (0, 150000, 150000, 0)
)
os.makedirs("./datasets/trial_4", exist_ok=True)
trial4_train_df.to_csv("./datasets/trial_4/train.csv", index=False)
trial4_test_df.to_csv("./datasets/trial_4/test.csv", index=False)

# Trial 5

trial5_train_df, trial5_test_df = create_trial_df(
    original_df, generated_df, (150000, 0, 0, 150000)
)
os.makedirs("./datasets/trial_5", exist_ok=True)
trial5_train_df.to_csv("./datasets/trial_5/train.csv", index=False)
trial5_test_df.to_csv("./datasets/trial_5/test.csv", index=False)
