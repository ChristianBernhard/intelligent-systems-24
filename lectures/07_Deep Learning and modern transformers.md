### Rule based vs. ML
![img_55.png](img_55.png)

ML: get a computer to learn patterns

3 things you need: Data, Model, Cost

ML examples: classification, regression, clustering

The Bias-Variance balance in the model capacity:
High Variance: Overfitting
High Bias: Underfitting

Name 5 hyperparameters in NN:
- batchsize, epochs, neurons in hidden layer, hidden layers, loss function

Regularization – addressing overfitting:
one option: lower the weights
A weight represent the importance of the importance of the previous neuron (input,
hidden layer, etc)
Overfitting means exaggerating the importance of a data point (e.g.: the model follows
too much the inputs)
The intuitive solution is to lower the weights to lower the importance of the data point

- Dropout

Batch Normalization:
Normalization: collapsing inputs between 0 and 1

## Batch noramlization => more calculations. Does it make the whole training slower?
- Each epoch takes longer, but the convergence is faster
- It achieves the same accuracy faster

## Why do we have activation functions?
- Otherwise the network can‘t learn complex models (just linear transformations)

## What is the idea of auto encoders?
- We encode the input data X into a smaller space and we try to decode it back (aka reconstruct the input data X as X‘)

## CNN: Why fully connected layers don‘t work well for images?
- 100px by 100px => 10000 inputs and 10000 outputs even if we consider just one channel (not RGB) 100 m neuron connections
- Each pixel contributes equally (relative position is irrelevant) => it doesn‘t make sense (pixels closer to each other
make up features like an edge, and eye, etc

Convolutional layers make more sense:
- Each output for a pixel is determined by a grid of surrounding input pixels
- The output pixel is computed by multiplying the surrounding input pixels by the Kernel and then adding everything up


## Computer vision levels:
- image classification: The network just labels what it is in the image
- Image Classification and location: The network just labels what it is in the image and
adds a bounding box (we still assume only 1)
- object detection: The network just labels mutliple objects of the  same or different classes and adds the bounding  boxes for every one
- Semantic segmentation: The network assigns a label to each pixel in the
image (in the example to just one object). So it doesnt draw a box but the exact shape of the object e.g. cat.
- Instance segmentation: The network can identify multiple instances of the  same object

## Why is attention important?
- Position matters for the input (!) The man stops the car. The car stops the man.
- 
