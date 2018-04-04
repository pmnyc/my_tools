using Distributions
using PyPlot
using MAT 

srand(0) #seed

function generate_gaussian_data(N::Int64, D::Int64, K::Int64)
	x = randn(D,N)
	tpi = rand(Dirichlet(ones(K)))
	tzn = rand(Multinomial(N,tpi))  #number of points in each cluster, e.g. [2, 2, 6]
	tz = zeros(N)

	tmean = zeros(D,K)
	tcov = zeros(D,D,K)

	ind = 1
	println(tzn)
	for i=1:length(tzn)
		indices = ind:ind+tzn[i]-1
		tz[indices] = i
		tmean[:,i] = rand(MvNormal(zeros(D), 100*eye(D)))  #sample cluster mean
		tcov[:,:,i] = rand(InverseWishart(D+2, eye(D)))    #sample cluster covariance
		# T = chol(slice(tcov,:,:,i))
		# x[:,indices] = broadcast(+, T'*x[:,indices], tmean[:,i]);
		d = MvNormal(tmean[:,i], tcov[:,:,i])  #form cluster distribution
		for j=indices
			x[:,j] = rand(d)  #generate cluster point
		end
		ind += tzn[i]
	end
	x, tz, tmean, tcov
end

N = 1000 
D = 2 
K = 6 
latent, latent_z, latent_mu, latent_cov = generate_gaussian_data(N, D, K)

figure()
scatter(latent[1,:], latent[2,:], c=latent_z)

file = matopen("clusters.mat", "w")
write(file, "data", latent)
write(file, "labels", latent_z)
close(file)



