// api.tsx

export type Video = {
  name: string;
  path: string;
};

export type VideoInfo = {
  name: string;
  subtitles: string;
  duration: string;
};

export function getDefaultInfo(): VideoInfo {
  return {
    name: "-",
    subtitles: "-",
    duration: "-",
  };
}

export const addVideoData = async (path: string) => {
  const response = await fetch("/control/add", {
    method: "POST",
    body: JSON.stringify({ type: "video", path: path }),
  });
  const text = await response.text();
  console.log(`Add returned: ${text}`);
};

export const fetchData = async (callback: any) => {
  const response = await fetch("/videos");
  const { data } = await response.json();
  callback(data);
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
