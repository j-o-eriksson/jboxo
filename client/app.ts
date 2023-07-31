// index.js

const makeRequest = async (
  callback: (r: Response) => any,
  endpoint: string,
  init?: RequestInit,
) => {
  try {
    const response = await fetch(endpoint, init);
    return callback(response);
  } catch (error) {
    return error.message;
  }
};

const fetchData = async (path: string) => {
  return makeRequest(async (response: Response) => {
    const { data } = await response.json();
    return data;
  }, path);
};

const fetchVideos = async () => {
  return fetchData("/videos")
};

const fetchSubtitles = async () => {
  return fetchData("/subtitles")
};

const fetchInfo = async () => {
  return fetchData("/selected")
};

const addVideoData = async (type: string, path: string) => {
  return makeRequest(
    async (r: Response) => {
      return await r.text();
    },
    "/control/add",
    {
      method: "POST",
      body: JSON.stringify({ type: type, path: path }),
    },
  );
};

const postBase = async (cmd: string) => {
  return makeRequest(
    async (r: Response) => {
      let text = await r.text();
      console.log(text);
      return text;
    },
    cmd,
    {
      method: "POST",
    },
  );
};

const playVideo = async () => {
  return postBase("control/play");
};

const pauseVideo = async () => {
  return postBase("control/pause");
};

const stopVideo = async () => {
  return postBase("control/stop");
};

const wakeScreen = async () => {
  return postBase("control/wake");
};

const populateList = (list: HTMLElement, items: any) => {
  for (let item of items) {
    let a = document.createElement("a");
    a.innerText = item["name"];
    a.setAttribute("path", item["path"]);

    let li = document.createElement("li");
    li.appendChild(a);

    list?.appendChild(li);
  }
};

const updateInfo = async () => {
  let info = await fetchInfo();
  console.log(info);

  let p1 = document.getElementById("videoInfo");
  p1.innerHTML =
    `<b>video:</b><br> ${info["name"]}<br>` +
    `<b>subtitles:</b><br> ${info["subtitle_name"]}<br>` +
    `<b>duration:</b> ${info["video_duration_str"]}`;
};

const setupList = async (
  fetchFunction: () => Promise<any>,
  listId: string,
  typeStr: string,
) => {
  let stuff = await fetchFunction();
  console.log(stuff);

  let list = document.getElementById(listId);
  populateList(list, stuff);

  list?.addEventListener("click", (e) => {
    const item = e.target as HTMLElement;
    let path: string = item.getAttribute("path");

    (async () => {
      let response = await addVideoData(typeStr, path);
      console.log(response);
      await updateInfo();
    })();
  });
};

(async () => {
  setupList(fetchVideos, "myList", "video");
  setupList(fetchSubtitles, "subList", "subtitles");
})();
