//

const request = async (
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
  return request(
    async (response: Response) => {
      const { data } = await response.json();
      return data;
    },
    "/videos",
  );
};

const addVideo = async (path: string) => {
  return request(
    async (r: Response) => {
      return await r.text();
    },
    "/control/add",
    {
      method: "POST",
      body: JSON.stringify({ videoPath: path }),
    },
  );
};

const stopVideo = async () => {
  return request(
    async (r: Response) => {
      return await r.text();
    },
    "/control/stop",
    {
      method: "POST",
    },
  );
};

(async () => {
  let stuff = await fetchVideos();
  console.log(stuff);

  let list = document.getElementById("myList");
  for (let item of stuff) {
    let li = document.createElement("li");
    li.innerText = item["name"];
    li.setAttribute("path", item["path"]);
    list?.appendChild(li);
  }

  list?.addEventListener("click", (e) => {
    const item = e.target as HTMLElement;
    let path: string = item.getAttribute("path");
    console.log(
      `Clicked list element with name ${item.innerText} and content ${path}`,
    );

    (async () => {
      let response = await addVideo(path);
      console.log(response);
    })();
  });
})();
