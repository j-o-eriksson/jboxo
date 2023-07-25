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

const fetchVideos = async () => {
  return makeRequest(async (response: Response) => {
    const { data } = await response.json();
    return data;
  }, "/videos");
};

const fetchSubtitles = async () => {
  return makeRequest(async (response: Response) => {
    const { data } = await response.json();
    return data;
  }, "/subtitles");
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
    `/control/${cmd}`,
    {
      method: "POST",
    },
  );
};

const playVideo = async () => {
  return postBase("play");
};

const pauseVideo = async () => {
  return postBase("pause");
};

const stopVideo = async () => {
  return postBase("stop");
};

const populateList = (list: HTMLElement, items: any) => {
  for (let item of items) {
    let li = document.createElement("li");

    let a = document.createElement("a");
    a.innerText = item["name"];
    li.appendChild(a);

    li.setAttribute("path", item["path"]);
    list?.appendChild(li);
  }
};

const openForm = async () => {
  // document.getElementById("myForm").style.display = "block";
  let stuff = await fetchSubtitles();
  console.log(stuff);

  let list = document.getElementById("subList");
  populateList(list, stuff);

  list?.addEventListener("click", (e) => {
    const item = e.target as HTMLElement;
    let path: string = item.getAttribute("path");
    console.log(path);

    (async () => {
      let response = await addVideoData("subtitles", path);
      console.log(response);
    })();

    // list.innerHTML = "";
    // closeForm();
  });
};

// function closeForm() {
//   document.getElementById("myForm").style.display = "none";
// }

(async () => {
  let stuff = await fetchVideos();
  console.log(stuff);

  let list = document.getElementById("myList");
  populateList(list, stuff);

  list?.addEventListener("click", (e) => {
    const item = e.target as HTMLElement;
    let path: string = item.getAttribute("path");

    (async () => {
      let response = await addVideoData("video", path);
      console.log(response);
    })();
  });

  openForm();
})();
