import numpy as np
import scipy
import matplotlib.pyplot as plt
from scipy.ndimage import imread

def pca(X):
  """  Principal Component Analysis
    input: X, matrix with training data stored as flattened arrays in rows
    return: projection matrix (with important dimensions first), variance
    and mean."""

  # get dimensions
  num_data,dim = X.shape

  # center data
  mean_X = X.mean(axis=0)
  X = X - mean_X

  if dim>num_data:
    # PCA - compact trick used
    M = np.dot(X,X.T) # covariance matrix
    e,EV = np.linalg.eigh(M) # eigenvalues and eigenvectors
    tmp = np.dot(X.T,EV).T # this is the compact trick
    V = tmp[::-1] # reverse since last eigenvectors are the ones we want
    S = np.sqrt(e)[::-1] # reverse since eigenvalues are in increasing order
    for i in range(V.shape[1]):
      V[:,i] /= S
  else:
    # PCA - SVD used
    U,S,V = np.linalg.svd(X)
    V = V[:num_data] # only makes sense to return the first num_data

  # return the projection matrix, the variance and the mean
  return V,S,mean_X


def svd(image, S=2, output_image=None, image_width=10):
    image_ = imread(image)
    A = np.double(image_)
    A_shape = map(lambda x: int(x), np.shape(A))
    X = A.reshape((A_shape[0] * A_shape[1], 3))
    #mean_X = X.mean(axis=0)
    #X = X - mean_X
    #calculate SVD
    #samples,features = np.shape(X)
    U, sigma, V = scipy.linalg.svd(X,full_matrices=False)
    #Sig = np.mat(np.eye(S)*s[:S])
    #tak out columns you don't need
    newdata = np.matrix(U[:, :S]) * np.diag(sigma[:S]) * np.matrix(V[:S, :])
    newdata = np.asarray(newdata.astype(int))
    X2 = newdata.reshape((A_shape[0], A_shape[1], 3))
    # this line is used to retrieve dataset 
    #~ new = U[:,:2]*Sig*V[:2,:]
    fig = plt.figure()
    image_height = image_width/((A_shape[1]+0.0)/(A_shape[0]+0.0))
    fig.set_size_inches(image_width,image_height)
    plt.imshow(X2)
    #plt.show()
    fig.savefig(output_image)
    del fig


def resize(image, output_image=None, image_width=10):
    A = imread(image)
    A_shape = map(lambda x: int(x), np.shape(A))
    fig = plt.figure()
    image_height = image_width/((A_shape[1]+0.0)/(A_shape[0]+0.0))
    fig.set_size_inches(image_width,image_height)
    plt.imshow(A)
    #plt.show()
    fig.savefig(output_image)
    del fig

########### Codes are Done ##############
#########################################

resize(image="testhouse.jpg", output_image="5 Nichols St_resize.jpg", image_width=10)

svd(image="testhouse.jpg",S=2, output_image="testhouse_svd.jpg",image_width=10)
        # S defines how many significant factors to consider in SVD
        # image_width is in inches
