import React, { useEffect, useState } from "react";
import { Info } from "./info";
import * as utils from "../utils";

type InfoCallback = React.Dispatch<React.SetStateAction<utils.VideoInfo>>;

export const Main: React.FC<{
  info: utils.VideoInfo;
  setInfo: InfoCallback;
}> = ({ info, setInfo }) => {
  const [videos, setVideo] = useState<utils.Video[]>([]);

  useEffect(() => {
    utils.fetchData(setVideo);
    utils.fetchInfo(setInfo);
  }, []);

  return (
    <div>
      <MyList videos={videos} setInfo={setInfo} />
      <Info info={info} />
    </div>
  );
};

type ListProps = {
  video: utils.Video;
  callback: React.Dispatch<React.SetStateAction<utils.VideoInfo>>;
};

const MyListItem: React.FC<ListProps> = ({ video, callback }) => {
  return (
    <li
      key={video.name}
      onClick={async () => {
        await utils.addVideoData(video.path);
        await utils.fetchInfo(callback);
      }}
    >
      <a>{video.name}</a>
    </li>
  );
};

const MyList: React.FC<{
  videos: utils.Video[];
  setInfo: InfoCallback;
}> = ({ videos, setInfo }) => {
  return (
    <nav>
      <ul>
        {videos.map((video) => (
          <MyListItem key={video.name} video={video} callback={setInfo} />
        ))}
      </ul>
    </nav>
  );
};
