"""
The class create instance that read the data, detect and remove outliers and ignore experiments
that disqualified according to previous decisions.
"""
from toolBox import *


class Processor:

    def __init__(self, target):
        self.data = pd.read_excel(PATH)
        self.target = target

    def pre_processing(self):
        """
        The function pre process the data, get the data from the input file, remove bad samples and
        prepare the data according to chosen lipids and proteins types.
        """
        # ignore experiment that disqualified - appears in the bad_samples table in toolBox
        for bad_sample in bad_samples:
            self.data = self.data[self.data.ExpNum != bad_sample]
        self.data = self.data[self.data[LIPID] != 0.0]

    def get_data(self):
        return self.data

    def relations_target(self, for_hue, target, relation_sub):
        """
        the function calculates the correlation between the target and the other parameter.
        """
        # Compute the correlation matrix
        corr = self.data.corr()
        # print(corr[target])
        print(stats.pearsonr(self.data[target], self.data[relation_sub]))

        g = sns.pairplot(self.data, hue=for_hue, palette="muted", size=5,
                         vars=[target, relation_sub], kind='reg')

        # remove the top and right line in graph
        sns.despine()
        # Additional line to adjust some appearance issue
        plt.subplots_adjust(top=0.9)

        plt.show()

    def detect_outliers(self):
        """
        The function detect and update the data without outliers that are chose according to
        samples that are far from the mean more then 3 standard deviations. the function plot the
        data before and after outliers removal.
        """
        sns.boxplot(x=self.data[self.target])
        plt.show()

        highest = self.data[self.target].mean() + 3 * self.data[self.target].std()
        lowest = self.data[self.target].mean() - 3 * self.data[self.target].std()
        self.data = self.data[(self.data[self.target] < highest) &
                              (self.data[self.target] > lowest)]
        sns.boxplot(x=self.data[self.target])
        plt.show()
