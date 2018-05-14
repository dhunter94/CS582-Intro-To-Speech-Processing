function [score, path] = Viterbi(A,B,Pi,Obv)
    %Index of current state
    i = length(A);
    
    %Number of steps/time index
    t = length(Obv);
    
    %Initialization
    for j = 1:i
        delta(1,j) = Pi(1,j)*B(Obv(1),j);
        psi(1,j) = 0;
    end
    
    %Induction
    for k = 1:t-1
       for m = 1:i
           for n = 1:i
                  delta_max(1,n) = delta(1,n)*A(n,m);
                  psi_max(1,n) = delta(1,n)*A(n,m);
           end
           delta_temp(1,m) = max(delta_max)*B(Obv(k+1),m);
           
           %Needed for floating point comparison
           I = 0;
           RE = 1e-12;
           if abs(psi_max(1,1) - psi_max(1,2)) < RE*max(psi_max(1,1),psi_max(1,2))
               I = 1;
           end
           
           %if argmax has the same values take the first index
           if I == 1
               psi_temp(1,m) = I;
           else
               [M,I] = max(psi_max);
               psi_temp(1,m) = I;
           end
       end
       delta = delta_temp;
       psi(k,:) = psi_temp;
    end
    
    %Termination
    [M,I] = max(delta);
    track(1,t) = I;
    for j = t-1:-1:1
        track(1,j) = psi(j,track(1,j+1));
    end
    
    score = max(delta);
    path = track;
    
end