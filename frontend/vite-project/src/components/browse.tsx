import { useEffect, useState } from "react";
import * as utils from "../utils";

export const Browse: React.FC<{
  setInfo: utils.InfoCallback;
  setCurrentTab: utils.TabCallback;
}> = ({ setInfo, setCurrentTab }) => {
  return (
    <div className="stuff">
      <MyList setInfo={setInfo} setCurrentTab={setCurrentTab} />
    </div>
  );
};

const MyList: React.FC<{
  setInfo: utils.InfoCallback;
  setCurrentTab: utils.TabCallback;
}> = ({ setInfo, setCurrentTab }) => {
  const [videos, setVideo] = useState<utils.Video[]>([]);
  useEffect(() => {
    utils.fetchData("/api/movies", setVideo);
  }, []);

  return (
    <>
      <select
        className="play-select upper-bold col-b"
        onChange={async (e) => {
          utils.fetchData(`/api/${e.target.value}`, setVideo);
        }}
      >
        <option value={"movies"}>{"movies"}</option>
        <option value={"series"}>{"series"}</option>
      </select>
      <nav>
        <ul>
          {videos.map((video) => (
            <MyListItem
              key={video.id}
              video={video}
              setInfo={setInfo}
              setCurrentTab={setCurrentTab}
            />
          ))}
        </ul>
      </nav>
    </>
  );
};

const MyListItem: React.FC<{
  video: utils.Video;
  setInfo: utils.InfoCallback;
  setCurrentTab: utils.TabCallback;
}> = ({ video, setInfo, setCurrentTab }) => {
  return (
    <li
      key={video.name}
      onClick={async () => {
        await utils.addVideoData("video", video.id);
        await utils.fetchInfo(setInfo);
        setCurrentTab("2");
      }}
    >
      <img src={`data:image/jpeg;base64,${video.thumbnail}`} />
      <h3>{video.name}</h3>
      <p>
        Lorem {video.duration} ipsum dolor sit amet, consectetur adipiscing
        elit...
      </p>
    </li>
  );
};
