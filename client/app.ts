//

const fetchVideos = async (): Promise<string> => {
  const api = "/videos";
  try {
    const response = await fetch(api, { mode: "cors" });
    const { data } = await response.json();
    return data;
  } catch (error) {
    if (error) {
      return error.message;
    }
  }
};

const addVideo = async (path: string): Promise<string> => {
  const api = "/control/add";
  try {
    const response = await fetch(api, {
      method: "POST",
      mode: "cors",
      body: JSON.stringify({ videoPath: path }),
    });
    const text = await response.text();
    return text;
  } catch (error) {
    if (error) {
      return error.message;
    }
  }
};

const stopVideo = async (): Promise<string> => {
  const api = "/control/stop";
  try {
    const response = await fetch(api, {
      method: "POST",
      mode: "cors",
    });
    const text = await response.text();
    console.log(`stop video returned ${text}`);
    return text;
  } catch (error) {
    if (error) {
      return error.message;
    }
  }
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
