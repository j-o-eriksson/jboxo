import React, { useEffect, useState } from "react";
import { Info } from "./info";
import * as utils from "../utils";

export const Play: React.FC<{
  info: utils.VideoInfo;
  setInfo: utils.InfoCallback;
}> = ({ info, setInfo }) => {
  return (
    <div className="play-wrapper">
      <img className="myimg" src={`data:image/jpeg;base64,${info.thumbnail}`} />
      <SubPicker setInfo={setInfo} />
      <Info info={info} />
      <input
        className="seek"
        type="range"
        onChange={(e) => {
          console.log(e.target.value);
        }}
      />
      <Control />
    </div>
  );
};

const SubPicker: React.FC<{ setInfo: utils.InfoCallback }> = ({ setInfo }) => {
  const [subtitles, setSubtitles] = useState<utils.Subtitle[]>([]);

  useEffect(() => {
    utils.fetchData("/api/subtitles", setSubtitles);
  }, []);

  const subList = subtitles.map((sub, i) => (
    <option value={sub.path} key={i}>
      {sub.name}
    </option>
  ));

  return (
    <>
      <label className="play-label upper-bold col-b">subtitles:</label>
      <select
        className="play-select upper-bold col-b"
        onChange={async (e) => {
          await utils.addVideoData("subtitles", e.target.value);
          await utils.fetchInfo(setInfo);
        }}
      >
        {subList}
      </select>
    </>
  );
};

const Control = () => {
  const styles = "play-button upper-bold col-a";
  return (
    <div className="wrapper2">
      <button className={styles} id="one" onClick={utils.playVideo}>
        play
      </button>
      <button className={styles} id="two" onClick={utils.pauseVideo}>
        pause
      </button>
      <button className={styles} id="three" onClick={utils.stopVideo}>
        stop
      </button>
    </div>
  );
};
