import React from "react";

export type InfoCallback = React.Dispatch<React.SetStateAction<VideoInfo>>;
export type TabCallback = React.Dispatch<React.SetStateAction<string>>;

export type Video = {
  id: number;
  name: string;
  path: string;
  duration: string;
  thumbnail: string;
};

export type Subtitle = {
  name: string;
  path: string;
}

export type VideoInfo = {
  name: string;
  subtitles: string;
  duration: string;
  thumbnail: string;
};

export function getDefaultInfo(): VideoInfo {
  return {
    name: "-",
    subtitles: "-",
    duration: "-",
    thumbnail: "-",
  };
}

export const addVideoData = async (dataType: string, asset_id: number) => {
  const response = await fetch("/api/control/add", {
    method: "POST",
    body: JSON.stringify({ type: dataType, id: asset_id }),
  });
  const text = await response.text();
  console.log(`Add returned: ${text}`);
};

export const fetchData = async (endpoint: string, callback: any) => {
  const response = await fetch(endpoint);
  const data = await response.json();
  callback(data);
};

export const fetchInfo = async (callback: any) => {
  const response = await fetch("/api/selected");
  const info = await response.json();
  console.log(info)
  callback({
    name: info.name,
    subtitles: "",
    duration: info.video_duration_str,
    thumbnail: info.thumbnail,
  });
};

const postBase = async (endpoint: string) => {
  const response = await fetch(endpoint, {
    method: "POST",
  });
  const text = await response.text();
  console.log(`Post request to ${endpoint} returned: ${text}`);
};

export const playVideo = async () => {
  return postBase("/api/control/play");
};

export const pauseVideo = async () => {
  return postBase("/api/control/pause");
};

export const stopVideo = async () => {
  return postBase("/api/control/stop");
};

export const wakeScreen = async () => {
  return postBase("/api/control/wake");
};
