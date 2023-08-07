import React, { useEffect, useState } from "react";
import { addVideoData, fetchInfo } from "../utils";

type Video = {
  name: string;
  path: string;
};

type VideoInfo = {
  name: string;
  subtitles: string;
  duration: string;
};

export default function Main() {
  const [videos, setVideo] = useState<Video[]>([]);

  const fetchData = async () => {
    const response = await fetch("/videos");
    const { data } = await response.json();
    setVideo(data);
  };

  useEffect(() => {
    fetchData();
  }, []);

  return <MyList videos={videos} />;
}

type ListProps = {
  video: Video;
  callback: React.Dispatch<React.SetStateAction<VideoInfo>>;
};

const MyListItem: React.FC<ListProps> = ({ video, callback }) => {
  return (
    <li
      key={video.name}
      onClick={async () => {
        await addVideoData(video.path);
        await fetchInfo(callback);
      }}
    >
      <a>{video.name}</a>
    </li>
  );
};

const MyList: React.FC<{ videos: Video[] }> = ({ videos }) => {
  const [info, setInfo] = useState<VideoInfo>({
    name: "-",
    subtitles: "-",
    duration: "-",
  });

  return (
    <div className="stuff">
      <nav>
        <ul>
          {videos.map((video) => (
            <MyListItem key={video.name} video={video} callback={setInfo} />
          ))}
        </ul>
      </nav>
      <Info info={info} />
    </div>
  );
};

const Info: React.FC<{ info: VideoInfo }> = ({ info }) => {
  return (
    <p>
      <b>name:</b> {info.name}
      <br />
      <b>subtitles:</b> {info.subtitles}
      <br />
      <b>duration</b>: {info.duration}
    </p>
  );
};
