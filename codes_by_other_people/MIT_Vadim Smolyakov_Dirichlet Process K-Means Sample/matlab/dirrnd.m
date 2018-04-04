function pi = dirrnd(aa);
% pi = dirrnd(aa)
% draws a sample from a dirichlet with parameter vector aa

pi = randg(aa); %gamma rnd number with scale=1 and shape aa(i)
pi = pi./repmat(sum(pi),size(pi,1),1); %normalized to obtain samples of dirichlet distrib
