import numpy as np
from deepautoencoder import BasicAutoEncoder

allowed_activations = ['sigmoid', 'tanh', 'softmax']
allowed_noises = [None, 'gaussian', 'mask']
allowed_losses = ['rmse', 'cross-entropy']


class StackedAutoEncoder:
    """A deep autoencoder"""

    def assertions(self):
        global allowed_activations, allowed_noises, allowed_losses
        assert self.loss in allowed_losses, 'Incorrect loss given'
        assert 'list' in str(type(self.dims)), 'dims must be a list even if there is one layer.'
        assert len(self.activations) == len(self.dims), "No. of activations must equal to no. of hidden layers"
        assert self.epoch > 0, "No. of epoch must be atleast 1"
        assert set(self.activations + allowed_activations) == set(allowed_activations), "Incorrect activation given."
        assert self.noise in allowed_noises, "Incorrect noise given"

    def __init__(self, dims, activations, epoch=1000, noise=None, loss='rmse',lr=0.001):
        self.lr = lr
        self.ae = None
        self.loss = loss
        self.activations = activations
        self.noise = noise
        self.epoch = epoch
        self.dims = dims
        self.assertions()
        self.depth = len(dims)

    def add_noise(self, x):
        if self.noise == 'gaussian':
            n = np.random.normal(0, 0.1, (len(x), len(x[0])))
            return x + n
        if 'mask' in self.noise:
            frac = float(self.noise.split('-')[1])
            temp = np.copy(x)
            for i in temp:
                n = np.random.choice(len(i), round(frac * len(i)), replace=False)
                i[n] = 0
            return temp
        if self.noise == 'sp':
            pass

    def fit(self, x):
        for i in range(self.depth):
            if self.noise is None:
                self.ae = BasicAutoEncoder(data_x=x, activation=self.activations[i], data_x_=x,
                                           hidden_dim=self.dims[i], epoch=self.epoch, loss=self.loss,
                                           batch_size=int(0.3 * len(x)), lr=self.lr)
            else:
                self.ae = BasicAutoEncoder(data_x=self.add_noise(x), activation=self.activations[i], data_x_=x,
                                           hidden_dim=self.dims[i],
                                           epoch=self.epoch, loss=self.loss, batch_size=int(0.3 * len(x)), lr=self.lr)
            self.ae.run()
            self.x = self.ae.get_hidden_feature()

    def transform(self, x):
        return self.ae.transform(x)

    def fit_transform(self, x):
        self.fit(x)
        return self.transform(x)
