using Distributions
using PyPlot
using RDatasets
using MAT

include("./cluster_eval.jl")

srand(0) #seed

@everywhere function kpp_init(X::Array{Float64,2}, K::Int64)

    n, d = size(X)
    mu = zeros(K,d)
    dist = Inf * ones(n)
    Lambda = 1

    idx = round(Int64, rand(Uniform(1,n)))
    mu[1,:] = X[idx,:]
    for i = 2:K
        D = X - repmat(mu[i-1,:]',n,1)
        dist = min(dist, sum(D.*D,2))
        idx_cond = rand(Uniform(0,1)) .< cumsum(dist/sum(dist))
        idx_mu = find(idx_cond)[1]
        mu[i,:] = X[idx_mu,:]
        Lambda = maximum(dist)
    end
    Lambda
end

@everywhere function dpmeans_fit(X::Array{Float64, 2})

    #init params
    K = 1
    K_init = 9
    d = size(X,2)
    z = mod(randperm(size(X,1)),K)+1
    mu = rand(MvNormal(zeros(d), 10*eye(d)))
    sigma = 1
    nk = zeros(K)
    pik = ones(K)/K

    mu = mean(X,1)
    Lambda = kpp_init(X, K_init)
    println("lambda: ", Lambda)

    max_iter = 100
    obj = zeros(max_iter)
    em_time = zeros(max_iter)

    obj_tol = 1e-3
    n, d = size(X)

    for iter = 1:max_iter
        dist = zeros(n,K)

        #assignment step
        for kk = 1:K
            Xm = X - repmat(mu[kk,:]',n,1)
            dist[:,kk] = sum(Xm.*Xm,2)
        end

        #update labels
        dmin = minimum(dist,2)
        z = mapslices(indmin, dist, 2)
        #find(dist->dist==0, dist)
        idx = find(dmin->dmin > Lambda, dmin)
        if (size(idx)[1] > 0)
            K = K + 1
            z[idx] = K
            mu = cat(1, mu, mean(X[idx,:],1))
            Xm = X - repmat(mu[K,:]',n,1)
            dist = cat(2, dist, sum(Xm.*Xm,2))
        end

        #update step
        nk = zeros(K)
        for kk = 1:K
            nk[kk] = counts(z, kk)[1]
            idx2 = find(z->z==kk, z)
            if (length(idx2)>0)
                mu[kk,:] = mean(X[idx2,:],1)
            end
        end
        pik = nk / sum(nk)

        #compute objective
        for kk = 1:K
            idx = find(z->z==kk, z)
            obj[iter] = obj[iter] + sum(dist[idx,kk])
        end
        obj[iter] = obj[iter] + Lambda * K

        #check convergence
        if (iter > 1 && abs(obj[iter] - obj[iter-1]) < obj_tol * obj[iter])
            println("converged in ", iter, " iterations.")
            break
        end
        em_time[iter] = 0

    end

    z, obj, em_time
end

#generate data (X is NxD)
load_data = "synthetic"  #"synthetic", "iris", "wine", "soybean", "pima", "car"

if load_data == "synthetic"
    println("synthetic dataset")
    file = matread("./data/clusters.mat")
    X = transpose(file["data"])
    z_true = round(Int64, file["labels"])
elseif load_data == "iris"
    println("iris dataset")
    iris = dataset("datasets","iris")
    X = convert(Array, iris[:,1:4])
    species = convert(Array, iris[:,5])
    z_true = zeros(length(species))
    cnt = 1
    for sp in unique(species)
        idx = find(species->species == sp, species)
        z_true[idx] = cnt
        cnt = cnt + 1
    end
    z_true = round(Int64, z_true)
elseif load_data == "wine"
    println("wine dataset")
    file = matread("./data/wine.mat")
    X = 1.0 .* file["wine"]
    z_true = round(Int64, file["label"])
    z_true = squeeze(z_true, 2)
elseif load_data == "soybean"
    println("soybean dataset")
    file = matread("./data/soybean.mat")
    X = file["data"]
    z_true = round(Int64, file["label"])
    z_true = squeeze(z_true, 2)
elseif load_data == "pima"
    println("pima dataset")
    file = matread("./data/pima.mat")
    X = file["data"]
    z_true = round(Int64, file["label"])
    z_true = squeeze(z_true, 2)
elseif load_data == "car"
    println("car dataset")
    file = matread("./data/car.mat")
    X = file["data"]
    z_true = round(Int64, file["label"])
    z_true = squeeze(z_true, 2)
else
    println("choose a dataset")
    quit()
end

#DP means
tic()
labels, obj, em_time = dpmeans_fit(X)
ftime = toc()

#evaluate clustering
labels_ord = zeros(length(labels)) 
cnt = 1 
for kk in unique(labels)
    cidx = find(labels->labels == kk, labels)
    labels_ord[cidx] = cnt  
    cnt = cnt + 1
end
labels_ord = round(Int64, labels_ord)
println("K true: ", length(unique(z_true)))
println("K dpmeans: ", length(unique(labels_ord)))
cluster_eval(labels_ord, z_true)

#generate plots
figure()
scatter(X[:,1], X[:,2], c=z_true)
title("ground truth clustering")

figure()
scatter(X[:,1], X[:,2], c=labels_ord)
title("dp-means clustering")


