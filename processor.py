from toolBox import *


class Processor:

    def __init__(self, target):
        self.data = pd.read_excel(PATH)
        self.target = target

    def pre_processing(self):
        """
        The function pre process the data, get the data from the input file, remove bad samples and
        prepare the data according to chosen lipids and proteins types.
        :return:
        """
        # ignore experiments 6
        for bad_sample in bad_samples:
            self.data = self.data[self.data.ExpNum != bad_sample]
        self.data = self.data[self.data[LIPID] != 0.0]

    def get_data(self):
        return self.data

    def relations_target(self, for_hue, target, relation_sub):

        # Compute the correlation matrix
        corr = self.data.corr()
        # print(corr[target])
        print(stats.pearsonr(self.data[target], self.data[relation_sub]))

        # # Generate a mask for the upper triangle
        # mask = np.triu(np.ones_like(corr, dtype=bool))
        #
        # # Set up the matplotlib figure
        # f, ax = plt.subplots(figsize=(11, 9))
        #
        # # Generate a custom diverging colormap
        # cmap = sns.diverging_palette(230, 20, as_cmap=True)
        #
        # # Draw the heatmap with the mask and correct aspect ratio
        # sns.heatmap(corr, mask=mask, cmap=cmap, vmax=.3, center=0,
        #             square=True, linewidths=.5, cbar_kws={"shrink": .5})
        # plt.show()

        g = sns.pairplot(self.data, hue=for_hue, palette="muted", size=5,
                         vars=[target, relation_sub], kind='reg')

        # remove the top and right line in graph
        sns.despine()
        # Additional line to adjust some appearance issue
        plt.subplots_adjust(top=0.9)

        plt.show()

    def detect_outliers(self):
        import warnings

        sns.boxplot(x=self.data[self.target])
        plt.show()

        highest = self.data[self.target].mean() + 3 * self.data[self.target].std()
        lowest = self.data[self.target].mean() - 3 * self.data[self.target].std()
        self.data = self.data[(self.data[self.target] < highest) & (self.data[self.target] > lowest)]


        sns.boxplot(x=self.data[self.target])
        plt.show()



