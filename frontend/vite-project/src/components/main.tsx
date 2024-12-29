import { useState } from "react";
import { Play } from "./play";
import { Browse } from "./browse";
import * as utils from "../utils";

const Main = () => {
  const [currentTab, setCurrentTab] = useState("1");
  const [info, setInfo] = useState(utils.getDefaultInfo);

  const tabs = [
    {
      id: "1",
      title: "browse",
      content: <Browse setInfo={setInfo} setCurrentTab={setCurrentTab} />,
    },
    {
      id: "2",
      title: "play",
      content: <Play info={info} setInfo={setInfo} />,
    },
    {
      id: "3",
      title: "info",
      content: <p>Not implemented</p>,
    },
  ];

  return (
    <div className="container">
      <div className="tabs">
        {tabs.map((tab, i) => (
          <button className="col-b upper-bold"
            key={i}
            id={tab.id}
            disabled={currentTab === `${tab.id}`}
            onClick={() => {
              setCurrentTab(tab.id);
            }}
          >
            {tab.title}
          </button>
        ))}
      </div>
      <div>
        {tabs.map((tab) => (
          <div key={tab.id}>
            {currentTab === tab.id && tab.content}
          </div>
        ))}
      </div>
    </div>
  );
};

export default Main;
