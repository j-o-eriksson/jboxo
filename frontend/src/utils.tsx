// api.tsx

export const addVideoData = async (path: string) => {
  const response = await fetch("/control/add", {
    method: "POST",
    body: JSON.stringify({ type: "video", path: path }),
  });
  const text = await response.text();
  console.log(`Add returned: ${text}`);
};

export const fetchInfo = async (callback: any) => {
  const response = await fetch("/selected");
  const { data } = await response.json();
  callback({
    name: data.name,
    subtitles: data.subtitles,
    duration: data.video_duration_str,
  });
};
