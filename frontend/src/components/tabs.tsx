import { useState } from "react";
import Main from "./main";

const Tabs = () => {
  const [currentTab, setCurrentTab] = useState("1");
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
        <div key="1">{currentTab === "1" && <Main />}</div>
        <div key="2">
          {currentTab === "2" && (
            <div>
              <p className="title">Hello 2</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default Tabs;
