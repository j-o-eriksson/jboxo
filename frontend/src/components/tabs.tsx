import { useState } from "react";
import { getDefaultInfo } from "../utils";
import { Info } from "./info";
import { Main } from "./main";

const Tabs = () => {
  const [currentTab, setCurrentTab] = useState("1");
  const [info, setInfo] = useState(getDefaultInfo);

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
          {currentTab === "2" && <Info info={info} />}
        </div>
      </div>
    </div>
  );
};

export default Tabs;
