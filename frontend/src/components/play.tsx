import React, { useEffect, useState } from "react";
import * as utils from "../utils";
import { Info } from "./info";

export const Play: React.FC<{
  info: utils.VideoInfo;
  setInfo: utils.InfoCallback;
}> = ({ info, setInfo }) => {
  return (
    <div>
      <Info info={info} />
      <SubPicker setInfo={setInfo} />
    </div>
  );
};

const SubPicker: React.FC<{ setInfo: utils.InfoCallback }> = ({ setInfo }) => {
  const [subtitles, setSubtitles] = useState<utils.Video[]>([]);

  useEffect(() => {
    utils.fetchData("/subtitles", setSubtitles);
  }, []);

  const subList = subtitles.map((sub, i) => (
    <option
      value={sub.path}
      key={i}
      onClick={async () => {
        await utils.addVideoData("subtitles", sub.path);
        await utils.fetchInfo(setInfo);
      }}
    >
      {sub.name}
    </option>
  ));

  return (
    <>
      <label>subtitles:</label>
      <select className="sub" name="selectedFruit">
        {subList}
      </select>
    </>
  );
};
