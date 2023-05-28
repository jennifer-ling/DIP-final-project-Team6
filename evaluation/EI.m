function [ei] = EI(im)

    %Here im is the array for which Gradient is to be calculated
    im = double(im);
    [H W] = size(im);
    [Gg ~] = imgradient(im, 'sobel');
    ei = sum(sum(Gg))/(H*W);

end