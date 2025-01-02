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
  const [elapsed, setElapsed] = useState(0);

  const fullTime = new Date(info.duration * 1000).toISOString().slice(12, 19);
  const durationString = (t: number) => {
    const currentTime = new Date(t * 1000).toISOString().slice(12, 19);
    return `${currentTime} / ${fullTime}`
  }

  useEffect(() => {
    const id = setInterval(() => {
      utils.fetchElapsed(setElapsed)
    }, 5000)

    return () => {
      clearInterval(id)
    }
  }, [elapsed]);

  return (
    <>
      <div className="progress">
        <input
          type="range"
          value={elapsed}
          onChange={(e) => {
            setElapsed(parseInt(e.target.value))
          }}
        />
        <p className="upper-bold">{durationString(elapsed * info.duration / 100)}</p>
      </div>
      <div className="wrapper2">
        <button className={styles} id="one" onClick={async () => { utils.playVideo(elapsed) }}>
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
