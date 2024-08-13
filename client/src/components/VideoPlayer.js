import React from "react";

const VideoPlayer = ({ currentVideo, videoPlaying, videoRef }) => {
  return (
    <div className="video-container">
      {(currentVideo || videoPlaying) && (
        <div>
          <video ref={videoRef} key={currentVideo || videoPlaying}>
            <source src={currentVideo || videoPlaying} type="video/mp4" />
          </video>
        </div>
      )}
    </div>
  );
};

export default VideoPlayer;
