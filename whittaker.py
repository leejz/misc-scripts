
def dist_whittaker(datamtx, strict=True):
    """ returns whittaker distance (manhattan distance with sample normalization) btw rows
    
    dist(a,b) = 0.5*manhattan distance(ai/A, bi/B) where ai is each element of a, and A is the sum of all ai. 1 indicates complete similarity, 0 indicates complete dissimilarity.
    
    see for example:
    D9 p. 198 Legendre and Legendre 
    Developments in Environmental Modeling Vol. 3  1983
    
    this code added jzl 3/17/11

    * comparisons are between rows (samples)
    * input: 2D numpy array.  Limited support for non-2D arrays if 
    strict==False
    * output: numpy 2D array float ('d') type.  shape (inputrows, inputrows)
    for sane input data
    * two rows of all zeros returns 0 distance between them
    * if strict==True, raises ValueError if any of the input data is negative,
    not finite, or if the input data is not a rank 2 array (a matrix).
    * if strict==False, assumes input data is a matrix with nonnegative 
    entries.  If rank of input data is < 2, returns an empty 2d array (shape:
    (0, 0) ).  If 0 rows or 0 colunms, also returns an empty 2d array.
    """
    if strict:
        if not all(isfinite(datamtx)):
            raise ValueError("non finite number in input matrix")
        if any(datamtx<0.0):
            raise ValueError("negative value in input matrix")
        if rank(datamtx) != 2:
            raise ValueError("input matrix not 2D")
        numrows, numcols = shape(datamtx)
    else:
        try:
            numrows, numcols = shape(datamtx)
        except ValueError:
            return zeros((0,0),'d')

    if numrows == 0 or numcols == 0:
        return zeros((0,0),'d')

    dists = zeros((numrows,numrows),'d')
    for i in range(numrows):
        r1 = array(datamtx[i,:],'d')
        r1sum = sum(r1)
        for j in range(i):
            r2 = array(datamtx[j,:], 'd')
            r2sum = sum(r2)
            cur_d = 0.0
            if r1sum > 0 and r2sum > 0:
                cur_d = 0.5*float(sum(abs(r1/r1sum - r2/r2sum)))

            dists[i][j] = dists[j][i] = cur_d
    return dists
