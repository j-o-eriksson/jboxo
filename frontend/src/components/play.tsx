import React from "react";
import { VideoInfo } from "../utils";
import { Info } from "./info";

export const Play: React.FC<VideoInfo> = (info) => {
  return (
    <div>
      <Info info={info} />
    </div>
  );
};
