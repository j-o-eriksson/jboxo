import React from "react";

export type InfoCallback = React.Dispatch<React.SetStateAction<VideoInfo>>;

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

export const addVideoData = async (dataType: string, path: string) => {
  const response = await fetch("/api/control/add", {
    method: "POST",
    body: JSON.stringify({ type: dataType, path: path }),
  });
  const text = await response.text();
  console.log(`Add returned: ${text}`);
};

export const fetchData = async (endpoint: string, callback: any) => {
  const response = await fetch(endpoint);
  const { data } = await response.json();
  callback(data);
};

export const fetchInfo = async (callback: any) => {
  const response = await fetch("/api/selected");
  const { data } = await response.json();
  callback({
    name: data.name,
    subtitles: data.subtitle_name,
    duration: data.video_duration_str,
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
