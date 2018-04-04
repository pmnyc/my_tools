function [dpm, obj, time] = dp_means(X, lambda)
%% Dirichlet Process K-means
%  X: n x d data matrix
%  lambda: cluster penalty parameter
%
% Reference:
% B. Kulis and M. Jordan, "Revisiting k-means: New Algorithms via Bayesian Nonparametrics"

rng('default');
options.display_plots = 1;

%% generate data
if (nargin < 1)

n=1e4;
d=2;
K=4;

[X,trueZ,mu0,V0] = gen_data(n,d,K);

if (options.display_plots)
    figure;   
    for k=1:K
        scatter(X(trueZ==k,1),X(trueZ==k,2)); hold on; grid on;
        plot2dgauss(mu0(:,k), V0(:,:,k)); hold on; 
    end
    title('ground truth'); xlabel('X1'); ylabel('X2');
end

end

%% DP-means parameters

K = 1;
K_init = 4;
[n,d] = size(X);

dpm.K = K;
dpm.d = d;
dpm.z = mod(randperm(n),K)+1;
dpm.mu = randn(K,d);
dpm.sigma = 1;
dpm.pik = 1/K*ones(K,1);
dpm.nk = zeros(K,1);

%% init cluster mean and lambda

dpm.mu = mean(X,1); 

if (nargin < 2)
    lambda = kpp_init(X,K_init);
end

%% DP-means algorithm

max_iter = 1e2;
obj = zeros(max_iter,1);
time = zeros(max_iter,1);

obj_tol = 1e-3;
Np = [1 2 3 max_iter]; cnt = 1;

fprintf('running dp-means...\n');
for iter = 1:max_iter
    tic;
    dist = zeros(n,dpm.K);
    
    %assignment step
    for kk = 1:dpm.K
        Xm = bsxfun(@minus,X,dpm.mu(kk,:));
        dist(:,kk) = dot(Xm,Xm,2);
    end

    %update labels
    [dmin,dpm.z] = min(dist,[],2);
    
    idx = find(dmin > lambda);
    if (~isempty(idx))
       dpm.K = dpm.K + 1;
       dpm.z(idx) = dpm.K;
       
       dpm.mu = [dpm.mu; mean(X(idx,:),1)];
       Xm = bsxfun(@minus,X,dpm.mu(dpm.K,:));
       dist = [dist, dot(Xm,Xm,2)];
    end
        
    %update step
    for kk = 1:dpm.K
        dpm.nk(kk) = sum(dpm.z == kk);
        dpm.mu(kk,:) = sum(X(dpm.z == kk,:),1)/dpm.nk(kk);
    end
    dpm.pik = dpm.nk/sum(dpm.nk);
    
    %compute objective
    for kk = 1:dpm.K
       obj(iter) = obj(iter) + sum(dist(dpm.z == kk,kk));
    end
    obj(iter) = obj(iter) + lambda*dpm.K;

    %check convergence
    if (iter > 1 && abs(obj(iter) - obj(iter-1)) < obj_tol*obj(iter))
        break;
    end
    
    %generate plots
    if (iter == Np(cnt) && options.display_plots)
        cnt = cnt+1;
        figure;
        for kk = 1:dpm.K
            scatter(X(dpm.z==kk,1),X(dpm.z==kk,2)); hold on; grid on;
        end
        xlabel('X1'); ylabel('X2'); title(['dp-means, iter: ',num2str(iter)]);
    end
    time(iter) = toc;
end

nmi = compute_nmi(trueZ, dpm.z); % in [0,1]
fprintf('NMI: %.4f\n', nmi);

%% generate plots

if (options.display_plots)

figure;
for kk = 1:dpm.K
    scatter(X(dpm.z==kk,1),X(dpm.z==kk,2)); hold on;
    %plot2dgauss(dpm.mu(kk,:), eye(d,d)); hold on;
end
xlabel('X1'); ylabel('X2'); title('dp-means clusters'); grid on;

figure;
plot(obj,'-b','linewidth',1.0); xlabel('iterations'); ylabel('sum of l2 squared distances');
title('DP-means objective');

figure;
plot(time,'-b','linewidth',1.0); xlabel('iterations'); ylabel('time per iter, sec');
title('DP-means time');

end


end

function [lambda] = kpp_init(X,k)
%k++ init
%lambda: max distance to k++ means

[n,d] = size(X);
mu = zeros(k,d);
dist = inf(n,1);

mu(1,:) = X(ceil(rand*n),:);
for i = 2:k
    D = bsxfun(@minus,X,mu(i-1,:));
    dist = min(dist,dot(D,D,2));    
    idx = find(rand < cumsum(dist/sum(dist)),1);
    mu(i,:) = X(idx,:);
    lambda = max(dist);
end

end

function [nmi] = compute_nmi(z1, z2)

n = length(z1);
k1 = length(unique(z1));
k2 = length(unique(z2));

nk1 = zeros(k1,1);
nk2 = zeros(k2,1);

for kk = 1:k1, nk1(kk) = sum(z1==kk); end
for kk = 1:k2, nk2(kk) = sum(z2==kk); end
pk1 = nk1/sum(nk1); pk2 = nk2/sum(nk2);

nk12 = zeros(k1,k2);
for ii = 1:k1
    for jj = 1:k2
        nk12(ii,jj) = sum((z1==ii).*(z2==jj));
    end
end
pk12 = bsxfun(@times, nk12, 1/n);

Hx = -sum(pk1.*log(pk1+eps));
Hy = -sum(pk2.*log(pk2+eps));
Hxy = -sum(dot(pk12,log(pk12+eps)));

MI = Hx + Hy - Hxy;
nmi = MI/((Hx+Hy)/2);

end


%% notes

%Lambda is chosen as farthest from k++ means distance

%Normalized MI between ground truth and posterior clusters
%is used to measure clustering performance
