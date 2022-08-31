key='1024';
a=key(1)-'0';
b=key(2)-'0';
c=key(3)-'0';
d=key(4)-'0';

imgtobehidden=imread('image.jpg');
sizeofimage=size(imgtobehidden);
imagenomat=[];

workingDir = 'E:\college\sem 6\DIP\Project';
mkdir(workingDir);
mkdir(workingDir,'videoimagesafterhiding');

for iter1=1:8
    imageno=a*(iter1^3)+b*(iter1^2)+c*(iter1)+d;
    imagenomat=[imagenomat imageno];
    imagename=[sprintf('%03d',imageno) '.png'];
    image=imread(imagename);
    for iter2=1:(sizeofimage(1)*sizeofimage(2)*sizeofimage(3))
        if rem(image(iter2),2)==1
            image(iter2)=image(iter2)-1;
        end
    end
    image=image+rem(imgtobehidden,2);
    imgtobehidden=double(imgtobehidden);
    imgtobehidden=floor(imgtobehidden/2);
    imgtobehidden=uint8(imgtobehidden);
    fullname=fullfile(workingDir,'videoimagesafterhiding',imagename);
    imwrite(image,fullname);
end

for iter3=1:1525
    if(any(imagenomat(:)==iter3))
        continue
    end
    imagename=[sprintf('%03d',iter3) '.png'];
    image=imread(imagename);
    fullname=fullfile(workingDir,'videoimagesafterhiding',imagename);
    imwrite(image,fullname);
end
