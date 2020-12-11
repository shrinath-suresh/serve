from argparse import ArgumentParser

import pytorch_lightning as pl
import torch
from pytorch_lightning import seed_everything
from sklearn.datasets import load_iris
from torch.utils.data import DataLoader, random_split, TensorDataset


class IrisDataModule(pl.LightningDataModule):
    def __init__(self, **kwargs):
        """
        Initialization of inherited lightning data module
        """
        super(IrisDataModule, self).__init__()

        self.train_set = None
        self.val_set = None
        self.test_set = None
        self.args = kwargs

    def prepare_data(self):
        """
        Implementation of abstract class
        """

    def setup(self, stage=None):
        """
        Downloads the data, parse it and split the data into train, test, validation data

        :param stage: Stage - training or testing
        """
        iris = load_iris()
        df = iris.data
        target = iris["target"]

        data = torch.Tensor(df).float()
        labels = torch.Tensor(target).long()
        RANDOM_SEED = 42
        seed_everything(RANDOM_SEED)

        data_set = TensorDataset(data, labels)
        self.train_set, self.val_set = random_split(data_set, [130, 20])
        self.train_set, self.test_set = random_split(self.train_set, [110, 20])

    @staticmethod
    def add_model_specific_args(parent_parser):
        """
        Adds model specific arguments batch size and num workers

        :param parent_parser: Application specific parser

        :return: Returns the augmented arugument parser
        """
        parser = ArgumentParser(parents=[parent_parser], add_help=False)
        parser.add_argument(
            "--batch-size",
            type=int,
            default=128,
            metavar="N",
            help="input batch size for training (default: 16)",
        )
        parser.add_argument(
            "--num-workers",
            type=int,
            default=3,
            metavar="N",
            help="number of workers (default: 3)",
        )
        return parser

    def create_data_loader(self, dataset):
        """
        Generic data loader function

        :param data_set: Input data set

        :return: Returns the constructed dataloader
        """

        return DataLoader(
            dataset, batch_size=self.args["batch_size"], num_workers=self.args["num_workers"]
        )

    def train_dataloader(self):
        train_loader = self.create_data_loader(dataset=self.train_set)
        return train_loader

    def val_dataloader(self):
        validation_loader = self.create_data_loader(dataset=self.val_set)
        return validation_loader

    def test_dataloader(self):
        test_loader = self.create_data_loader(dataset=self.test_set)
        return test_loader


if __name__ == "__main__":
    pass
