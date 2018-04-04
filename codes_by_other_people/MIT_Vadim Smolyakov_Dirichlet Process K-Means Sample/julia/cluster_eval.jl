using Clustering 

@everywhere function compute_nmi(z1::Array{Int64,1}, z2::Array{Int64,1})

    n = length(z1)
    k1 = length(unique(z1))
    k2 = length(unique(z2))

    nk1 = zeros(k1,1)
    nk2 = zeros(k2,1)

    for (idx,val) in enumerate(unique(z1))
        cluster_idx = find(z1->z1 == val, z1)
        nk1[idx] = length(cluster_idx)
    end

    for (idx,val) in enumerate(unique(z2))
        cluster_idx = find(z2->z2 == val, z2)
        nk2[idx] = length(cluster_idx)
    end

    pk1 = nk1/float(sum(nk1))
    pk2 = nk2/float(sum(nk2))

    nk12 = zeros(k1,k2)
    for (idx1, val1) in enumerate(unique(z1))
        for (idx2, val2) in enumerate(unique(z2))
            cluster_idx1 = find(z1->z1 == val1, z1)
            cluster_idx2 = find(z2->z2 == val2, z2)
            common_idx12 = intersect(Set(cluster_idx1), Set(cluster_idx2))
            nk12[idx1,idx2] = length(common_idx12)
        end
    end
    pk12 = nk12/float(n) 
 
    Hx = -sum(pk1.*log(pk1+eps(Float64)))
    Hy = -sum(pk2.*log(pk2+eps(Float64)))
    Hxy = -sum(pk12.*log(pk12+eps(Float64)))

    MI = Hx + Hy - Hxy
    nmi = MI/float(0.5*(Hx+Hy))

    nmi
end

@everywhere function cluster_eval(z1::Array{Int64,1}, z2::Array{Int64,1})

    K1 = length(unique(z1))
    K2 = length(unique(z2))

    #normalized MI
    nmi = compute_nmi(z1,z2)
    println("nmi: ", nmi)

    #variation of information
    vi = varinfo(K1,z1,K2,z2)
    println("vi: ", vi)

    #adjusted rand index
    ari = randindex(z1,z2)
    println("ari: ", ari[1])

end

#z1 = [1,1,1,2,2,2]
#z2 = [1,1,2,2,3,3]
#cluster_eval(z1, z2)




