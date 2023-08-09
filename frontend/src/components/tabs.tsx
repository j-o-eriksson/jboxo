import { useState } from "react";
import * as utils from "../utils";
import { Main } from "./main";
import { Play } from "./play";

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

  const tab1 = <Main info={info} setInfo={setInfo} />;
  const tab2 = <Play info={info} setInfo={setInfo} />;

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
          {currentTab === "1" && tab1}
        </div>
        <div key="2" className="stuff">
          {currentTab === "2" && tab2}
        </div>
      </div>
    </div>
  );
};

export default Tabs;
