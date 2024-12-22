import React, { useEffect, useState } from "react";
import { Info } from "./info";
import * as utils from "../utils";

export const Browse: React.FC<{
  info: utils.VideoInfo;
  setInfo: utils.InfoCallback;
}> = ({ info, setInfo }) => {
  const [videos, setVideo] = useState<utils.Video[]>([]);

  useEffect(() => {
    utils.fetchData("/api/videos", setVideo);
    utils.fetchInfo(setInfo);
  }, [setInfo]);

  return (
    <div className="stuff">
      <MyList videos={videos} setInfo={setInfo} />
      <Info info={info} />
    </div>
  );
};

const MyListItem: React.FC<{
  video: utils.Video;
  setInfo: utils.InfoCallback;
}> = ({ video, setInfo }) => {
  return (
    <li
      key={video.name}
      onClick={async () => {
        await utils.addVideoData("video", video.path);
        await utils.fetchInfo(setInfo);
      }}
    >
      <a className="col-a upper-bold">{video.name}</a>
    </li>
  );
};

const MyList: React.FC<{
  videos: utils.Video[];
  setInfo: utils.InfoCallback;
}> = ({ videos, setInfo }) => {
  return (
    <nav>
      <ul>
        {videos.map((video) => (
          <MyListItem key={video.name} video={video} setInfo={setInfo} />
        ))}
      </ul>
    </nav>
  );
};
