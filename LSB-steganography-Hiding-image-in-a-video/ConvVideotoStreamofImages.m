workingDir = 'E:\college\sem 6\DIP\Project';
mkdir(workingDir,'videoimages2');

vid=VideoReader('originalvideo.avi');
i=1;
while hasFrame(vid)
    img=readFrame(vid);
    filename=[sprintf('%03d',i) '.png'];
    fullname=fullfile(workingDir,'videoimages',filename);
    imwrite(img,fullname);
    i=i+1;
end

