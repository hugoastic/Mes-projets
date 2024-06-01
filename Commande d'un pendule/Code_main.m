m = 0.1;
M = 2;
L = 0.5;
g = 9.81;

%Obtention de A
A = [[0 0 1 0]
    [0 0 0 1]
    [0 (-m*g)/M 0 0]
    [0 (M+m)*g/(M*L) 0 0]]

%Obtention de B
B = transpose([0 0 1/M (-1)/(M*L)])


[nz, dz] = ss2tf(A, B, [1 0 0 0], 0);
H2 = tf(nz, dz)
[nTheta, dTheta] = ss2tf(A, B, [0 1 0 0], 0);
H1 = tf(nTheta, dTheta)

k2 = -1;
k1 = -1;
K=[0 k1 0 k2];
eig(A-B*K)

x0 = transpose([1 5*pi/180 0 0])
initial(A-B*K, zeros(4, 1), eye(4), zeros(4, 1), x0);

rank(ctrb(A, B))%Completement commandable si et seulement = 4
Cth = [0 1 0 0];%Le cas où on observe Theta
rank(obsv(A, Cth))
null(obsv(A, Cth))
Cksi = [1 0 0 0]%Le cas où on observe Ksii1
rank(obsv(A, Cksi))
null(obsv(A, Cksi))
figure(2);
sigma(A,B,Cth,0)
hold on
sigma(A,B,Cksi,0)
legend("Fonction de transfert avec Ctheta", "Fonction de transfert avec Cksi")
K = place(A, B, [-10, -11, -12, -13])
K=lqr(A,B,Cksi'*Cksi,10)
figure(4);
initial(A-B*K, zeros(4, 1), eye(4), zeros(4, 1), x0);
[Nkab, Dkab] = ss2tf(A, B, K, 0);
KAB = tf(Nkab, Dkab);
S = feedback(1, KAB);
figure(3);
sigma(KAB, S, {10^-3, 10^3});
legend("Transfert de boucle", "Fonction de sensibilité")

L = transpose(place(transpose(A), transpose(Cksi), transpose(10*[-11, -12, -13, -14])));
L=(lqr(A',Cksi',B*B',1))'
figure(5);
initial(A-L*Cksi, zeros(4, 1), eye(4), zeros(4, 1), x0);