function [P,f] = Forward(A, B, Pi, Obv)
    %Index of current state
    i = length(A);
    
    %Number of observations/time index
    t = length(Obv);
    
    %Initialization
    for j = 1:i
        alp(1,j) = Pi(j)*B(Obv(1),j);
    end
    
    %Induction
    for k = 1:t-1
        for m = 1:i
            for n = 1:i
               x(m,n) =  alp(k,n)*A(n,m);
            end
            induc(1,m) = sum(x(m,:))*B(Obv(k+1),m);
        end
        alp(k+1,:) = induc;
        
    end
    
    %Termination
    P = sum(alp(t,:));
    f = alp;
end