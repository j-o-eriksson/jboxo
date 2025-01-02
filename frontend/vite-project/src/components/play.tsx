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
      <Control info={info} />
    </div>
  );
};

const SubPicker: React.FC<{ setInfo: utils.InfoCallback }> = ({ setInfo }) => {
  const [subtitles, setSubtitles] = useState<utils.Subtitle[]>([]);

  useEffect(() => {
    utils.fetchData("/api/subtitles", setSubtitles);
  }, []);

  const subList = subtitles.map((sub, i) => (
    <option value={sub.id} key={i}>
      {sub.name}
    </option>
  ));

  return (
    <>
      <label className="play-label upper-bold col-b">subtitles:</label>
      <select
        className="play-select upper-bold col-b"
        onChange={async (e) => {
          await utils.addVideoData("subtitles", parseInt(e.target.value));
          await utils.fetchInfo(setInfo);
        }}
      >
        {subList}
      </select>
    </>
  );
};

const Control: React.FC<{ info: utils.VideoInfo }> = ({ info }) => {
  const styles = "play-button upper-bold col-a";
  const [seekTime, setSeekTime] = useState(0);

  const durationString = (t: number) => {
    return new Date(t * 1000).toISOString().slice(11, 19);
  }

  return (
    <>
      <div className="progress">
        <p className="upper-bold">{durationString(seekTime / 100 * info.duration)}</p>
        <input
          type="range"
          onChange={(e) => {
            setSeekTime(parseInt(e.target.value))
          }}
        />
        <p className="upper-bold">{durationString(info.duration)}</p>
      </div>
      <div className="wrapper2">
        <button className={styles} id="one" onClick={async () => { utils.playVideo(seekTime) }}>
          play
        </button>
        <button className={styles} id="two" onClick={utils.pauseVideo}>
          pause
        </button>
        <button className={styles} id="three" onClick={utils.stopVideo}>
          stop
        </button>
      </div>
    </>
  );
};
