import React, { useEffect, useState } from "react";
import { Info } from "./info";
import * as utils from "../utils";

export const Browse: React.FC<{
  info: utils.VideoInfo;
  setInfo: utils.InfoCallback;
  setCurrentTab: utils.TabCallback;
}> = ({ info, setInfo, setCurrentTab }) => {
  const [videos, setVideo] = useState<utils.Video[]>([]);

  useEffect(() => {
    utils.fetchData("/api/movies", setVideo);
    utils.fetchInfo(setInfo);
  }, [setInfo]);

  return (
    <div className="stuff">
      <MyList videos={videos} setInfo={setInfo} setCurrentTab={setCurrentTab} />
      <Info info={info} />
    </div>
  );
};

const MyListItem: React.FC<{
  video: utils.Video;
  setInfo: utils.InfoCallback;
  setCurrentTab: utils.TabCallback
}> = ({ video, setInfo, setCurrentTab }) => {
  return (
    <li
      key={video.name}
      onClick={async () => {
        await utils.addVideoData("video", video.path);
        await utils.fetchInfo(setInfo);
        setCurrentTab("2")
      }}
    >
      <img src={`data:image/jpeg;base64,${video.thumbnail}`} />
      <h3>{video.name}</h3>
      <p>Lorem {video.duration} ipsum dolor sit amet, consectetur adipiscing elit...</p>
    </li>
  );
};

const MyList: React.FC<{
  videos: utils.Video[];
  setInfo: utils.InfoCallback;
  setCurrentTab: utils.TabCallback;
}> = ({ videos, setInfo, setCurrentTab }) => {
  return (
    <nav>
      <ul>
        {videos.map((video) => (
          <MyListItem key={video.id} video={video} setInfo={setInfo} setCurrentTab={setCurrentTab} />
        ))}
      </ul>
    </nav>
  );
};
