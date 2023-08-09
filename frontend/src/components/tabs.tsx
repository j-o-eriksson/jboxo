import React, { useEffect, useState } from "react";
import * as utils from "../utils";
import { Info } from "./info";
import { Main } from "./main";

const Tabs = () => {
  const [currentTab, setCurrentTab] = useState("1");
  const [info, setInfo] = useState(utils.getDefaultInfo);

  const tabs = [
    {
      id: "1",
      tabTitle: "videos",
    },
    {
      id: "2",
      tabTitle: "play",
    },
    {
      id: "3",
      tabTitle: "info",
    },
  ];

  return (
    <div className="container">
      <div className="tabs">
        {tabs.map((tab, i) => (
          <button
            key={i}
            id={tab.id}
            disabled={currentTab === `${tab.id}`}
            onClick={() => {
              setCurrentTab(tab.id);
            }}
          >
            {tab.tabTitle}
          </button>
        ))}
      </div>
      <div className="content">
        <div key="1" className="stuff">
          {currentTab === "1" && <Main info={info} setInfo={setInfo} />}
        </div>
        <div key="2" className="stuff">
          {currentTab === "2" && (
            <div>
              <Info info={info} />
              <SubPicker setInfo={setInfo} />
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

const SubPicker: React.FC<{ setInfo: utils.InfoCallback }> = ({ setInfo }) => {
  const [subtitles, setSubtitles] = useState<utils.Video[]>([]);

  useEffect(() => {
    utils.fetchData("/subtitles", setSubtitles);
  }, []);

  return (
    <>
      <label>subtitles:</label>
      <select className="sub" name="selectedFruit">
        {subtitles.map((sub, i) => (
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
        ))}
      </select>
    </>
  );
};

export default Tabs;
