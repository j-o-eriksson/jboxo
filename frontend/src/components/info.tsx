import React from "react";
import { VideoInfo } from "../utils";

export const Info: React.FC<{ info: VideoInfo }> = ({ info }) => {
  return (
    <p className="info upper-bold">
      <b>name:</b> {info.name}
      <br />
      <b>subtitles:</b> {info.subtitles}
      <br />
      <b>duration:</b> {info.duration}
    </p>
  );
};
