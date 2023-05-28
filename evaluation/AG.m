function [ag] = AG(im)

    %Here im is the array for which Gradient is to be calculated
    im = double(im);
    [H W] = size(im);
    [dx dy] = gradient(im);
    ag = sum(sum(sqrt(dx.^2+dy.^2)))/(H*W);

end