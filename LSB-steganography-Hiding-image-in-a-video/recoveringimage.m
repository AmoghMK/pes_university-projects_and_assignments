key='1024';
a=key(1)-'0';
b=key(2)-'0';
c=key(3)-'0';
d=key(4)-'0';

sampleimg=imread('007.png');
sizeofimg=size(sampleimg);

recoveredimg=uint8(zeros(sizeofimg));

for iter1=1:8
    imageno=a*(iter1^3)+b*(iter1^2)+c*(iter1)+d;
    imagename=[sprintf('%03d',imageno) '.png'];
    image=imread(imagename);
    recoveredimg=recoveredimg+(2^(iter1-1))*rem(image,2);
end

imshow(recoveredimg);
imwrite(recoveredimg,'recovered image.png');

