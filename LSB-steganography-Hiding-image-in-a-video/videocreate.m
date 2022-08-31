workingDir = 'E:\college\sem 6\DIP\Project';

vid=VideoReader('video.mp4');

video=VideoWriter(fullfile(workingDir,'originalvideo'));
video.FrameRate=vid.FrameRate;
open(video);

for i=1:1525
    imagename=[sprintf('%03d',i) '.png'];
    img=imread(fullfile(workingDir,'videoimages',imagename));
    writeVideo(video,img)
end